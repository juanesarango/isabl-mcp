# 🧬🤖 Isabl MCP Server

[![CI](https://github.com/juanesarango/isabl-mcp/actions/workflows/ci.yml/badge.svg)](https://github.com/juanesarango/isabl-mcp/actions/workflows/ci.yml)

> Talk to your genomics data. MCP server + knowledge base for the [Isabl](https://docs.isabl.io) platform.

## Install

### <img src="https://cdn.simpleicons.org/claude" width="16" height="16"> Claude Code

```text
/plugin marketplace add juanesarango/isabl-mcp
/plugin install isabl
```

Installs the MCP server (11 tools) + 8 guided skills as `/isabl-*` slash commands (type `/isabl` to see all). Credentials are auto-discovered from `~/.isabl/settings.json`. For MCP only (no skills): `claude mcp add isabl -- uvx isabl-mcp`.

### <img src="https://cdn.simpleicons.org/cursor" width="16" height="16"> Cursor

[![Install MCP Server](https://cursor.com/deeplink/mcp-install-dark.svg)](https://cursor.com/en/install-mcp?name=isabl&config=eyJjb21tYW5kIjogInV2eCIsICJhcmdzIjogWyJpc2FibC1tY3AiXSwgImVudiI6IHsiSVNBQkxfQVBJX1VSTCI6ICJodHRwczovL3lvdXItaXNhYmwtaW5zdGFuY2UuY29tL2FwaS92MS8iLCAiSVNBQkxfQVBJX1RPS0VOIjogInlvdXItdG9rZW4taGVyZSJ9fQ%3D%3D)

Click the badge above, or add to `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "isabl": {
      "command": "uvx",
      "args": ["isabl-mcp"],
      "env": {
        "ISABL_API_URL": "https://your-isabl-instance.com/api/v1/",
        "ISABL_API_TOKEN": "your-token"
      }
    }
  }
}
```

### <img src="https://img.icons8.com/fluency/16/chatgpt.png" width="16" height="16"> Codex

Add to `~/.codex/config.toml`:

```toml
[mcp_servers.isabl]
command = "uvx"
args = ["isabl-mcp"]
env = { "ISABL_API_URL" = "https://your-isabl-instance.com/api/v1/", "ISABL_API_TOKEN" = "your-token" }
```

### Other MCP clients

```bash
uvx isabl-mcp        # run directly, no install needed
pip install isabl-mcp # or install globally
```

Works with any MCP-compatible client (Windsurf, Zed, Claude Desktop, etc.).

## What's included

| Component | Claude Code Plugin | MCP only (Cursor, Codex, etc.) |
|-----------|-------------------|------------------------|
| 11 MCP tools (query, debug, search) | ✅ | ✅ |
| 8 MCP prompts (guided workflows) | ✅ | ✅ (client support varies) |
| 8 skills (`/isabl-*` slash commands) | ✅ | ❌ (Claude Code only) |
| Knowledge base (347 docs) | ✅ | ✅ |
| Auto-discover credentials | ✅ | ✅ |

## Credentials

The server auto-discovers your API URL and token from `~/.isabl/settings.json` (created by `isabl_cli login`). No env vars needed if you've already logged in.

You can also set them explicitly:

```bash
export ISABL_API_URL="https://your-isabl-instance.com/api/v1/"
export ISABL_API_TOKEN="your-token"
```

Env vars always take precedence over the settings file.

## What can I ask?

> "Show me all failed analyses in project 102"

> "How many WGS experiments do we have for patient ISB_H000001?"

> "Analysis 12345 failed. Show me the error logs and help me figure out what went wrong"

> "Get the VCF file paths from all succeeded MUTECT analyses in project 102"

> "How do I write a new paired tumor-normal application?"

> "Give me a summary of project 102"

## Tools (11)

| Tool | Description |
|------|------------|
| `isabl_query` | Query any API endpoint with Django-style filters |
| `isabl_get_tree` | Get Individual → Sample → Experiment → Analysis hierarchy |
| `isabl_get_results` | Get result file paths from a completed analysis |
| `isabl_get_logs` | Read stdout/stderr/script logs from any analysis |
| `get_apps` | Search for installed applications by name |
| `get_app_template` | Generate boilerplate code for a new application |
| `merge_results` | Collect and preview result files across multiple analyses |
| `project_summary` | Get project stats: experiment counts, analysis breakdown |
| `search_knowledge` | Search 347 docs from Isabl's code, docs, and API specs |
| `get_knowledge_tree` | Browse the hierarchical knowledge tree |
| `get_knowledge_doc` | Get full content of any knowledge base document |

## Skills (8) — Claude Code only

Skills are guided multi-step workflows available as `/isabl-*` slash commands. Included automatically with the plugin install.

| Skill | Purpose |
|-------|---------|
| `/isabl-query-data` | Query data from Isabl API |
| `/isabl-write-app` | Create a new Isabl application |
| `/isabl-monitor-analyses` | Track analysis status |
| `/isabl-debug-analysis` | Debug a failed analysis |
| `/isabl-merge-results` | Aggregate results across analyses |
| `/isabl-submit-data` | Submit new sequencing data |
| `/isabl-project-report` | Generate project status reports |
| `/isabl-run-pipeline` | Run multiple apps as pipeline |

## How it works

```
You (plain English) → AI Assistant → MCP Server → Isabl API → Your data
                                  |
                                  └→ Knowledge Base → Platform docs & code
```

The AI assistant uses the MCP tools to query your Isabl instance in real time, and the built-in knowledge base to understand Isabl concepts, API patterns, and best practices.

## Knowledge Tree

The knowledge base is built from 347 documents extracted from Isabl's source code, documentation, and API specifications. Browse the interactive visualization:

[**Explore the Knowledge Tree →**](https://juanesarango.github.io/isabl-mcp)

## Configuration

| Variable | Description | Default |
|----------|-------------|---------|
| `ISABL_API_URL` | Isabl API base URL | auto from `~/.isabl/settings.json` |
| `ISABL_API_TOKEN` | API authentication token | auto from `~/.isabl/settings.json` |
| `ISABL_VERIFY_SSL` | Verify SSL certificates | `true` |
| `ISABL_TIMEOUT` | HTTP timeout in seconds | `30` |

## Development

```bash
cd mcp-server
uv sync --dev
uv run pytest
uv run ruff check isabl_mcp/  # lint
uv run mcp dev isabl_mcp/server.py  # test with MCP Inspector
uv run isabl-mcp           # start server locally
```

### Contributing

1. Add tools in `mcp-server/isabl_mcp/tools/`, register in `server.py`, add tests
2. Add skills as `skills/isabl-*.md` (YAML frontmatter + workflow steps)
3. Use `ruff` for linting, type hints for Python
4. Submit a PR

## Related

- [Isabl Documentation](https://docs.isabl.io)
- [isabl_cli](https://github.com/papaemmelab/isabl_cli) — Python SDK
- [Isabl Paper](https://link.springer.com/article/10.1186/s12859-020-03879-7)

## License

MIT
