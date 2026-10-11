#!/usr/bin/env python3
"""Check local Markdown references and public-repo hygiene without network access."""
from pathlib import Path
import re
import sys
from urllib.parse import unquote
from public_assets import audit_assets

root=Path(__file__).resolve().parents[1]
errors=audit_assets(root)
skip={'.git','node_modules','out','build','local','analysis','exports','private','__pycache__'}
for path in root.rglob('*'):
    if set(path.relative_to(root).parts)&skip or not path.is_file():continue
    if path.suffix not in {'.md','.py','.tsx','.ts','.json','.yaml','.yml','.csv'}:continue
    text=path.read_text(encoding='utf-8')
    if path.name!='check_repo.py' and re.search(r'/Users/[^/\s]+/|/home/[^/\s]+/',text):
        errors.append(str(path.relative_to(root))+': absolute private user path')
    if path.suffix=='.md':
        for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)',text):
            target=target.strip('<>').split('#')[0]
            if not target or re.match(r'^[a-z]+:',target):continue
            resolved=(path.parent/unquote(target)).resolve()
            if not resolved.exists():errors.append(str(path.relative_to(root))+': broken link '+target)
if errors:
    print('\n'.join(errors));sys.exit(1)
print('Local Markdown links, path hygiene and public asset inventory passed')
