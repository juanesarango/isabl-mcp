# Job Arrays, Cleanup & Metrics

Patterns and helpers for submitting grouped array jobs, creating exit/cleanup tasks and collecting job metrics (SEFF integration).

## Source Documents

- **Submit LSF array of bash scripts with cleanup** — Explains how to submit an array of bash scripts to LSF, including creation of auxiliary EXIT and CLEAN jobs for failure handling and cleanup. The function takes command tuples, LSF requirement strings, a job name, and options like throttling, wait, and unbuffer, and returns the cleanup job ID. It supports throttling concurrent tasks and optionally waiting for cleanup completion.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/batch_systems/lsf.py)
- **Submit SGE array with exit and cleanup jobs** — Describes submitting arrays of bash scripts to SGE, automatically adding EXIT and CLEAN jobs for error handling and resource cleanup. The function accepts commands, SGE requirements, a job name, and options like throttle_by, wait, and unbuffer and returns the cleanup job ID. It follows the same pattern as other scheduler-specific array submission helpers.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/batch_systems/sge.py)
- **Submit SLURM array including SEFF and cleanup jobs** — Explains how to submit an array of bash scripts to SLURM while automatically creating EXIT, SEFF, and CLEAN jobs to handle failures, collect job metrics, and clean temporary files. The function accepts commands, SLURM requirements, jobname, and optional extra args like throttle_by, wait, and unbuffer, and returns the cleanup job ID. It documents SLURM-specific behavior (SEFF) in addition to common array submission options.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/batch_systems/slurm.py)
- **Using Batch Systems for Scalable Job Submission** — Describes how Isabl submits jobs to common cluster batch systems and the import strings to use from isabl_cli. The page lists supported systems (LSF, Slurm, SGE), points to their submit_* import strings, and references vendor documentation for resource and queue configuration. It also explains that submissions are customizable through Isabl settings and batch system hooks.
  [Source](https://docs.isabl.io/batch-systems)
