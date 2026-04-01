# Isabl MCP Server

MCP server providing AI agents access to the Isabl genomics platform.

11 tools for querying data, searching applications, aggregating results,
and searching the built-in knowledge base (347 documents from Isabl's
source code, documentation, and API specs).

## Quick Start

```bash
# Run directly with uvx (no install needed)
uvx isabl-mcp

# Or install with pip
pip install isabl-mcp
isabl-mcp
```

Set your credentials:

```bash
export ISABL_API_URL="https://your-isabl-instance.com/api/v1/"
export ISABL_API_TOKEN="your-token-here"
```

## Tools (11)

### Data Access

| Tool | Description |
|------|-------------|
| `isabl_query` | Query any API endpoint with Django-style filters |
| `isabl_get_tree` | Get individual -> samples -> experiments hierarchy |
| `isabl_get_results` | Get result files from an analysis |
| `isabl_get_logs` | Get execution logs (stdout, stderr, script) |

### Query output convention

For experiment/sample/individual queries, use a human-readable identifier by default:

- Prefer `["system_id"]` for experiments
- Use `["identifier"]` when `system_id` is not available
- Include `pk` only when explicitly requested

Example:

```python
isabl_query(
    endpoint="experiments",
    filters={"projects": 102},
    output_fields=["system_id"]
)
```

For analysis summaries:

- If analysis is `individual_level_analysis`, show individual `system_id` (for example `IID_H210514`) instead of long targets/references experiment lists.
- If analysis is `project_level_analysis`, show project `pk` instead of long targets/references experiment lists.
- Build frontend links from `ISABL_API_URL` by removing `/api/v1/` and adding query params (for example `?analysis=<pk>`).
- Before displaying a table, include a one-line summary of what the table shows (scope, filters, and count when available).

### Applications

| Tool | Description |
|------|-------------|
| `get_apps` | Search apps and get details (`detailed=True` for full info) |
| `get_app_template` | Get boilerplate code for new apps |

### Aggregation

| Tool | Description |
|------|-------------|
| `merge_results` | Combine results from multiple analyses |
| `project_summary` | Get project statistics |

### Knowledge Base

| Tool | Description |
|------|-------------|
| `search_knowledge` | Search 347 docs by keyword |
| `get_knowledge_tree` | Browse the knowledge tree hierarchy |
| `get_knowledge_doc` | Get full content of a document |

## Configuration

| Variable | Description | Default |
|----------|-------------|---------|
| `ISABL_API_URL` | Isabl API base URL | `http://localhost:8000/api/v1/` |
| `ISABL_API_TOKEN` | API authentication token | (none) |
| `ISABL_VERIFY_SSL` | Verify SSL certificates | `true` |
| `ISABL_TIMEOUT` | HTTP timeout in seconds | `30` |

## Development

```bash
uv sync --dev
uv run pytest
uv run isabl-mcp     # start server
```

## License

MIT
