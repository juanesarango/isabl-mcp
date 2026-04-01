# Analysis Management Commands

CLI commands to process, patch, merge and manage analysis lifecycle and statuses.

## Source Documents

- **Process and update completed analyses** — Finds analyses marked as finished and performs post-processing updates such as updating metadata or triggering downstream bookkeeping. The command accepts filters and a force flag to control which finished analyses are processed or reprocessed.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/commands.py)
- **Bulk update results field of analyses** — Provides a bulk patch command to update the results field for many analyses at once, based on provided filters. This is useful for correcting, augmenting, or standardizing result metadata across multiple analyses.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/commands.py)
- **Update status field for a specific analysis** — Implements a command to patch the status of a given analysis identified by a key. This allows operators to correct or advance an analysis' lifecycle state from the CLI.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/commands.py)
- **Merge application analyses across a project** — Implements a command to merge analyses at the project level, combining results produced by one or more applications across all individuals/samples in a project. This is useful to produce consolidated outputs or aggregated datasets for project-wide reporting.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/commands.py)
- **Merge analyses for a single individual** — Provides a command to merge multiple application analyses belonging to a specific individual. This consolidates per-individual results so downstream tools or reports can consume a single merged representation per person/sample.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/commands.py)
- **Mark an analysis as rejected with reason** — Provides a simple CLI helper to patch an analysis' status to REJECTED while recording a rejection reason. It accepts the analysis key and a reason string and updates the analysis status accordingly.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/commands.py)
