# Isabl Knowledge Tree (root)

Top-level navigation for Isabl platform documentation organized by capabilities and use cases (CLI, data import, applications, execution, settings, utilities, errors, automation, and user-facing docs). Each leaf points to relevant source documents by doc_id.

## Contents

- [API & HTTP Helpers](./api-http-helpers/) — Client-side helpers for communicating with the Isabl API: request building, retries, pagination, resource CRUD, authentication, and Isabl-specific serialization wrappers.
- [Application Framework & Lifecycle](./application-framework-lifecycle/) — APIs, hooks and helpers to author, validate, run and collect results from Isabl Applications — the metadata-driven analysis units that submit jobs and record tracked analyses.
- [Data Import & Storage Management](./data-import-storage-management/) — Tools and import engines to associate raw files with experiments, register reference resources (BEDs, genomes), create storage directories, symlink/move files, and validate ownership/readability.
- [Batch Systems & Job Execution](./batch-systems-job-execution/) — Integrations and submission helpers for local and HPC schedulers (LSF, Slurm, SGE), including array submission helpers and scheduler-specific cleanup/seff/exit jobs.
- [CLI Commands & User Tools](./cli-commands-user-tools/) — Top-level CLI entrypoint, user-facing commands for authentication, data retrieval, job/process management, and convenience helpers for interacting with Isabl from the terminal.
- [Settings & Configuration](./settings-configuration/) — Management of system-wide and per-user settings, dynamic import resolution for configured values, and helpers to build application-specific settings structures.
- [Utilities & Filesystem Helpers](./utilities-filesystem-helpers/) — General-purpose utilities used across the CLI and importers for filesystem operations, archiving, rsync command generation, results discovery, UX messages and debugging aids.
- [Exceptions & Validators](./exceptions-validators/) — Custom exception types used across isabl_cli and validation helpers for CLI options, files and pair definitions.
- [Signals & Automation](./signals-automation/) — Signal functions and automation patterns that drive post-import or status-change workflows, and CLI triggers to run or rerun signals.
- [Documentation & Guides](./documentation-guides/) — Top-level user and developer documentation pages explaining Isabl features, deployment, import workflows, data model and tutorials.
- [Factories, Options & Small Helpers](./factories-options-small-helpers/) — Lightweight helpers for lazy factories and reusable CLI option builders used by isabl-cli commands.
