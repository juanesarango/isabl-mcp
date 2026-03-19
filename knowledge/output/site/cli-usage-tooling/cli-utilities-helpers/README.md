# CLI Utilities & Helpers

Common utilities used across CLI commands: filesystem helpers, messaging, analytics decorators and result helpers.

## Source Documents

- **Make directories while ignoring umask settings** — makedirs(path, exist_ok=True, mode=511) is a utility wrapper to create directories while ignoring the process umask so the requested mode is honored. It supports an exist_ok flag and accepts a numeric mode (default 511, i.e. 0o777) to control created permissions.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/utils.py)
- **Retrieve matched analysis results from experiments** — get_results(...) searches an experiment object for results matching a result_key and optional application, target, reference, or analysis constraints. It supports filtering by application pk, name, version, and assembly, allows status filtering, and returns a list of (result_value, analysis_pk) tuples; use result_key='storage_url' to get output directories.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/utils.py)
- **Get a single validated analysis result tuple** — get_result(...) is a convenience wrapper around get_results that returns a single (result_value, analysis_pk) tuple and provides clearer error messages including application_name and application_assembly. It reuses the same filtering/signature as get_results but enforces a single-match expectation and better user-facing errors.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/utils.py)
- **Traverse nested dictionary by list of keys** — traverse_dict(dictionary, keys, serialize=False) walks through a nested dictionary following the provided list of keys to return the nested value. If serialize is True it forces the return to a string, converting nested dict values to JSON, otherwise it returns the raw Python object.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/utils.py)
- **Apply a list of decorators to callable** — apply_decorators(decorators) is a small utility that composes and applies a list of decorators to a target callable. It automates wrapping a function with multiple decorators in the correct order and references a common StackOverflow pattern for implementation.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/utils.py)
- **Generate rsync command string for directory transfer** — Describes a helper that builds an rsync command string to move or synchronize a source directory to a destination path. The function accepts src, dst and an optional chmod argument (default 'a-w') and returns the constructed command string for execution by the CLI.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/utils.py)
- **Detect outdated rsync lacking append-verify option** — Explains a utility that parses rsync version output to determine if the installed rsync supports the --append-verify option. This check is used to detect older rsync installations that may not safely support certain resume/append behaviors.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/utils.py)
- **Compute total directory size in bytes** — Documents a utility that recursively computes the total size of a directory tree and returns the result in bytes. It accepts a path and an optional follow_symlinks flag (default False) to control whether symlinked files are included in the calculation.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/utils.py)
- **Create or replace hard link between paths** — Describes a helper that forcefully creates a hard link from src to dst. The utility ensures the link is created even if a destination exists (typically by removing or replacing it) and surfaces relevant filesystem errors.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/utils.py)
- **Create or replace symbolic link between paths** — Documents a utility that forcefully creates a symbolic link pointing from dst to src, replacing any existing destination. This helper simplifies safe symlink creation in scripts by handling pre-existing files or links and raising on fatal errors.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/utils.py)
- **Compress directory into tar archive at output path** — Provides a utility to create a tar archive of a source directory at a specified output path. The function encapsulates archiving logic used by the CLI to bundle directories for storage or transfer.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/utils.py)
- **Enforce admin user permissions for CLI actions** — Describes a permission-check helper that raises a PermissionError if the current user is not the configured system admin (system_settings.ADMIN_USER). An optional message parameter can customize the raised error message for clearer diagnostics in CLI commands.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/utils.py)
- **Print advisory about --commit flag usage** — Documents a small helper that echoes a message advising about the use of the --commit flag in CLI commands. It is intended to standardize and centralize the informational text shown to users when committing changes via the CLI.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/utils.py)
- **Print colored blinking title text to console** — Explains a utility to print a title string to the console with optional color and blinking effect. The function accepts a title, a color (default 'cyan'), and a blink boolean to style CLI output consistently across commands.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/utils.py)
- **Determine filesystem owner of a directory** — Describes a helper that returns the owner of a file or directory. The function inspects filesystem metadata to resolve the owning user (typically by uid -> username lookup) and is useful for permission checks or reporting in the CLI.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/utils.py)
- **Ensure filesystem path owned by current user** — Small utility that validates a filesystem path is owned by the same user (owner) as the process. Use it to guard operations that require files or directories to be owned by the invoking user to avoid permission or security issues.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/utils.py)
- **Print caller location for debugging traces** — Utility to print where the current function was called from, with configurable stack depth and verbosity. It is useful for debugging or logging to trace call sites during CLI execution or while troubleshooting code paths.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/utils.py)
- **Send analytics for CLI commands (decorator)** — Helper that can be used either as a method or as a decorator on click group commands to send analytics events. It integrates telemetry into CLI commands so usage and events can be tracked after command execution.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/utils.py)
- **Find first file matching pattern recursively** — Searches a directory recursively and returns the first file matching a glob pattern, with options to exclude substrings, sort by newest first, and allow no-match as optional. Raises errors for invalid directories or when no match is found unless optional=True.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/utils.py)
- **CLI command wrapper to send tracking events** — A wrapper function for CLI command contexts that sends a tracking/analytics event after the command finishes. It is intended to be used with click command invocations so telemetry is emitted post-execution.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/utils.py)
- **Lazy projects() factory method for project lists** — A lazy accessor method that returns a list of projects when called. It is designed to defer loading until needed, reducing upfront computation or IO, and likely used by CLI commands or higher-level APIs to enumerate projects.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/factories.py)
