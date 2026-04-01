---
description: 
alwaysApply: true
---

# Isabl MCP Server

MCP server and Claude Code skills for the Isabl genomics platform.

## What This Repo Contains

- `mcp-server/` - MCP server with 11 tools + 8 prompts for Isabl API and knowledge base
- `skills/` - 8 Claude Code skills for guided Isabl workflows
- `knowledge/` - Knowledge tree pipeline (347 docs from Isabl source, docs, API specs)
- `dev/` - Development notes and reference documentation

## Quick Reference

### Isabl Data Model

```
Individual → Sample → Experiment → Analysis
                ↓
              Aliquot
```

- **Experiment**: Sequencing data (FASTQ, BAM)
- **Analysis**: Pipeline run on experiment(s)
- **Application**: Pipeline definition (inherits AbstractApplication)

### Common Patterns

```python
import isabl_cli as ii

# Query data
experiments = ii.get_experiments(projects=102, technique__method="WGS")
analyses = ii.get_analyses(status="SUCCEEDED", application__name="MUTECT")

# Get results
for a in analyses:
    results = a.results  # Dict of result files
    storage = a.storage_url  # Path to analysis directory
```

### Analysis Statuses

`CREATED` → `STAGED` → `SUBMITTED` → `STARTED` → `SUCCEEDED` / `FAILED`

## Development Commands

```bash
# Install skills locally
./scripts/install.sh

# Run MCP server tests
cd mcp-server && uv run pytest

# Start local API (requires podman)
cd ~/isabl/isabl_api && podman compose up -d
```

## Code Style

- Use `isabl_cli as ii` import convention
- Filter queries with Django-style syntax: `status="SUCCEEDED"`
- Applications inherit from `AbstractApplication`
