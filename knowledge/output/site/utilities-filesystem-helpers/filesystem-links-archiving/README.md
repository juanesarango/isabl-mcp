# Filesystem, Links & Archiving

Directory creation honoring mode, forced link/symlink helpers, tar archiving and directory size inspection utilities.

## Source Documents

- **Make directories ignoring process umask settings** — makedirs(path, exist_ok=True, mode=511) creates directories while explicitly handling permissions to ignore the process umask. It behaves similarly to os.makedirs but ensures the requested mode is applied regardless of the calling process's umask.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/utils.py)
- **Create or replace a hard link forcefully** — Creates a link from src to dst, ensuring the destination is created or replaced as needed. The helper enforces the link operation even if the destination already exists by removing or overwriting it. It is useful for atomic replacement or ensuring expected file layout in the CLI workflow.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/utils.py)
- **Create or replace a symbolic link safely** — Creates a symlink from src to dst, replacing any pre-existing destination to ensure the requested symlink is present. This utility manages removal of the old destination and creation of the new symlink in one step, simplifying CLI commands that update references. It handles common edge cases around existing files and permission constraints.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/utils.py)
- **Create a tar archive from a source directory** — Compresses or archives a source directory into the specified output path (tarball) for transport or storage. The helper packages a directory tree into a single file, preserving necessary metadata depending on implementation, and is intended for use in export/transfer CLI operations. Behavior for compression format and overwriting is driven by the function's implementation details.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/utils.py)
- **Compute total directory size in bytes** — Returns the aggregate size in bytes for all files under a given path. The function supports an option to follow or ignore symbolic links (follow_symlinks=False by default) and recursively sums file sizes. It provides a simple way for CLI commands to report or validate storage usage.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/utils.py)
- **Identify the owner user of a file or directory** — Determines the owner (user) of a given filename or directory path, returning identification suitable for access checks or reporting. The helper is useful for validating ownership before operations like transfers, deletions, or permission changes in CLI workflows. It handles filesystem queries to map file metadata to a user identifier.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/utils.py)
- **Validate filesystem path ownership by current user** — Describes a utility function assert_same_owner(path) that verifies a filesystem path is owned by the same user. It is intended to be used in CLI utilities or scripts to enforce ownership constraints before performing operations on files or directories.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/utils.py)
