# Validators & CLI Callbacks

Small validation utilities used for CLI argument validation: directory/file pattern checks and parsing sample pair TSVs.

## Source Documents

- **Validate that file patterns match existing non-empty files** — Covers validate_patterns_are_files(patterns, check_size=True), a validator that ensures each pattern in a list resolves to existing files. Optionally, it checks that matched files are non-zero size, and returns True when all patterns successfully match files.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/validators.py)
- **Check that directory patterns resolve to directories** — Describes validate_patterns_are_dirs(patterns), which validates that each provided pattern corresponds to an existing directory. It accepts a list of directory patterns and returns True if all patterns resolve to directories, useful for validating CLI arguments or config inputs.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/validators.py)
- **Resolve and validate experimental sample pairs** — Briefly documents validate_pairs(pairs), a function intended to retrieve or validate experiment objects for provided sample pairs. It is used to ensure pair inputs map to valid experiments in downstream processing or CLI commands.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/validators.py)
- **Parse and validate sample pairs from TSV file** — Describes validate_pairs_from_file(ctx, _, path), a validator/Click callback that reads a TSV file and returns pairs parsed from it. It is intended for CLI commands that accept a file of sample pairs, performing parsing and validation before command execution.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/validators.py)
