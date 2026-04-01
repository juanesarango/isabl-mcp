# Resource CRUD & Retrieval

Convenience functions to fetch, list, count and mutate resources (instances, experiments, analyses, projects) and to retrieve aggregated trees of related data.

## Source Documents

- **Fetch single resource by id, system_id, or username** — get_instance retrieves a single database/resource instance from an API endpoint using various identifier types (primary key, system_id, email, or username). It supports an optional fields argument to limit returned attributes and returns a SimpleNamespace populated with the response.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/api.py)
- **Retrieve list of instances from API endpoints** — Describes get_instances which fetches objects from a list-style API endpoint. It supports optional identifiers, API filter kwargs, and a verbose flag; if neither identifiers nor filters are given it retrieves all objects and will raise click.UsageError for certain invalid string identifiers and endpoints.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/api.py)
- **Count objects matching filters on endpoint** — Explains get_instances_count which returns the number of objects available at a list API endpoint matching provided filters. You provide the endpoint (e.g., 'analyses') and any name/value filter pairs, and it returns an integer count.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/api.py)
- **Create a new API database instance** — Describes the create_instance helper that creates a new database object via the Isabl API. It takes an endpoint path and a data dict of fields to create and returns a SimpleNamespace loaded with the API response.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/api.py)
- **Patch an existing database instance via API** — Documents the patch_instance helper for updating fields of an existing database object through the Isabl API. It requires an endpoint, an instance identifier (primary key, system_id, email or username) and keyword fields to patch, returning a SimpleNamespace with the API response.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/api.py)
- **Delete a database instance through API** — Explains delete_instance which removes a database object using the Isabl API. It accepts an endpoint and an identifier (primary key, system_id, email or username) to identify which object to delete.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/api.py)
- **Get experiment objects by identifiers or filters** — Documents get_experiments which retrieves experiment resources by accepting optional identifiers or filter keyword arguments. It provides a simple entry point for fetching experiments from the API using the same identifier/filter pattern as other getters.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/api.py)
- **Get analysis records using identifiers or filters** — Documents get_analyses which fetches analysis objects from the API by either identifiers or filter keyword arguments. It mirrors the common pattern used by other endpoint-specific getters for convenience.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/api.py)
- **Fetch project records with identifiers or filters** — Describes get_projects which retrieves project resources from the API using optional identifiers or filter keyword arguments. It provides the standard identifier/filter interface used across other resource getters.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/api.py)
- **Retrieve full data tree for an individual** — Documents get_tree which fetches all related data for a single individual identified by an identifier. It is a convenience helper to obtain the complete aggregated tree of resources associated with that individual from the API.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/api.py)
- **Retrieve full data trees for multiple individuals** — Describes get_trees which retrieves the complete aggregated data trees for multiple individuals by accepting identifiers or filters. It extends the single-individual get_tree behavior to batch retrieval across multiple subjects.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/api.py)
- **Retrieve experiment FASTQ R1 and R2 files** — get_fastq returns the paired FASTQ file lists for an experiment: a list of R1 files and a list of R2 files. It validates pairing and raises a MissingDataError if the number of R1 and R2 files does not match.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/api.py)
- **Lazy projects factory method returning project list** — A lazy accessor method named projects that returns a list of project objects. The method delays evaluation until called, providing on-demand retrieval of project lists from the factory context.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/factories.py)
