# Storage & Instance Management

Helpers to provision storage directories, update storage URLs, and manage analysis storage lifecycle.

## Source Documents

- **Create hierarchical storage directory path** — Describes a helper that computes and creates a storage directory path of the form <root>/<base>/<identifier>, with an optional hashed hierarchy using the last four digits of an integer identifier. The function accepts root, base, identifier, and a use_hash flag and returns the full path to the instance's data directory.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/data.py)
- **Create storage directory and return patched instance** — Explains a utility that creates the storage directory for an instance (optionally hashed) and returns the patched instance via the API. The function takes an endpoint, an identifier, and a use_hash flag to compute and provision the storage URL.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/data.py)
- **Update storage URL and create storage directory** — Utility function that ensures an instance has an on-disk storage directory and patches the instance's storage_url via the API. It accepts an endpoint and identifier (with optional hashing) and returns the updated/patched instance after creating the storage location.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/data.py)
- **Update experiment default BAM for assembly** — Describes a function that updates the default BAM file for an experiment for a specified assembly. It accepts an experiment dict, assembly name, analysis primary key, and bam URL, patches the experiment, and returns the updated experiment object.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/data.py)
- **Move analysis storage to trash directory** — Documents a routine that moves an analysis' storage_url into a designated trash directory for cleanup or archival. This provides a safe way to remove or quarantine storage associated with an analysis without immediate deletion.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/data.py)
- **Produce summary of an import operation** — Returns a summary of a data import operation given the list of files, the experiment record, whether the run was committed, and which files were matched. This function formats the result of an import attempt to help users review what was imported and what remains.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/data.py)
