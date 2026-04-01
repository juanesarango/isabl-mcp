# Operational & Reference Guides

Operational topics such as automation with signals, maintenance, supported batch systems, settings and application development guidance.

## Source Documents

- **Automating Workflows with Signals and Triggers** — Explains Isabl's signals system for automating actions when experiments are imported or analyses change status. It shows how to register signal functions via ON_DATA_IMPORT and ON_STATUS_CHANGE settings, gives code examples for common automations (alignment, QC, downstream apps), and documents manual triggering with the CLI.
  [Source](https://docs.isabl.io/operational-automations)
- **Maintenance: Backups and Best Practices** — Lists utilities and recommended practices to keep an Isabl instance healthy and data safe, with an emphasis on Postgres backups. The guide shows docker-compose commands to create, list, and restore database backups and points to maintenance-related files included in the cookiecutter-api project.
  [Source](https://docs.isabl.io/maintenance)
- **Supported Batch Systems for Job Submission** — Describes the batch systems Isabl supports out-of-the-box and how the CLI submits jobs to them. Lists supported systems (LSF, Slurm, SGE) and gives the import strings to reference the submission functions used by isabl_cli.
  [Source](https://docs.isabl.io/batch-systems)
- **Configuring Isabl Settings and Managed Options** — Covers how Isabl components are configured through settings (strings, objects, import strings) and how some settings can be managed from the database admin. It explains import strings, database-managed clients for API/web/CLI settings, and points to where to update default backend and frontend settings in the admin UI.
  [Source](https://docs.isabl.io/isabl-settings)
- **Configuring Project Privacy and Access Controls in Isabl** — Describes Isabl's project-level privacy features, including how projects can be marked as private or public and the visual indicators used in the UI. Notes the Isabl versions that introduced project privacy and explains that privacy settings control metadata access per project.
  [Source](https://docs.isabl.io/project-privacy)
- **Developing Metadata-Driven Applications in Isabl** — Introduces Isabl Applications, which let you deploy data science tools across many experiments using metadata-driven rules. It highlights that applications are tool-agnostic, can submit jobs to multiple compute environments (local, cluster, cloud), and store results as tracked analyses.
  [Source](https://docs.isabl.io/writing-applications)
