# Custom Exceptions

Package-level exception hierarchy and common error types to signal validation issues, missing resources, configuration problems and automation failures.

## Source Documents

- **Base exception class for isabl_cli package** — Defines the foundational exception type for the isabl_cli package. Other custom exceptions in isabl_cli inherit from this class to provide a consistent error hierarchy and catch-all handling when needed.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/exceptions.py)
- **Validation error for input and config checks** — Represents errors raised when validation of inputs, parameters, or configuration fails. Use this exception to indicate user-supplied data or settings did not meet required constraints.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/exceptions.py)
- **Error for missing external or internal requirement** — Signals that a required component, dependency, or resource is not available. This exception should be raised when prerequisites for an operation are absent, such as missing binaries, libraries, or configuration entries.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/exceptions.py)
- **Missing output file or artifact error class** — Raised when a file or artifact that should have been produced by a process is not found. This exception highlights failures in pipeline steps or post-processing where expected outputs are absent.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/exceptions.py)
- **Configuration error indicating improper setup** — Indicates that the application or environment is not properly configured. Use this exception to signal missing or invalid configuration entries that prevent normal operation.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/exceptions.py)
- **Error for incomplete or incorrect implementation** — Used to indicate that a feature or function is not correctly implemented or contains a programming error. This exception is appropriate for signaling missing implementation details or internal inconsistencies.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/exceptions.py)
- **Exception for applications that cannot be executed** — Signals that an application or command cannot be run under current conditions. Use this to indicate fatal precondition failures that prevent execution even before runtime steps begin.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/exceptions.py)
- **Error indicating missing required data resources** — Raised when required data for processing or analysis is missing. This exception helps identify situations where input datasets, sample records, or other essential data are unavailable.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/exceptions.py)
- **AutomationError exception class for automation failures** — Defines an AutomationError exception used to signal failures in automation processes. This class is intended to be raised when automated tasks or workflows fail, allowing callers to catch and handle automation-specific errors.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/exceptions.py)
