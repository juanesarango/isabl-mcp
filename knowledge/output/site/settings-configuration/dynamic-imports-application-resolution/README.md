# Dynamic Imports & Application Resolution

Utilities that perform dynamic imports for configured import strings, import valid application identifiers from settings, and build application-specific settings dictionaries.

## Source Documents

- **Perform module/class imports for configured values** — Performs one or multiple dynamic imports for values specified in settings, handling strings or iterables that represent import paths. This helper centralizes the import logic used across settings parsing to convert string references into live Python objects.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/settings.py)
- **Import a class or module from string path** — Attempts to import a class, function, or module given its string representation (dot-separated path), optionally providing the originating setting name for clearer error messages. It is a utility to dynamically resolve references in configuration to actual Python objects.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/settings.py)
- **Import valid application strings from client settings** — Parses and imports all valid application identifiers declared in client settings, ensuring configured application strings resolve to actual importable objects. It validates the configured application entries and imports them for use by the system.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/settings.py)
- **Build application settings dictionary from defaults** — Constructs a nested settings dictionary for applications given defaults, the environment settings, reference data, and importable strings. This function centralizes the logic to expand application configuration into a structured settings object ready for consumption by the platform.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/settings.py)
