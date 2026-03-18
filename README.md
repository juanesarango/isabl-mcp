# 🧬 🦾 Isabl Skills

[![CI](https://github.com/juanesarango/isabl-skills/actions/workflows/ci.yml/badge.svg)](https://github.com/juanesarango/isabl-skills/actions/workflows/ci.yml)

> Claude Code skills and MCP server for the Isabl genomics platform

## What is Isabl?

[Isabl](https://docs.isabl.io) is a platform for the management, analysis, and visualization of genomic data ([paper](https://link.springer.com/article/10.1186/s12859-020-03879-7)).

## Install Skills

```bash
curl -fsSL https://raw.githubusercontent.com/juanesarango/isabl-skills/main/scripts/install.sh | bash
```

## Available Skills

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

See [skills/README.md](skills/README.md) for detailed guidance on which skill to use.

## MCP Server

For programmatic access to Isabl from any MCP-compatible client:

```bash
cd mcp-server && pip install -e .
```

See [mcp-server/README.md](mcp-server/README.md) for setup and available tools.

## Knowledge Base

The `knowledge/` package builds a hierarchical knowledge tree from Isabl's documentation sources (GitHub repos, Gitbook docs) for agent-consumable retrieval.

```bash
cd knowledge && uv sync
source ../.env
uv run isabl-knowledge build        # extract → summarize → tree → publish
uv run isabl-knowledge serve         # start MCP server with tree tools
```

### LLM Configuration

The summarizer and tree builder require an LLM. Configure via environment variables in `.env`:

| Variable | Description | Default |
|----------|-------------|---------|
| `LLM_BASE_URL` | Gateway URL (e.g. Portkey, Galileo) | Anthropic API |
| `LLM_API_KEY` | API key for the gateway | `ANTHROPIC_API_KEY` |
| `LLM_MODEL` | Model identifier (e.g. `@bedrock/claude-opus-4-6`) | `claude-sonnet-4-20250514` |

Copy `.env.example` to `.env` and fill in your values. The `.env` file is gitignored.

## Repository Structure

```
isabl-skills/
├── skills/          # 8 Claude Code skills
├── mcp-server/      # MCP server (9 tools)
├── knowledge/       # Knowledge tree pipeline
├── scripts/         # Install script
└── dev/             # Development notes & reference docs
```

## Related

- [Isabl Documentation](https://docs.isabl.io)
- [isabl_cli](https://github.com/papaemmelab/isabl_cli) - Python SDK

## License

MIT
