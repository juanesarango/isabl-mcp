# Admin & Runtime Accessors

Convenience accessors for checking admin status and fetching current API username and client configuration.

## Source Documents

- **Check whether current user is admin** — Provides an is_admin_user helper that returns True when the current runtime user matches the ADMIN_USER configured in settings. Useful for gating CLI or API operations that require administrative privileges.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/settings.py)
- **Fetch current API username from database** — Defines an api_username accessor that retrieves the current username from the database (the Isabl user record). This abstracts the underlying data lookup so various parts of the CLI can consistently determine the active user.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/settings.py)
- **Retrieve Isabl client configuration from database** — This function fetches the client configuration object from the Isabl database. It is used by the CLI to obtain runtime client settings (credentials, endpoints, etc.) needed to interact with the Isabl server.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/settings.py)
