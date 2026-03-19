# Import Engines & CLI wrappers

Importer classes and the CLI wrappers that drive bulk and local import operations for experiments, BEDs and reference data.

## Source Documents

- **Local reference data importer for assemblies and techniques** — An import engine class used to register reference resources (e.g., reference data files) for an assembly or technique. The class exposes import_data to move or symlink local reference data into Isabl storage and as_cli_command to expose the importer via a Click-based CLI.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/data.py)
- **Local reference genome importer CLI interface** — A minimal import engine specialized for importing a reference genome for an assembly. The class provides an as_cli_command method so the genome importer can be invoked from the command line via Click.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/data.py)
- **Local BED importer for techniques with processing** — An importer class for technique BED files that can preprocess BED files (sort, bgzip, tabix) and register them in a technique's storage directory. It offers process_bedfile to prepare the file and import_bedfiles to register targets/baits, assembly and species metadata, and update the technique instance via the API, plus a CLI wrapper.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/data.py)
- **Local data importer for experiment raw files** — A comprehensive data import engine for associating raw data files with experiments. It supports directory traversal, pattern matching, multiple data types (BAM, FASTQ, images, etc.), ownership and readability checks, options to copy/symlink/move, per-file annotations, and returns a summary plus updated experiment entries after committing.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/data.py)
- **Bulk raw data importer for multiple experiments** — Imports raw files for many experiments by scanning directories, matching files to experiments, and optionally moving, copying, or symlinking them into storage. It updates experiments' storage metadata (storage_url, storage_usage, raw_data), supports filtering by data types, and has a commit flag to perform or dry-run the operation.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/data.py)
- **Import data into Isabl from a YAML file** — Imports data definitions from a local YAML file into Isabl, offering options to symlink or copy files, and to commit changes to the database. Accepts per-file metadata (files_data), ownership override, and filtering parameters to narrow which entries are processed. Designed to streamline bulk imports described in YAML manifests.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/data.py)
- **Create Click CLI wrapper for data importers** — Provides a helper to produce a Click command for a data importer class so it can be executed from the command line. Standardizes the CLI interface for different importers and reduces repetitive boilerplate. Ensures consistent option parsing and invocation patterns across import utilities.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/data.py)
- **Register BED files to technique storage** — Registers targets and baits BED files into a technique's storage directory and updates the technique's data record via the API. It accepts assembly, species and optional description metadata and returns the updated technique object.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/data.py)
