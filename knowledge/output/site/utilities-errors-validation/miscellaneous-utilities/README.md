# Miscellaneous Utilities

Small helpers and decorators found across the codebase (e.g., traversal, rsync command builder, analytics wrappers).

## Source Documents

- **Array chunking helper yields fixed-size groups** — chunks splits an input array into successive n-sized pieces and yields each piece in turn. It's a small utility useful for batching operations (for example batching IDs into requests) while avoiding copying the entire sequence.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/api.py)
- **Apply a list of decorators to callable** — apply_decorators(decorators) is a small utility that composes and applies a list of decorators to a target callable. It automates wrapping a function with multiple decorators in the correct order and references a common StackOverflow pattern for implementation.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/utils.py)
- **Generate rsync command string for directory transfer** — Describes a helper that builds an rsync command string to move or synchronize a source directory to a destination path. The function accepts src, dst and an optional chmod argument (default 'a-w') and returns the constructed command string for execution by the CLI.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/utils.py)
- **Detect outdated rsync lacking append-verify option** — Explains a utility that parses rsync version output to determine if the installed rsync supports the --append-verify option. This check is used to detect older rsync installations that may not safely support certain resume/append behaviors.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/utils.py)
- **Find first file matching pattern recursively** — Searches a directory recursively and returns the first file matching a glob pattern, with options to exclude substrings, sort by newest first, and allow no-match as optional. Raises errors for invalid directories or when no match is found unless optional=True.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/utils.py)
- **Traverse nested dictionary by list of keys** — traverse_dict(dictionary, keys, serialize=False) walks through a nested dictionary following the provided list of keys to return the nested value. If serialize is True it forces the return to a string, converting nested dict values to JSON, otherwise it returns the raw Python object.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/utils.py)
- **Print caller location for debugging traces** — Utility to print where the current function was called from, with configurable stack depth and verbosity. It is useful for debugging or logging to trace call sites during CLI execution or while troubleshooting code paths.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/utils.py)
- **Send analytics for CLI commands (decorator)** — Helper that can be used either as a method or as a decorator on click group commands to send analytics events. It integrates telemetry into CLI commands so usage and events can be tracked after command execution.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/utils.py)
