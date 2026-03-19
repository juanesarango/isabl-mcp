# BED & Reference File Processing

Prepare and register BED and other reference resources (sorting, bgzip, tabix) and commands to register technique-specific resources.

## Source Documents

- **Sort, compress and index BED files** — Utility function that sorts a BED file, compresses it with bgzip, and creates a tabix index. It prepares BED files for efficient querying and downstream usage in genomic workflows.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/data.py)
- **Register BED files to technique storage** — Registers targets and baits BED files into a technique's storage directory and updates the technique's data record via the API. It accepts assembly, species and optional description metadata and returns the updated technique object.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/data.py)
- **Register BED targets and baits for a technique** — Registers targets and baits BED files for a given technique and assembly, compressing and tabix-indexing incoming BEDs. Both gzipped and uncompressed versions are preserved, and instance fields such as storage_url, storage_usage, and reference_data are updated accordingly. This automates preparing capture kit resources for downstream analyses.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/data.py)
