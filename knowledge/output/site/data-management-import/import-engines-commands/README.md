# Import Engines & Commands

High-level import classes and CLI entrypoints for registering experiments and reference assets.

## Source Documents

- **Local data importer for experiment raw files** — Comprehensive engine to import raw experiment data from local directories into Isabl, supporting recursive discovery, file-type inspectors, and per-file annotations. It can copy/move/symlink files, perform ownership and readability checks, match files to experiments using regex/grouping rules, and update experiment storage_url, storage_usage, and raw_data in the API; errors are raised for ambiguous or conflicting matches.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/data.py)
- **Local reference data importer for assemblies** — Class that implements an import engine to register reference resources (reference_data) for assemblies or techniques. The key method import_data copies or symlinks data from a local source into Isabl storage, updates the model (assemblies or techniques) with a data_id and description, and returns the patched instance; a CLI wrapper is exposed via as_cli_command.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/data.py)
- **Local reference genome importer command-line interface** — A focused import engine class for loading a single assembly reference genome into Isabl. It exposes an as_cli_command method so the import process can be invoked from the command line, simplifying registration of genome resources into the platform.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/data.py)
- **Technique BED file processing and import engine** — Importer class for technique-specific BED files that provides utilities to process (sort, bgzip, tabix) BED files and register them in a technique's storage directory. The import_bedfiles method accepts paths to targets and baits, assembly and species metadata, and a description, updating the technique record via the API; a CLI entrypoint is also provided.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/data.py)
- **Bulk import raw sequencing data for experiments** — import_data recursively scans directories to match and import raw files into multiple experiments, updating each experiment's storage_url, storage_usage, and raw_data. It supports options to copy or symlink files, case-insensitive matching, filtering by data type, attaching per-file annotations, and dry-run versus commit modes.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/data.py)
- **Import dataset definitions from a local YAML file** — Documents import_data_from_yaml which loads data definitions from a local YAML file and imports the files into Isabl. It supports options to symlink or copy, commit versus dry-run, attach per-file metadata (files_data), ignore ownership checks, and apply filters for selecting records to import.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/data.py)
- **Register and import BED files into technique storage** — import_bedfiles registers targets and baits BED files into a technique's storage directory and updates the technique's data metadata via the API. It accepts assembly, species, and an optional description and returns the updated technique record.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/data.py)
- **Register technique targets and baits BED files** — Explains a cmd that registers target and bait BED files into a technique's data directory. Incoming BEDs are compressed and tabixed (both gzipped and uncompressed kept), and the instance's storage_url, storage_usage, and reference_data fields are updated accordingly.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/data.py)
- **Build a Click command for the importer class** — Another reference to as_cli_command showing the mechanism to convert a data importer class into a Click-based command. It encapsulates CLI wiring so the importer can be invoked with consistent command-line semantics and options.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/data.py)
