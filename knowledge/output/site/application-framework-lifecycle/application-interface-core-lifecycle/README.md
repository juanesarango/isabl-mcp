# Application Interface & Core Lifecycle

AbstractApplication contract, dependency resolution, command generation and the run orchestration used to create and submit analyses.

## Source Documents

- **AbstractApplication base class and method contract** — AbstractApplication defines the interface and lifecycle hooks for Isabl applications. It documents the methods subclasses must implement (e.g., get_command, get_dependencies, validation hooks, result collectors) and their expected arguments and return types to integrate with the Isabl platform.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Resolve analysis dependencies before command generation** — get_dependencies is executed before get_command to collect and return inputs required by the analysis. It should return a tuple of (list of dependency primary keys, inputs dict) that the platform will use to wire dependencies and populate inputs for command construction.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Define shell command for an analysis run** — get_command must return a shell command string that will be executed for a given analysis. It receives the analysis object, resolved inputs (from get_dependencies), and application settings so the subclass can build the exact command to run.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Execute analyses from tuples with commit options** — Primary runner that accepts a list of (targets, references) tuples and executes the corresponding analyses with fine-grained control flags: commit, force, restart, verbose, and local. It orchestrates whether analyses are actually submitted, wiped before submission, restarted, or executed locally, and returns categorized tuples summarizing the run outcomes.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Run a list of analyses with control flags** — Function that takes a list of analysis objects and executes them honoring control flags such as commit, force, restart, and local. It implements the lower-level iteration and submission logic used by higher-level run orchestrators and returns a summary list of outcomes for each analysis.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Map CLI options to experiment tuples** — get_experiments_from_cli_options converts parsed command-line options into a list of (targets, references) experiment tuples that the application should run on. Implementations must interpret CLI flags and selectors and return the target/reference groupings accordingly.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Resolve experiments from default CLI options** — Class helper that extracts or resolves experiment objects based on the default CLI options provided by the user. It centralizes mapping of typical flags/identifiers to the internal experiment representations used by downstream commands.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Retrieve current Isabl client identifier** — This method returns the current client ID used by the Isabl CLI application. It provides a simple accessor for retrieving the identifier that represents the running client instance.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Construct space-separated primary key string** — This accessor builds and returns the primary key string composed of name, version, and assembly separated by spaces. The primary key provides a compact identifier used for application-level naming or lookup.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Retrieve application database model object** — This accessor returns the database object representing the application entity stored in Isabl's database. It is used when interacting with the application record for queries, updates, or relations to other models.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Access application configuration and settings** — This method returns the application's settings object, exposing configuration values used by the CLI and runtime. It provides a centralized way to read configuration for workflows, logging, and integrations.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **String representation shows name, version, assembly** — __repr__(self) returns a concise string containing the object's name, version, and assembly. This representation is useful for logging and debugging to quickly identify the application instance and its genomic assembly.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
