# Isabl Knowledge Tree: Design Document

## Problem

Isabl platform knowledge is scattered across GitHub repos (API, CLI, frontend, apps), Gitbook docs, and Jupyter notebooks. Today, our MCP server can query the Isabl API, and our skills guide how to use it — but agents lack deep domain knowledge:

- **Which API endpoints to use** for a given task
- **How to build apps** with the SDK (`AbstractApplication` patterns, real examples)
- **How to use `isabl_cli`** in notebooks (SDK reference + real patterns)
- **What pipelines exist**, what they do, what their outputs mean
- **How entities relate** in real-world usage

The agent can call the API but doesn't understand *what to call* or *why*. We need to extract this knowledge from source material and make it available as a structured, navigable resource.

## Approach

Inspired by [Genentech's arcane_knowledge](https://github.com/Genentech-Corporate-Communications/arcane_knowledge) and [PageIndex](https://github.com/VectifyAI/PageIndex), we build an LLM-generated hierarchical knowledge tree from all Isabl sources. The tree is the single artifact; multiple renderers consume it.

The tree replaces traditional RAG/vector stores with a navigable hierarchy that agents traverse by reasoning — the same approach that gives arcane_knowledge 98%+ retrieval relevance.

## Architecture

```
EXTRACT → SUMMARIZE → BUILD TREE → RENDER
                          │
                      tree.json
                       ╱  │  ╲
                      ╱   │   ╲
               GitHub    MCP       Static
               Repo      Resources Site
              (folders)  (agents)  (browsable)
```

The tree is the product. The GitHub repo of folders with READMEs IS the tree. MCP resources serve the same tree to agents. The static site renders it for humans. Same content, different access patterns.

### Three consumers of tree.json

| Output | Purpose | Audience |
|---|---|---|
| **MCP resources** | Agent navigates tree on-demand via `get_tree()`, `get_node()`, `get_document()` | LLMs, Claude Code skills |
| **GitHub repo** (`isabl-knowledge-tree`) | Folder hierarchy with README.md at each node | Developers, human browsing |
| **Static site** (GitHub Pages) | Interactive browsable version of the repo | Conference attendees, researchers |

### MCP Integration

The knowledge tree is served as a **separate MCP server** from the existing Isabl API MCP server:

- **Existing `isabl-mcp`**: live API access (queries, analyses, experiments). Requires auth.
- **New `isabl-knowledge-mcp`**: static reference material (docs, patterns, examples). No auth needed, portable.

An agent uses both together: knowledge MCP to understand *what to do*, API MCP to *do it*.

MCP tools:

| Tool | Description |
|---|---|
| `get_tree()` | Returns top-level nodes with summaries |
| `get_node(node_id)` | Returns a node's children, summary, and linked documents |
| `get_document(doc_id)` | Returns the full markdown content of a source document |

The agent walks the tree by starting at the root, reading summaries, and drilling into relevant branches — reasoning-based retrieval, not vector similarity.

## Pipeline Stages

### Stage 1: Extract

Pull content from each source into a unified markdown format.

Each document becomes:
```python
{
    "doc_id": "isabl_cli/api/get_experiments",
    "source_type": "github_docstring",
    "source_url": "https://github.com/...",
    "title": "",          # filled by LLM in stage 2
    "content": "...",     # raw markdown
    "metadata": {}
}
```

Six extractors:

| Source | Strategy | What gets extracted |
|---|---|---|
| **isabl_api** (Django) | Parse OpenAPI spec, scan models/views/serializers | API endpoints, model schemas, relationships |
| **isabl_cli** (Python CLI) | AST parse docstrings + function signatures | CLI commands, SDK functions, usage examples |
| **Frontend** (web) | Extract routes, component names, inline docs | UI capabilities, user-facing features |
| **Apps** (2-3 repos) | Parse `AbstractApplication` subclasses | Pipeline definitions, inputs/outputs, what each app does |
| **Gitbook docs** | Fetch published pages, convert to markdown | Tutorials, guides, conceptual docs |
| **Jupyter notebooks** | `nbconvert` to markdown, preserve code + outputs | Analysis workflows, real-world usage patterns |

### Stage 2: Summarize

For each document, an LLM generates:
- Descriptive title (5-10 words)
- 2-3 sentence summary
- 3-5 topic tags
- 3-5 questions this document answers
- For code documents: key function signatures, parameters, return types

### Stage 3: Build Tree

All summaries sent to an LLM:

> "Organize these {N} documents into a 3-4 level hierarchy. Group by
> capabilities and use cases: API usage, pipeline development, data analysis,
> platform administration. Max 100 nodes. Output JSON."

Output: `tree.json`

```json
{
  "id": "root",
  "title": "Isabl Genomics Platform",
  "children": [
    {
      "id": "0001",
      "title": "API & SDK Reference",
      "summary": "Endpoints, query patterns, and Python SDK usage",
      "children": [
        {
          "id": "0001.0001",
          "title": "Querying Experiments & Analyses",
          "summary": "How to find and filter experiments, analyses, and results",
          "documents": ["cli/get_experiments", "api/experiments_endpoint", "docs/querying_data"]
        }
      ]
    },
    {
      "id": "0002",
      "title": "Building Pipeline Applications",
      "summary": "How to create apps using AbstractApplication",
      "children": [
        {
          "id": "0002.0001",
          "title": "Variant Calling Pipelines",
          "summary": "...",
          "documents": ["apps/mutect2", "apps/strelka", "notebooks/somatic_analysis"]
        }
      ]
    }
  ]
}
```

### Stage 4: Render

Three renderers consume `tree.json`:

**GitHub renderer**: writes folder hierarchy with README.md at each node (like arcane_knowledge). Pushes to `isabl-knowledge-tree` repo.

**MCP renderer**: bundles tree.json + all document markdown into the knowledge MCP server's data directory. Agent accesses via tools.

**Static site**: GitHub Pages renders the repo directly. The README hierarchy IS the site.

## Configuration

Single YAML file drives the pipeline:

```yaml
# knowledge.yaml
name: isabl-knowledge
output:
  github_repo: isabl-knowledge-tree
  site: github-pages

sources:
  - name: isabl_api
    type: github_django
    repo: isabl/isabl_api
    extract: [openapi, models, views]

  - name: isabl_cli
    type: github_python
    repo: isabl/isabl_cli
    extract: [docstrings, cli_commands]

  - name: frontend
    type: github_frontend
    repo: isabl/isabl_web
    extract: [routes, components]

  - name: docs
    type: gitbook
    url: https://docs.isabl.io

  - name: apps
    type: github_apps
    repos:
      - isabl/isabl-apps-repo-1
      - isabl/isabl-apps-repo-2
    base_class: AbstractApplication

  - name: notebooks
    type: jupyter
    repos:
      - isabl/analysis-notebooks

tree:
  max_depth: 4
  max_nodes: 100
  orientation: "capabilities and use cases, not code internals"
```

## Project Structure

```
isabl-ai-integration/
├── skills/
├── mcp-server/                   # existing API MCP server
└── knowledge/                    # NEW
    ├── knowledge.yaml            # pipeline config
    ├── pyproject.toml            # uv project, CLI entrypoint
    ├── src/isabl_knowledge/
    │   ├── cli.py                # CLI: extract, summarize, build, publish
    │   ├── extractors/
    │   │   ├── github_python.py  # docstrings, CLI commands
    │   │   ├── github_django.py  # OpenAPI, models, views
    │   │   ├── github_apps.py    # AbstractApplication subclasses
    │   │   ├── gitbook.py        # fetch published docs
    │   │   └── jupyter.py        # nbconvert notebooks
    │   ├── summarizer.py         # LLM summarization (pass 1)
    │   ├── tree_builder.py       # LLM clustering (pass 2)
    │   ├── renderers/
    │   │   ├── github_repo.py    # write folder + README hierarchy
    │   │   └── mcp_resources.py  # bundle for MCP server
    │   └── mcp_server.py         # standalone knowledge MCP server
    ├── data/                     # extracted documents cache (markdown)
    └── output/
        ├── tree.json             # the tree
        └── site/                 # generated repo/site content
```

## CLI Usage

```bash
# Full pipeline
uv run isabl-knowledge build

# Step by step
uv run isabl-knowledge extract      # pull all sources → data/
uv run isabl-knowledge summarize    # LLM summarize → data/*.meta.json
uv run isabl-knowledge tree         # LLM cluster → output/tree.json
uv run isabl-knowledge publish      # render repo + push to GitHub

# Serve knowledge MCP locally
uv run isabl-knowledge serve        # start MCP server on stdio
```

## Implementation Phases

1. **Scaffold** — project setup (`uv init`), CLI skeleton, config loader
2. **Extractors** — start with `github_python` (isabl_cli) and `jupyter`. Get one end-to-end flow working before building other extractors
3. **Summarizer + tree builder** — LLM calls via Anthropic SDK. Test with small subset first
4. **GitHub renderer** — write folder/README hierarchy, push to output repo. This also gives you the static site via GitHub Pages
5. **MCP server** — load `tree.json`, expose 3 tools. Reuse patterns from existing `mcp-server/`

Phase 2 = first working demo. Phase 4 = browsable output. Phase 5 = agent-accessible.

## Key Design Decisions

- **Fully automated**: LLM generates the tree structure and summaries, no manual curation
- **Tree over vectors**: reasoning-based retrieval (navigate hierarchy) instead of similarity search (vector RAG)
- **Separate MCP servers**: knowledge (static, no auth) vs. API (live, auth required)
- **Config-driven**: adding sources = adding lines to `knowledge.yaml`
- **Single artifact**: `tree.json` is rendered three ways — GitHub repo, MCP resources, static site
- **Separate output repo**: generated tree lives in `isabl-knowledge-tree`, pipeline lives here
