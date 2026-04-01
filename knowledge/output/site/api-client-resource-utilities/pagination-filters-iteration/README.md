# Pagination, Filters & Iteration

Helpers to format filter params, iterate paginated endpoints and batch items for efficient retrieval.

## Source Documents

- **Format keyword filters into requests-compatible params** — process_api_filters accepts keyword filter arguments and converts them into a params dict suitable for requests (for example turning lists into comma-separated strings). It normalizes filtering input so the client can pass clean query parameters to endpoints.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/api.py)
- **Iterate over paginated API endpoint yielding results** — iterate walks through a paginated API endpoint, applying provided filters and yielding each object from the 'results' field across pages. It abstracts pagination so callers can consume a continuous stream of items without manually handling page tokens or offsets.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/api.py)
- **Yield successive fixed-size chunks from arrays** — chunks yields successive n-sized segments from an input sequence, producing an iterator suitable for batching operations. It is useful for splitting work into manageable pieces for bulk API calls or parallel processing and gracefully handles final smaller remainder chunks.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/api.py)
