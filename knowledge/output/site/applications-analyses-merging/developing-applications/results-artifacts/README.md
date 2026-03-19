# Results & Artifacts

Helpers to assemble analysis result dictionaries, discover files by pattern and combine dependency results for use at runtime or completion.

## Source Documents

- **Produce analysis results dictionary on completion** — get_analysis_results is a completion hook that should return a JSON-serializable dictionary of results for a finished analysis. It is called when an analysis succeeds and provides a standard place to extract summary metrics, output file locations, and other metadata to be stored by Isabl.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Collect analysis results and attach logs/scripts** — Describes the method that builds a results dictionary for an analysis and appends related artifacts such as the head job script, log files, and error outputs. The function can consider whether results were just created (created=True) when assembling the returned information.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Find analysis files matching result patterns** — Explains the helper that resolves application result specifications that include a "pattern" entry by returning the first file that matches the pattern. This function is used when result definitions are expressed as filename patterns instead of explicit paths, enabling flexible discovery of outputs.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Fetch a single application result entry** — Documents the get_result helper used to return a single result from an application or analysis. It is a convenience wrapper for retrieving a specific result by key or name and will return the result metadata/path as defined by the application specification.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Retrieve multiple application results at once** — Explains the get_results function that retrieves a collection of results for an application or analysis. It complements get_result by returning all or filtered results (depending on arguments) and is used to assemble inputs or report outputs for downstream steps.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Resolve application dependency results and metadata** — Describes how the CLI gathers results from applications declared as dependencies of another application. It explains the dependency object structure (result key, name, application info, assembly, version selection like 'any', and linking behavior) and how those fields influence which dependency result is picked and whether it is linked to the analysis.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
