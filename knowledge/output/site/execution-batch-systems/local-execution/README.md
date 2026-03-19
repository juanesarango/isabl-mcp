# Local Execution

Run analysis commands locally (serial execution) for testing or small-scale runs.

## Source Documents

- **Local batch submission executed serially** — Defines submit_local(app, command_tuples), a batch system implementation that runs analysis commands locally and serially. It accepts a list of command tuples and executes them on the local machine without array scheduling.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/batch_systems/local.py)
