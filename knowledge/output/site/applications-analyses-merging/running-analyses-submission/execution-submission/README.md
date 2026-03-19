# Execution & Submission

Top-level runners and logic to create or fetch analyses, execute runs, and emit analytics for runs.

## Source Documents

- **Execute analyses from tuples with commit options** — Primary runner that accepts a list of (targets, references) tuples and executes the corresponding analyses with fine-grained control flags: commit, force, restart, verbose, and local. It orchestrates whether analyses are actually submitted, wiped before submission, restarted, or executed locally, and returns categorized tuples summarizing the run outcomes.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Run a list of analyses with control flags** — Function that takes a list of analysis objects and executes them honoring control flags such as commit, force, restart, and local. It implements the lower-level iteration and submission logic used by higher-level run orchestrators and returns a summary list of outcomes for each analysis.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Get or create analyses for application tuples** — get_or_create_analyses(tuples) attempts to retrieve existing analyses for a list of (targets, references, analyses) tuples and creates analyses when necessary. It returns a list of analyses for valid tuples and a list of invalid tuples paired with error messages for those that could not be created or validated.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Find existing analyses matching given tuples** — get_existing_analyses(tuples) searches for analyses that exactly match the specified targets and references and verifies that the requested analyses are present in analysis.analyses. It returns a tuple containing the list of found analyses and the list of tuples for which no matching analysis exists.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Retrieve existing individual-level analyses** — get_individual_level_analyses(tuples) retrieves analyses that operate at the individual level for the provided tuples. It focuses on finding analyses that are specific to individual samples rather than cohort- or project-level analyses.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Submit or run merge analysis depending on settings** — Explains submit_merge_analysis which either directly invokes merge logic or enqueues it depending on the SUBMIT_MERGE_ANALYSIS setting. It accepts a project or individual instance and delegates to custom submission logic when configured to do so.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Send analytics event for CLI-run analyses** — Utility that composes and emits an analytics event summarizing a CLI-driven run: command tuples, skipped and invalid items, and runtime flags (commit, force, restart) along with submitter identity. Useful for telemetry, usage tracking, and auditing of what was executed from the CLI.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
