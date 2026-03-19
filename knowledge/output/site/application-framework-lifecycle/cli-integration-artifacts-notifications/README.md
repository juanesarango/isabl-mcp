# CLI Integration, Artifacts & Notifications

Helpers to expose applications as CLI commands, generate job scripts/log paths, patch status from jobs, send analytics after runs and notify project analysts.

## Source Documents

- **Expose application as click CLI command** — This class method returns the application wrapped as a Click command-line interface entry point. It enables the application to be registered and executed as a CLI command with Click's tooling.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Retrieve CLI command name for isabl_cli app** — Lightweight helper that returns the CLI command name associated with an isabl_cli application instance. Useful for reporting, logging, and constructing script headers when creating job submission artifacts.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Get filesystem path to analysis command script** — Helper that computes where an analysis command script should live on disk based on the analysis metadata and configured workspace layout. Callers use this path to write or reference the bash script that will execute the analysis.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Compute log file path for analysis execution** — Returns the filesystem path where an analysis's stdout log should be written. This deterministic path helps orchestrate log collection, monitoring, and debugging of analysis runs.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Compute stderr path for analysis execution** — Helper that computes the file path where an analysis's stderr (error) output should be redirected. It standardizes the location of error logs so users and tools can find failure output consistently across runs.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Write analysis command to bash script file** — Creates a bash script file for an analysis by writing the provided command string to disk and returning the script path. This helper typically sets up file permissions and headers so the script can be executed directly by local or batch runners.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Construct command to patch analysis status** — Generates a command string that, when executed, will update (patch) the status field of a specific analysis identified by key. This is useful for programmatically marking analyses as started, completed, failed, or other custom statuses from scripts or job wrappers.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Construct scheduler-friendly job names** — Explains how the job name is derived from an analysis instance for use in batch schedulers or logging. The helper ensures a consistent, reproducible job name that identifies the analysis (likely incorporating fields like application, version, or analysis id) so jobs are traceable across systems.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Print run summaries and error explanations** — Documents a utility that prints a concise summary of what ran, what was skipped, and what failed by consuming run_tuples, skipped_tuples, and invalid_tuples. It formats and echoes errors and skip reasons so users can quickly understand run outcomes and failure causes.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Send analytics event for CLI-run analyses** — Utility that composes and emits an analytics event summarizing a CLI-driven run: command tuples, skipped and invalid items, and runtime flags (commit, force, restart) along with submitter identity. Useful for telemetry, usage tracking, and auditing of what was executed from the CLI.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Notify project analysts via email** — Defines notify_project_analyst(self, analysis, subject, message), a helper that sends an email notification to the analysts associated with a project. It is intended to inform project analysts about analysis events or updates from the CLI/application.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Update experiment default BAM file (admin)** — update_experiment_bam_file(experiment, bam_url, analysis_pk) sets or replaces an experiment's default BAM file for an assembly. This operation is restricted to ADMIN users and records the association with a specific analysis primary key.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Resolve experiment bedfile for targets or baits** — Describes the helper to obtain a target or bait BED file associated with an experiment, with bedfile_type defaulting to 'targets'. It selects the bedfile that matches the experiment and (implicitly) the application's assembly so callers can feed region definitions into downstream tools.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Find experiment BAM matching application assembly** — Explains the helper that fetches the BAM file for an experiment appropriate for the application's assembly. The function resolves the correct BAM to use as input to applications, handling assembly compatibility and experiment-level associations.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Retrieve BAM files for multiple experiments** — get_bams(experiments) collects the BAM file locations associated with a list of experiments. It is used to aggregate BAM inputs before downstream analyses or validation steps.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Patch application settings programmatically** — Describes a helper to update (patch) application settings from the CLI client, accepting a client_id and arbitrary settings to change. The function is intended to modify application configuration when needed, likely performing minimal updates only when values differ.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Resolve application dependency results and metadata** — Describes how the CLI gathers results from applications declared as dependencies of another application. It explains the dependency object structure (result key, name, application info, assembly, version selection like 'any', and linking behavior) and how those fields influence which dependency result is picked and whether it is linked to the analysis.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
