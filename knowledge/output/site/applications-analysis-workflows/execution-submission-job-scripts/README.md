# Execution, Submission & Job Scripts

Running analyses, creating job scripts, and mechanisms to submit or run analyses (local or scheduler-backed).

## Source Documents

- **Run analyses for targets and references tuples** — Orchestrates running analyses given a list of (targets, references) tuples and several control flags. It supports options to commit (submit), force (wipe existing analyses), restart, run locally, and pass extra run_args, and returns command, skipped, and invalid tuple lists.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Run and manage a list of analyses** — Runs a supplied list of analysis objects while respecting submission and control options like commit, force, restart, and local. The function handles actual execution/submission logic and collects results into returned lists (e.g., successful commands, skipped, invalid).
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Compute path for analysis command script** — Returns the filesystem path where an analysis command script should be written for a given analysis object. This path is used by the script-writing routine and determines where the CLI places executable job scripts.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Write analysis command to executable bash script** — Writes the provided command string to a bash script file for the given analysis and returns the path to that script. It encapsulates file creation, content writing, and likely sets executable permissions so the script can be run locally or submitted to a scheduler.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Get filesystem path for analysis log file** — Provides the path to the standard output log file associated with a specific analysis. This utility is used to locate where analysis stdout should be written or reviewed after job execution.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Get filesystem path for analysis error file** — Returns the path to the error (stderr) file for a given analysis so that job failures and error messages can be captured separately from standard output. It complements the log path utility for full job output management.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Generate job name from analysis metadata** — Describes how to construct a job name string from properties of an analysis instance for use in job scripts and tracking. The function standardizes naming so jobs can be identified and associated with their analysis.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Create CLI command to patch analysis status** — Generates a shell command string that, when executed, will patch the status field of a specified analysis key. This helper is used to update analysis records (for example marking success or failure) from scripts or post-run hooks.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Send CLI analytics for executed analyses** — Builds and sends an analytics event describing analyses run from the CLI, including successful, skipped, and invalid tuples. It also includes contextual flags (commit, force, restart) and the identity of the submitter to allow telemetry and usage tracking of CLI operations.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Send CLI analytics for executed analyses** — Builds and sends an analytics event describing analyses run from the CLI, including successful, skipped, and invalid tuples. It also includes contextual flags (commit, force, restart) and the identity of the submitter to allow telemetry and usage tracking of CLI operations.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
