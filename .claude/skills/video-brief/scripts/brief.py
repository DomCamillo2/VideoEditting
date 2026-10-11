#!/usr/bin/env python3
"""Create a local editing brief; Python 3.9+, no dependencies, no overwrite."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import sys

PROFILE_FILE = Path(__file__).resolve().parents[1] / "assets" / "profiles.json"
PROFILES = json.loads(PROFILE_FILE.read_text(encoding="utf-8"))
HUMOR = {
    "none": "Keine eingefügten Gags; authentisches Lachen darf zur Geschichte gehören.",
    "light": "Wenige passende Gags mit Setup und Pointe; ruhige Kapitel zulassen.",
    "high": "Mehr abwechslungsreiche Gags, lesbare Pausen, keine dauerhafte Zielperson.",
}


def make_brief(style, humor=None, **values):
    if style not in PROFILES:
        raise ValueError("Unknown style: " + str(style))
    effective_humor = humor if humor is not None else PROFILES[style]["humor"]
    if effective_humor not in HUMOR:
        raise ValueError("Unknown humor level: " + str(effective_humor))
    brief = {
        "schema_version": 1,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "style": style,
        "style_label": PROFILES[style]["label"],
        "humor": effective_humor,
        "humor_basis": "explicit" if humor is not None else "profile_default",
        "gag_policy": HUMOR[effective_humor],
        "pacing": None,
        "mode": None,
        "audience": None,
        "format": None,
        "duration": None,
        "media": None,
        "music": None,
        "original_sound": None,
        "must_keep": None,
        "avoid": None,
        "chronology": None,
        "recap_allowed": None,
        "resolution_fps_color": None,
        "publishing_restrictions": None,
        "existing_project": None,
        "next_deliverable": None,
    }
    for key, value in values.items():
        if key not in brief or key in {"style", "humor", "gag_policy", "schema_version", "created_utc", "style_label", "humor_basis"}:
            raise ValueError("Unsupported brief field: " + key)
        brief[key] = (value.strip() or None) if isinstance(value, str) else value
    brief["unresolved"] = [key for key, value in brief.items() if value is None]
    return brief


def choose(prompt, options, default=None, reader=input):
    keys = list(options)
    labels = "; ".join(f"{i + 1}: {options[key]}" for i, key in enumerate(keys))
    while True:
        suffix = f" [Enter: {default}]" if default else ""
        answer = reader(f"{prompt} ({labels}){suffix}: ").strip()
        if not answer and default:
            return default
        if answer in options:
            return answer
        if answer.isdigit() and 1 <= int(answer) <= len(keys):
            return keys[int(answer) - 1]
        print("Bitte eine angezeigte Zahl oder den internen Namen eingeben.")


def write_brief(path, brief):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    # Exclusive creation is also safe against a file appearing after the prompt.
    with path.open("x", encoding="utf-8") as output:
        json.dump(brief, output, ensure_ascii=False, indent=2)
        output.write("\n")


def main(argv=None, reader=input):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    parser.add_argument("--style", choices=list(PROFILES))
    parser.add_argument("--humor", choices=list(HUMOR))
    parser.add_argument("--format", choices=["16:9", "9:16", "1:1", "4:5"])
    for flag in ("duration", "media", "music", "pacing", "must-keep", "avoid", "original-sound"):
        parser.add_argument("--" + flag)
    parser.add_argument("--non-interactive", action="store_true")
    args = parser.parse_args(argv)
    try:
        if args.output.exists() or args.output.is_symlink():
            raise FileExistsError("Briefing existiert; bitte neuen Versionsnamen wählen.")
        if args.non_interactive and not args.style:
            raise ValueError("--non-interactive braucht --style; keine stille Stilwahl.")
        if not args.non_interactive:
            if not args.style:
                args.style = choose("Welche Richtung?", {k: v["label"] for k, v in PROFILES.items()}, reader=reader)
            if args.humor is None:
                args.humor = choose("Wie viel eingefügter Humor?", {"none": "keiner", "light": "etwas", "high": "viel"}, PROFILES[args.style]["humor"], reader)
            if not args.format:
                args.format = choose("Format?", {"16:9": "Breitbild", "9:16": "Reel / Hochformat", "1:1": "Quadrat", "4:5": "Portrait"}, reader=reader)
            for field, prompt in (("duration", "Gewünschte Länge"), ("media", "Medienordner"), ("music", "Musikdateien / Wunsch")):
                if getattr(args, field) is None:
                    setattr(args, field, reader(prompt + " [Enter: noch offen]: ").strip() or None)
        fields = {key: getattr(args, key) for key in ("format", "duration", "media", "music", "pacing", "must_keep", "avoid", "original_sound")}
        result = make_brief(args.style, args.humor, **fields)
        write_brief(args.output, result)
        print(f"Briefing gespeichert: {args.output}")
        print("Offene Punkte: " + ", ".join(result["unresolved"]))
        return 0
    except (ValueError, OSError, EOFError, KeyboardInterrupt) as exc:
        print("Briefing nicht erstellt: " + (str(exc) or "Eingabe abgebrochen."), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
