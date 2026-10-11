#!/usr/bin/env python3
"""Verify the explicit publication inventory, including force-added ignored media."""
import hashlib
import json
from pathlib import Path
import subprocess
import shutil

MEDIA_EXTENSIONS = {'.mp3', '.wav', '.m4a', '.aac', '.flac', '.ogg', '.opus', '.aiff',
                    '.mp4', '.mov', '.m4v', '.mkv', '.webm', '.avi',
                    '.jpg', '.jpeg', '.png', '.gif', '.webp', '.heic', '.heif', '.svg'}
PRIVATE_PREFIXES = ('local/', 'private/', 'analysis/', 'exports/', 'studio/public/local/')
SKIP = {'.git', 'node_modules', 'out', 'build', '__pycache__', '.cache'}


def repository_files(root):
    root = Path(root).resolve()
    # A downloaded ZIP might live inside an unrelated parent Git repository.
    result = (subprocess.run(['git', '-C', str(root), 'rev-parse', '--show-toplevel'],
                             capture_output=True, text=True) if shutil.which('git') else None)
    if result is not None and result.returncode == 0 and Path(result.stdout.strip()).resolve() == root:
        raw = subprocess.check_output(['git', '-C', str(root), 'ls-files', '-z'])
        return [name.decode('utf-8') for name in raw.split(b'\0') if name]
    # ZIP fallback: examine distributable files, not local working media.
    files = []
    def walk(folder):
        for path in folder.iterdir():
            relative = path.relative_to(root).as_posix()
            if path.name in SKIP or relative.startswith(PRIVATE_PREFIXES) or relative + '/' in PRIVATE_PREFIXES:
                continue
            if path.is_symlink() or path.is_file():
                files.append(relative)
            elif path.is_dir():
                walk(path)
    walk(root)
    return files


def audit_assets(root, files=None):
    root = Path(root).resolve()
    files = repository_files(root) if files is None else files
    errors = []
    try:
        inventory = json.loads((root / 'public-assets.json').read_text(encoding='utf-8'))
        entries = inventory['assets']
        if not isinstance(entries, list):
            raise ValueError('assets must be a list')
        approved = {}
        for entry in entries:
            name = entry['path']
            if not isinstance(name, str) or name in approved:
                raise ValueError('Duplicate or invalid asset path')
            if not name or ':' in name or '\\' in name or any(p in ('', '.', '..') for p in name.split('/')):
                raise ValueError('Asset inventory paths must be project-relative')
            if not all(isinstance(entry.get(key), str) and entry[key].strip() for key in ('sha256', 'license', 'provenance')):
                raise ValueError('Asset needs hash, license and provenance')
            approved[name] = entry
    except (OSError, ValueError, KeyError, TypeError) as exc:
        return ['Invalid public-assets.json: ' + str(exc)]
    media = {name for name in files if Path(name).suffix.lower() in MEDIA_EXTENSIONS}
    for name in files:
        if name.startswith(PRIVATE_PREFIXES):
            errors.append(name + ': private working file is tracked by Git')
    for name in sorted(media):
        if name not in approved:
            errors.append(name + ': media is not in the publication inventory')
            continue
        path = root / name
        if path.is_symlink() or root not in path.resolve().parents:
            errors.append(name + ': public media must not be a symlink or escape the project')
            continue
        try:
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
        except OSError as exc:
            errors.append(name + ': ' + str(exc))
            continue
        if digest != approved[name]['sha256']:
            errors.append(name + ': content differs from reviewed publication hash')
    for name in sorted(set(approved) - media):
        errors.append(name + ': inventory entry has no distributed media file')
    return errors
