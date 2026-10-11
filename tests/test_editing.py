import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('editing', ROOT/'tools/editing.py')
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

class EditingTests(unittest.TestCase):
    def test_negative_half_hour_offset(self):
        self.assertEqual(m.timestamp('2024:01:01 12:00:00', '-03:30')[0], '2024-01-01T15:30:00+00:00')
    def test_quarter_hour_offset(self):
        self.assertEqual(m.timestamp('2024:01:01 12:00:00', '+05:45')[0], '2024-01-01T06:15:00+00:00')
    def test_utc_and_offset_same(self):
        self.assertEqual(m.timestamp('2024-08-01T12:00:00+02:00')[0],m.timestamp('2024-08-01T10:00:00Z')[0])
    def test_naive_not_guessed(self):
        self.assertIsNone(m.timestamp('2024:08:01 12:00:00')[0])
    def test_summer_and_winter(self):
        self.assertIn('10:00:00',m.timestamp('2024:08:01 12:00:00',zone='Europe/Berlin')[0])
        self.assertIn('11:00:00',m.timestamp('2024:01:01 12:00:00',zone='Europe/Berlin')[0])
    def test_dst_ambiguous(self):
        self.assertIsNone(m.timestamp('2024-10-27T02:30:00',zone='Europe/Berlin')[0])
    def test_dst_nonexistent(self):
        self.assertIsNone(m.timestamp('2024-03-31T02:30:00',zone='Europe/Berlin')[0])
    def test_original_before_export(self):
        d=m.choose_time({'Keys:CreationDate':'2024-01-01T10:00:00Z','QuickTime:CreateDate':'2025-01-01T10:00:00Z'})
        self.assertEqual(d['time_source'],'Keys:CreationDate'); self.assertTrue(d['issues'])
    def test_no_mtime(self):
        self.assertIsNone(m.choose_time({'File:FileModifyDate':'2024-01-01T10:00:00Z'})['captured_utc'])
    def test_invalid_timestamp_preserved(self):
        d=m.choose_time({'DateTimeOriginal':'0000:00:00 00:00:00','creation_time':'2024-01-01T10:00:00Z'})
        self.assertEqual(d['time_source'],'creation_time'); self.assertEqual(len(d['candidates']),2)
    def test_filename_fallback(self):
        d=m.choose_time({'SourceFile':'IMG_20240801_120000.jpg'},'Europe/Berlin')
        self.assertEqual(d['time_source'],'filename-fallback')
    def test_rounding(self):
        self.assertEqual(m.frame_at(.05,30),2)
        for i in range(1000):
            seconds=i/101
            self.assertLessEqual(abs(m.frame_at(seconds,30)/30-seconds),1/60+1e-10)
    def fixture(self):
        return json.loads((ROOT/'examples/timeline.json').read_text())
    def test_valid_fixture(self):
        self.assertEqual(m.validate(self.fixture()),([],[]))
    def test_gap(self):
        d=self.fixture();d['shots'][1]['start_frame']+=1
        self.assertTrue(m.validate(d)[0])
    def test_overlap(self):
        d=self.fixture();d['shots'][1]['start_frame']-=1
        self.assertTrue(m.validate(d)[0])
    def test_recap_can_go_back(self):
        d=self.fixture();d['shots'][1]['role']='recap';d['shots'][1]['captured_utc']='2020-01-01T00:00:00Z'
        self.assertEqual(m.validate(d)[0],[])
    def test_main_inversion_detected(self):
        d=self.fixture();d['shots'][1]['captured_utc']='2020-01-01T00:00:00Z'
        self.assertTrue(m.validate(d)[0])
    def test_escape_rejected(self):
        d=self.fixture();d['shots'][1]['asset']='../private.jpg'
        self.assertTrue(m.validate(d)[0])
    def test_effect_overrun(self):
        d=self.fixture();d['effects'][0]['duration_frames']=10000
        self.assertTrue(m.validate(d)[0])
    def test_beat_not_claim_listening(self):
        r=m.beat_report({'fps':30,'beats_seconds':[1.001],'cuts_frames':[30]})
        self.assertTrue(r['all_frame_aligned']);self.assertEqual(r['listening_review'],'pending')
    def test_empty_beats_rejected(self):
        with self.assertRaises(ValueError):m.beat_report({'fps':30,'beats_seconds':[],'cuts_frames':[]})
    def test_no_overwrite(self):
        with tempfile.TemporaryDirectory() as td:
            f=Path(td)/'report.json';m.write_new(f,{'a':1})
            with self.assertRaises(FileExistsError):m.write_new(f,{'a':2})
            self.assertEqual(json.loads(f.read_text()),{'a':1})
    def test_catalog_duplicates_and_unknown(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);(root/'a.jpg').write_bytes(b'fixture');(root/'b.jpg').write_bytes(b'fixture')
            raw=root/'metadata.json';raw.write_text(json.dumps([{'SourceFile':'a.jpg','DateTimeOriginal':'2024-01-01T00:00:00Z'},{'SourceFile':'b.jpg'}]))
            out=root/'catalog.json';m.catalog(root,out,metadata_json=raw)
            data=json.loads(out.read_text());self.assertEqual(data['unresolved'],['b.jpg']);self.assertEqual(data['media'][1]['duplicate_of'],'a.jpg')
    def test_catalog_path_escape(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);raw=root/'metadata.json';raw.write_text('[{"SourceFile":"../outside.jpg"}]')
            with self.assertRaises(ValueError):m.catalog(root,root/'out.json',metadata_json=raw)

if __name__=='__main__':unittest.main()
