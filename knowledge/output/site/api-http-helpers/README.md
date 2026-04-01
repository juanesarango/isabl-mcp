# API & HTTP Helpers

Client-side helpers for communicating with the Isabl API: request building, retries, pagination, resource CRUD, authentication, and Isabl-specific serialization wrappers.

## Contents

- [HTTP & Request Helpers](./http-request-helpers/) — Generic request utilities, URL normalization, retries and a high-level api_request wrapper used by CLI operations.
- [Authentication & Token Management](./authentication-token-management/) — Helpers for obtaining, caching and attaching API authentication tokens to requests.
- [Pagination, Batching & Iteration](./pagination-batching-iteration/) — Helpers to iterate paginated API endpoints and to batch or chunk work for bulk operations.
- [Resource CRUD & Retrieval](./resource-crud-retrieval/) — Convenience routines for fetching, listing, creating, patching and deleting API resources, plus specialized getters for projects, experiments and analyses.
- [IsablDict & Serialization Helpers](./isabldict-serialization-helpers/) — Utilities to convert arbitrary Python objects and nested dicts into IsablDict instances and Isabl-specific accessors (custom field access, popping and representations).
- [Analysis-specific API Helpers & Notifications](./analysis-specific-api-helpers-notifications/) — Helpers to fetch/validate analysis results, patch analysis statuses in bulk or singly, and send error/notification emails.
