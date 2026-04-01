# File Operations, Linking & Delivery

Filesystem operations used during import and delivery: symlinks, copying, moving, symlinking experiments into project directories and exposing analysis outputs to targets.

## Source Documents

- **Create symbolic link helper function** — A helper function that creates a symbolic link from a given source path to a destination path. This is used by importers when the symlink option is selected instead of moving or copying data.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/data.py)
- **Move (rename) file or directory helper function** — A utility function that renames (moves) a file or directory from src to dst. It is used by import routines when files are intended to be relocated into Isabl storage rather than copied or linked.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/data.py)
- **Copy files helper function for imports** — A small utility to copy files from a source location to a destination. It supports import workflows where the original data must be preserved and a duplicate placed into Isabl storage.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/data.py)
- **Create symlinks from experiments into projects** — Creates filesystem symbolic links from an experiment directory into one or more project directories. This utility helps expose experiment data inside project-level directory structures for downstream access and workflows.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/data.py)
- **Create symlinks from analyses to configured targets** — Creates symbolic links for an analysis into configured target directories (for example project or delivery locations). This function automates exposing analysis outputs where other systems or users expect them.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/data.py)
- **Echo source-to-destination informational message** — A small utility function that prints an informational message describing a source path and its destination (src -> dst). It is used to log or display file move/link/copy operations to the user.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/data.py)
