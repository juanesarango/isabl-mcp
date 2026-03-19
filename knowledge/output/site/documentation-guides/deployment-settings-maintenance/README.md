# Deployment, Settings & Maintenance

Instructions for production deployment, configuring Isabl settings, backups and operational best practices.

## Source Documents

- **Production Deployment: Installing Isabl API and CLI** — Provides guidance for deploying Isabl components in production: installing isabl-api on premise as a Django app and installing isabl-cli in your production environment. It documents installation methods for the CLI (pip from GitHub or editable install) and references deployment-related considerations and files used in production setups.
  [Source](https://docs.isabl.io/production-deployment)
- **Configuring Isabl Settings and Managed Options** — Covers how Isabl components are configured through settings (strings, objects, import strings) and how some settings can be managed from the database admin. It explains import strings, database-managed clients for API/web/CLI settings, and points to where to update default backend and frontend settings in the admin UI.
  [Source](https://docs.isabl.io/isabl-settings)
- **Maintenance: Backups and Best Practices** — Lists utilities and recommended practices to keep an Isabl instance healthy and data safe, with an emphasis on Postgres backups. The guide shows docker-compose commands to create, list, and restore database backups and points to maintenance-related files included in the cookiecutter-api project.
  [Source](https://docs.isabl.io/maintenance)
