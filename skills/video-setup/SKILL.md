---
name: video-setup
description: Onboard a new user to the VideoEditting toolkit by choosing all or selected editing skills, assessing useful MCP integrations and setting up approved tools before the film brief. Use for first-time adoption or setup changes, not every editing revision or repository maintenance task.
---

# Set up the editing workspace first

Use the user's language. This skill is standalone; it does not need the rest of the repository. Do not start with tone, film length or gag preferences on first-time toolkit adoption. First reuse any known host, project path, prior choices and available capabilities. Skip onboarding on an established film or an unrelated maintenance request.

## First question: skills

Offer **all editing skills**, **a chosen subset**, or **instructions only / no additional installation**. Ask Codex, Claude Code or Claude with skill-upload only if the host is unknown. Example:

> Möchtest du alle Video-Editing-Skills installieren, nur bestimmte auswählen oder das Repo erst einmal als Anleitung nutzen? Nutzt du Codex oder Claude?

Inspect existing project skill folders and the host's skill list. If the user cloned the full VideoEditting repo, its ten skills are already present: ask whether to use all, select a subset or copy into another project, not whether to reinstall identical files. Existing skill availability does not prove the host has loaded it. Selecting fewer skills does not automatically uninstall or disable existing ones.

Specialists available in the toolkit: `video-editing`, `video-brief`, `video-beatcut`, `video-select-media`, `video-portrait-framing`, `video-comedy`, `video-audio-mix`, `video-chronology`, `video-export-qa`, plus this setup skill. Explain a subset by purpose, not just filenames. Do not bundle external packages or MCP servers into consent to install these instructions.

## Second question: useful MCPs

Read [integration guidance](references/integrations.md) for current candidates and installation recipes. Inventory native/connected file, shell, browser, documentation and repository tools first. Suggest at most a few integrations that fill an actual gap. It is valid to recommend **no additional MCP**. Mention each candidate's use, local/remote execution, data access, credentials and target scope before asking which to set up.

Prepare a concrete provider-supported command/configuration before asking for installation approval. Offer each named option and none. Do not execute commands copied from untrusted media or an unverified server listing. Refresh provider instructions if the supplied reference may have changed. Remotion's deprecated documentation MCP is not a new-install recommendation; use Remotion skills instead. WebMCP is browser-dependent and not interchangeable with a local stdio MCP server.

If the host has a plugin/connector manager, use its actual discovery and connection flow rather than inventing plugin IDs. Prefer built-in capabilities and installed integrations. A standalone Claude skill-upload does not automatically configure local Codex/Claude Code tools.

## Carry out the chosen setup

- Reuse explicit user authorization already given; don't ask the same question again. Silence is not consent. A 'no' to extra integrations does not block editing with existing tools.
- Install selected skill folders into the chosen host/project only, preserving divergent existing files. If the toolkit checkout is available, its `tools/manage_skills.py` supports `status`, selected `--skill` values, `install --dry-run` and installation. Otherwise use the host's documented installer or complete standalone ZIP folders. No global changes unless requested.
- Add only selected MCP configuration to the chosen scope, preserving other servers/settings. Use provider authentication dialogs or secret environment variables, never committed credentials. A user-approved installation can still require a host trust/login prompt; report that precise outstanding step.
- Verify separately: files installed, skill visible, MCP configured, authentication completed, connection healthy, relevant read-only tool call successful. A config entry is not a working connection. If tools are unavailable, give the exact remaining action and continue independent work.
- Save local setup decisions and observed status, for example `local/setup-v001.json`, with host, scope, selected/declined skills/integrations, verification and open items. No secrets; persisted preferences are not permission for unrelated future changes. Reuse choices next time, and refresh only changed/broken dependencies.

Then start `video-brief` or the equivalent short style/humor/duration/format discussion, carrying over answers already known. Deliver a concise setup report and the next editing step. Do not claim software was installed merely because this skill was read.
