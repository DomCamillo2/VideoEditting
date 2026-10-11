#!/usr/bin/env python3
"""Local contact sheets and review candidates. No deletion or automatic aesthetic ranking."""
import argparse
import hashlib
import io
import json
from pathlib import Path
import subprocess
import sys
from datetime import datetime, timezone

from editing import sha256, write_new, relative_asset

IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.webp', '.tif', '.tiff', '.bmp'}
VIDEO_EXTENSIONS = {'.mp4', '.mov', '.m4v', '.mkv', '.webm'}


def libraries():
    try:
        import numpy as np
        from PIL import Image, ImageOps, ImageDraw
    except ImportError:
        raise ValueError('Install optional analysis dependencies: python -m pip install -r requirements-analysis.txt') from None
    return np, Image, ImageOps, ImageDraw


def image_metrics(image, region=None):
    np, Image, ImageOps, _ = libraries()
    image = ImageOps.exif_transpose(image).convert('RGB')
    if region is not None:
        if (not isinstance(region, list) or len(region) != 4 or
                any(type(v) not in (int, float) or not 0 <= v <= 1 for v in region) or
                region[0] >= region[2] or region[1] >= region[3]):
            raise ValueError('Focus ROI must be normalized [left, top, right, bottom]')
        box = tuple(round(v * (image.width if i % 2 == 0 else image.height)) for i, v in enumerate(region))
        if box[2] - box[0] < 3 or box[3] - box[1] < 3:
            raise ValueError('Focus ROI is too small')
        subject = image.crop(box)
    else:
        subject = image
    subject.thumbnail((512, 512), Image.Resampling.LANCZOS)
    gray = np.asarray(subject.convert('L'), dtype=np.float64)
    lap = (-4 * gray[1:-1, 1:-1] + gray[:-2, 1:-1] + gray[2:, 1:-1] + gray[1:-1, :-2] + gray[1:-1, 2:])
    small = np.asarray(image.convert('L').resize((9, 8), Image.Resampling.LANCZOS))
    bits = (small[:, 1:] > small[:, :-1]).flatten()
    dhash = sum(int(bit) << i for i, bit in enumerate(bits))
    color = np.asarray(image.resize((32, 32)), dtype=np.float64)
    return dict(dhash=f'{dhash:016x}', mean_rgb=[round(float(v), 2) for v in color.mean(axis=(0, 1))],
                focus_variance=round(float(lap.var()), 3) if lap.size else None,
                focus_region=region or 'whole-frame', metric_size=list(subject.size),
                dark_fraction=round(float((gray < 13).mean()), 3),
                bright_fraction=round(float((gray > 242).mean()), 3))


def distance(a, b):
    return bin(int(a['dhash'], 16) ^ int(b['dhash'], 16)).count('1')


def near(a, b, max_distance):
    return (a['kind'] == b['kind'] == 'image' and abs(a['aspect'] - b['aspect']) < .08
            and distance(a, b) <= max_distance
            and max(abs(x-y) for x, y in zip(a['mean_rgb'], b['mean_rgb'])) <= 24)


def cluster_rows(rows, max_distance=6):
    """Complete-link grouping avoids chaining unrelated A~B~C images into one cluster."""
    groups = []
    for row in rows:
        if row.get('error'):
            continue
        group = next((g for g in groups if all(row['sha256'] == old['sha256'] or near(row, old, max_distance) for old in g)), None)
        if group is None:
            group = []; groups.append(group)
        group.append(row)
        row['cluster_id'] = f'cluster-{groups.index(group) + 1:04d}'
    return [[row['asset_id'] for row in group] for group in groups]


def video_samples(path):
    _, Image, _, _ = libraries()
    result = subprocess.run(['ffprobe', '-v', 'error', '-show_format', '-show_streams', '-of', 'json', str(path)], capture_output=True, text=True, check=True)
    metadata = json.loads(result.stdout)
    stream = next(s for s in metadata['streams'] if s.get('codec_type') == 'video')
    duration = float(stream.get('duration') or metadata.get('format', {}).get('duration') or 0)
    if duration <= 0:
        raise ValueError('Video duration unavailable')
    samples = []
    for fraction in (.1, .5, .9):
        second = max(0, min(duration - .05, duration * fraction))
        result = subprocess.run(['ffmpeg', '-v', 'error', '-ss', str(second), '-i', str(path), '-frames:v', '1',
                                 '-vf', 'scale=640:640:force_original_aspect_ratio=decrease', '-f', 'image2pipe', '-vcodec', 'png', '-'], capture_output=True, check=True)
        samples.append((second, Image.open(io.BytesIO(result.stdout)).convert('RGB')))
    return duration, samples


def analyze(root, output, rois=None, max_distance=6):
    _, Image, ImageOps, ImageDraw = libraries()
    root, output = Path(root).resolve(), Path(output).resolve()
    if not root.is_dir(): raise ValueError('Media root must exist')
    if output == root or root in output.parents: raise ValueError('Keep analysis output outside the media input directory')
    if not 0 <= max_distance <= 64: raise ValueError('Hash distance must be 0..64')
    rois = rois or {}
    if not isinstance(rois, dict) or any(not relative_asset(key) for key in rois): raise ValueError('ROI file maps relative media paths to rectangles')
    files = sorted(p for p in root.rglob('*') if p.is_file() and p.suffix.lower() in IMAGE_EXTENSIONS | VIDEO_EXTENSIONS)
    if not files: raise ValueError('No supported image/video files found; HEIC needs a local conversion/plugin first')
    missing_rois = set(rois) - {p.relative_to(root).as_posix() for p in files}
    if missing_rois: raise ValueError('Focus ROI references missing/unsupported media: '+', '.join(sorted(missing_rois)))
    output.mkdir(parents=True, exist_ok=False)
    (output/'thumbnails').mkdir()
    rows, exact, tiles = [], {}, []
    for path in files:
        relative = path.relative_to(root).as_posix()
        row = dict(asset_id='asset-'+hashlib.sha256(relative.encode('utf-8')).hexdigest()[:12], path=relative, decision='review', review_status='pending')
        try:
            if root not in path.resolve().parents: raise ValueError('Symlink escapes media root')
            digest = sha256(path); row['sha256'] = digest
            row['exact_duplicate_of'] = exact.get(digest); exact.setdefault(digest, row['asset_id'])
            if path.suffix.lower() in IMAGE_EXTENSIONS:
                with Image.open(path) as source:
                    image = ImageOps.exif_transpose(source).convert('RGB')
                samples = [(None, image)]; row['kind'] = 'image'
            else:
                row['kind'] = 'video'; row['duration_seconds'], samples = video_samples(path)
            image = samples[len(samples)//2][1]
            row.update(width=image.width, height=image.height, aspect=image.width/image.height)
            row.update(image_metrics(image.copy(), rois.get(relative)))
            row['samples'] = []
            for number, (second, sample) in enumerate(samples):
                thumb_name = f"thumbnails/{row['asset_id']}-{number}.jpg"
                thumbnail = ImageOps.contain(sample, (320, 200))
                thumbnail.save(output/thumb_name, quality=88)
                row['samples'].append(dict(seconds=second, thumbnail=thumb_name))
                tiles.append((row, second, thumbnail.copy()))
        except (OSError, ValueError, subprocess.SubprocessError, StopIteration) as exc:
            row['error'] = type(exc).__name__ + ': media could not be inspected; check decoder/file/ROI'
        rows.append(row)
    groups = cluster_rows(rows, max_distance)
    for start in range(0, len(tiles), 12):
        page = Image.new('RGB', (1000, 1040), '#eff2ed'); draw = ImageDraw.Draw(page)
        for i, (row, second, thumb) in enumerate(tiles[start:start+12]):
            x, y = (i%3)*332+8, (i//3)*258+8
            page.paste(thumb, (x+(320-thumb.width)//2, y+(200-thumb.height)//2))
            label = row['asset_id'] + (f' / {second:.2f}s' if second is not None else '')
            draw.text((x, y+204), label, fill='#17343e')
            draw.text((x, y+220), row['path'][:44].encode('ascii','replace').decode(), fill='#17343e')
            draw.text((x, y+236), row.get('cluster_id','') + (' / exact duplicate' if row.get('exact_duplicate_of') else ''), fill='#526c75')
        page.save(output/f'contact-{start//12+1:03d}.jpg', quality=90)
    report = dict(schema_version=1, checked_at=datetime.now(timezone.utc).isoformat(), media=rows, groups=groups,
                  parameters=dict(max_hash_distance=max_distance, normalization_max_pixels=512),
                  note='Candidates only. Compare subject focus at source resolution; no universal blur threshold. Video dimensions describe sampled frames, not original resolution.')
    write_new(output/'review.json', report)
    return report


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root'); parser.add_argument('output'); parser.add_argument('--roi-json'); parser.add_argument('--hash-distance',type=int,default=6)
    args=parser.parse_args()
    try:
        report=analyze(args.root,args.output,json.loads(Path(args.roi_json).read_text()) if args.roi_json else None,args.hash_distance)
        errors=sum('error' in r for r in report['media'])
        print(json.dumps(dict(media=len(report['media']),groups=len(report['groups']),errors=errors,review='pending')))
        return 1 if errors else 0
    except (ValueError,OSError,subprocess.SubprocessError) as exc:
        print(str(exc),file=sys.stderr);return 2
if __name__=='__main__':sys.exit(main())
