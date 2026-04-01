# CLI Option Builders

Factories for Click options to standardize analysis filters and dependency resolution from CLI inputs.

## Source Documents

- **Configure analyses filter option with defaults** — Function to construct analysis filter options for the CLI, accepting optional application class filters and default parameters. It centralizes how analysis filters are produced so CLI commands can apply consistent default filters and override them via inputs.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/options.py)
- **Resolve dependency analyses option from results** — Builds a CLI option to resolve dependency analyses from provided dependency results, allowing specification by application primary key or app name with optional version. The function also accepts extra filters to further restrict which dependency analyses are returned.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/options.py)
