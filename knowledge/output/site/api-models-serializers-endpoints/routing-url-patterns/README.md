# Routing & URL Patterns

Top-level API URL patterns and the automatic model route generation helpers.

## Source Documents

- **API URL Patterns and Model Route Generation** — Lists the top-level URL patterns for the Isabl API and shows how model-specific routes are generated. It documents endpoints for analyses (download, raw, stream, IGV), assemblies, system_id redirect, individuals tree, submissions processing, registration settings, send_email, and a helper get_models_patterns() that auto-creates list/detail routes for registered models (excluding preferences). The file also defines named path constants used across the API.
  [Source](https://github.com/papaemmelab/isabl_api/blob/master/isabl_api/urls/base.py)
