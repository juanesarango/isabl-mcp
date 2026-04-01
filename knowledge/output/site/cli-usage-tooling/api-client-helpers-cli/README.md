# API Client Helpers (CLI)

Helpers for making API requests from the CLI, token handling, pagination, retries and instance-level helpers.

## Source Documents

- **Recursive conversion to IsablDict utility function** — isablfy converts arbitrary Python objects into IsablDict representations recursively. It is used to normalize nested data structures (e.g., API responses or model objects) into the Isabl expected dictionary-like format for downstream processing or serialization.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/api.py)
- **Array chunking helper yields fixed-size groups** — chunks splits an input array into successive n-sized pieces and yields each piece in turn. It's a small utility useful for batching operations (for example batching IDs into requests) while avoiding copying the entire sequence.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/api.py)
- **Resolve and normalize base API URL** — get_api_url returns a normalized API URL suitable for client requests. It ensures the provided URL is in the correct form (trailing slashes, base path) so other API helpers can construct endpoints consistently.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/api.py)
- **Retry wrapper for HTTP request operations** — retry_request wraps HTTP calls and retries them multiple times to improve robustness against transient failures. It accepts a request method and keyword arguments and will attempt repeated calls (optionally with backoff) until success or timeout.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/api.py)
- **Obtain and cache API token in home** — get_token_headers retrieves an API token and stores it in the user's home directory for reuse, returning HTTP headers (e.g., Authorization) ready for authenticated requests. This centralizes token retrieval/caching to streamline authenticated API calls from CLI tools.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/api.py)
- **Send user identity and group analytics** — send_analytics transmits telemetry about the user's identity and group membership to the analytics service. It is intended to collect usage data for the CLI or platform and typically runs when a user performs certain operations.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/api.py)
- **Generic API request with naive retry logic** — api_request performs HTTP requests to the API with built-in, simple retry logic and optional authentication. It centralizes request behavior (headers, retries, error handling) so callers can execute API operations with consistent semantics.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/api.py)
- **Convert keyword filters to requests params** — process_api_filters converts function keyword filter arguments into a requests-compatible params dictionary for API queries. It takes name/value pairs used for filtering and returns properly formatted query parameters to be appended to GET requests.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/api.py)
- **Paginated API iterator yielding all results** — iterate walks through a paginated API endpoint and yields each object in the 'results' key across pages. It accepts URL and filter parameters, handling pagination transparently so callers can stream or collect all items without manual page handling.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/api.py)
- **Lookup database instance by various identifiers** — get_instance retrieves a database instance from an API endpoint using flexible identifiers (primary key, system_id, email, or username). It accepts an endpoint and optional fields list, returning a SimpleNamespace populated with the instance data for easy attribute access.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/api.py)
- **Create a database instance via API** — Describes the create_instance function used to create a new database object through the Isabl API. It takes an endpoint string (e.g., 'analyses') and a data dict of fields to set, and returns a types.SimpleNamespace populated with the API response.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/api.py)
- **Patch (update) a database instance remotely** — Documents the patch_instance function for updating fields on an existing database object via the Isabl API. It requires an endpoint, an instance identifier (primary key, system_id, email or username), and keyword fields to patch, returning a types.SimpleNamespace with the API response.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/api.py)
- **Delete a database instance via API call** — Explains the delete_instance function for removing an object from the Isabl database through the API. It requires the endpoint name and an identifier (primary key, system_id, email, or username) to specify which object to delete.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/api.py)
- **Retrieve instances from a list API endpoint** — Describes get_instances, a flexible function to fetch objects from list endpoints. It supports optional identifiers and filters, can retrieve all objects when none provided, prints a verbose count if requested, and returns a list of types.SimpleNamespace objects; it raises a UsageError for certain string identifier misuse.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/api.py)
- **Fetch experiments by identifiers or filters** — A convenience accessor to retrieve experiment records from the API using either identifiers or filter keyword arguments. Intended to simplify calling the generic get_instances function for experiments.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/api.py)
- **Retrieve analyses via identifiers or filters** — Provides a simple function to fetch analysis records from the Isabl API by passing identifiers or filters. It offers the same usage pattern as other entity-specific getters to streamline access to analyses.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/api.py)
- **Query projects using identifiers or filters** — Documents get_projects, a helper to fetch project records from the API using identifiers or filter keyword arguments. It follows the same simple interface as other entity-specific getters to return matching objects.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/api.py)
- **Return count of objects from list endpoint** — Explains get_instances_count, a function that returns the integer count of objects matching optional filters at a given list endpoint. You provide the endpoint name and any filter name/value pairs to determine how many objects match the query.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/api.py)
- **Retrieve the full data tree for an individual** — Describes get_tree, which fetches all related information for a single individual identified by an identifier. It is meant to return the complete 'tree' of records linked to that individual within the Isabl system.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/api.py)
- **Fetch full data trees for multiple individuals** — Documents get_trees, which retrieves the complete related records for multiple individuals using identifiers or filters. It provides a bulk version of get_tree to obtain the 'trees' for several individuals in one call.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/api.py)
- **Batch update analyses status utility function** — patch_analyses_status updates the status field for multiple analysis instances in one call. It accepts a list of analysis objects and a status string, asserts the status is one of the allowed values, and returns the list of updated analyses.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/api.py)
- **Patch single analysis status and results** — patch_analysis_status updates a single analysis instance (typically after a successful run). It ensures the analysis is owned by an admin user and that the analysis results field is updated, then returns the patched analysis dictionary.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/api.py)
- **Send error notification emails via API** — send_error_email composes and sends an error notification email to a list of recipients. It accepts recipients, subject, and message and returns the HTTP response object from the underlying API request.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/api.py)
- **Internal helper to fetch or patch results** — _get_analysis_results is an internal utility for obtaining (and potentially patching) the results field of an analysis. It accepts an analysis instance and a raise_error flag to control whether failures raise exceptions.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/api.py)
- **Constructor that retrieves instance by id** — The __init__ method is implemented so that if the first constructor argument is an integer or string it will use that value to retrieve an existing instance. This provides convenience instantiation by id or identifier.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/api.py)
- **Recursive conversion from dicts to IsablDicts** — fromDict is a class method that recursively transforms standard Python dictionaries into IsablDict (or related) objects. This is useful for normalizing nested API payloads into the richer Isabl typed dicts.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/api.py)
- **Get method aware of custom fields** — This get implementation first checks whether the requested key corresponds to a custom field before falling back to the default value. It provides custom-field-aware lookup semantics for Isabl dict-like objects.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/api.py)
- **Pop method honoring custom fields first** — This pop implementation checks whether the key to remove is a custom field and handles that case before falling back to normal dictionary pop behavior. It provides a safe way to remove values while respecting custom field semantics.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/api.py)
- **Improved representation for assembly instances** — This __repr__ provides a concise, informative string representation for assembly objects to make them easier to inspect in logs and interactive sessions. It replaces the generic object repr with key assembly identifiers.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/api.py)
- **Retrieve experiment FASTQ R1 and R2 files** — Describes the get_fastq method which returns paired FASTQ files for an experiment. The function provides two lists: R1 and R2 FASTQ file paths, and raises a MissingDataError if the number of R1 and R2 files does not match.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/api.py)
