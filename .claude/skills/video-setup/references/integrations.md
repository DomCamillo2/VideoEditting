# Integrations for video editing

Research checked 2026-10-11. These are candidates, not mandatory dependencies. Re-check provider instructions before installation. Native tools, existing connections and a working CLI can already cover the need. No external service gets permission to upload media merely by being installed.

## Choose by missing capability

| Candidate | When it helps | Requirements / access | When to skip |
|---|---|---|---|
| Context7 MCP | Current API/library docs while building effects | Remote documentation queries; provider API key/OAuth depending setup and limits | Existing docs/browser tools already suffice |
| Microsoft Playwright MCP | Inspect and operate a local Remotion Studio or browser preview | Local Node.js process and compatible browser; pages visited are accessible to the agent | Existing browser control or Playwright CLI already works |
| GitHub MCP | Repositories, issues, PRs and CI in a hosted workflow | GitHub authentication and chosen repository permissions; remote or local server | `git`/`gh` or a GitHub connector already covers the task |
| Filesystem reference MCP | A desktop host lacks local file tools | Local Node.js process; explicitly allowed project/media directories; server includes write tools | Codex/Claude Code already have suitable workspace access |

Provider documentation: [Context7](https://github.com/upstash/context7), [Playwright MCP](https://github.com/microsoft/playwright-mcp), [GitHub MCP](https://github.com/github/github-mcp-server), [Filesystem server](https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem). The table is our task-specific assessment, not a claim that these providers are needed by every editor.

**Remotion:** prefer the official [Remotion skills](https://github.com/remotion-dev/skills) for renderer guidance and `/remotion-docs`. The old documentation MCP is [deprecated](https://www.remotion.dev/docs/ai/mcp), so don't recommend installing it. Inspect whether a Remotion plugin is already installed before adding duplicate skills. Remotion [WebMCP](https://www.remotion.dev/docs/ai/webmcp) exposes Studio features through compatible browsers/agents; verify both host support and the project's pinned Remotion version. It is not a generic server URL to paste into every MCP client.

FFmpeg/ffprobe, ExifTool, Node/npm and Remotion are **local programs/libraries**, not MCP servers. A filesystem MCP alone cannot render a film or execute those programs. A VN editor integration is editor-specific, not a universal MCP requirement. Cloud storage connectors are useful only when the user's material is actually there; prefer the host's official connection flow.

## Installation after the user's choice

Before making changes, name the selected server, source, configuration location and access. Read existing config safely without printing secrets. Keep unrelated entries and use project scope unless a broader scope was requested. Validate the current release/command before executing; `latest` below is an upstream example, not a pinned reproducible dependency.

### Codex

Codex supports local stdio and remote HTTP MCPs. Inspect configured servers with `codex mcp list`; configuration alone doesn't prove connection. Project-scoped entries live in `.codex/config.toml` in a trusted project; user-wide entries live in the user's Codex config. `codex mcp add` uses the default configuration scope, so **do not claim that command is project-local**. For a project-only request, merge the selected table into the project config. [Official Codex MCP documentation](https://developers.openai.com/codex/mcp).

Example **only for a selected Playwright integration**:

```toml
[mcp_servers.video_playwright]
command = "npx"
args = ["-y", "@playwright/mcp@latest", "--isolated"]
```

The isolated browser starts without the user's normal browser profile. Verify current package version and record the resolved version in the local setup report. Check the host's active MCP tools and open the intended local preview as a smoke test; DOM success is not pixel or audio QA.

Context7 offers `https://mcp.context7.com/mcp` for API-key access and `/mcp/oauth` for supported OAuth clients; follow its current [client setup](https://context7.com/docs/resources/all-clients). For a selected OAuth connection, a project entry is:

```toml
[mcp_servers.video_context7]
url = "https://mcp.context7.com/mcp/oauth"
```

Then use `codex mcp login video_context7` from the trusted project and complete the provider's login. For API-key access to `/mcp`, a Codex HTTP entry can use `bearer_token_env_var` instead of a literal key. No authentication success should be inferred until a documentation query works.

### Claude Code

For a selected local Playwright server, this stores project configuration:

```sh
claude mcp add --scope project --transport stdio video-playwright -- npx -y @playwright/mcp@latest --isolated
```

For a selected Context7 OAuth connection:

```sh
claude mcp add --scope project --transport http video-context7 https://mcp.context7.com/mcp/oauth
```

Project MCP entries are in `.mcp.json`; retain existing servers. Inspect with `claude mcp list`, then `/mcp` for connection/authentication status. The host may require approval of a project server. [Official Claude Code MCP documentation](https://code.claude.com/docs/en/mcp).

### GitHub, files and account connectors

Follow the provider's current host-specific recipe rather than pasting a VS Code `servers` object into a Claude `mcpServers` file. GitHub read-only mode is suitable for inspection; writing PRs needs the corresponding requested permissions. Access tokens stay in the host's secret mechanism. Limit a filesystem server to the actual workspace/media folders; never substitute the whole home folder merely to avoid choosing paths.

Claude account skills, Claude Code project configuration and desktop connectors are distinct installation surfaces. Use the current host's supported flow; a ZIP upload doesn't install a stdio process. If local execution is unavailable, explain that limitation and use available connected tools or produce an edit plan.

## Record truthful status

Distinguish `declined`, `already_available`, `selected`, `configured`, `auth_pending`, `connected`, `smoke_test_passed`, and `failed`. Store a short test result and time, not credentials or complete raw configs. Check only the selected integrations; don't add unrelated MCPs as an upgrade bundle. If an installation fails, preserve the usable setup, report the specific failing step and continue work that doesn't depend on it.
