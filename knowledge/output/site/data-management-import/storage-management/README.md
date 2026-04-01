# Storage Management

Compute and create storage directories, patch instance storage URLs, and register files into instance storage.

## Source Documents

- **Construct and create hierarchical storage directories** — Computes and creates a filesystem path for data storage using a root, base, and identifier. Optionally uses a hashed layout by splitting the identifier into subdirectories derived from the last four digits to avoid large flat directories.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/data.py)
- **Create storage directory and return patched instance** — Creates the appropriate storage directory for an instance and returns the patched instance with the storage URL. The function takes an API endpoint, an identifier, and an optional use_hash flag to control directory layout.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/data.py)
- **Update storage URL and create storage directory** — A helper function that creates a storage directory for an instance and patches the instance via the API, returning the updated object. It takes an API endpoint, an identifier and optional data payload and hashing flag to compute or modify the storage URL before persisting the change.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/data.py)
- **Import and register files into instance storage** — Moves or symlinks files into an experiment instance's storage_url and updates the database to register them. Supports copying instead of moving and accepts per-file metadata (files_data) such as platform or library identifiers. Raises an error if multiple conflicting data formats are detected and returns the patched experiment instance dictionary.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/data.py)
- **Move an analysis storage URL to trash directory** — Moves an analysis' storage_url into a designated trash directory for cleanup or soft-deletion. This function is intended to remove active storage references while preserving data in a trash area for recovery or auditing.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/data.py)
- **Generate import operation summary and outcomes** — Produces a summary of an import operation given the file list, target experiment, commit decision, and matched items. Aggregates the actions that would be or were performed and helps communicate the import result to users. Useful for pre-commit review and post-commit reporting.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/data.py)
