# File handling & Preprocessing

File-level utilities: matching, ownership checks, movement/copying/symlinking, and BED preprocessing/indexing.

## Source Documents

- **Inspect path for supported raw data files** — Provides a utility that determines whether a given filesystem path points to a supported raw data file. It is used to validate input data before ingestion or processing.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/data.py)
- **Match filesystem paths to sample identifiers and types** — match_path compares a file system path against a matching pattern and updates an internal cache when the file appears to be a FASTQ or BAM. This routine is used to detect file types, pair reads, and associate files with experiment identifiers during import.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/data.py)
- **Verify matched file ownership before importing** — check_ownership validates that the files identified for import are owned by the current user. This pre-import check prevents importing files with incorrect ownership and enforces operational security or policy constraints.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/data.py)
- **Confirm matched files are readable and accessible** — check_are_readable ensures that every file selected for import can be accessed and read by the process. It performs I/O permission checks to catch unreadable files before attempting to move, copy, or link them into Isabl storage.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/data.py)
- **Import files into instance storage and database** — Describes the import_files routine that moves, copies, or symlinks files into an experiment instance's storage_url and updates the database record. Covers arguments for instance metadata, file lists, file annotations, and behavior when copying versus moving, and notes an error condition when multiple data formats are detected.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/data.py)
- **Customize file metadata annotations during import** — annotate_file_data is an overrideable method intended to add or modify annotations on file metadata prior to import. Implementations can inject library (LB), platform (PL), or other sample/file-level attributes to be stored with raw data.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/data.py)
- **Create filesystem symbolic link utility** — Utility function that creates a symbolic link from a source path to a destination path on the filesystem. It is used by importers when the symlink option is requested instead of copying or moving data.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/data.py)
- **Move or rename files utility function** — Simple utility to rename or move a file or directory from a source path to a destination path. This function is typically used by import routines when moving data into an instance's storage_url.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/data.py)
- **Copy files between paths utility function** — Utility function that copies files or directories from a source to a destination. Used by importers when the copy option is selected instead of moving or symlinking data into Isabl-managed storage.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/data.py)
- **Sort, compress, and index BED files** — process_bedfile(path) prepares a BED file for use by sorting it, compressing with bgzip, and creating a tabix index. This ensures the BED is in an efficient, queryable format suitable for downstream tools and storage.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/data.py)
- **Print source-to-destination message helper** — Small utility that prints a standardized message describing a source and destination pair (e.g., when moving or copying files). It takes a message template, source path, and destination path and echoes the operation to the user/console.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/data.py)
- **Symlink experiment directory into projects** — Documents a helper that creates filesystem symlinks from an experiment directory into project directories. This utility is intended to expose experiment data within relevant project contexts without copying files.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/data.py)
- **Symlink analysis outputs to target directories** — Describes a utility that creates symbolic links for an analysis, linking its outputs into configured target locations (such as project directories or shared targets). This helps make analysis outputs discoverable without duplicating data.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/data.py)
