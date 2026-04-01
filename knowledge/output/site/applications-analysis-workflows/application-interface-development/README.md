# Application Interface & Development

Core Application class interface and helpers used when authoring Isabl applications.

## Source Documents

- **AbstractApplication base class and required methods** — Defines the AbstractApplication class for Isabl applications and documents the interface methods that subclasses must implement. It lists responsibilities such as building commands, resolving experiments from CLI options, validating inputs/settings, producing results, handling dependencies, and optionally merging project-level analyses.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Construct shell command for analysis execution** — Documents the get_command method which must produce the shell command string used to run an analysis. It takes the analysis object, resolved inputs from get_dependencies, and application settings as arguments and must return a command string.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Map CLI options to target-reference experiment tuples** — Specifies get_experiments_from_cli_options which translates parsed CLI options into a list of (targets, references) experiment tuples. This method enables applications to determine which experiment pairs to operate on based on user-provided command-line arguments.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Retrieve experiments from default CLI options** — Classmethod that extracts a list of experiment objects based on the CLI options provided. It parses standard/default CLI flags and returns the matching experiments for downstream processing or submission.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Expose application as Click CLI command** — Describes the as_cli_command classmethod that returns the application represented as a Click command-line interface command. This helper is used to integrate the application object with Click-based CLI tooling so the app can be invoked or inspected from the terminal.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Get name for Isabl CLI command** — Defines a helper that returns the command name used by an Isabl CLI app. This name is used for generating command scripts, logging, and analytics events so the CLI knows how to identify the current command.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Access application settings and configuration** — Explains the settings method that returns the Isabl application settings object or configuration. Use this accessor to retrieve runtime configuration, feature flags, or other application-level parameters required by tooling or scripts.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Get the application database object** — Covers the application method which returns the application database object (likely an ORM model instance) representing this application in the database. This is used when code needs to query or update the application record stored in the Isabl database.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Retrieve current Isabl client identifier** — Describes the client_id method that returns the current client identifier used by the Isabl application. This is a simple accessor for the client ID value, intended for components that need to label or scope operations to a client instance.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Build application primary key string** — Documents the primary_key method which returns a space-separated string composed of the application's name, version, and assembly. This primary key is intended for uniquely identifying an application build or configuration in downstream logic or logs.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Object representation showing name, version, assembly** — __repr__ returns a string representation of the application object that includes its name, version, and assembly. This representation is useful for logging, debugging, and quick inspection of the app state.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
