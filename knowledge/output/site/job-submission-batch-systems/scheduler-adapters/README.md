# Scheduler Adapters

Implementations for local execution and common batch systems (LSF, SGE, SLURM).

## Source Documents

- **Submit analyses locally and serially** — Describes a backend for executing analyses locally by running commands in serial. The submit_local function accepts an app context and a list of command tuples and executes them sequentially on the local host. It's intended for testing, development, or environments without a batch scheduler.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/batch_systems/local.py)
- **Submit grouped array jobs to LSF scheduler** — Provides a function to submit application jobs to LSF as grouped arrays according to target methods. The submit_lsf function takes the app context and command tuples and organizes them into LSF array submissions. It enables efficient submission to clusters using LSF.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/batch_systems/lsf.py)
- **Submit LSF array of bash scripts with cleanup** — Explains how to submit an array of bash scripts to LSF, including creation of auxiliary EXIT and CLEAN jobs for failure handling and cleanup. The function takes command tuples, LSF requirement strings, a job name, and options like throttling, wait, and unbuffer, and returns the cleanup job ID. It supports throttling concurrent tasks and optionally waiting for cleanup completion.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/batch_systems/lsf.py)
- **Submit grouped array jobs to SGE scheduler** — Documents a function that submits application jobs to SGE as grouped arrays by target methods. The submit_sge function accepts the application context and command tuples, packaging them for submission to an SGE scheduler. It is part of Isabl's batch system abstraction to support multiple schedulers.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/batch_systems/sge.py)
- **Submit SGE array with exit and cleanup jobs** — Describes submitting arrays of bash scripts to SGE, automatically adding EXIT and CLEAN jobs for error handling and resource cleanup. The function accepts commands, SGE requirements, a job name, and options like throttle_by, wait, and unbuffer and returns the cleanup job ID. It follows the same pattern as other scheduler-specific array submission helpers.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/batch_systems/sge.py)
- **Submit grouped array jobs to SLURM scheduler** — Provides a function to submit grouped application jobs to SLURM as array jobs organized by target methods. submit_slurm takes the app context and command tuples and manages submission to SLURM clusters. It integrates with the unified Isabl batch interface to support SLURM-specific behavior.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/batch_systems/slurm.py)
- **Submit SLURM array including SEFF and cleanup jobs** — Explains how to submit an array of bash scripts to SLURM while automatically creating EXIT, SEFF, and CLEAN jobs to handle failures, collect job metrics, and clean temporary files. The function accepts commands, SLURM requirements, jobname, and optional extra args like throttle_by, wait, and unbuffer, and returns the cleanup job ID. It documents SLURM-specific behavior (SEFF) in addition to common array submission options.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/batch_systems/slurm.py)
