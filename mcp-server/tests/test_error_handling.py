"""Tests for error handling across all MCP server components.

These tests verify proper error handling for:
- Network errors
- Invalid inputs
- Missing data
- API errors
- File system errors
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from pathlib import Path
import tempfile

import httpx


class TestAPIClientErrorHandling:
    """Tests for API client error handling."""

    @pytest.fixture
    def mock_settings(self):
        """Mock settings for testing."""
        with patch("isabl_mcp.clients.isabl_api.settings") as mock:
            mock.isabl_api_url = "https://test.isabl.io/api/v1/"
            mock.isabl_api_token = "test-token"
            mock.timeout = 30
            mock.verify_ssl = True
            yield mock

    @pytest.fixture
    def api_client(self, mock_settings):
        """Create an API client for testing."""
        from isabl_mcp.clients.isabl_api import IsablAPIClient
        return IsablAPIClient()

    @pytest.mark.asyncio
    async def test_connection_timeout(self, api_client):
        """Test handling connection timeout."""
        with patch.object(api_client, "_get_client") as mock_get_client:
            mock_client = AsyncMock()
            mock_client.get.side_effect = httpx.TimeoutException("Connection timed out")
            mock_get_client.return_value = mock_client

            with pytest.raises(httpx.TimeoutException):
                await api_client.query("experiments")

    @pytest.mark.asyncio
    async def test_connection_refused(self, api_client):
        """Test handling connection refused."""
        with patch.object(api_client, "_get_client") as mock_get_client:
            mock_client = AsyncMock()
            mock_client.get.side_effect = httpx.ConnectError("Connection refused")
            mock_get_client.return_value = mock_client

            with pytest.raises(httpx.ConnectError):
                await api_client.query("experiments")

    @pytest.mark.asyncio
    async def test_http_401_unauthorized(self, api_client):
        """Test handling 401 unauthorized error."""
        with patch.object(api_client, "_get_client") as mock_get_client:
            mock_client = AsyncMock()
            mock_response = MagicMock()
            mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
                "Unauthorized",
                request=MagicMock(),
                response=MagicMock(status_code=401)
            )
            mock_client.get = AsyncMock(return_value=mock_response)
            mock_get_client.return_value = mock_client

            with pytest.raises(httpx.HTTPStatusError) as exc_info:
                await api_client.query("experiments")

            assert exc_info.value.response.status_code == 401

    @pytest.mark.asyncio
    async def test_http_403_forbidden(self, api_client):
        """Test handling 403 forbidden error."""
        with patch.object(api_client, "_get_client") as mock_get_client:
            mock_client = AsyncMock()
            mock_response = MagicMock()
            mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
                "Forbidden",
                request=MagicMock(),
                response=MagicMock(status_code=403)
            )
            mock_client.get = AsyncMock(return_value=mock_response)
            mock_get_client.return_value = mock_client

            with pytest.raises(httpx.HTTPStatusError) as exc_info:
                await api_client.query("experiments")

            assert exc_info.value.response.status_code == 403

    @pytest.mark.asyncio
    async def test_http_404_not_found(self, api_client):
        """Test handling 404 not found error."""
        with patch.object(api_client, "_get_client") as mock_get_client:
            mock_client = AsyncMock()
            mock_response = MagicMock()
            mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
                "Not Found",
                request=MagicMock(),
                response=MagicMock(status_code=404)
            )
            mock_client.get = AsyncMock(return_value=mock_response)
            mock_get_client.return_value = mock_client

            with pytest.raises(httpx.HTTPStatusError) as exc_info:
                await api_client.get_instance("analyses", 99999)

            assert exc_info.value.response.status_code == 404

    @pytest.mark.asyncio
    async def test_http_500_server_error(self, api_client):
        """Test handling 500 server error."""
        with patch.object(api_client, "_get_client") as mock_get_client:
            mock_client = AsyncMock()
            mock_response = MagicMock()
            mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
                "Internal Server Error",
                request=MagicMock(),
                response=MagicMock(status_code=500)
            )
            mock_client.get = AsyncMock(return_value=mock_response)
            mock_get_client.return_value = mock_client

            with pytest.raises(httpx.HTTPStatusError) as exc_info:
                await api_client.query("experiments")

            assert exc_info.value.response.status_code == 500

    @pytest.mark.asyncio
    async def test_malformed_json_response(self, api_client):
        """Test handling malformed JSON response."""
        with patch.object(api_client, "_get_client") as mock_get_client:
            mock_client = AsyncMock()
            mock_response = MagicMock()
            mock_response.raise_for_status = MagicMock()
            mock_response.json.side_effect = ValueError("Invalid JSON")
            mock_client.get = AsyncMock(return_value=mock_response)
            mock_get_client.return_value = mock_client

            with pytest.raises(ValueError):
                await api_client.query("experiments")


class TestDataToolsErrorHandling:
    """Tests for data tools error handling."""

    @pytest.fixture
    def mock_client(self):
        """Create a mock API client."""
        return AsyncMock()

    @pytest.fixture
    def mock_mcp(self):
        """Create a mock MCP server."""
        return MagicMock()

    @pytest.fixture
    def data_tools(self, mock_mcp, mock_client):
        """Get data tools."""
        from isabl_mcp.tools.data import register_data_tools

        tools = {}

        def capture_tool():
            def decorator(func):
                tools[func.__name__] = func
                return func
            return decorator

        mock_mcp.tool = capture_tool
        register_data_tools(mock_mcp, mock_client)
        return tools

    @pytest.mark.asyncio
    async def test_query_client_error_propagates(self, mock_client, data_tools):
        """Test that client errors propagate from query."""
        mock_client.query_all.side_effect = Exception("API unavailable")

        with pytest.raises(Exception) as exc_info:
            await data_tools["isabl_query"]("experiments")

        assert "API unavailable" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_get_tree_not_found(self, mock_client, data_tools):
        """Test getting tree for nonexistent individual."""
        mock_client.get_tree.side_effect = httpx.HTTPStatusError(
            "Not Found",
            request=MagicMock(),
            response=MagicMock(status_code=404)
        )

        with pytest.raises(httpx.HTTPStatusError):
            await data_tools["isabl_get_tree"]("NONEXISTENT_ID")

    @pytest.mark.asyncio
    async def test_get_results_analysis_not_found(self, mock_client, data_tools):
        """Test getting results for nonexistent analysis."""
        mock_client.get_analysis_results.side_effect = httpx.HTTPStatusError(
            "Not Found",
            request=MagicMock(),
            response=MagicMock(status_code=404)
        )

        with pytest.raises(httpx.HTTPStatusError):
            await data_tools["isabl_get_results"](99999)

    @pytest.mark.asyncio
    async def test_get_logs_permission_denied(self, mock_client, data_tools):
        """Test handling permission denied when reading logs."""
        mock_client.get_analysis_logs.side_effect = PermissionError(
            "Permission denied"
        )

        with pytest.raises(PermissionError):
            await data_tools["isabl_get_logs"](123)


class TestAggregationToolsErrorHandling:
    """Tests for aggregation tools error handling."""

    @pytest.fixture
    def mock_client(self):
        """Create a mock API client."""
        return AsyncMock()

    @pytest.fixture
    def mock_mcp(self):
        """Create a mock MCP server."""
        return MagicMock()

    @pytest.fixture
    def aggregation_tools(self, mock_mcp, mock_client):
        """Get aggregation tools."""
        from isabl_mcp.tools.aggregation import register_aggregation_tools

        tools = {}

        def capture_tool():
            def decorator(func):
                tools[func.__name__] = func
                return func
            return decorator

        mock_mcp.tool = capture_tool
        register_aggregation_tools(mock_mcp, mock_client)
        return tools

    @pytest.mark.asyncio
    async def test_merge_results_partial_failure(self, mock_client, aggregation_tools):
        """Test merge_results handles partial failures gracefully."""
        mock_client.get_analysis_results.side_effect = [
            {"storage_url": "/data/1", "status": "SUCCEEDED", "results": {"vcf": "/data/1/out.vcf"}},
            Exception("Network error"),
            {"storage_url": "/data/3", "status": "SUCCEEDED", "results": {"vcf": "/data/3/out.vcf"}},
            Exception("Timeout"),
        ]

        result = await aggregation_tools["merge_results"]([1, 2, 3, 4], "vcf")

        assert result["total_requested"] == 4
        assert result["files_found"] == 2
        assert len(result["errors"]) == 2
        assert any("Network error" in e for e in result["errors"])
        assert any("Timeout" in e for e in result["errors"])

    @pytest.mark.asyncio
    async def test_merge_results_all_failures(self, mock_client, aggregation_tools):
        """Test merge_results when all analyses fail."""
        mock_client.get_analysis_results.side_effect = Exception("API down")

        result = await aggregation_tools["merge_results"]([1, 2, 3], "vcf")

        assert result["total_requested"] == 3
        assert result["files_found"] == 0
        assert len(result["errors"]) == 3

    @pytest.mark.asyncio
    async def test_merge_results_unreadable_file(self, mock_client, aggregation_tools):
        """Test merge_results handles unreadable files in preview mode."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a file that will cause read error
            test_file = Path(tmpdir) / "output.tsv"
            test_file.write_text("data")
            test_file.chmod(0o000)  # Remove read permissions

            mock_client.get_analysis_results.return_value = {
                "storage_url": tmpdir,
                "status": "SUCCEEDED",
                "results": {"tsv": str(test_file)},
            }

            result = await aggregation_tools["merge_results"]([1], "tsv", output_format="preview")

            # Should capture the error but not crash
            assert result["files_found"] == 1
            # Cleanup - restore permissions for temp dir cleanup
            test_file.chmod(0o644)

    @pytest.mark.asyncio
    async def test_project_summary_not_found(self, mock_client, aggregation_tools):
        """Test project summary for nonexistent project."""
        mock_client.get_project_summary.side_effect = httpx.HTTPStatusError(
            "Not Found",
            request=MagicMock(),
            response=MagicMock(status_code=404)
        )

        with pytest.raises(httpx.HTTPStatusError):
            await aggregation_tools["project_summary"](99999)


class TestAppToolsErrorHandling:
    """Tests for app tools error handling."""

    @pytest.fixture
    def mock_client(self):
        """Create a mock API client."""
        return AsyncMock()

    @pytest.fixture
    def mock_mcp(self):
        """Create a mock MCP server."""
        return MagicMock()

    @pytest.fixture
    def app_tools(self, mock_mcp, mock_client):
        """Get app tools."""
        from isabl_mcp.tools.apps import register_app_tools

        tools = {}

        def capture_tool():
            def decorator(func):
                tools[func.__name__] = func
                return func
            return decorator

        mock_mcp.tool = capture_tool
        register_app_tools(mock_mcp, mock_client)
        return tools

    @pytest.mark.asyncio
    async def test_get_apps_api_error(self, mock_client, app_tools):
        """Test get_apps handles API errors."""
        mock_client.query.side_effect = httpx.HTTPStatusError(
            "Service Unavailable",
            request=MagicMock(),
            response=MagicMock(status_code=503)
        )

        with pytest.raises(httpx.HTTPStatusError):
            await app_tools["get_apps"]("MUTECT")

    @pytest.mark.asyncio
    async def test_get_apps_empty_query(self, mock_client, app_tools):
        """Test get_apps with empty query string."""
        mock_client.query.side_effect = [
            {"results": []},  # Exact match
            {"results": []},  # Search
        ]

        result = await app_tools["get_apps"]("")

        assert result["match_type"] == "none"

    @pytest.mark.asyncio
    async def test_get_app_template_invalid_type(self, app_tools):
        """Test get_app_template with invalid app type."""
        # The function accepts any string, so it should still generate a template
        # using the cohort path (which is the fallback)
        result = await app_tools["get_app_template"](app_type="invalid_type")

        # Should still produce valid Python
        compile(result, "<template>", "exec")


class TestInputValidation:
    """Tests for input validation across tools."""

    @pytest.fixture
    def mock_client(self):
        """Create a mock API client."""
        return AsyncMock()

    @pytest.fixture
    def mock_mcp(self):
        """Create a mock MCP server."""
        return MagicMock()

    @pytest.fixture
    def all_tools(self, mock_mcp, mock_client):
        """Register all tools."""
        from isabl_mcp.tools.data import register_data_tools
        from isabl_mcp.tools.apps import register_app_tools
        from isabl_mcp.tools.aggregation import register_aggregation_tools

        tools = {}

        def capture_tool():
            def decorator(func):
                tools[func.__name__] = func
                return func
            return decorator

        mock_mcp.tool = capture_tool
        register_data_tools(mock_mcp, mock_client)
        register_app_tools(mock_mcp, mock_client)
        register_aggregation_tools(mock_mcp, mock_client)
        return tools

    @pytest.mark.asyncio
    async def test_query_invalid_endpoint(self, mock_client, all_tools):
        """Test query with invalid endpoint name."""
        mock_client.query_all.side_effect = httpx.HTTPStatusError(
            "Not Found",
            request=MagicMock(),
            response=MagicMock(status_code=404)
        )

        with pytest.raises(httpx.HTTPStatusError):
            await all_tools["isabl_query"]("invalid_endpoint_name")

    @pytest.mark.asyncio
    async def test_get_logs_invalid_log_type(self, mock_client, all_tools):
        """Test get_logs with invalid log type."""
        mock_client.get_analysis_logs.return_value = {}

        result = await all_tools["isabl_get_logs"](123, log_type="invalid")

        # Should return empty dict - invalid types are ignored
        mock_client.get_analysis_logs.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_results_negative_analysis_id(self, mock_client, all_tools):
        """Test get_results with negative analysis ID."""
        mock_client.get_analysis_results.side_effect = httpx.HTTPStatusError(
            "Not Found",
            request=MagicMock(),
            response=MagicMock(status_code=404)
        )

        with pytest.raises(httpx.HTTPStatusError):
            await all_tools["isabl_get_results"](-1)

    @pytest.mark.asyncio
    async def test_merge_results_negative_limit(self, mock_client, all_tools):
        """Test merge_results handles negative values in list gracefully."""
        mock_client.get_analysis_results.side_effect = httpx.HTTPStatusError(
            "Not Found",
            request=MagicMock(),
            response=MagicMock(status_code=404)
        )

        result = await all_tools["merge_results"]([-1, -2], "vcf")

        # Should record errors for invalid IDs
        assert result["files_found"] == 0
        assert len(result["errors"]) == 2
