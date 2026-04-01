# Settings Objects & Persistence

Classes and persistence primitives for per-user and base settings, including JSON-backed UserSettings and BaseSettings with defaults and import handling.

## Source Documents

- **UserSettings class managing per-user JSON configurations** — A class that manages user-specific configuration persisted to a JSON file at settings_path. It provides attribute-style access and mutation (__getattr__, __setattr__), a readable representation, and internal methods to read and write the settings.json file.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/settings.py)
- **BaseSettings wrapper with defaults and imports handling** — A settings wrapper adapted from drf-yasg/rest_framework that merges defaults with user-supplied values, and supports importable strings and path-based settings. It exposes methods to initialize with defaults, produce a combined settings dictionary, and resolve attributes by checking user settings before falling back to defaults.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/settings.py)
- **Initialize settings with defaults and import rules** — Constructor for the settings object that accepts defaults and optional import_strings and path_strings parameters. It follows patterns used by other libraries (see drf-yasg reference) to support automatic import resolution and path handling when building the effective settings.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/settings.py)
- **String representation of settings object** — Defines the __repr__ method to produce a human-readable representation of the settings object by showing all configurations stored under the settings_path. Useful for debugging and quickly inspecting current in-memory and persisted configuration values.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/settings.py)
- **Persist attribute assignments to settings file** — Implements __setattr__ so that assigning attributes on the settings object writes the change to the persistent settings_path (settings.json). This ensures runtime attribute updates are saved for subsequent runs or shared processes.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/settings.py)
- **Attribute lookup with default fallback logic** — A __getattr__ variant that checks whether an attribute is present in user settings and falls back to default values if not. This enforces a consistent lookup order so callers always receive the most relevant configuration value.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/settings.py)
- **Load settings.json into memory** — Defines a private _read method that opens and parses the settings.json file to obtain persisted configuration. It centralizes file reading and any associated error handling for missing or malformed JSON files.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/settings.py)
- **Write key-value pairs to settings.json** — Implements a private _write method to persist a key and value into the settings.json file. It encapsulates the write operation so higher-level code can update configuration atomically and consistently.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/settings.py)
- **Return dictionary of system-wide settings** — This helper returns a dictionary containing system settings used by the Isabl CLI. It centralizes configuration values so callers can read settings consistently across the application.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/settings.py)
