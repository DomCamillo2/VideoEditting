# VideoEditting

Read [AGENTS.md](AGENTS.md) for repository rules. Read [START_HERE.md](START_HERE.md) for a new editing job. Current user instructions and an existing brief take priority over examples.

Project skills are in `.claude/skills/`; use `/video-editing` for a full edit or the relevant specialist. On a **new film with missing preferences**, offer serious/no gags, emotional/light humor, or clearly funny before creative cutting. Reuse known answers; do not ask this for repository maintenance or a small revision.

Edit canonical skill sources in `skills/`, then run `python3 tools/manage_skills.py sync`. The generated copies must match. Test with `python3 -m unittest discover -s tests -v`, `python3 tools/manage_skills.py sync --check` and `python3 tools/check_repo.py`. For studio changes also run its lint/build and relevant visual checks.
