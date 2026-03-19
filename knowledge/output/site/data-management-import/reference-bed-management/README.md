# Reference & BED Management

Importing and registering reference genomes and technique BED assets, including compression and indexing for fast queries.

## Source Documents

- **Local reference genome importer command-line interface** — A focused import engine class for loading a single assembly reference genome into Isabl. It exposes an as_cli_command method so the import process can be invoked from the command line, simplifying registration of genome resources into the platform.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/data.py)
- **Local reference data importer for assemblies** — Class that implements an import engine to register reference resources (reference_data) for assemblies or techniques. The key method import_data copies or symlinks data from a local source into Isabl storage, updates the model (assemblies or techniques) with a data_id and description, and returns the patched instance; a CLI wrapper is exposed via as_cli_command.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/data.py)
- **Technique BED file processing and import engine** — Importer class for technique-specific BED files that provides utilities to process (sort, bgzip, tabix) BED files and register them in a technique's storage directory. The import_bedfiles method accepts paths to targets and baits, assembly and species metadata, and a description, updating the technique record via the API; a CLI entrypoint is also provided.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/data.py)
- **Register and import BED files into technique storage** — import_bedfiles registers targets and baits BED files into a technique's storage directory and updates the technique's data metadata via the API. It accepts assembly, species, and an optional description and returns the updated technique record.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/data.py)
- **Sort, compress, and index BED files** — process_bedfile(path) prepares a BED file for use by sorting it, compressing with bgzip, and creating a tabix index. This ensures the BED is in an efficient, queryable format suitable for downstream tools and storage.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/data.py)
- **Register technique targets and baits BED files** — Explains a cmd that registers target and bait BED files into a technique's data directory. Incoming BEDs are compressed and tabixed (both gzipped and uncompressed kept), and the instance's storage_url, storage_usage, and reference_data fields are updated accordingly.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/data.py)
