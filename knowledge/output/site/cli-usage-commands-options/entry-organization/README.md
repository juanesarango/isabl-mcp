# Entry & Organization

CLI entrypoint and organizational helpers that show and group available applications and commands.

## Source Documents

- **CLI entry point for Isabl command suite** — Defines the main() entry point that runs the Isabl command line interface. This function initializes the CLI environment and dispatches to subcommands, enabling users to run Isabl tools from a console entrypoint.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/cli.py)
- **Group applications by genome assembly** — Provides a helper that organizes a list of applications into groups keyed by genome assembly. It is used to present or process apps in assembly-specific groups for downstream commands or UI display.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/cli.py)
- **CLI command wrapper supporting commit and quiet** — Defines command(commit, quiet, **cli_options), a Click command wrapper used throughout the CLI. It standardizes common CLI options (like commit and quiet) and propagates additional options to subcommands or command factories.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
