# Merging & Aggregation

Hooks and commands to merge multiple analyses into aggregated project- or individual-level analyses and to trigger merge jobs.

## Source Documents

- **Merge project-level analyses into a single run** — Describes the merge_project_analyses hook that combines multiple succeeded analyses into a new project-level analysis. It explains that this method is only invoked when no other analysis of the same application is running or submitted, and provides argument expectations for implementing custom merge logic.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Merge individual-level analyses into aggregated run** — Describes merge_individual_analyses, the hook used to merge multiple succeeded individual-level analyses into a new aggregated individual analysis. The method is only called when no other analysis of the same application is running or submitted, and receives the pending individual analysis and the list of succeeded analyses to combine.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Validate whether project-level merge should run** — Documents validate_project_analyses, a hook that asserts whether project-level merge logic should proceed. If the validation fails, the method should raise an AssertionError to prevent further merge processing.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Assert whether individual merges should proceed** — Documents validate_individual_analyses, a validation hook that should raise an AssertionError if individual-level merge logic should not occur. It receives the individual instance and the candidate analyses to validate before merging.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Get or create project-level auto-merge analysis instance** — Describes get_project_level_auto_merge_analysis which finds or creates the project-level analysis used for automatic merges. It takes a project instance and returns a project-level analysis dictionary that can be used to coordinate or record merge operations.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Retrieve or create individual-level auto-merge analysis** — Documents get_individual_level_auto_merge_analysis which fetches or instantiates the individual-level analysis object used for automatic merging tasks. It accepts an individual instance and returns a dictionary-like analysis instance to use for tracking or triggering merges.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Trigger project-level analyses merge when necessary** — Submits a merge job for project-level analyses when required. This helper checks conditions and triggers consolidation of analyses across a project to produce merged representations.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/data.py)
- **Run the project-level merge process** — Documents run_project_merge which executes the project-level merge workflow for a given project instance. It is the entry point for performing merging operations at the project scope and expects a project dictionary-like instance as input.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Execute the individual-level merge workflow** — Explains run_individual_merge which performs the merge process for a specific individual instance. This function is the individual-scope counterpart to run_project_merge and expects an individual dictionary-like instance to coordinate the merge.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
