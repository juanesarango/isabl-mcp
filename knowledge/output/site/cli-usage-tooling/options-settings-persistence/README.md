# Options, Settings & Persistence

CLI option builders, user-level settings and application settings helpers used to configure the CLI and applications.

## Source Documents

- **Build analyses filters option for CLI** — Helper to construct analysis filter options for the CLI, accepting optional application_classes and other default filter values. It centralizes default filter behavior so commands can present and apply consistent analysis selection criteria.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/options.py)
- **Construct dependency analyses option for CLI** — Produces a dependency-analysis option given dependency specifications and extra filters. It supports resolving dependencies by application primary key or by name (optionally with version), enabling commands to gather analyses that satisfy dependency requirements.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/options.py)
- **Import and validate application strings from settings** — Loads and imports application classes listed in client settings, validating that configured application strings can be imported successfully. It ensures that configured applications are available at runtime and converts string references to actual imported types or raises meaningful errors.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/settings.py)
- **Perform_import utility to import configured objects** — Utility function that performs one or more imports based on the provided value and setting name. It wraps import logic and error handling so higher-level settings loaders can import modules, classes, or lists of import strings consistently.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/settings.py)
- **Import a class or module from a string path** — Attempts to import a class or module given its dotted-string representation (e.g., 'module.ClassName'). It provides a reusable import helper that reports clear errors for mis-specified import strings and is used by other settings import utilities.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/settings.py)
- **UserSettings manager for per-user configuration files** — A class that manages user-specific configuration stored in a JSON file at settings_path. It exposes attribute-style access (__getattr__/__setattr__), read/write helpers (_read/_write), and a __repr__ to display current user configurations, encapsulating persistence details for CLI clients.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/settings.py)
- **BaseSettings wrapper supporting defaults and imports** — Wrapper class (inspired by drf-yasg) that initializes with defaults, optional import string lists, and path strings, and exposes combined settings via __getattr__. It returns a merged settings dictionary and falls back to defaults when an attribute is not present in user settings.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/settings.py)
- **Build application settings dictionary from defaults** — Combines provided defaults, current settings, reference data, and import_strings into a coherent application settings dot-dictionary. This helper centralizes how application-level settings are assembled so downstream code can consume a predictable configuration structure.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/settings.py)
- **Check if current user has admin privileges** — Defines is_admin_user to return True when the currently authenticated username matches the configured ADMIN_USER. This helper is used to gate admin-only CLI actions or privileged operations within the Isabl CLI.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/settings.py)
- **Retrieve current API username from database** — Provides api_username method to fetch the current username from the database (the active API user). This accessor centralizes how the CLI determines the identity used for API interactions.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/settings.py)
- **Get client configuration from database function** — Describes the client() helper which retrieves the API/client configuration from the database for the CLI. This function centralizes access to client-related settings so other CLI components can use consistent connection parameters.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/settings.py)
- **Return system-wide settings as dictionary** — _settings() builds and returns a dictionary of system settings used by the CLI and other components. The function provides a single place to gather application-level configuration values into a Python dict for consumption across the codebase.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/settings.py)
