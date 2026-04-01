# Validation During Import

Checks performed by importers such as file-type detection, ownership/readability assertions and raw-data inspection for matching and QC.

## Source Documents

- **Detect supported raw data file types on a path** — Implements a helper that inspects a filesystem path to determine whether it represents a supported raw data file. This is used to validate input file paths before ingest or processing steps.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/data.py)
- **Ensure matched files are owned by current user** — Validation helper that verifies the matched files are owned by the current user. It is used to prevent administrators from importing files they do not own unless ownership checks are explicitly ignored.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/data.py)
- **Verify matched files are readable and accessible** — Validation function that ensures all matched files can be accessed and read by the process. It helps catch permission or path issues early in the import workflow to avoid partial imports or runtime failures.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/data.py)
- **Match path to detect FASTQ and BAM files** — Matches a filesystem path against a pattern and updates an internal cache when a FASTQ or BAM file is detected. This function performs pattern matching and classification used by the importer to assign files to experiments and determine read pairs.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/data.py)
- **Customize file-level metadata annotation method** — Hook method intended to be overridden to add or modify file-level annotations during import. Implementations can inject sample metadata such as PL (platform), LB (library), or other custom tags into file_data entries.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/data.py)
