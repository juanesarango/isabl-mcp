# Batch Systems Integrations

Submission helpers and array submission utilities for supported schedulers (SLURM, LSF, SGE) including auxiliary helper jobs and throttling.

## Source Documents

- **SLURM batch submission grouped by methods** — Defines submit_slurm(app, command_tuples), a SLURM batch system implementation that submits application commands as job arrays grouped by target methods. It integrates Isabl's array submission model with SLURM scheduling.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/batch_systems/slurm.py)
- **Submit SLURM job arrays with SEFF and cleanup** — Defines submit_slurm_array(commands, requirements, jobname, extra_args=None, throttle_by=50, wait=False, unbuffer=False) to submit an array of bash scripts to SLURM. It additionally schedules three helper jobs—EXIT (failure handling), SEFF (collects job resource metrics), and CLEAN (cleanup)—supports throttling, optional waiting, and returns the cleanup job ID.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/batch_systems/slurm.py)
- **LSF batch submission grouped by methods** — Defines submit_lsf(app, command_tuples), an LSF batch system implementation that submits application commands as job arrays grouped by target methods. It integrates with LSF scheduling to dispatch grouped jobs to the cluster.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/batch_systems/lsf.py)
- **Submit LSF job arrays with cleanup and exit** — Defines submit_lsf_array(commands, requirements, jobname, extra_args=None, throttle_by=50, wait=False, unbuffer=False) to submit an array of bash scripts to LSF. It also submits two auxiliary jobs (EXIT for failures and CLEAN to remove temporary files), supports throttling, optional waiting, and returns the cleanup job ID.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/batch_systems/lsf.py)
- **SGE batch submission grouped by methods** — Defines submit_sge(app, command_tuples), a Sun Grid Engine (SGE) batch system implementation that submits application commands as arrays grouped by target methods. It adapts Isabl's batching to SGE scheduling semantics.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/batch_systems/sge.py)
- **Submit SGE job arrays with cleanup and exit** — Defines submit_sge_array(commands, requirements, jobname, extra_args=None, throttle_by=50, wait=False, unbuffer=False) to submit an array of bash scripts to SGE. It also schedules EXIT and CLEAN helper jobs, supports throttling and optional waiting, and returns the cleanup job ID upon submission.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/batch_systems/sge.py)
- **Supported Batch Systems for Job Submission** — Describes the batch systems Isabl supports out-of-the-box and how the CLI submits jobs to them. Lists supported systems (LSF, Slurm, SGE) and gives the import strings to reference the submission functions used by isabl_cli.
  [Source](https://docs.isabl.io/batch-systems)
