# CLI & Metadata Helpers

Convenience accessors for exposing applications as CLI commands and for retrieving application metadata like IDs, primary keys and assemblies.

## Source Documents

- **Expose application as click CLI command** — This class method returns the application wrapped as a Click command-line interface entry point. It enables the application to be registered and executed as a CLI command with Click's tooling.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Retrieve CLI command name for isabl_cli app** — Lightweight helper that returns the CLI command name associated with an isabl_cli application instance. Useful for reporting, logging, and constructing script headers when creating job submission artifacts.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **String representation shows name, version, assembly** — __repr__(self) returns a concise string containing the object's name, version, and assembly. This representation is useful for logging and debugging to quickly identify the application instance and its genomic assembly.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Retrieve current Isabl client identifier** — This method returns the current client ID used by the Isabl CLI application. It provides a simple accessor for retrieving the identifier that represents the running client instance.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Construct space-separated primary key string** — This accessor builds and returns the primary key string composed of name, version, and assembly separated by spaces. The primary key provides a compact identifier used for application-level naming or lookup.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Access application configuration and settings** — This method returns the application's settings object, exposing configuration values used by the CLI and runtime. It provides a centralized way to read configuration for workflows, logging, and integrations.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Retrieve application database model object** — This accessor returns the database object representing the application entity stored in Isabl's database. It is used when interacting with the application record for queries, updates, or relations to other models.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Retrieve assembly database object for application** — This method returns the assembly database object associated with the application (e.g., genome assembly reference). It is used to access assembly metadata required by analyses and pipelines.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
