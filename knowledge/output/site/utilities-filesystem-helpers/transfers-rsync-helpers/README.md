# Transfers & rsync Helpers

Helpers to build rsync command lines and to check installed rsync compatibility for append/verify features.

## Source Documents

- **Build rsync command string for moving directories** — Defines a helper that constructs an rsync command string to copy/move a source directory to a destination path. It accepts a chmod option (default 'a-w') to set permissions on the destination after transfer. The function returns the assembled command string for execution by the CLI or subprocess wrapper.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/utils.py)
- **Detect outdated rsync lacking --append-verify support** — Parses rsync version stdout to determine whether the installed rsync supports the --append-verify option. The utility flags older rsync installations that do not include that feature so callers can adjust transfer strategies or warn the user. It is intended to be used before building rsync commands reliant on that flag.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/utils.py)
