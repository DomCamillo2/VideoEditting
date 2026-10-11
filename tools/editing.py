#!/usr/bin/env python3
"""Local, read-only media audit helpers. Python 3.9+, no Python dependencies."""
import argparse
import csv
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
    text = json.dumps(data, ensure_ascii=False, indent=2, allow_nan=False) + "\n"
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as f:
        f.write(text)


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


def rational(value, positive=False):
    if isinstance(value, bool) or not isinstance(value, (int, float, str, Fraction)):
        raise ValueError('Finite number or rational string required')
    try:
        result = Fraction(str(value))
    except (ValueError, ZeroDivisionError, OverflowError):
        raise ValueError('Finite number or rational string required') from None
    if result < 0 or (positive and result == 0):
        raise ValueError('Positive value required' if positive else 'Nonnegative value required')
    return result


def frame_at(seconds, fps):
    # Keep exact rational arithmetic through the half-up rounding boundary.
    return math.floor(rational(seconds) * rational(fps, positive=True) + Fraction(1, 2))


def relative_asset(value):
    """Portable project-relative paths, not URLs, drive paths or traversal."""
    return (isinstance(value, str) and bool(value)
            and not any(ord(c) < 32 for c in value)
            and not any(c in value for c in ('\\', ':'))
            and all(part not in ('', '.', '..') for part in value.split('/')))


def validate(data, media_root=None):
    errors, warnings = [], []
    if not isinstance(data, dict):
        return ['Timeline must be a JSON object'], []
    try:
        fps = rational(data.get('fps'), positive=True)
    except ValueError:
        return ['fps must be a positive number or rational string'], []
    if 'schema_version' in data and (type(data['schema_version']) is not int or data['schema_version'] != 1):
        errors.append('Unsupported schema_version; expected 1')
    duration = data.get('duration_frames')
    valid_duration = type(duration) is int and duration > 0
    if not valid_duration:
        errors.append('duration_frames must be a positive integer')
    root = Path(media_root).resolve() if media_root is not None else None
    if root is not None and not root.is_dir():
        errors.append('media_root must be an existing directory')
    shots = data.get('shots')
    if not isinstance(shots, list) or not shots:
        errors.append('shots must be a nonempty list')
        shots = []
    cursor, ids, last_main = 0, set(), None
    for index, shot in enumerate(shots):
        if not isinstance(shot, dict):
            errors.append(f'Shot {index}: must be an object')
            continue
        sid = shot.get('id')
        if not isinstance(sid, str) or not sid or sid in ids:
            errors.append(f'Shot {index}: missing or duplicate shot id')
        else:
            ids.add(sid)
        label = sid if isinstance(sid, str) else f'Shot {index}'
        start, length = shot.get('start_frame'), shot.get('duration_frames')
        interval_ok = type(start) is int and type(length) is int and start >= 0 and length > 0
        if not interval_ok:
            errors.append(f'{label}: invalid frame interval')
        else:
            if start != cursor:
                errors.append(f'{label}: gap/overlap at {start}; expected {cursor}')
            cursor = start + length
            if length / fps < Fraction(1, 2) and not shot.get('short_shot_reason'):
                warnings.append(f'{label}: under 0.5 seconds without stated reason')
        asset = shot.get('asset')
        if not relative_asset(asset):
            errors.append(f'{label}: asset must be a relative path inside the project')
        elif root is not None:
            candidate = (root / asset).resolve()
            try:
                candidate.relative_to(root)
            except ValueError:
                errors.append(f'{label}: asset resolves outside media_root')
            else:
                if not candidate.is_file():
                    errors.append(f'{label}: asset is missing or not a file: {asset}')
        role = shot.get('role', 'main')
        if role not in ('main', 'recap', 'graphic'):
            errors.append(f'{label}: role must be main, recap or graphic')
        captured = shot.get('captured_utc')
        if captured:
            try:
                utc, _ = timestamp(captured)
                if not utc:
                    raise ValueError()
                stamp = datetime.fromisoformat(utc)
                if role == 'main':
                    if last_main and stamp < last_main and not shot.get('chronology_override_reason'):
                        errors.append(f'{label}: chronology inversion without explanation')
                    last_main = stamp
            except (ValueError, TypeError, OverflowError):
                errors.append(f'{label}: captured_utc requires a valid explicit offset')
        elif role == 'main':
            warnings.append(f'{label}: capture time unresolved')
        if 'beat_seconds' in shot:
            try:
                if frame_at(shot['beat_seconds'], fps) != start:
                    errors.append(f'{label}: start does not match rounded selected beat')
            except ValueError:
                errors.append(f'{label}: beat_seconds must be finite and nonnegative')
        source = shot.get('source')
        if source is not None:
            try:
                if not isinstance(source, dict):
                    raise ValueError('source must be an object')
                source_fps = rational(source.get('fps'), positive=True)
                speed = rational(source.get('playback_rate', 1), positive=True)
                begin, end = source.get('in_frame'), source.get('out_frame')
                if type(begin) is not int or type(end) is not int or begin < 0 or end <= begin:
                    raise ValueError('source requires 0 <= in_frame < out_frame (exclusive)')
                total = source.get('total_frames')
                if total is not None and (type(total) is not int or total <= 0 or end > total):
                    raise ValueError('source range exceeds total_frames or total_frames is invalid')
                if total is None:
                    warnings.append(f'{label}: source total_frames unknown; bounds not verified')
                expected = frame_at(Fraction(end - begin, 1) / source_fps / speed, fps)
                if interval_ok and expected != length:
                    raise ValueError(f'source range maps to {expected} timeline frames, expected {length}')
            except ValueError as exc:
                errors.append(f'{label}: {exc}')
        elif isinstance(asset, str) and Path(asset).suffix.lower() in ('.mp4', '.mov', '.m4v', '.mkv', '.webm'):
            warnings.append(f'{label}: video source in/out and source fps not recorded')
    if valid_duration and cursor != duration:
        errors.append(f'Timeline ends at {cursor}, expected {duration}')
    effects = data.get('effects', [])
    if not isinstance(effects, list):
        errors.append('effects must be a list')
        effects = []
    for fx in effects:
        if not isinstance(fx, dict):
            errors.append('Effect must be an object')
            continue
        start, length = fx.get('start_frame'), fx.get('duration_frames')
        if type(start) is not int or type(length) is not int or start < 0 or length <= 0 or not valid_duration or start + length > duration:
            errors.append('Effect outside timeline or invalid duration')
    return errors, warnings


def beat_report(data):
    if not isinstance(data, dict):
        raise ValueError('Beat input must be an object')
    fps = rational(data.get('fps'), positive=True)
    beats = data.get('beats_seconds')
    cuts = data.get('cuts_frames')
    if not isinstance(beats, list) or not beats or not isinstance(cuts, list):
        raise ValueError('Nonempty beat list and cut list required')
    beats = [rational(value) for value in beats]
    rows = []
    for frame in cuts:
        if type(frame) is not int or frame < 0:
            raise ValueError('Cut frames must be nonnegative integers')
        nearest = min(beats, key=lambda b: abs(b - frame / fps))
        rows.append(dict(frame=frame, nearest_selected_beat=float(nearest),
                         error_ms=round(float((frame / fps - nearest) * 1000), 3),
                         nearest_frame=frame_at(nearest, fps),
                         frame_aligned=frame == frame_at(nearest, fps)))
    return dict(fps=float(fps), fps_rational=str(fps), cuts=rows,
                all_frame_aligned=bool(rows) and all(x['frame_aligned'] for x in rows),
                listening_review='pending', note='Selected-marker alignment, not musical or auditory validation.')


def cut_list(data, output, media_root=None):
    """Export a review CSV, not an editor-specific EDL or rendered effects."""
    errors, warnings = validate(data, media_root)
    if errors:
        raise ValueError('Invalid timeline: ' + '; '.join(errors))
    fields = ['id', 'asset', 'timeline_fps', 'start_frame', 'end_frame_exclusive',
              'duration_frames', 'source_fps', 'source_in_frame', 'source_out_frame_exclusive',
              'playback_rate', 'role', 'captured_utc']
    rows = []
    for shot in data['shots']:
        source = shot.get('source') or {}
        row = dict(id=shot['id'], asset=shot['asset'], timeline_fps=str(rational(data['fps'])),
                   start_frame=shot['start_frame'], end_frame_exclusive=shot['start_frame'] + shot['duration_frames'],
                   duration_frames=shot['duration_frames'], source_fps=source.get('fps', ''),
                   source_in_frame=source.get('in_frame', ''), source_out_frame_exclusive=source.get('out_frame', ''),
                   playback_rate=source.get('playback_rate', 1) if source else '',
                   role=shot.get('role', 'main'), captured_utc=shot.get('captured_utc', ''))
        # This CSV is for human review; don't execute filenames as spreadsheet formulas.
        rows.append({key: "'" + value if isinstance(value, str) and value.startswith(('=', '+', '-', '@', '\t', '\r', '\n')) else value
                     for key, value in row.items()})
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open('x', encoding='utf-8', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    return warnings


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
    v = sub.add_parser('validate'); v.add_argument('timeline'); v.add_argument('--media-root')
    e = sub.add_parser('cut-list'); e.add_argument('timeline'); e.add_argument('output'); e.add_argument('--media-root')
    b = sub.add_parser('beat-report'); b.add_argument('input'); b.add_argument('output')
    q = sub.add_parser('qa'); q.add_argument('video'); q.add_argument('output'); q.add_argument('--expected-frames', type=int)
    a = p.parse_args()
    try:
        if a.command == 'catalog':
            catalog(a.root, a.output, a.zone, a.metadata_json)
        elif a.command == 'validate':
            errors, warnings = validate(json.loads(Path(a.timeline).read_text()), a.media_root)
            print(json.dumps(dict(errors=errors, warnings=warnings), indent=2))
            return 1 if errors else 0
        elif a.command == 'cut-list':
            warnings = cut_list(json.loads(Path(a.timeline).read_text()), a.output, a.media_root)
            print(json.dumps(dict(warnings=warnings, note='Review CSV; effects and audio are not exported'), indent=2))
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
