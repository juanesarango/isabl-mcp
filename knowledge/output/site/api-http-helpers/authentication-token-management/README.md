# Authentication & Token Management

Helpers for obtaining, caching and attaching API authentication tokens to requests.

## Source Documents

- **Retrieve and cache API token into auth headers** — get_token_headers obtains an API authentication token and builds the corresponding HTTP headers, storing the token in the user's home directory for reuse. This central helper ensures requests are authenticated and avoids repeatedly prompting for credentials.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/api.py)
