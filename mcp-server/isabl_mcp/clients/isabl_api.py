"""Isabl REST API client."""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from pathlib import Path

import httpx

from isabl_mcp.config import settings


class IsablAPIClient:
    """Client for the Isabl REST API."""

    def __init__(
        self,
        base_url: Optional[str] = None,
        token: Optional[str] = None,
        timeout: Optional[int] = None,
        verify_ssl: Optional[bool] = None,
    ):
        self.base_url = (base_url or settings.isabl_api_url).rstrip("/")
        self.token = token or settings.isabl_api_token
        self.timeout = timeout or settings.timeout
        self.verify_ssl = verify_ssl if verify_ssl is not None else settings.verify_ssl

        self._client: Optional[httpx.AsyncClient] = None

    @property
    def headers(self) -> Dict[str, str]:
        """Get request headers with authentication."""
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["Authorization"] = f"Token {self.token}"
        return headers

    async def _get_client(self) -> httpx.AsyncClient:
        """Get or create the HTTP client."""
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(
                base_url=self.base_url,
                headers=self.headers,
                timeout=self.timeout,
                verify=self.verify_ssl,
            )
        return self._client

    async def close(self) -> None:
        """Close the HTTP client."""
        if self._client is not None:
            await self._client.aclose()
            self._client = None

    async def query(
        self,
        endpoint: str,
        filters: Optional[Dict[str, Any]] = None,
        fields: Optional[List[str]] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> Dict[str, Any]:
        """
        Query an Isabl API endpoint.

        Args:
            endpoint: API endpoint (e.g., "experiments", "analyses", "projects")
            filters: Django-style query filters
            fields: List of fields to return (optional)
            limit: Maximum number of results
            offset: Pagination offset

        Returns:
            API response with count, next, previous, and results
        """
        client = await self._get_client()

        # Build query parameters
        params: Dict[str, Any] = {"limit": limit, "offset": offset}

        # Add filters
        if filters:
            for key, value in filters.items():
                if isinstance(value, list):
                    params[key] = ",".join(str(v) for v in value)
                else:
                    params[key] = value

        # Add field selection
        if fields:
            params["fields"] = ",".join(fields)

        # Note: Isabl API requires no trailing slash
        response = await client.get(f"/{endpoint}", params=params)
        response.raise_for_status()
        return response.json()

    async def query_all(
        self,
        endpoint: str,
        filters: Optional[Dict[str, Any]] = None,
        fields: Optional[List[str]] = None,
        limit: int = 100,
        max_results: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Query an endpoint and transparently paginate through all pages.

        Args:
            endpoint: API endpoint (e.g., "analyses")
            filters: Django-style query filters
            fields: List of fields to return (optional)
            limit: Page size for each API call
            max_results: Optional cap on total returned rows

        Returns:
            Combined API response with merged `results`
        """
        offset = 0
        combined_results: List[Dict[str, Any]] = []
        count = 0
        has_more = False
        next_url: Optional[str] = None

        while True:
            page = await self.query(
                endpoint,
                filters=filters,
                fields=fields,
                limit=limit,
                offset=offset,
            )

            count = page.get("count", count)
            next_url = page.get("next")
            page_results = page.get("results", [])
            combined_results.extend(page_results)

            if max_results is not None and len(combined_results) >= max_results:
                combined_results = combined_results[:max_results]
                has_more = (next_url is not None) or (count > len(combined_results))
                next_url = page.get("next")
                break

            if next_url is None or not page_results:
                has_more = False
                break

            offset += limit

        return {
            "count": count,
            "next": next_url if has_more else None,
            "results": combined_results,
            "has_more": has_more,
        }

    def analysis_browse_url(self, analysis_pk: int) -> str:
        """
        Build analysis browse URL from ISABL_API_URL.

        Example: http://localhost:8000/?analysis=123
        """
        frontend_base = self.base_url.rstrip("/")
        if frontend_base.endswith("/api/v1"):
            frontend_base = frontend_base[: -len("/api/v1")]
        return f"{frontend_base}/?analysis={analysis_pk}"

    async def get_instance(
        self,
        endpoint: str,
        pk: "int | str",
    ) -> Dict[str, Any]:
        """
        Get a single instance by primary key.

        Args:
            endpoint: API endpoint (e.g., "experiments", "analyses")
            pk: Primary key or identifier

        Returns:
            Instance data
        """
        client = await self._get_client()
        # Note: Isabl API requires no trailing slash
        response = await client.get(f"/{endpoint}/{pk}")
        response.raise_for_status()
        return response.json()

    async def get_tree(self, individual_pk: "int | str") -> Dict[str, Any]:
        """
        Get the full hierarchy tree for an individual.

        Args:
            individual_pk: Individual primary key or system_id

        Returns:
            Nested structure with individual, samples, experiments
        """
        client = await self._get_client()
        # Note: Isabl API requires no trailing slash
        response = await client.get(f"/individuals/tree/{individual_pk}")
        response.raise_for_status()
        return response.json()

    async def get_analysis_results(self, analysis_pk: int) -> Dict[str, Any]:
        """
        Get results and storage URL for an analysis.

        Args:
            analysis_pk: Analysis primary key

        Returns:
            Analysis data with results and storage_url
        """
        data = await self.get_instance("analyses", analysis_pk)
        return {
            "pk": data.get("pk"),
            "status": data.get("status"),
            "storage_url": data.get("storage_url"),
            "results": data.get("results", {}),
            "application": data.get("application", {}).get("name"),
        }

    async def get_analysis_logs(
        self,
        analysis_pk: int,
        log_type: str = "all",
        tail_lines: Optional[int] = None,
    ) -> Dict[str, str]:
        """
        Get execution logs for an analysis.

        Args:
            analysis_pk: Analysis primary key
            log_type: "stdout", "stderr", "script", or "all"
            tail_lines: Only return last N lines (optional)

        Returns:
            Dict with log file contents
        """
        # First get the storage URL
        data = await self.get_instance("analyses", analysis_pk)
        storage_url = data.get("storage_url")

        if not storage_url:
            return {"error": "No storage_url for this analysis"}

        storage_path = Path(storage_url)
        logs: Dict[str, str] = {}

        log_files = {
            "stdout": "head_job.log",
            "stderr": "head_job.err",
            "script": "head_job.sh",
        }

        files_to_read = (
            log_files.keys() if log_type == "all" else [log_type]
        )

        for log_key in files_to_read:
            if log_key not in log_files:
                continue

            log_path = storage_path / log_files[log_key]
            if log_path.exists():
                content = log_path.read_text()
                if tail_lines:
                    lines = content.splitlines()
                    content = "\n".join(lines[-tail_lines:])
                logs[log_files[log_key]] = content
            else:
                logs[log_files[log_key]] = f"File not found: {log_path}"

        return logs

    async def get_project_summary(self, project_pk: int) -> Dict[str, Any]:
        """
        Get summary statistics for a project.

        Args:
            project_pk: Project primary key

        Returns:
            Project summary with counts and statistics
        """
        # Get project info
        project = await self.get_instance("projects", project_pk)

        # Get experiment count
        exp_response = await self.query(
            "experiments",
            filters={"projects": project_pk},
            fields=["pk"],
            limit=1,
        )

        # Get analysis counts by status
        analysis_response = await self.query(
            "analyses",
            filters={"targets__projects": project_pk},
            fields=["pk", "status", "application"],
            limit=10000,  # Get all for counting
        )

        analyses = analysis_response.get("results", [])
        status_counts: Dict[str, int] = {}
        app_counts: Dict[str, int] = {}

        for a in analyses:
            status = a.get("status", "UNKNOWN")
            status_counts[status] = status_counts.get(status, 0) + 1

            app_name = a.get("application", {}).get("name", "UNKNOWN")
            app_counts[app_name] = app_counts.get(app_name, 0) + 1

        return {
            "project": {
                "pk": project.get("pk"),
                "title": project.get("title"),
                "short_title": project.get("short_title"),
            },
            "counts": {
                "experiments": exp_response.get("count", 0),
                "analyses": {
                    "total": len(analyses),
                    "by_status": status_counts,
                    "by_application": app_counts,
                },
            },
            "storage_usage_gb": (project.get("storage_usage") or 0) / 1e9,
        }
