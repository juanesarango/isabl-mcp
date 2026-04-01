# Analysis Results & Status Helpers

Server-side helpers for validating and patching analysis results and bulk status updates used by CLI and automation code.

## Source Documents

- **Batch update analysis status helper** — Utility function to patch the status field of multiple analysis instances in bulk. It validates the requested status (only 'SUBMITTED' or 'STAGED' allowed), applies the update and returns the list of updated analyses, raising an AssertionError for invalid statuses.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/api.py)
- **Patch single analysis status and results** — Function to patch a single analysis instance, ensuring the analysis is owned by the admin user and that the results field is properly updated. It accepts an analysis dict and a status dict and returns the patched analysis instance.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/api.py)
- **Retrieve or validate analysis result data** — Internal helper intended to obtain an analysis's results (and/or patch them) with an option to raise an error if results are missing or invalid. The function accepts an analysis object and a raise_error flag to control error handling behavior.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/api.py)
