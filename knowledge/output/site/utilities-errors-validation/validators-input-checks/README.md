# Validators & Input Checks

Reusable validators for file/directory patterns and pair/TSV inputs used in CLI commands and submission flows.

## Source Documents

- **Validate file patterns exist and non-empty** — Validator that checks a list of filename patterns (globs) match existing files and optionally ensures matched files are non-zero size. Returns True when all patterns resolve to existing files (and non-empty when check_size=True).
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/validators.py)
- **Validate directory patterns exist** — Checks that a list of directory patterns resolves to existing directories. It returns True when all provided patterns match directories, and is intended for validating directory-type CLI inputs before further processing.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/validators.py)
- **Validate and retrieve experiment pairs** — Utility to validate 'pairs' input and retrieve the corresponding experiments. It is used to ensure pair specifications map to existing experiment records before downstream processing or analysis.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/validators.py)
- **Parse and validate sample pairs from TSV file** — A click-style validator that reads a TSV file from a given path and returns pair definitions. Designed as a CLI callback (ctx, _, path) to load and validate pair lists provided via files before running commands.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/validators.py)
- **Serializer to register and configure Django validators** — Serializer that accepts a validator class (restricted to django.core.validators via a custom validator) and a dictionary of keyword arguments to configure it. Its Meta declares a validators list that references a builder function for the validator. This enables API-driven registration or configuration of Django validators.
  [Source](https://github.com/papaemmelab/isabl_api/blob/master/isabl_api/serializers.py)
