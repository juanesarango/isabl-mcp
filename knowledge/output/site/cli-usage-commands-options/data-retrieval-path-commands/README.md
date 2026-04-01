# Data Retrieval & Path Commands

Commands to locate files, directories and metadata for experiments, analyses, references and storage locations.

## Source Documents

- **Bulk metadata retrieval for multiple instances** — Provides a command to retrieve metadata fields for multiple instances (samples, individuals, analyses) from a specified endpoint. It supports options for selecting fields, applying filters, choosing output format (JSON, pretty), optionally suppressing headers, and other output customizations.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/commands.py)
- **Retrieve storage directories and match file patterns** — Describes get_paths(endpoint, pattern, filters, identifiers) which locates storage directories for a given endpoint and can match files inside those directories using a pattern. Useful for discovering where raw or processed files are stored and selecting files by name or glob.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/commands.py)
- **Locate analysis output directories matching patterns** — Documents get_outdirs(pattern, filters, identifiers) which returns analysis output directories and optionally matches files inside those directories using a pattern. This function helps locate pipeline result folders for downstream inspection or retrieval.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/commands.py)
- **Fetch raw experimental data file paths** — Explains get_data(filters, identifiers, verbose, dtypes), which returns file paths for experiments' raw data according to provided filters, identifiers, and desired data types. The verbose flag enables more detailed output for debugging or inspection.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/commands.py)
- **Get BED files for sequencing techniques** — Describes get_bed(technique, bed_type, assembly) which returns an appropriate BED file for a specified sequencing technique, BED type, and genome assembly. This is useful for providing regions (e.g., capture targets or blacklists) required by analyses.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/commands.py)
- **Retrieve reference data from assemblies or techniques** — Covers get_reference(identifier, data_id, resources, model) which retrieves reference data either from assemblies (default) or sequencing techniques depending on arguments. The function supports selecting specific resources and can target different internal models for reference lookup.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/commands.py)
- **Fetch analysis results with result key filter** — Defines get_results(filters, identifiers, result_key, verbose) to retrieve analysis results matching filters or specific identifiers and a result_key. The verbose option provides additional context or metadata about the returned results.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/commands.py)
- **Locate BAM files and storage directories by assembly** — Describes get_bams(filters, assembly, verbose, identifiers) which locates BAM files or the storage directories that contain them, filtered by assembly and other criteria. The function is intended to simplify finding alignment files for downstream processing.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/commands.py)
- **Count database instances using CLI command** — Defines get_count(endpoint, filters) which returns the number of database instances that match the provided criteria. It is a lightweight query utility used to obtain counts from a given endpoint with optional filtering.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/commands.py)
