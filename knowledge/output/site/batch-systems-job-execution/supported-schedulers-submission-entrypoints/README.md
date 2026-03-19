# Supported Schedulers & Submission Entrypoints

Main submission functions that group commands by methods and hand off to scheduler-specific submission implementations.

## Source Documents

- **Local batch submission executed serially** — Defines submit_local(app, command_tuples), a batch system implementation that runs analysis commands locally and serially. It accepts a list of command tuples and executes them on the local machine without array scheduling.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/batch_systems/local.py)
- **LSF batch submission grouped by methods** — Defines submit_lsf(app, command_tuples), an LSF batch system implementation that submits application commands as job arrays grouped by target methods. It integrates with LSF scheduling to dispatch grouped jobs to the cluster.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/batch_systems/lsf.py)
- **SGE batch submission grouped by methods** — Defines submit_sge(app, command_tuples), a Sun Grid Engine (SGE) batch system implementation that submits application commands as arrays grouped by target methods. It adapts Isabl's batching to SGE scheduling semantics.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/batch_systems/sge.py)
- **SLURM batch submission grouped by methods** — Defines submit_slurm(app, command_tuples), a SLURM batch system implementation that submits application commands as job arrays grouped by target methods. It integrates Isabl's array submission model with SLURM scheduling.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/batch_systems/slurm.py)
- **Supported Batch Systems for Job Submission** — Describes the batch systems Isabl supports out-of-the-box and how the CLI submits jobs to them. Lists supported systems (LSF, Slurm, SGE) and gives the import strings to reference the submission functions used by isabl_cli.
  [Source](https://docs.isabl.io/batch-systems)
