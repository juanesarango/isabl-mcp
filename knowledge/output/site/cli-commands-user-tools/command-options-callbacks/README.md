# Command Options & Callbacks

Helpers to create reusable Click options, callbacks and validators used by CLI commands (analysis filters, dependency selection, result-key helpers).

## Source Documents

- **Configure analyses filter option with defaults** — Function to construct analysis filter options for the CLI, accepting optional application class filters and default parameters. It centralizes how analysis filters are produced so CLI commands can apply consistent default filters and override them via inputs.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/options.py)
- **Resolve dependency analyses option from results** — Builds a CLI option to resolve dependency analyses from provided dependency results, allowing specification by application primary key or app name with optional version. The function also accepts extra filters to further restrict which dependency analyses are returned.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/options.py)
- **Callback to display application result keys** — Implements a callback that prints available result keys for applications, typically used as a CLI option validator or helper. It assists users in discovering which result fields are available when constructing queries or formatting output.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/commands.py)
