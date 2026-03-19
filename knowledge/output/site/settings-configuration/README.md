# Settings & Configuration

Management of system-wide and per-user settings, dynamic import resolution for configured values, and helpers to build application-specific settings structures.

## Contents

- [Settings Objects & Persistence](./settings-objects-persistence/) — Classes and persistence primitives for per-user and base settings, including JSON-backed UserSettings and BaseSettings with defaults and import handling.
- [Dynamic Imports & Application Resolution](./dynamic-imports-application-resolution/) — Utilities that perform dynamic imports for configured import strings, import valid application identifiers from settings, and build application-specific settings dictionaries.
- [Runtime Accessors & Identity](./runtime-accessors-identity/) — Helpers to fetch the current API username, client configuration and to determine whether the running user is an admin.
