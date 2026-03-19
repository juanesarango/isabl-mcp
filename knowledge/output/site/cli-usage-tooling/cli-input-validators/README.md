# CLI Input Validators

Validators used as CLI callbacks for files, directories and pair lists.

## Source Documents

- **Validate file patterns exist and non-empty** — Validator that checks a list of filename patterns (globs) match existing files and optionally ensures matched files are non-zero size. Returns True when all patterns resolve to existing files (and non-empty when check_size=True).
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/validators.py)
- **Validate directory patterns exist** — Checks that a list of directory patterns resolves to existing directories. It returns True when all provided patterns match directories, and is intended for validating directory-type CLI inputs before further processing.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/validators.py)
- **Validate and retrieve experiment pairs** — Utility to validate 'pairs' input and retrieve the corresponding experiments. It is used to ensure pair specifications map to existing experiment records before downstream processing or analysis.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/validators.py)
- **Parse and validate sample pairs from TSV file** — A click-style validator that reads a TSV file from a given path and returns pair definitions. Designed as a CLI callback (ctx, _, path) to load and validate pair lists provided via files before running commands.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/validators.py)
- **Callback: print application result keys** — A CLI callback function that prints or validates result keys for applications. It is intended to be used with click (or similar) to display available result fields for a chosen application.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/commands.py)
