#!/usr/bin/env python3
"""Sync repo skill copies/ZIPs or install into an explicit project, without dependencies."""
import argparse
import io
import json
from pathlib import Path
import re
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]
TARGETS = {"codex": Path(".agents/skills"), "claude": Path(".claude/skills")}


def tree_bytes(folder):
    """Reject symlinks; never package or overwrite an indirect path."""
    if folder.is_symlink():
        raise ValueError(f"Symlink not supported: {folder}")
    if not folder.is_dir():
        raise ValueError(f"Not a directory: {folder}")
    result = {}
    for path in sorted(folder.rglob("*")):
        if "__pycache__" in path.parts or path.name == ".DS_Store":
            continue
        if path.is_symlink():
            raise ValueError(f"Symlink not supported: {path}")
        if path.is_file():
            result[path.relative_to(folder).as_posix()] = path.read_bytes()
    return result


def sources(root=ROOT):
    result = {}
    for folder in sorted((root / "skills").iterdir()):
        if not folder.is_dir():
            continue
        name = folder.name
        if not re.fullmatch(r"video-[a-z0-9]+(?:-[a-z0-9]+)*", name):
            raise ValueError(f"Unexpected skill name: {name}")
        files = tree_bytes(folder)
        text = files.get("SKILL.md", b"").decode("utf-8")
        if not text.startswith(f"---\nname: {name}\ndescription: ") or "\n---\n" not in text[4:]:
            raise ValueError(f"Invalid skill frontmatter: {name}")
        result[name] = files
    if not result:
        raise ValueError("No source skills found")
    return result


def selected_sources(root=ROOT, selected=None):
    available = sources(root)
    if selected is None:
        return available
    if not selected:
        raise ValueError("Empty skill selection; skip installation instead")
    unknown = set(selected) - set(available)
    if unknown:
        raise ValueError("Unknown skills: " + ", ".join(sorted(unknown)))
    return {name: files for name, files in available.items() if name in selected}


def validate_targets(targets):
    if not targets or set(targets) - set(TARGETS):
        raise ValueError("Choose codex, claude or both")


def status(project, targets, root=ROOT, selected=None):
    """Report project-file presence, not host activation or global/MCP state."""
    validate_targets(targets)
    project = Path(project).resolve()
    if not project.is_dir():
        raise ValueError("Project must be an existing directory")
    source = selected_sources(root, selected)
    result = {}
    for target in targets:
        result[target] = {}
        for name, files in source.items():
            destination = project / TARGETS[target] / name
            try:
                safe_destination(destination, project)
                if not destination.exists():
                    state = "missing"
                else:
                    state = "identical" if tree_bytes(destination) == files else "different"
            except (ValueError, OSError):
                state = "unreadable_or_unsupported"
            result[target][name] = state
    return result


def zip_bytes(name, files):
    output = io.BytesIO()
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for relative, data in sorted(files.items()):
            info = zipfile.ZipInfo(name + "/" + relative, date_time=(2026, 1, 1, 0, 0, 0))
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, data)
    return output.getvalue()


def safe_destination(path, project):
    """Check all destination components before any writes begin."""
    path.relative_to(project)
    current = path
    while current != project:
        if current.is_symlink():
            raise ValueError(f"Destination is a symlink: {current}")
        if current != path and current.exists() and not current.is_dir():
            raise ValueError(f"Parent is not a directory: {current}")
        current = current.parent


def expected_outputs(source, project, targets, packages=False):
    result = {}
    for target in targets:
        for name, files in source.items():
            for relative, data in files.items():
                result[project / TARGETS[target] / name / relative] = data
    if packages:
        for name, files in source.items():
            result[project / "dist/skills" / (name + ".zip")] = zip_bytes(name, files)
    return result


def install(project, targets, root=ROOT, selected=None, dry_run=False):
    validate_targets(targets)
    project = Path(project).resolve()
    if not project.is_dir():
        raise ValueError("Project must be an existing directory")
    source = selected_sources(root, selected)
    output = expected_outputs(source, project, targets)
    # Preflight every skill before creating anything. Exact copies are idempotent.
    for path in output:
        safe_destination(path, project)
    for target in targets:
        for name, files in source.items():
            destination = project / TARGETS[target] / name
            if destination.exists() and tree_bytes(destination) != files:
                raise ValueError(f"Existing skill differs; preserve/move it before installing: {destination}")
    if dry_run:
        return len(source)
    for path, data in output.items():
        if not path.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open("xb") as handle:
                handle.write(data)
    return len(source)


def sync(check=False, root=ROOT):
    root = root.resolve()
    source = sources(root)
    output = expected_outputs(source, root, list(TARGETS), packages=True)
    errors = []
    # Generated directories are deliberately tracked; unrelated skills are left alone.
    for target in TARGETS.values():
        for name in source:
            folder = root / target / name
            safe_destination(folder, root)
            if folder.exists():
                extras = set(tree_bytes(folder)) - set(source[name])
                if extras:
                    raise ValueError(f"Unexpected files in generated skill {folder}: {sorted(extras)}")
    for path in output:
        safe_destination(path, root)
        if path.exists() and not path.is_file():
            raise ValueError(f"Expected file: {path}")
    for path, data in output.items():
        if not path.exists() or path.read_bytes() != data:
            errors.append(str(path.relative_to(root)))
            if not check:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(data)
    if check and errors:
        raise ValueError("Generated copies/ZIPs differ; run sync:\n" + "\n".join(errors))
    return len(source)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    sync_parser = sub.add_parser("sync", help="Regenerate only this repo's distributed copies and ZIPs")
    sync_parser.add_argument("--check", action="store_true")
    install_parser = sub.add_parser("install", help="Copy to an existing project; refuse divergent skills")
    install_parser.add_argument("--project", type=Path, required=True)
    install_parser.add_argument("--target", choices=["codex", "claude", "both"], default="both")
    install_parser.add_argument("--skill", action="append", help="Install only this skill; repeat for a subset")
    install_parser.add_argument("--dry-run", action="store_true", help="Preflight selected copies without writing")
    status_parser = sub.add_parser("status", help="Inspect project skill files without modifying anything")
    status_parser.add_argument("--project", type=Path, required=True)
    status_parser.add_argument("--target", choices=["codex", "claude", "both"], default="both")
    status_parser.add_argument("--skill", action="append")
    args = parser.parse_args(argv)
    try:
        if args.command == "sync":
            count = sync(args.check)
            print(f"{count} skills: copies and ZIPs {'verified' if args.check else 'synchronized'}")
        else:
            targets = list(TARGETS) if args.target == "both" else [args.target]
            if args.command == "status":
                print(json.dumps(status(args.project, targets, selected=args.skill), indent=2))
            else:
                count = install(args.project, targets, selected=args.skill, dry_run=args.dry_run)
                action = "would be installed/retained" if args.dry_run else "installed/retained"
                print(f"{count} skills {action} in {args.project} for {', '.join(targets)}")
        return 0
    except (ValueError, OSError) as exc:
        print(str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
