# Results, Artifacts & Post-completion Hooks

Hooks and helpers to collect per-analysis, per-individual and per-project results, attach logs/scripts, pattern-based result discovery, and to expose results via API.

## Source Documents

- **Produce analysis results dictionary on completion** — get_analysis_results is a completion hook that should return a JSON-serializable dictionary of results for a finished analysis. It is called when an analysis succeeds and provides a standard place to extract summary metrics, output file locations, and other metadata to be stored by Isabl.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Collect results for completed individual analysis** — Explains get_individual_analysis_results, which is executed when an individual-level analysis completes to return a JSON-serializable results dictionary. The function accepts the succeeded analysis instance and must return a dict of results that can be stored or consumed downstream.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Collect project-level analysis results on completion** — get_project_analysis_results is a completion hook for project-level analyses that should return a JSON-serializable dictionary of aggregated results. It is used to summarize outcomes across multiple sample-level analyses at the project scope.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Collect analysis results and attach logs/scripts** — Describes the method that builds a results dictionary for an analysis and appends related artifacts such as the head job script, log files, and error outputs. The function can consider whether results were just created (created=True) when assembling the returned information.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Find analysis files matching result patterns** — Explains the helper that resolves application result specifications that include a "pattern" entry by returning the first file that matches the pattern. This function is used when result definitions are expressed as filename patterns instead of explicit paths, enabling flexible discovery of outputs.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Fetch a single application result entry** — Documents the get_result helper used to return a single result from an application or analysis. It is a convenience wrapper for retrieving a specific result by key or name and will return the result metadata/path as defined by the application specification.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Retrieve multiple application results at once** — Explains the get_results function that retrieves a collection of results for an application or analysis. It complements get_result by returning all or filtered results (depending on arguments) and is used to assemble inputs or report outputs for downstream steps.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
