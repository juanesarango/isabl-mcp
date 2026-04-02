"""Tests for IsablAPIClient."""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from pathlib import Path
import tempfile

import httpx

from isabl_mcp.clients.isabl_api import IsablAPIClient


@pytest.fixture
def mock_settings():
    """Mock settings for testing."""
    with patch("isabl_mcp.clients.isabl_api.settings") as mock:
        mock.isabl_api_url = "https://test.isabl.io/api/v1/"
        mock.isabl_api_token = "test-token"
        mock.timeout = 30
        mock.verify_ssl = True
        yield mock


@pytest.fixture
def api_client(mock_settings):
    """Create an API client for testing."""
    return IsablAPIClient()


class TestIsablAPIClientInit:
    """Tests for client initialization."""

    def test_default_initialization(self, mock_settings):
        """Test client initializes with default settings."""
        client = IsablAPIClient()
        assert client.base_url == "https://test.isabl.io/api/v1"
        assert client.token == "test-token"
        assert client.timeout == 30
        assert client.verify_ssl is True

    def test_custom_initialization(self, mock_settings):
        """Test client initializes with custom settings."""
        client = IsablAPIClient(
            base_url="https://custom.api.io/api/v2/",
            token="custom-token",
            timeout=60,
            verify_ssl=False,
        )
        assert client.base_url == "https://custom.api.io/api/v2"
        assert client.token == "custom-token"
        assert client.timeout == 60
        assert client.verify_ssl is False

    def test_base_url_trailing_slash_stripped(self, mock_settings):
        """Test trailing slash is removed from base URL."""
        client = IsablAPIClient(base_url="https://test.io/api/v1///")
        assert client.base_url == "https://test.io/api/v1"


class TestIsablAPIClientHeaders:
    """Tests for request headers."""

    def test_headers_with_token(self, api_client):
        """Test headers include auth token when provided."""
        headers = api_client.headers
        assert headers["Content-Type"] == "application/json"
        assert headers["Authorization"] == "Token test-token"

    def test_headers_without_token(self, mock_settings):
        """Test headers work without auth token."""
        mock_settings.isabl_api_token = ""
        client = IsablAPIClient()
        client.token = ""
        headers = client.headers
        assert headers["Content-Type"] == "application/json"
        assert "Authorization" not in headers


class TestIsablAPIClientQuery:
    """Tests for the query method."""

    @pytest.mark.asyncio
    async def test_query_basic(self, api_client):
        """Test basic query without filters."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "count": 2,
            "next": None,
            "previous": None,
            "results": [{"pk": 1}, {"pk": 2}],
        }
        mock_response.raise_for_status = MagicMock()

        with patch.object(api_client, "_get_client") as mock_get_client:
            mock_client = AsyncMock()
            mock_client.get = AsyncMock(return_value=mock_response)
            mock_get_client.return_value = mock_client

            result = await api_client.query("experiments")

            mock_client.get.assert_called_once_with(
                "/experiments",
                params={"limit": 100, "offset": 0}
            )
            assert result["count"] == 2
            assert len(result["results"]) == 2

    @pytest.mark.asyncio
    async def test_query_with_filters(self, api_client):
        """Test query with Django-style filters."""
        mock_response = MagicMock()
        mock_response.json.return_value = {"count": 1, "results": [{"pk": 1}]}
        mock_response.raise_for_status = MagicMock()

        with patch.object(api_client, "_get_client") as mock_get_client:
            mock_client = AsyncMock()
            mock_client.get = AsyncMock(return_value=mock_response)
            mock_get_client.return_value = mock_client

            await api_client.query(
                "analyses",
                filters={"status": "SUCCEEDED", "projects": 102}
            )

            call_args = mock_client.get.call_args
            params = call_args[1]["params"]
            assert params["status"] == "SUCCEEDED"
            assert params["projects"] == 102

    @pytest.mark.asyncio
    async def test_query_with_list_filter(self, api_client):
        """Test query with list filter values."""
        mock_response = MagicMock()
        mock_response.json.return_value = {"count": 0, "results": []}
        mock_response.raise_for_status = MagicMock()

        with patch.object(api_client, "_get_client") as mock_get_client:
            mock_client = AsyncMock()
            mock_client.get = AsyncMock(return_value=mock_response)
            mock_get_client.return_value = mock_client

            await api_client.query(
                "experiments",
                filters={"projects": [1, 2, 3]}
            )

            call_args = mock_client.get.call_args
            params = call_args[1]["params"]
            assert params["projects"] == "1,2,3"

    @pytest.mark.asyncio
    async def test_query_with_fields(self, api_client):
        """Test query with field selection."""
        mock_response = MagicMock()
        mock_response.json.return_value = {"count": 1, "results": [{"pk": 1}]}
        mock_response.raise_for_status = MagicMock()

        with patch.object(api_client, "_get_client") as mock_get_client:
            mock_client = AsyncMock()
            mock_client.get = AsyncMock(return_value=mock_response)
            mock_get_client.return_value = mock_client

            await api_client.query(
                "experiments",
                fields=["pk", "system_id", "results"]
            )

            call_args = mock_client.get.call_args
            params = call_args[1]["params"]
            assert params["fields"] == "pk,system_id,results"

    @pytest.mark.asyncio
    async def test_query_with_pagination(self, api_client):
        """Test query with custom limit and offset."""
        mock_response = MagicMock()
        mock_response.json.return_value = {"count": 100, "results": []}
        mock_response.raise_for_status = MagicMock()

        with patch.object(api_client, "_get_client") as mock_get_client:
            mock_client = AsyncMock()
            mock_client.get = AsyncMock(return_value=mock_response)
            mock_get_client.return_value = mock_client

            await api_client.query("experiments", limit=50, offset=100)

            call_args = mock_client.get.call_args
            params = call_args[1]["params"]
            assert params["limit"] == 50
            assert params["offset"] == 100

    @pytest.mark.asyncio
    async def test_query_http_error(self, api_client):
        """Test query raises HTTP errors properly."""
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

            with pytest.raises(httpx.HTTPStatusError):
                await api_client.query("invalid_endpoint")

    @pytest.mark.asyncio
    async def test_query_all_transparent_pagination(self, api_client):
        """Test query_all fetches all pages transparently."""
        with patch.object(api_client, "query", new_callable=AsyncMock) as mock_query:
            mock_query.side_effect = [
                {
                    "count": 3,
                    "next": "https://test.isabl.io/api/v1/analyses?limit=2&offset=2",
                    "results": [{"pk": 1}, {"pk": 2}],
                },
                {
                    "count": 3,
                    "next": None,
                    "results": [{"pk": 3}],
                },
            ]

            result = await api_client.query_all("analyses", limit=2)

            assert result["count"] == 3
            assert result["next"] is None
            assert result["results"] == [{"pk": 1}, {"pk": 2}, {"pk": 3}]
            assert mock_query.await_count == 2
            mock_query.assert_any_await(
                "analyses",
                filters=None,
                fields=None,
                limit=2,
                offset=0,
            )
            mock_query.assert_any_await(
                "analyses",
                filters=None,
                fields=None,
                limit=2,
                offset=2,
            )

    @pytest.mark.asyncio
    async def test_query_all_respects_max_results(self, api_client):
        """Test query_all stops once max_results is reached."""
        with patch.object(api_client, "query", new_callable=AsyncMock) as mock_query:
            mock_query.side_effect = [
                {
                    "count": 10,
                    "next": "https://test.isabl.io/api/v1/analyses?limit=5&offset=5",
                    "results": [{"pk": i} for i in range(5)],
                },
                {
                    "count": 10,
                    "next": None,
                    "results": [{"pk": i} for i in range(5, 10)],
                },
            ]

            result = await api_client.query_all("analyses", limit=5, max_results=6)

            assert len(result["results"]) == 6
            assert result["has_more"] is True

    def test_analysis_browse_url_uses_api_base(self, api_client):
        """Test analysis browse URL is derived from ISABL_API_URL."""
        assert (
            api_client.analysis_browse_url(518730)
            == "https://test.isabl.io/?analysis=518730"
        )


class TestIsablAPIClientGetInstance:
    """Tests for the get_instance method."""

    @pytest.mark.asyncio
    async def test_get_instance_by_pk(self, api_client):
        """Test getting instance by primary key."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "pk": 123,
            "status": "SUCCEEDED",
            "results": {"vcf": "/path/to/file.vcf"},
        }
        mock_response.raise_for_status = MagicMock()

        with patch.object(api_client, "_get_client") as mock_get_client:
            mock_client = AsyncMock()
            mock_client.get = AsyncMock(return_value=mock_response)
            mock_get_client.return_value = mock_client

            result = await api_client.get_instance("analyses", 123)

            mock_client.get.assert_called_once_with("/analyses/123")
            assert result["pk"] == 123

    @pytest.mark.asyncio
    async def test_get_instance_by_string_id(self, api_client):
        """Test getting instance by string identifier."""
        mock_response = MagicMock()
        mock_response.json.return_value = {"pk": 1, "system_id": "ISB_H000001"}
        mock_response.raise_for_status = MagicMock()

        with patch.object(api_client, "_get_client") as mock_get_client:
            mock_client = AsyncMock()
            mock_client.get = AsyncMock(return_value=mock_response)
            mock_get_client.return_value = mock_client

            result = await api_client.get_instance("individuals", "ISB_H000001")

            mock_client.get.assert_called_once_with("/individuals/ISB_H000001")
            assert result["system_id"] == "ISB_H000001"


class TestIsablAPIClientGetTree:
    """Tests for the get_tree method."""

    @pytest.mark.asyncio
    async def test_get_tree(self, api_client):
        """Test getting individual tree."""
        mock_tree = {
            "pk": 1,
            "system_id": "ISB_H000001",
            "samples": [
                {
                    "pk": 10,
                    "experiments": [{"pk": 100}],
                }
            ],
        }
        mock_response = MagicMock()
        mock_response.json.return_value = mock_tree
        mock_response.raise_for_status = MagicMock()

        with patch.object(api_client, "_get_client") as mock_get_client:
            mock_client = AsyncMock()
            mock_client.get = AsyncMock(return_value=mock_response)
            mock_get_client.return_value = mock_client

            result = await api_client.get_tree("ISB_H000001")

            mock_client.get.assert_called_once_with("/individuals/tree/ISB_H000001")
            assert result["system_id"] == "ISB_H000001"
            assert len(result["samples"]) == 1


class TestIsablAPIClientGetAnalysisResults:
    """Tests for the get_analysis_results method."""

    @pytest.mark.asyncio
    async def test_get_analysis_results(self, api_client):
        """Test getting analysis results."""
        mock_analysis = {
            "pk": 123,
            "status": "SUCCEEDED",
            "storage_url": "/data/analyses/123",
            "results": {"vcf": "/data/analyses/123/output.vcf"},
            "application": {"name": "MUTECT"},
        }

        with patch.object(api_client, "get_instance", new_callable=AsyncMock) as mock_get:
            mock_get.return_value = mock_analysis

            result = await api_client.get_analysis_results(123)

            mock_get.assert_called_once_with("analyses", 123)
            assert result["pk"] == 123
            assert result["status"] == "SUCCEEDED"
            assert result["storage_url"] == "/data/analyses/123"
            assert "vcf" in result["results"]
            assert result["application"] == "MUTECT"

    @pytest.mark.asyncio
    async def test_get_analysis_results_empty(self, api_client):
        """Test getting analysis with no results."""
        mock_analysis = {
            "pk": 456,
            "status": "FAILED",
            "storage_url": None,
            "application": {},
        }

        with patch.object(api_client, "get_instance", new_callable=AsyncMock) as mock_get:
            mock_get.return_value = mock_analysis

            result = await api_client.get_analysis_results(456)

            assert result["pk"] == 456
            assert result["status"] == "FAILED"
            assert result["results"] == {}


class TestIsablAPIClientGetAnalysisLogs:
    """Tests for the get_analysis_logs method."""

    @pytest.mark.asyncio
    async def test_get_logs_all(self, api_client):
        """Test getting all log files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create mock log files
            (Path(tmpdir) / "head_job.log").write_text("stdout content\n")
            (Path(tmpdir) / "head_job.err").write_text("stderr content\n")
            (Path(tmpdir) / "head_job.sh").write_text("#!/bin/bash\necho hello\n")

            with patch.object(api_client, "get_instance", new_callable=AsyncMock) as mock_get:
                mock_get.return_value = {"storage_url": tmpdir}

                result = await api_client.get_analysis_logs(123, log_type="all")

                assert result["head_job.log"] == "stdout content\n"
                assert result["head_job.err"] == "stderr content\n"
                assert "#!/bin/bash" in result["head_job.sh"]

    @pytest.mark.asyncio
    async def test_get_logs_stderr_only(self, api_client):
        """Test getting only stderr log."""
        with tempfile.TemporaryDirectory() as tmpdir:
            (Path(tmpdir) / "head_job.err").write_text("error message\n")

            with patch.object(api_client, "get_instance", new_callable=AsyncMock) as mock_get:
                mock_get.return_value = {"storage_url": tmpdir}

                result = await api_client.get_analysis_logs(123, log_type="stderr")

                assert "head_job.err" in result
                assert result["head_job.err"] == "error message\n"
                assert "head_job.log" not in result

    @pytest.mark.asyncio
    async def test_get_logs_tail_lines(self, api_client):
        """Test getting only last N lines of logs."""
        with tempfile.TemporaryDirectory() as tmpdir:
            lines = "\n".join([f"line {i}" for i in range(100)])
            (Path(tmpdir) / "head_job.err").write_text(lines)

            with patch.object(api_client, "get_instance", new_callable=AsyncMock) as mock_get:
                mock_get.return_value = {"storage_url": tmpdir}

                result = await api_client.get_analysis_logs(
                    123, log_type="stderr", tail_lines=5
                )

                content = result["head_job.err"]
                assert content.count("\n") == 4  # 5 lines = 4 newlines
                assert "line 99" in content
                assert "line 95" in content
                assert "line 0" not in content

    @pytest.mark.asyncio
    async def test_get_logs_no_storage_url(self, api_client):
        """Test handling missing storage URL."""
        with patch.object(api_client, "get_instance", new_callable=AsyncMock) as mock_get:
            mock_get.return_value = {"storage_url": None}

            result = await api_client.get_analysis_logs(123)

            assert "error" in result
            assert "No storage_url" in result["error"]

    @pytest.mark.asyncio
    async def test_get_logs_file_not_found(self, api_client):
        """Test handling missing log files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Don't create any files

            with patch.object(api_client, "get_instance", new_callable=AsyncMock) as mock_get:
                mock_get.return_value = {"storage_url": tmpdir}

                result = await api_client.get_analysis_logs(123, log_type="stderr")

                assert "File not found" in result["head_job.err"]


class TestIsablAPIClientGetProjectSummary:
    """Tests for the get_project_summary method."""

    @pytest.mark.asyncio
    async def test_get_project_summary(self, api_client):
        """Test getting project summary statistics."""
        mock_project = {
            "pk": 102,
            "title": "Test Project",
            "short_title": "TEST",
            "storage_usage": 1_500_000_000_000,  # 1.5 TB
        }

        mock_exp_response = {"count": 50}

        mock_analyses = {
            "results": [
                {"pk": 1, "status": "SUCCEEDED", "application": {"name": "MUTECT"}},
                {"pk": 2, "status": "SUCCEEDED", "application": {"name": "MUTECT"}},
                {"pk": 3, "status": "FAILED", "application": {"name": "STAR"}},
                {"pk": 4, "status": "STARTED", "application": {"name": "STAR"}},
            ]
        }

        with patch.object(api_client, "get_instance", new_callable=AsyncMock) as mock_get_inst:
            mock_get_inst.return_value = mock_project

            with patch.object(api_client, "query", new_callable=AsyncMock) as mock_query:
                mock_query.side_effect = [mock_exp_response, mock_analyses]

                result = await api_client.get_project_summary(102)

                assert result["project"]["pk"] == 102
                assert result["project"]["title"] == "Test Project"
                assert result["counts"]["experiments"] == 50
                assert result["counts"]["analyses"]["total"] == 4
                assert result["counts"]["analyses"]["by_status"]["SUCCEEDED"] == 2
                assert result["counts"]["analyses"]["by_status"]["FAILED"] == 1
                assert result["counts"]["analyses"]["by_application"]["MUTECT"] == 2
                assert result["counts"]["analyses"]["by_application"]["STAR"] == 2
                assert result["storage_usage_gb"] == 1500.0

    @pytest.mark.asyncio
    async def test_get_project_summary_empty(self, api_client):
        """Test getting summary for project with no data."""
        mock_project = {
            "pk": 999,
            "title": "Empty Project",
            "short_title": "EMPTY",
            "storage_usage": None,
        }

        with patch.object(api_client, "get_instance", new_callable=AsyncMock) as mock_get_inst:
            mock_get_inst.return_value = mock_project

            with patch.object(api_client, "query", new_callable=AsyncMock) as mock_query:
                mock_query.side_effect = [{"count": 0}, {"results": []}]

                result = await api_client.get_project_summary(999)

                assert result["counts"]["experiments"] == 0
                assert result["counts"]["analyses"]["total"] == 0
                assert result["storage_usage_gb"] == 0.0


class TestIsablAPIClientClose:
    """Tests for client cleanup."""

    @pytest.mark.asyncio
    async def test_close_client(self, api_client):
        """Test closing the HTTP client."""
        mock_client = AsyncMock()
        api_client._client = mock_client

        await api_client.close()

        mock_client.aclose.assert_called_once()
        assert api_client._client is None

    @pytest.mark.asyncio
    async def test_close_no_client(self, api_client):
        """Test closing when no client exists."""
        api_client._client = None

        # Should not raise
        await api_client.close()

        assert api_client._client is None
