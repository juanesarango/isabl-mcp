# HTTP & Request Helpers

Generic request utilities, URL normalization, retries and a high-level api_request wrapper used by CLI operations.

## Source Documents

- **Construct canonical API URL from provided address** — get_api_url produces a full API URL from a provided address or path, ensuring calls go to the correct API base. It normalizes the input so other request helpers can rely on a consistent URL format.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/api.py)
- **Retry wrapper for HTTP requests with simple backoff** — retry_request wraps HTTP request calls and attempts them multiple times on transient failures, providing a naive retry/backoff strategy. It helps make the CLI more resilient to temporary network or server errors when performing API operations.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/api.py)
- **Generic API request helper with authentication and retry** — api_request is a high-level wrapper for making HTTP requests against the Isabl API, supporting optional authentication and a naive retry mechanism. It centralizes header injection, URL normalization, error handling, and retry behavior for all client operations.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/api.py)
- **Format keyword filters into requests-compatible params** — process_api_filters accepts keyword filter arguments and converts them into a params dict suitable for requests (for example turning lists into comma-separated strings). It normalizes filtering input so the client can pass clean query parameters to endpoints.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/api.py)
- **Transmit user identity and group analytics data** — send_analytics sends information about the CLI user identity and group to an analytics endpoint, helping track usage and adoption. The function packages user/group metadata and emits it when appropriate (typically during CLI operations).
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/api.py)
