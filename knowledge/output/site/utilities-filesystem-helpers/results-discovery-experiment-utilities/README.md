# Results Discovery & Experiment Utilities

Utilities that find analysis results on experiment records, wrapper helpers to obtain single results with clearer errors, and traversal helpers for nested dicts.

## Source Documents

- **Find matching analysis results for an experiment** — get_results searches an experiment object for results that match multiple filter criteria: result key, application key/name/version/assembly, target/reference dependencies, analyses, and expected status. It returns a list of tuples (result_value, analysis_pk) and supports complex matching rules including matching by app pk, name, or name+version; pass result_key='storage_url' to get output directories.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/utils.py)
- **Get single matching result with error handling** — get_result is a convenience wrapper around get_results that returns a single matching result (value and producing analysis PK) and raises a clearer error when no or ambiguous matches are found. It accepts the same filters as get_results and allows passing application_name and application_assembly to produce more informative error messages.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/utils.py)
- **Traverse nested dictionary using list of keys** — traverse_dict(dictionary, keys, serialize=False) walks a nested dictionary following an ordered list of keys to retrieve a nested value. If serialize is True, the function forces the result to a string and JSON-serializes any dict values; otherwise it returns the raw object.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/utils.py)
- **Find first file matching pattern recursively** — Documents first_matching_file(directory, pattern, exclude=None, sort_by_newest=True, optional=False), which recursively searches a directory for the first file matching a glob pattern. It supports excluding files by substring, sorting results by creation time, and an optional mode that allows no-match to be acceptable, and raises errors when directory is invalid or no match is found (unless optional).
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/utils.py)
