# API Client & Resource Utilities

HTTP helpers, authentication, resource CRUD operations, pagination helpers and lightweight client-side serialization wrappers for interacting with the Isabl REST API.

## Contents

- [HTTP, Auth & Networking](./http-auth-networking/) — URL normalization, request wrappers, token management and retry logic to ensure reliable authenticated API calls.
- [Resource CRUD & Retrieval](./resource-crud-retrieval/) — Convenience functions to fetch, list, count and mutate resources (instances, experiments, analyses, projects) and to retrieve aggregated trees of related data.
- [Pagination, Filters & Iteration](./pagination-filters-iteration/) — Helpers to format filter params, iterate paginated endpoints and batch items for efficient retrieval.
- [Serialization & IsablDict Utilities](./serialization-isabldict-utilities/) — Utilities that convert API responses and nested Python objects into IsablDict wrappers and provide custom dict-like accessors and representations.
- [Analysis Results & Status Helpers](./analysis-results-status-helpers/) — Server-side helpers for validating and patching analysis results and bulk status updates used by CLI and automation code.
