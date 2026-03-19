# Results, Aggregation & Merging

Collecting analysis outputs, producing result dictionaries, and merging analyses at individual and project levels.

## Source Documents

- **Produce analysis completion results dictionary** — Describes get_analysis_results which is called when an analysis succeeds to produce a JSON-serializable dictionary of results. Implementations should return structured result data that can be stored or displayed after job completion.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Aggregate and return project-level analysis results** — Describes get_project_analysis_results, a function run on completion of a project-level analysis that should return a JSON-serializable dictionary of aggregated results. This is analogous to per-analysis results but scoped to project-level outputs.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Extract results for an individual analysis** — Runs on completion of an individual-level analysis to produce a json-serializable results dictionary. It accepts a succeeded analysis instance and returns a dictionary suitable for storing or downstream use.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Resolve analysis outputs using file patterns** — Explains a helper that finds analysis output files by applying a pattern specified in a result specification. The function returns the first matching file found when a "pattern" key is present in the specification.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Collect analysis results and append job artifacts** — Describes how the CLI collects an analysis's result dictionary and augments it with auxiliary artifacts like the head job script, logs, and error files. The function supports an optional created flag to control inclusion or handling of newly created analyses.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Fetch application dependency results for inputs** — Describes how the CLI function gathers results produced by dependent applications for use as inputs to another application run. It documents the expected structure of dependency entries (result key, name, app, app_version, assembly, linked) and how app_version and linked flags affect selection and linking behavior.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Retrieve single application result by key** — Documents a convenience function to fetch a single application result, likely by delegating to the broader results-fetching logic. It describes the purpose and expected usage for obtaining one result entry for an application run.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Fetch multiple application results for analysis** — Covers the function that retrieves a set of results for an application run, returning structured result entries for downstream consumption. It explains the expected output format and how results are aggregated for an application instance.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Individual-level analysis merge handler method** — Defines the merge hook for combining multiple analyses at the individual level. If implemented, a new individual-level analysis will be created from succeeded instances and this function runs only when no other analyses of the same application are running or submitted.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Project-level analysis merge handler method** — Defines the hook to merge multiple analyses at the project level. If implemented, this will create a new project-level analysis from a set of succeeded analyses and is only invoked when no other analysis of the same application is currently running or submitted.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Dispatch or submit merge analysis work** — Controls how merge work is triggered: it will directly call the merge logic unless the SUBMIT_MERGE_ANALYSIS setting is enabled, in which case merge work should be submitted via custom logic. The method accepts either a project or individual instance and delegates accordingly.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Execute project-level merge workflow** — Triggers the merge process for analyses at the project level. The function takes a project instance and runs the logic that combines or consolidates project-level analyses.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Execute individual-level merge workflow** — Starts the merge process for analyses at the individual level. It accepts an individual instance and runs the consolidation or merging logic for that individual's analyses.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Get or create project-level auto-merge analysis** — Fetches an existing project-level analysis configured for automatic merging or creates one if it does not exist. The function accepts a project instance and returns an analysis instance that represents the auto-merge target.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Get or create individual-level auto-merge analysis** — Retrieves an existing individual-level auto-merge analysis or creates one if missing. The function takes an individual instance and returns the analysis instance used as the auto-merge target for that individual.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Individual-level analysis merge handler method** — Defines the merge hook for combining multiple analyses at the individual level. If implemented, a new individual-level analysis will be created from succeeded instances and this function runs only when no other analyses of the same application are running or submitted.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Project-level analysis merge handler method** — Defines the hook to merge multiple analyses at the project level. If implemented, this will create a new project-level analysis from a set of succeeded analyses and is only invoked when no other analysis of the same application is currently running or submitted.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
