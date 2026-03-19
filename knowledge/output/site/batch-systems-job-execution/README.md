# Batch Systems & Job Execution

Integrations and submission helpers for local and HPC schedulers (LSF, Slurm, SGE), including array submission helpers and scheduler-specific cleanup/seff/exit jobs.

## Contents

- [Supported Schedulers & Submission Entrypoints](./supported-schedulers-submission-entrypoints/) — Main submission functions that group commands by methods and hand off to scheduler-specific submission implementations.
- [Array Submission Helpers & Cleanup Jobs](./array-submission-helpers-cleanup-jobs/) — Scheduler-specific helpers to submit job arrays, schedule cleanup/exit/seff helper jobs, and support throttling, waiting and resource metric collection.
- [Local Execution & Development](./local-execution-development/) — Running jobs serially on the local machine for debugging or small-scale execution.
