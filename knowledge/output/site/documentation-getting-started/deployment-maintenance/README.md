# Deployment & Maintenance

Production deployment guidance and maintenance / backup best practices for operators.

## Source Documents

- **Deploying Isabl in Production Environments** — Provides guidance for deploying Isabl components in production: installing isabl-api on-premise as a Django third-party app and installing isabl-cli in production environments. The doc includes recommended installation commands (pip install from GitHub or clone+editable install) and references to on-premise deployment patterns. It is intended for ops engineers and platform maintainers preparing Isabl for production use.
  [Source](https://docs.isabl.io/production-deployment)
- **Maintenance Utilities and Backup Best Practices** — Provides recommended utilities and best practices to maintain an Isabl instance and keep data safe, with a focus on PostgreSQL backups. It documents cookiecutter-api maintenance helpers accessible in the project compose directory and gives docker-compose commands to create, list, and restore backups. The guide is targeted at sysadmins and operators responsible for production upkeep and recovery planning.
  [Source](https://docs.isabl.io/maintenance)
