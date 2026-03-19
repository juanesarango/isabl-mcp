# CLI Helpers & Misc Utilities

General helpers for CLI UX, traversal, decorator composition, analytics wrappers, searching files, and small debugging utilities.

## Source Documents

- **Traverse nested dictionary using list of keys** — traverse_dict(dictionary, keys, serialize=False) walks a nested dictionary following an ordered list of keys to retrieve a nested value. If serialize is True, the function forces the result to a string and JSON-serializes any dict values; otherwise it returns the raw object.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/utils.py)
- **Apply multiple decorators to a callable** — apply_decorators(decorators) returns a utility that composes and applies a list of decorator callables to a target callable. It simplifies programmatic application of several decorators in a specified order; the implementation references a StackOverflow pattern for decorator composition.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/utils.py)
- **Print guidance message for --commit flag usage** — Displays an informational message about the --commit flag to the user, typically when a CLI action can be performed in dry-run vs commit modes. This helper centralizes the wording so commands can consistently inform users about making destructive or permanent changes. It is a small UX utility for CLI interactions.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/utils.py)
- **Print colored, optionally blinking CLI titles** — Prints a formatted title line to the console with configurable color and optional blink attribute for emphasis. It standardizes header output across CLI commands to improve readability and UX. Supported colors and behavior are provided by the implementation and intended for interactive terminal output.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/utils.py)
- **Print caller location for debugging and tracing** — Documents called_from(depth=1, verbose=True), a helper that prints where the current function was called from. The function accepts a stack depth and verbosity flag to customize the amount of caller information printed for debugging or logging purposes.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/utils.py)
- **Send analytics for click commands or decorators** — Explains send_analytics(command), a utility that can be used either as a method or as a decorator for Click group commands to emit analytics events. It integrates telemetry into CLI commands so usage and execution can be tracked centrally.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/utils.py)
- **Find first file matching pattern recursively** — Documents first_matching_file(directory, pattern, exclude=None, sort_by_newest=True, optional=False), which recursively searches a directory for the first file matching a glob pattern. It supports excluding files by substring, sorting results by creation time, and an optional mode that allows no-match to be acceptable, and raises errors when directory is invalid or no match is found (unless optional).
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/utils.py)
- **Command wrapper that sends analytics after execution** — Describes wrapper(ctx, *args, **kwargs), a helper wrapper that sends a tracking event after a command has executed. It is intended to be used around Click command invocations so that telemetry is captured post-execution.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/utils.py)
- **Find matching analysis results for an experiment** — get_results searches an experiment object for results that match multiple filter criteria: result key, application key/name/version/assembly, target/reference dependencies, analyses, and expected status. It returns a list of tuples (result_value, analysis_pk) and supports complex matching rules including matching by app pk, name, or name+version; pass result_key='storage_url' to get output directories.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/utils.py)
- **Get single matching result with error handling** — get_result is a convenience wrapper around get_results that returns a single matching result (value and producing analysis PK) and raises a clearer error when no or ambiguous matches are found. It accepts the same filters as get_results and allows passing application_name and application_assembly to produce more informative error messages.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/utils.py)
