# Local Execution & Development

Running jobs serially on the local machine for debugging or small-scale execution.

## Source Documents

- **Local batch submission executed serially** — Defines submit_local(app, command_tuples), a batch system implementation that runs analysis commands locally and serially. It accepts a list of command tuples and executes them on the local machine without array scheduling.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/batch_systems/local.py)
- **Tips and Tricks for Isabl CLI** — Collects helpful extra features and UX tips to improve the Isabl experience, including enhancements like colored logs when using batch systems. The page highlights small customizations and practical tips that make using Isabl-CLI and job submission more efficient and readable.
  [Source](https://docs.isabl.io/bonus-tips)
