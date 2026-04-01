# Pagination, Batching & Iteration

Helpers to iterate paginated API endpoints and to batch or chunk work for bulk operations.

## Source Documents

- **Iterate over paginated API endpoint yielding results** — iterate walks through a paginated API endpoint, applying provided filters and yielding each object from the 'results' field across pages. It abstracts pagination so callers can consume a continuous stream of items without manually handling page tokens or offsets.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/api.py)
- **Yield successive fixed-size chunks from arrays** — chunks yields successive n-sized segments from an input sequence, producing an iterator suitable for batching operations. It is useful for splitting work into manageable pieces for bulk API calls or parallel processing and gracefully handles final smaller remainder chunks.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/api.py)
