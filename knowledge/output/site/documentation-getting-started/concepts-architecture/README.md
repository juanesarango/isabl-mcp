# Concepts & Architecture

Core platform concepts: data model, application model, signals/automa­tions, settings and batch-system overview.

## Source Documents

- **Isabl Data Model: Individuals, Samples, Experiments** — Explains the core Isabl data model that normalizes a data generation process into Individuals, Samples, and Experiments. The page outlines relationships, unique-together constraints to avoid redundancy, and includes a database diagram to visualize entity links. It guides users on how to register metadata before importing data to ensure integrity and consistent tracking.
  [Source](https://docs.isabl.io/data-model)
- **Writing Applications: Building Reproducible Analyses** — Introduces Isabl Applications, which let you deploy data-science tools across many Experiments using a metadata-driven approach. Covers core concepts: applications are tool-agnostic, can submit to multiple compute environments (local, cluster, cloud), and store outputs as Analysis records.
  [Source](https://docs.isabl.io/writing-applications)
- **Configuring Isabl: Settings and Import Strings** — Describes Isabl's configuration system including settings types and 'import strings' that point to importable objects (classes, functions). It explains database-managed settings that can be edited through the Django admin (default-backend-settings and default-frontend-settings) and notes how to create client-specific settings for the CLI. The page directs users to where various components can be configured and extended.
  [Source](https://docs.isabl.io/isabl-settings)
- **Importing Raw Data with Isabl-CLI** — Covers how Isabl-CLI automates importing raw data by scanning deposition directories and matching files to registered metadata. It explains the default raw data formats recognized, how matched files are moved or symlinked on --commit, and the hashed storage layout used for experiments. The doc also shows how to extend supported formats via settings and how to import specific files into a single experiment using a YAML descriptor with -fi and --files-data.
  [Source](https://docs.isabl.io/import-data)
- **Signals and Operational Automations in Isabl** — Explains Isabl's automation mechanism based on signals that run on experiment import and analysis status changes. The document shows how to register signal functions via ON_DATA_IMPORT and ON_STATUS_CHANGE settings, details the single-argument signature (experiment or analysis), and provides examples to trigger downstream applications like aligners, QC, or reports. It also covers manually running signals via the CLI and designing robust automations.
  [Source](https://docs.isabl.io/operational-automations)
- **Using Batch Systems for Scalable Job Submission** — Describes how Isabl submits jobs to common cluster batch systems and the import strings to use from isabl_cli. The page lists supported systems (LSF, Slurm, SGE), points to their submit_* import strings, and references vendor documentation for resource and queue configuration. It also explains that submissions are customizable through Isabl settings and batch system hooks.
  [Source](https://docs.isabl.io/batch-systems)
- **Configuring Project Privacy and Access Controls** — Describes Isabl's project-level privacy features, including support for marking projects as private or public and the UI icons that indicate privacy status. Notes the minimum web/API package versions that introduced project privacy and explains how privacy affects metadata access visibility.
  [Source](https://docs.isabl.io/project-privacy)
