#!/usr/bin/env python3
"""Repository shortcut to the self-contained video-brief skill wizard."""
from pathlib import Path
import runpy

if __name__ == "__main__":
    runpy.run_path(str(Path(__file__).resolve().parents[1] / "skills/video-brief/scripts/brief.py"), run_name="__main__")
