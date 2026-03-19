# Core CLI Commands & Workflows

User-facing commands for authentication, running/merging analyses, retrieving metadata and data files.

## Source Documents

- **Isabl CLI main entry point command** — Defines the main entry point for the Isabl command-line interface. This function bootstraps and dispatches subcommands, enabling users to run Isabl CLI tools from a shell environment.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/cli.py)
- **Group installed applications by genome assembly** — Utility function that groups a list of application objects by their associated genome assembly. Useful for organizing and presenting apps that are assembly-specific when listing or configuring tools.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/cli.py)
- **CLI login: authenticate to Isabl platform** — Implements the login command to authenticate a user against the Isabl platform. It handles credential input and stores session information so subsequent CLI commands can access Isabl APIs.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/commands.py)
- **Merge project analyses for a specific application** — Provides a command to merge analysis results across all samples within a given project for a particular application. It consolidates outputs into a merged representation, useful for project-level reporting or downstream aggregation.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/commands.py)
- **Merge analyses for an individual sample** — Command to merge multiple analyses belonging to a single individual for a chosen application. This helps create consolidated results per individual, which can simplify review and downstream processing.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/commands.py)
- **Process and update finished analyses in Isabl** — Scans for analyses that have finished and performs post-run processing and updates, optionally forcing reprocessing. It updates metadata and status fields to reflect completed work and triggers any finalization steps.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/commands.py)
- **Bulk update analyses results field** — Allows bulk patching of the results field across multiple analyses, filtered by various criteria. Useful for correcting or augmenting stored results metadata when many analyses need the same update.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/commands.py)
- **Patch analysis status by key value** — Command to change the status of a specific analysis identified by a key. This can be used to correct status flags (e.g., to mark analyses as failed, running, or completed) for individual records.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/commands.py)
- **Retrieve metadata for multiple Isabl instances** — Fetches metadata fields for one or many Isabl objects (projects, individuals, analyses, etc.) with options for endpoint, field selection, filtering, and output formatting (JSON, headers, pretty). It supports combining identifiers and filters to produce customized metadata tables or JSON objects.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/commands.py)
- **Count database instances matching filters** — Describes get_count(endpoint, filters), a CLI helper that returns the number of database instances matching the provided filters for a given endpoint. It is intended for quick inventory queries and conditional logic in scripts or workflows.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/commands.py)
- **Retrieve storage directories and matching files** — Documents get_paths(endpoint, pattern, filters, identifiers), a command to list storage directories associated with database records and optionally match files inside those directories using a pattern. Useful for locating raw or derived files tied to samples, experiments, or analyses across storage backends.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/commands.py)
- **Find analysis output directories with pattern matching** — Describes get_outdirs(pattern, filters, identifiers), which locates analysis output directories and can match files within them using a pattern. This helps users inspect or retrieve results produced by analysis runs across projects and samples.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/commands.py)
- **Fetch raw experiment data file paths** — Covers get_data(filters, identifiers, verbose, dtypes), a function to retrieve file paths for raw experimental data. It supports filtering by metadata, selecting specific data types (dtypes), toggling verbose output, and targeting specific identifiers for precise data discovery.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/commands.py)
- **Retrieve BED file for sequencing technique** — Explains get_bed(technique, bed_type, assembly), a utility to obtain a BED file appropriate for a given sequencing technique, BED type (e.g., exome targets, blacklists), and genome assembly. It centralizes access to annotation intervals needed by analysis pipelines.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/commands.py)
- **Retrieve reference data from assemblies or techniques** — Documents get_reference(identifier, data_id, resources, model), which fetches reference data either by assemblies (default) or by sequencing techniques. The function allows selecting specific resource IDs and models to obtain genome FASTA, indexes, or other reference assets required by pipelines.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/commands.py)
- **Fetch analysis results using keys and filters** — Describes get_results(filters, identifiers, result_key, verbose), a command to obtain analysis result files or entries keyed by result_key and filtered by metadata or identifiers. It helps locate outputs from specific workflows or result types across experiments and projects.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/commands.py)
- **Locate BAM files and storage directories** — Explains get_bams(filters, assembly, verbose, identifiers), a helper to find BAM files and their storage directories, optionally filtered by genome assembly and other metadata. It is intended for quickly gathering alignment files for downstream analysis or inspection.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/commands.py)
- **Rerun failed signals for selected filters** — Describes rerun_signals(filters), a command to reschedule or rerun signals that previously failed, scoped by provided filters. This is useful for recovering from transient failures or reprocessing records without manually triggering each signal.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/commands.py)
- **Run signals triggered from the web frontend** — Covers run_web_signals(filters), which executes signals that were triggered via the Isabl web frontend and filtered by provided criteria. This allows CLI-based replay or execution of UI-driven events for debugging or bulk processing.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/commands.py)
- **Run arbitrary signals on analyses or experiments** — Describes a CLI helper that runs arbitrary signals on analyses or experiments using import strings. The function accepts an endpoint, a filter set to target resources, and one or more signal identifiers to execute.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/commands.py)
- **Reject an analysis with a provided reason** — Explains a CLI function that patches an analysis' status to REJECTED and records a rejection reason. The function takes an analysis key and a textual reason and updates the analysis via the API.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/commands.py)
- **Callback: print application result keys** — A CLI callback function that prints or validates result keys for applications. It is intended to be used with click (or similar) to display available result fields for a chosen application.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/commands.py)
