# Array Submission Helpers & Cleanup Jobs

Scheduler-specific helpers to submit job arrays, schedule cleanup/exit/seff helper jobs, and support throttling, waiting and resource metric collection.

## Source Documents

- **Submit LSF job arrays with cleanup and exit** — Defines submit_lsf_array(commands, requirements, jobname, extra_args=None, throttle_by=50, wait=False, unbuffer=False) to submit an array of bash scripts to LSF. It also submits two auxiliary jobs (EXIT for failures and CLEAN to remove temporary files), supports throttling, optional waiting, and returns the cleanup job ID.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/batch_systems/lsf.py)
- **Submit SGE job arrays with cleanup and exit** — Defines submit_sge_array(commands, requirements, jobname, extra_args=None, throttle_by=50, wait=False, unbuffer=False) to submit an array of bash scripts to SGE. It also schedules EXIT and CLEAN helper jobs, supports throttling and optional waiting, and returns the cleanup job ID upon submission.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/batch_systems/sge.py)
- **Submit SLURM job arrays with SEFF and cleanup** — Defines submit_slurm_array(commands, requirements, jobname, extra_args=None, throttle_by=50, wait=False, unbuffer=False) to submit an array of bash scripts to SLURM. It additionally schedules three helper jobs—EXIT (failure handling), SEFF (collects job resource metrics), and CLEAN (cleanup)—supports throttling, optional waiting, and returns the cleanup job ID.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/batch_systems/slurm.py)
