# Interface & Lifecycle

Core abstract class and lifecycle hooks to implement application behavior and dependency resolution.

## Source Documents

- **AbstractApplication base class and method contract** — AbstractApplication defines the interface and lifecycle hooks for Isabl applications. It documents the methods subclasses must implement (e.g., get_command, get_dependencies, validation hooks, result collectors) and their expected arguments and return types to integrate with the Isabl platform.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Define shell command for an analysis run** — get_command must return a shell command string that will be executed for a given analysis. It receives the analysis object, resolved inputs (from get_dependencies), and application settings so the subclass can build the exact command to run.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Resolve analysis dependencies before command generation** — get_dependencies is executed before get_command to collect and return inputs required by the analysis. It should return a tuple of (list of dependency primary keys, inputs dict) that the platform will use to wire dependencies and populate inputs for command construction.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Validate application settings and configuration** — validate_settings should assert that application settings are correctly configured and raise an AssertionError when misconfigured. It receives an ApplicationSettings object (Munch-like) and is used to fail fast if required parameters or resources are missing.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Map CLI options to experiment tuples** — get_experiments_from_cli_options converts parsed command-line options into a list of (targets, references) experiment tuples that the application should run on. Implementations must interpret CLI flags and selectors and return the target/reference groupings accordingly.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Resolve experiments from default CLI options** — Class helper that extracts or resolves experiment objects based on the default CLI options provided by the user. It centralizes mapping of typical flags/identifiers to the internal experiment representations used by downstream commands.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
