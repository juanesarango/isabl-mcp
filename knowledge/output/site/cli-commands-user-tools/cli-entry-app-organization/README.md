# CLI Entry & App Organization

Main CLI entrypoints and helpers that organize available applications for CLI presentation or invocation.

## Source Documents

- **CLI entry point for Isabl command suite** — Defines the main() entry point that runs the Isabl command line interface. This function initializes the CLI environment and dispatches to subcommands, enabling users to run Isabl tools from a console entrypoint.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/cli.py)
- **Group applications by genome assembly** — Provides a helper that organizes a list of applications into groups keyed by genome assembly. It is used to present or process apps in assembly-specific groups for downstream commands or UI display.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/cli.py)
