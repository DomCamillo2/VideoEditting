"""Regression cases found during the repository audit, plus interchange checks."""
import copy
import csv
from fractions import Fraction
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'tools' / (name + '.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
editing = load('editing')
assets = load('public_assets')


class TimelineAuditTests(unittest.TestCase):
    def fixture(self):
        return json.loads((ROOT / 'examples/timeline-source.json').read_text())

    def test_malformed_top_level_and_collections_report_errors(self):
        for data in [None, [], True, {'fps': 30, 'shots': 'oops'},
                     dict(self.fixture(), shots=[None]), dict(self.fixture(), effects=[False]),
                     dict(self.fixture(), effects={'start_frame': 0})]:
            with self.subTest(data=data):
                self.assertTrue(editing.validate(data)[0])

    def test_unhashable_id_does_not_crash(self):
        data = self.fixture(); data['shots'][0]['id'] = []
        self.assertTrue(editing.validate(data)[0])

    def test_invalid_assets_rejected_on_every_platform(self):
        for path in [None, 42, [], '/outside.mp4', '../outside.mp4', r'C:\outside.mp4',
                     r'..\outside.mp4', r'\\server\share.mp4', 'https://example.test/clip.mp4',
                     'file:clip.mp4', 'a/../b.mp4', 'bad\nname.mp4']:
            data = self.fixture(); data['shots'][0]['asset'] = path
            with self.subTest(path=path):
                self.assertTrue(editing.validate(data)[0])

    def test_invalid_beats_are_validation_errors(self):
        for beat in ['bad', None, float('nan'), float('inf'), True, [], -1]:
            data = self.fixture(); data['shots'][0]['beat_seconds'] = beat
            with self.subTest(beat=beat):
                self.assertTrue(editing.validate(data)[0])

    def test_rational_half_frame_rounding(self):
        self.assertEqual(editing.frame_at('1001/60000', '30000/1001'), 1)
        # Float arithmetic rounds this value up before the intended half-frame boundary.
        almost_half = Fraction(10**20 - 1, 2 * 10**20)
        self.assertEqual(editing.frame_at(almost_half, 1), 0)

    def test_empty_cuts_are_not_claimed_aligned(self):
        self.assertFalse(editing.beat_report({'fps': 30, 'beats_seconds': [1], 'cuts_frames': []})['all_frame_aligned'])

    def test_bad_beat_report_data_rejected(self):
        for data in [[], {'fps': '1/0'}, {'fps': True, 'beats_seconds': [1], 'cuts_frames': []},
                     {'fps': 30, 'beats_seconds': [None], 'cuts_frames': []}]:
            with self.subTest(data=data), self.assertRaises(ValueError):
                editing.beat_report(data)

    def test_unknown_schema_version_is_rejected(self):
        for version in [2, True, "1"]:
            self.assertTrue(editing.validate(dict(self.fixture(), schema_version=version))[0])

    def test_source_rate_mapping(self):
        self.assertEqual(editing.validate(self.fixture()), ([], []))
        data = self.fixture(); data['shots'][0]['source'].update(out_frame=96, playback_rate=2)
        self.assertEqual(editing.validate(data), ([], []))

    def test_source_ranges_and_rate_mismatches(self):
        for change in [{'in_frame': -1}, {'out_frame': 241}, {'out_frame': 48},
                       {'out_frame': 73}, {'fps': '0/0'}, {'playback_rate': 0},
                       {'total_frames': False}, {'in_frame': 1.5}]:
            data = self.fixture(); data['shots'][0]['source'].update(change)
            with self.subTest(change=change):
                self.assertTrue(editing.validate(data)[0])

    def test_unknown_source_bounds_remain_visible(self):
        data = self.fixture(); del data['shots'][0]['source']['total_frames']
        errors, warnings = editing.validate(data)
        self.assertFalse(errors); self.assertTrue(any('bounds not verified' in x for x in warnings))

    def test_missing_assets_and_symlink_escape(self):
        with tempfile.TemporaryDirectory() as td, tempfile.TemporaryDirectory() as other:
            data = self.fixture()
            self.assertTrue(editing.validate(data, td)[0])
            for shot in data['shots']:
                p = Path(td) / shot['asset']; p.parent.mkdir(parents=True, exist_ok=True); p.write_bytes(b'fixture')
            self.assertFalse(editing.validate(data, td)[0])
            p = Path(td) / data['shots'][0]['asset']; p.unlink()
            outside = Path(other) / 'clip.mp4'; outside.write_bytes(b'fixture'); p.symlink_to(outside)
            self.assertTrue(any('outside media_root' in x for x in editing.validate(data, td)[0]))

    def test_csv_preserves_source_and_timeline_ranges(self):
        with tempfile.TemporaryDirectory() as td:
            output = Path(td) / 'cuts.csv'
            self.assertEqual(editing.cut_list(self.fixture(), output), [])
            with output.open() as stream: rows = list(csv.DictReader(stream))
            self.assertEqual(rows[0]['source_in_frame'], '48')
            self.assertEqual(rows[0]['source_out_frame_exclusive'], '72')
            self.assertEqual(rows[0]['end_frame_exclusive'], '30')
            self.assertEqual(rows[1]['source_in_frame'], '')
            with self.assertRaises(FileExistsError): editing.cut_list(self.fixture(), output)

    def test_invalid_timeline_never_creates_csv(self):
        with tempfile.TemporaryDirectory() as td:
            output = Path(td) / 'cuts.csv'
            data = self.fixture(); data['shots'][0]['source']['out_frame'] = 999
            with self.assertRaises(ValueError): editing.cut_list(data, output)
            self.assertFalse(output.exists())

    def test_spreadsheet_formula_in_id_is_escaped(self):
        with tempfile.TemporaryDirectory() as td:
            output = Path(td) / 'cuts.csv'; data = self.fixture(); data['shots'][0]['id'] = '=1+1'
            editing.cut_list(data, output)
            with output.open() as stream: rows = list(csv.DictReader(stream))
            self.assertEqual(rows[0]['id'], "'=1+1")

    def test_invalid_json_number_does_not_leave_empty_output(self):
        with tempfile.TemporaryDirectory() as td:
            output = Path(td) / 'invalid.json'
            with self.assertRaises(ValueError): editing.write_new(output, {'fps': float('nan')})
            self.assertFalse(output.exists())

    def test_cli_bad_timeline_produces_structured_errors(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / 'bad.json'; path.write_text('{"fps": 30, "shots": [null]}')
            result = subprocess.run([sys.executable, str(ROOT / 'tools/editing.py'), 'validate', str(path)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 1)
            self.assertTrue(json.loads(result.stdout)['errors'])
            self.assertNotIn('Traceback', result.stderr)


class PublicationAuditTests(unittest.TestCase):
    def inventory(self, root):
        (root / 'demo.wav').write_bytes(b'own-demo-fixture')
        entry = dict(path='demo.wav', sha256=hashlib.sha256(b'own-demo-fixture').hexdigest(),
                     license='MIT', provenance='Synthetic test fixture')
        (root / 'public-assets.json').write_text(json.dumps({'assets': [entry]}))

    def test_approved_assets_pass_and_replacements_fail(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); self.inventory(root)
            self.assertEqual(assets.audit_assets(root, ['demo.wav']), [])
            (root / 'demo.wav').write_bytes(b'unreviewed-replacement')
            self.assertTrue(assets.audit_assets(root, ['demo.wav']))

    def test_force_added_ignored_song_is_seen(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); self.inventory(root)
            (root / '.gitignore').write_text('*.mp3\n')
            (root / 'song.mp3').write_bytes(b'not-actual-audio')
            subprocess.run(['git', 'init', '-q', str(root)], check=True)
            subprocess.run(['git', '-C', str(root), 'add', 'demo.wav', 'public-assets.json', '.gitignore'], check=True)
            subprocess.run(['git', '-C', str(root), 'add', '-f', 'song.mp3'], check=True)
            self.assertTrue(any('song.mp3' in x for x in assets.audit_assets(root)))

    def test_private_tracked_text_is_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); self.inventory(root)
            self.assertTrue(any('private working' in x for x in assets.audit_assets(root, ['demo.wav', 'local/notes.json'])))

    def test_stale_inventory_and_invalid_manifest_fail(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); self.inventory(root)
            self.assertTrue(assets.audit_assets(root, []))
            (root / 'public-assets.json').write_text('{"assets": null}')
            self.assertTrue(assets.audit_assets(root, []))

    def test_symlink_is_not_approved_by_matching_hash(self):
        with tempfile.TemporaryDirectory() as td, tempfile.TemporaryDirectory() as other:
            root = Path(td); self.inventory(root)
            source = Path(other) / 'sound.wav'; source.write_bytes((root / 'demo.wav').read_bytes())
            (root / 'demo.wav').unlink(); (root / 'demo.wav').symlink_to(source)
            self.assertTrue(assets.audit_assets(root, ['demo.wav']))

    def test_zip_fallback_works_without_git(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); self.inventory(root)
            with patch.object(assets.shutil, 'which', return_value=None):
                self.assertEqual(assets.audit_assets(root), [])

    def test_zip_fallback_ignores_local_media_but_checks_public_media(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); self.inventory(root)
            (root / 'local').mkdir(); (root / 'local/song.mp3').write_bytes(b'private')
            self.assertEqual(assets.audit_assets(root), [])
            (root / 'song.mp3').write_bytes(b'unreviewed')
            self.assertTrue(assets.audit_assets(root))


if __name__ == '__main__':
    unittest.main()
