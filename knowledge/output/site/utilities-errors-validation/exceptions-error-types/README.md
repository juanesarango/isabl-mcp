# Exceptions & Error Types

Custom exception classes used by isabl_cli to signal validation, configuration and runtime problems.

## Source Documents

- **Base exception class for isabl_cli package** — Defines the foundational exception type for the isabl_cli package that other custom exceptions inherit from. Serves as a single catch-all base to distinguish package-raised errors from other exceptions in client code.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/exceptions.py)
- **Validation error for input and configuration checks** — Represents errors raised when a validation step fails (e.g., incorrect inputs or parameter validation). Use this exception type to indicate user- or config-related validation problems that should be corrected before re-running operations.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/exceptions.py)
- **Missing requirement error for unmet dependencies** — Indicates that a required dependency, tool, or resource is missing and prevents an operation from proceeding. This exception communicates unmet prerequisites so callers or users can install or enable the missing requirement.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/exceptions.py)
- **Error for expected but absent output files** — Raised when a process should have produced an output file but the file is missing. Use this error to flag pipeline or job failures where outputs are absent despite successful run steps.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/exceptions.py)
- **Configuration error for improper setup or values** — Used to indicate that the system is improperly configured or configuration values are invalid. This exception signals configuration issues that must be corrected before normal operation can continue.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/exceptions.py)
- **Implementation error for unimplemented functionality** — Signals that a required behavior or function is not implemented or incorrectly implemented. This exception is intended for developer-facing errors where code paths are missing or incomplete.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/exceptions.py)
- **Runtime error when application cannot be executed** — Raised when an application or command cannot be run at all, typically due to fatal preconditions or environment issues. Use it to make clear that execution was impossible rather than merely failing during runtime.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/exceptions.py)
- **Missing data error for absent required inputs** — Used when required input data is missing and prevents further processing. This exception highlights data availability issues that need resolution before pipelines or commands can continue.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/exceptions.py)
- **AutomationError exception for failed automations** — Defines AutomationError, a specific exception raised when automated tasks or workflows fail. It is intended to signal automation-related failures so callers can catch and handle automation-specific errors separately from generic exceptions.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/exceptions.py)
