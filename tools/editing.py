#!/usr/bin/env python3
"""Local, read-only media audit helpers. Python 3.9+, no Python dependencies."""
import argparse
import hashlib
import json
import math
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path
from zoneinfo import ZoneInfo


def sha256(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def write_new(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2, allow_nan=False)
        f.write('\n')


def run(args):
    return subprocess.run(args, text=True, capture_output=True, check=True)


def timestamp(raw, offset=None, zone=None):
    """Return normalized UTC and provenance; ambiguous local times stay unresolved."""
    s = str(raw).strip()
    s = re.sub(r'^(\d{4}):(\d{2}):(\d{2})', r'\1-\2-\3', s)
    s = re.sub(r'([+-]\d{2})(\d{2})$', r'\1:\2', s)
    dt = datetime.fromisoformat(s.replace('Z', '+00:00'))
    if dt.tzinfo is None and offset:
        dt = datetime.fromisoformat(dt.isoformat() + str(offset))
    if dt.tzinfo is not None:
        return dt.astimezone(timezone.utc).isoformat(), 'explicit-offset'
    if not zone:
        return None, 'timezone-missing'
    tz = ZoneInfo(zone)
    valid = {}
    for fold in (0, 1):
        aware = dt.replace(tzinfo=tz, fold=fold)
        utc = aware.astimezone(timezone.utc)
        if utc.astimezone(tz).replace(tzinfo=None) == dt:
            valid[utc.isoformat()] = utc
    if len(valid) != 1:
        return None, 'ambiguous-or-nonexistent-local-time'
    return next(iter(valid)), 'assumed-zone:' + zone


TIME_FIELDS = [
    ('ExifIFD:DateTimeOriginal', 'ExifIFD:OffsetTimeOriginal'),
    ('EXIF:DateTimeOriginal', 'EXIF:OffsetTimeOriginal'),
    ('DateTimeOriginal', 'OffsetTimeOriginal'),
    ('Keys:CreationDate', None),
    ('com.apple.quicktime.creationdate', None),
    ('QuickTime:CreateDate', None),
    ('creation_time', None),
    ('Track1:MediaCreateDate', None),
    ('Track1:TrackCreateDate', None),
    ('ExifIFD:CreateDate', 'ExifIFD:OffsetTimeDigitized'),
]


def choose_time(meta, zone=None):
    candidates = []
    for key, offset_key in TIME_FIELDS:
        if key not in meta:
            continue
        raw = meta[key]
        offset = meta.get(offset_key) if offset_key else None
        try:
            utc, basis = timestamp(raw, offset, zone)
        except (ValueError, TypeError, OverflowError):
            utc, basis = None, 'invalid-timestamp'
        candidates.append(dict(source=key, raw=raw, offset=offset, utc=utc, basis=basis))
    if not candidates:
        match = re.search(r'(?<!\d)(20\d{6})[_-](\d{6})(?!\d)', Path(meta.get('SourceFile', '')).name)
        if match:
            raw = ''.join(match.groups())
            try:
                dt = datetime.strptime(raw, '%Y%m%d%H%M%S')
                utc, basis = timestamp(dt.isoformat(), zone=zone)
            except ValueError:
                utc, basis = None, 'invalid-timestamp'
            candidates.append(dict(source='filename-fallback', raw=raw, offset=None, utc=utc, basis=basis))
    selected = next((c for c in candidates if c['utc']), None)
    issues = [c['source'] + ': ' + c['basis'] for c in candidates if not c['utc']]
    if selected and selected['basis'].startswith('assumed'):
        issues.append('Selected timezone was assumed, not embedded')
    if selected:
        ref = datetime.fromisoformat(selected['utc'])
        for c in candidates:
            if c['utc'] and abs((datetime.fromisoformat(c['utc']) - ref).total_seconds()) > 2:
                issues.append('Conflicting timestamp: ' + c['source'])
    return dict(captured_utc=selected['utc'] if selected else None,
                time_source=selected['source'] if selected else None,
                time_basis=selected['basis'] if selected else None,
                candidates=candidates, issues=issues)


def catalog(root, output, zone=None, metadata_json=None):
    root = Path(root).resolve()
    if not root.is_dir():
        raise ValueError('Media root is not a directory')
    if zone:
        ZoneInfo(zone)  # Fail clearly on misspelled zones.
    if metadata_json:
        metadata = json.loads(Path(metadata_json).read_text())
    else:
        if not shutil.which('exiftool'):
            raise ValueError('Install ExifTool or provide --metadata-json from exiftool -json -G1 -a -s')
        cmd = ['exiftool', '-json', '-G1', '-a', '-s', '-r']
        for ext in ['jpg', 'jpeg', 'png', 'heic', 'heif', 'webp', 'mov', 'mp4', 'm4v']:
            cmd += ['-ext', ext]
        metadata = json.loads(run(cmd + [str(root)]).stdout)
    rows, hashes = [], {}
    for meta in metadata:
        source = Path(meta['SourceFile'])
        source = source.resolve() if source.is_absolute() else (root / source).resolve()
        try:
            rel = source.relative_to(root).as_posix()
        except ValueError:
            raise ValueError('Metadata references a file outside the media root') from None
        digest = sha256(source)
        row = dict(path=rel, sha256=digest, **choose_time(meta, zone))
        row['duplicate_of'] = hashes.get(digest)
        hashes.setdefault(digest, rel)
        rows.append(row)
    rows.sort(key=lambda x: (x['captured_utc'] is None, x['captured_utc'] or '', x['path']))
    write_new(output, dict(schema_version=1, assumed_zone=zone, media=rows,
                           unresolved=[x['path'] for x in rows if x['captured_utc'] is None],
                           note='Working order only. No mtime fallback; unresolved media require review.'))


def frame_at(seconds, fps):
    value = float(seconds) * float(fps)
    if not math.isfinite(value) or value < 0:
        raise ValueError('Nonnegative finite time required')
    return math.floor(value + 0.5)


def validate(data):
    errors, warnings = [], []
    try:
        fps = float(Fraction(str(data['fps'])))
        if not math.isfinite(fps) or fps <= 0:
            raise ValueError()
    except (KeyError, ValueError, ZeroDivisionError):
        return ['fps must be a positive number or rational string'], []
    duration = data.get('duration_frames')
    if type(duration) is not int or duration <= 0:
        errors.append('duration_frames must be a positive integer')
    shots = data.get('shots', [])
    if not shots:
        errors.append('No shots')
    cursor, ids, last_main = 0, set(), None
    for s in shots:
        sid = s.get('id')
        if not isinstance(sid, str) or not sid or sid in ids:
            errors.append('Missing or duplicate shot id')
        ids.add(sid)
        start, length = s.get('start_frame'), s.get('duration_frames')
        if type(start) is not int or type(length) is not int or start < 0 or length <= 0:
            errors.append(f'{sid}: invalid frame interval')
            continue
        if start != cursor:
            errors.append(f'{sid}: gap/overlap at {start}; expected {cursor}')
        cursor = start + length
        if length / fps < 0.5 and not s.get('short_shot_reason'):
            warnings.append(f'{sid}: under 0.5 seconds without stated reason')
        path = s.get('asset', '')
        if not path or Path(path).is_absolute() or '..' in Path(path).parts or re.match(r'^[A-Za-z]:', path):
            errors.append(f'{sid}: asset must be a relative path inside the project')
        if s.get('role', 'main') not in ('main', 'recap', 'graphic'):
            errors.append(f'{sid}: role must be main, recap or graphic')
        captured = s.get('captured_utc')
        if captured:
            try:
                utc, _ = timestamp(captured)
                if not utc:
                    raise ValueError()
                stamp = datetime.fromisoformat(utc)
                if s.get('role', 'main') == 'main':
                    if last_main and stamp < last_main and not s.get('chronology_override_reason'):
                        errors.append(f'{sid}: chronology inversion without explanation')
                    last_main = stamp
            except (ValueError, TypeError):
                errors.append(f'{sid}: captured_utc requires a valid explicit offset')
        elif s.get('role', 'main') == 'main':
            warnings.append(f'{sid}: capture time unresolved')
        if 'beat_seconds' in s and frame_at(s['beat_seconds'], fps) != start:
            errors.append(f'{sid}: start does not match rounded selected beat')
    if cursor != duration:
        errors.append(f'Timeline ends at {cursor}, expected {duration}')
    for fx in data.get('effects', []):
        start, length = fx.get('start_frame'), fx.get('duration_frames')
        if type(start) is not int or type(length) is not int or start < 0 or length <= 0 or type(duration) is not int or start + length > duration:
            errors.append('Effect outside timeline or invalid duration')
    return errors, warnings


def beat_report(data):
    fps = float(Fraction(str(data['fps'])))
    beats = data.get('beats_seconds', [])
    if fps <= 0 or not math.isfinite(fps) or not beats or any(not math.isfinite(x) or x < 0 for x in beats):
        raise ValueError('Positive fps and nonempty finite nonnegative beat list required')
    rows = []
    for frame in data['cuts_frames']:
        if type(frame) is not int or frame < 0:
            raise ValueError('Cut frames must be nonnegative integers')
        nearest = min(beats, key=lambda b: abs(b - frame / fps))
        rows.append(dict(frame=frame, nearest_selected_beat=nearest,
                         error_ms=round((frame / fps - nearest) * 1000, 3),
                         nearest_frame=frame_at(nearest, fps),
                         frame_aligned=frame == frame_at(nearest, fps)))
    return dict(fps=fps, cuts=rows, all_frame_aligned=all(x['frame_aligned'] for x in rows),
                listening_review='pending', note='Selected-marker alignment, not musical or auditory validation.')


def qa(path, output, expected_frames=None):
    path = Path(path).resolve()
    for binary in ('ffmpeg', 'ffprobe'):
        if not shutil.which(binary):
            raise ValueError('Required tool missing: ' + binary)
    probe = json.loads(run(['ffprobe', '-v', 'error', '-count_frames', '-show_streams', '-show_format', '-of', 'json', str(path)]).stdout)
    video = next((s for s in probe['streams'] if s['codec_type'] == 'video'), None)
    if not video:
        raise ValueError('No video stream')
    decode = subprocess.run(['ffmpeg', '-v', 'error', '-xerror', '-i', str(path), '-map', '0:v:0', '-map', '0:a?', '-f', 'null', '-'], capture_output=True, text=True)
    black = run(['ffmpeg', '-hide_banner', '-i', str(path), '-an', '-vf', 'blackdetect=d=0.1:pix_th=0.05:pic_th=0.98', '-f', 'null', '-'])
    intervals = [dict(start=float(a), end=float(b), duration=float(c)) for a,b,c in re.findall(r'black_start:([\d.]+) black_end:([\d.]+) black_duration:([\d.]+)', black.stderr)]
    loudness = None
    if any(s['codec_type'] == 'audio' for s in probe['streams']):
        audio = run(['ffmpeg', '-hide_banner', '-i', str(path), '-map', '0:a:0', '-af', 'loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json', '-f', 'null', '-'])
        found = re.findall(r'\{\s*"input_i".*?\}', audio.stderr, re.S)
        if not found:
            raise ValueError('Loudness output could not be parsed')
        loudness = json.loads(found[-1])  # Keep "-inf" as strings for silence.
    frames = int(video['nb_read_frames'])
    report = dict(schema_version=1, file=path.name, sha256=sha256(path), checked_at=datetime.now(timezone.utc).isoformat(),
                  frames=frames, expected_frames=expected_frames, frame_count_matches=frames == expected_frames if expected_frames is not None else None,
                  width=video['width'], height=video['height'], fps=video['avg_frame_rate'], codec=video['codec_name'], pixel_format=video.get('pix_fmt'),
                  color_transfer=video.get('color_transfer'), color_space=video.get('color_space'),
                  decode_exit_code=decode.returncode, decode_errors=decode.stderr[-2000:], black_intervals=intervals, loudness=loudness,
                  visual_review='pending', listening_review='pending',
                  loudness_note='input_* measures the file; output_* is discarded filter output, not applied normalization.')
    write_new(output, report)
    return decode.returncode == 0 and (expected_frames is None or frames == expected_frames)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest='command', required=True)
    c = sub.add_parser('catalog'); c.add_argument('root'); c.add_argument('output'); c.add_argument('--zone'); c.add_argument('--metadata-json')
    v = sub.add_parser('validate'); v.add_argument('timeline')
    b = sub.add_parser('beat-report'); b.add_argument('input'); b.add_argument('output')
    q = sub.add_parser('qa'); q.add_argument('video'); q.add_argument('output'); q.add_argument('--expected-frames', type=int)
    a = p.parse_args()
    try:
        if a.command == 'catalog':
            catalog(a.root, a.output, a.zone, a.metadata_json)
        elif a.command == 'validate':
            errors, warnings = validate(json.loads(Path(a.timeline).read_text()))
            print(json.dumps(dict(errors=errors, warnings=warnings), indent=2))
            return 1 if errors else 0
        elif a.command == 'beat-report':
            write_new(a.output, beat_report(json.loads(Path(a.input).read_text())))
        elif a.command == 'qa':
            return 0 if qa(a.video, a.output, a.expected_frames) else 1
    except (ValueError, OSError, KeyError, TypeError, subprocess.CalledProcessError) as e:
        print(str(e), file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    sys.exit(main())
