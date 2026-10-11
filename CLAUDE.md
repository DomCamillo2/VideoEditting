# VideoEditting

Read [AGENTS.md](AGENTS.md) for repository rules. On first adoption of this toolkit, read [SETUP.md](SETUP.md): first ask all/selected/no additional skills, then assess useful MCPs and ask which to install. Use `/video-setup`. Known choices and existing tools carry over. Do not trigger onboarding for repository maintenance or established film revisions. A clone already contains project skill copies; do not pretend they need reinstalling.

Project skills are in `.claude/skills/`. After setup (or declining additional installations), use [START_HERE.md](START_HERE.md) and `/video-editing` for an edit. Only then ask missing style preferences: serious/no gags, emotional/light humor, or clearly funny. Current user instructions and an existing brief take priority over examples. Setup instructions do not themselves authorize tool installation.

Edit canonical skill sources in `skills/`, then run `python3 tools/manage_skills.py sync`. The generated copies must match. Test with `python3 -m unittest discover -s tests -v`, `python3 tools/manage_skills.py sync --check` and `python3 tools/check_repo.py`. For studio changes also run its lint/build and relevant visual checks.
