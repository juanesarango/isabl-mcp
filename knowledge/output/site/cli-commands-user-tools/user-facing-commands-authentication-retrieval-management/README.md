# User-facing Commands (authentication, retrieval, management)

Commands exposed to end users for login, retrieving metadata/results/paths/data, running and merging analyses, running signals, and patching statuses or results.

## Source Documents

- **CLI login command for Isabl credentials** — Provides the CLI login command that authenticates a user against an Isabl server. The command handles credential collection and storage (e.g., token/session), enabling subsequent authenticated API calls from the CLI.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/commands.py)
- **Bulk metadata retrieval for multiple instances** — Provides a command to retrieve metadata fields for multiple instances (samples, individuals, analyses) from a specified endpoint. It supports options for selecting fields, applying filters, choosing output format (JSON, pretty), optionally suppressing headers, and other output customizations.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/commands.py)
- **Count database instances using CLI command** — Defines get_count(endpoint, filters) which returns the number of database instances that match the provided criteria. It is a lightweight query utility used to obtain counts from a given endpoint with optional filtering.
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
- **Merge application analyses across a project** — Implements a command to merge analyses at the project level, combining results produced by one or more applications across all individuals/samples in a project. This is useful to produce consolidated outputs or aggregated datasets for project-wide reporting.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/commands.py)
- **Merge analyses for a single individual** — Provides a command to merge multiple application analyses belonging to a specific individual. This consolidates per-individual results so downstream tools or reports can consume a single merged representation per person/sample.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/commands.py)
- **Process and update completed analyses** — Finds analyses marked as finished and performs post-processing updates such as updating metadata or triggering downstream bookkeeping. The command accepts filters and a force flag to control which finished analyses are processed or reprocessed.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/commands.py)
- **Bulk update results field of analyses** — Provides a bulk patch command to update the results field for many analyses at once, based on provided filters. This is useful for correcting, augmenting, or standardizing result metadata across multiple analyses.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/commands.py)
- **Update status field for a specific analysis** — Implements a command to patch the status of a given analysis identified by a key. This allows operators to correct or advance an analysis' lifecycle state from the CLI.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/commands.py)
- **Rerun failed asynchronous signals (jobs) selectively** — Documents rerun_signals(filters) which triggers reruns of previously failed signals based on provided filters. This is useful for recovering from transient failures in asynchronous tasks managed by the Isabl signaling system.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/commands.py)
- **Execute signals triggered from the web frontend** — Explains run_web_signals(filters) which runs signals that were initiated via the Isabl frontend, optionally constrained by filters. This bridges frontend-triggered events to backend signal execution for tasks such as reprocessing or manual starts.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/commands.py)
- **Run arbitrary signals on analyses or experiments** — Defines a CLI function to execute arbitrary signals against analyses or experiments by using import strings. The function accepts an endpoint, filter criteria, and a list of signals to run, allowing targeted programmatic triggers inside Isabl.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/commands.py)
- **Mark an analysis as rejected with reason** — Provides a simple CLI helper to patch an analysis' status to REJECTED while recording a rejection reason. It accepts the analysis key and a reason string and updates the analysis status accordingly.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/commands.py)
- **Callback to display application result keys** — Implements a callback that prints available result keys for applications, typically used as a CLI option validator or helper. It assists users in discovering which result fields are available when constructing queries or formatting output.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/commands.py)
