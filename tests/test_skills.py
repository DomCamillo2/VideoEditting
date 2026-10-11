"""Portable packaging and first-choice behavior; no network or LLM invocation."""
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def load(name, relative):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


manager = load("skill_manager", "tools/manage_skills.py")
brief = load("brief_wizard", "skills/video-brief/scripts/brief.py")


class BriefTests(unittest.TestCase):
    def test_style_defaults_and_missing_information(self):
        for style, humor in (("serious", "none"), ("emotional", "light"), ("funny", "high")):
            result = brief.make_brief(style)
            self.assertEqual(result["humor"], humor)
            self.assertEqual(result["humor_basis"], "profile_default")
            self.assertIn("duration", result["unresolved"])
            self.assertIsNone(result["format"])
            self.assertIsNone(result["pacing"])

    def test_explicit_humor_and_pace_override(self):
        result = brief.make_brief("funny", "none", pacing="ruhig", duration=" 30 Sekunden ")
        self.assertEqual(result["humor"], "none")
        self.assertEqual(result["humor_basis"], "explicit")
        self.assertEqual(result["pacing"], "ruhig")
        self.assertEqual(result["duration"], "30 Sekunden")
        self.assertNotIn("duration", result["unresolved"])
        self.assertTrue(result["gag_policy"].startswith("Keine"))

    def test_invalid_choices(self):
        for args in (("unknown", None), ("serious", "unknown")):
            with self.assertRaises(ValueError):
                brief.make_brief(*args)

    def test_no_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "brief.json"
            path.write_text("existing", encoding="utf-8")
            with self.assertRaises(FileExistsError):
                brief.write_brief(path, brief.make_brief("funny"))
            self.assertEqual(path.read_text(), "existing")

    def test_noninteractive_does_not_ask(self):
        with tempfile.TemporaryDirectory() as tmp, contextlib.redirect_stdout(io.StringIO()):
            path = Path(tmp) / "brief.json"
            def fail(_):
                self.fail("Known choices must not prompt")
            code = brief.main([str(path), "--style", "serious", "--non-interactive"], reader=fail)
            self.assertEqual(code, 0)
            self.assertEqual(json.loads(path.read_text())["humor"], "none")

    def test_noninteractive_requires_explicit_style(self):
        with tempfile.TemporaryDirectory() as tmp, contextlib.redirect_stderr(io.StringIO()):
            path = Path(tmp) / "brief.json"
            self.assertEqual(brief.main([str(path), "--non-interactive"]), 2)
            self.assertFalse(path.exists())

    def test_wizard_choices_and_retry(self):
        with tempfile.TemporaryDirectory() as tmp, contextlib.redirect_stdout(io.StringIO()):
            path = Path(tmp) / "brief.json"
            answers = iter(["invalid", "3", "1", "2", "40 Sekunden", "local/raw", "eigene.wav"])
            prompts = []
            def reader(prompt):
                prompts.append(prompt)
                return next(answers)
            self.assertEqual(brief.main([str(path)], reader=reader), 0)
            result = json.loads(path.read_text())
            self.assertIn("Welche Richtung", prompts[0])
            self.assertEqual((result["style"], result["humor"], result["format"]), ("funny", "none", "9:16"))

    def test_eof_does_not_choose_or_create(self):
        with tempfile.TemporaryDirectory() as tmp, contextlib.redirect_stderr(io.StringIO()):
            path = Path(tmp) / "brief.json"
            def reader(_):
                raise EOFError()
            self.assertEqual(brief.main([str(path)], reader=reader), 2)
            self.assertFalse(path.exists())


class PackageTests(unittest.TestCase):
    def test_skill_packages_have_only_internal_file_links(self):
        source = manager.sources()
        self.assertEqual(len(source), 9)
        for name, files in source.items():
            text = files["SKILL.md"].decode()
            for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", text):
                if "://" in target:
                    continue
                self.assertNotIn("..", Path(target).parts, (name, target))
                self.assertIn(target, files, (name, target))
            self.assertIn("agents/openai.yaml", files)

    def test_zip_is_deterministic_and_self_contained(self):
        for name, files in manager.sources().items():
            data = manager.zip_bytes(name, files)
            self.assertEqual(data, manager.zip_bytes(name, dict(reversed(list(files.items())))))
            with zipfile.ZipFile(io.BytesIO(data)) as package:
                self.assertEqual(set(package.namelist()), {name + "/" + path for path in files})
                self.assertEqual(package.read(name + "/SKILL.md"), files["SKILL.md"])

    def test_installer_copies_both_hosts_and_is_repeatable(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            self.assertEqual(manager.install(target, ["codex", "claude"]), 9)
            self.assertEqual(manager.install(target, ["codex", "claude"]), 9)
            for host in manager.TARGETS.values():
                for name, files in manager.sources().items():
                    self.assertEqual(manager.tree_bytes(target / host / name), files)

    def test_conflict_preflight_writes_nothing(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            conflict = target / ".claude/skills/video-comedy/SKILL.md"
            conflict.parent.mkdir(parents=True)
            conflict.write_text("custom user skill")
            with self.assertRaisesRegex(ValueError, "Existing skill differs"):
                manager.install(target, ["codex", "claude"])
            self.assertEqual(conflict.read_text(), "custom user skill")
            self.assertFalse((target / ".agents").exists())

    def test_destination_symlinks_are_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "project"
            outside = Path(tmp) / "outside"
            target.mkdir()
            outside.mkdir()
            (target / ".agents").symlink_to(outside, target_is_directory=True)
            with self.assertRaisesRegex(ValueError, "symlink"):
                manager.install(target, ["codex"])
            self.assertEqual(list(outside.iterdir()), [])

    def test_sync_check_detects_drift(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skill = root / "skills/video-test/SKILL.md"
            skill.parent.mkdir(parents=True)
            skill.write_text("---\nname: video-test\ndescription: A test skill\n---\nExample\n")
            manager.sync(root=root)
            manager.sync(check=True, root=root)
            generated = root / ".agents/skills/video-test/SKILL.md"
            generated.write_text("modified")
            with self.assertRaisesRegex(ValueError, "differ"):
                manager.sync(check=True, root=root)
            self.assertEqual(generated.read_text(), "modified")

    def test_extracted_brief_runs_without_repo(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            files = manager.sources()["video-brief"]
            data = manager.zip_bytes("video-brief", files)
            with zipfile.ZipFile(io.BytesIO(data)) as package:
                package.extractall(root)
            script = root / "video-brief/scripts/brief.py"
            output = root / "standalone.json"
            result = subprocess.run([sys.executable, str(script), str(output), "--style", "emotional", "--non-interactive"], cwd=root, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(output.read_text())["humor"], "light")


if __name__ == "__main__":
    unittest.main()
