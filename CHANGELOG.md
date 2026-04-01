# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## About

Isabl MCP Server provides 11 MCP tools and 8 prompts for the Isabl genomics platform. Claude Code skills (slash commands) are bundled via the plugin install.

## [0.2.0] - 2026-04-01

### Added

- 3 knowledge base tools: `search_knowledge`, `get_knowledge_tree`, `get_knowledge_doc`
- Knowledge data (347 documents) bundled inside the pip package
- 8 MCP prompts for guided workflows (debug, query, write-app, etc.)
- Claude Code plugin manifest (`.claude-plugin/`, `.mcp.json`)
- PyPI publish workflow (GitHub Actions, triggered on release)
- Auto-discovery of API URL and token from `~/.isabl/settings.json`
- Transparent pagination via `query_all()` with `max_results` cap
- Output formatting: `output_fields` projection, `output_format` (json/table/csv)
- Cursor one-click install badge (deeplink)

### Changed

- Server now exposes 11 tools + 8 prompts (up from 8 tools)
- README rewritten with MCP-server-first framing
- Project URLs updated to `juanesarango/isabl-skills`

## [0.1.0] - 2026-02-02

### Added

- Initial release of Isabl Skills and MCP server
- 8 Claude Code skills for guided Isabl workflows:
  - `/isabl-query-data` - Query data from Isabl API
  - `/isabl-write-app` - Create new Isabl applications
  - `/isabl-monitor-analyses` - Track analysis status
  - `/isabl-debug-analysis` - Debug failed analyses
  - `/isabl-merge-results` - Aggregate results across analyses
  - `/isabl-submit-data` - Submit new sequencing data
  - `/isabl-project-report` - Generate project status reports
  - `/isabl-run-pipeline` - Run multiple apps as a pipeline
- MCP server with 8 tools for programmatic Isabl API access
- Consolidated install script for easy setup
- CI/CD pipeline configuration

### Changed

- Merged `search_apps` and `explain_app` tools into a single `get_apps` tool
- Removed application path configuration in favor of API-based app discovery
- Restructured repository to separate user-facing skills from development documentation

### Fixed

- Resolved CI/CD implementation issues
- Fixed skill code bugs for reliable operation
- Corrected MCP server implementation for proper tool registration and execution
