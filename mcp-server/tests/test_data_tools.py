"""Tests for data access tools.

Tools tested:
- isabl_query
- isabl_get_tree
- isabl_get_results
- isabl_get_logs
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch


class TestIsablQuery:
    """Tests for the isabl_query tool."""

    @pytest.fixture
    def mock_client(self):
        """Create a mock API client."""
        return AsyncMock()

    @pytest.fixture
    def mock_mcp(self):
        """Create a mock MCP server."""
        return MagicMock()

    @pytest.fixture
    def isabl_query(self, mock_mcp, mock_client):
        """Get the isabl_query tool function."""
        from isabl_mcp.tools.data import register_data_tools

        # Capture the registered tool
        tool_func = None

        def capture_tool():
            def decorator(func):
                nonlocal tool_func
                if func.__name__ == "isabl_query":
                    tool_func = func
                return func
            return decorator

        mock_mcp.tool = capture_tool
        register_data_tools(mock_mcp, mock_client)
        return tool_func

    @pytest.mark.asyncio
    async def test_query_basic(self, mock_client, isabl_query):
        """Test basic query returns formatted results."""
        mock_client.query_all.return_value = {
            "count": 5,
            "next": None,
            "results": [{"pk": i} for i in range(5)],
        }

        result = await isabl_query("experiments")

        mock_client.query_all.assert_called_once_with(
            endpoint="experiments",
            filters={},
            fields=None,
            limit=100,
            max_results=None,
        )
        assert result["count"] == 5
        assert len(result["results"]) == 5
        assert result["has_more"] is False

    @pytest.mark.asyncio
    async def test_query_with_filters(self, mock_client, isabl_query):
        """Test query with filters."""
        mock_client.query_all.return_value = {
            "count": 2,
            "next": None,
            "results": [{"pk": 1}, {"pk": 2}],
        }

        result = await isabl_query(
            "analyses",
            filters={"status": "FAILED", "projects": 102}
        )

        mock_client.query_all.assert_called_once_with(
            endpoint="analyses",
            filters={"status": "FAILED", "projects": 102},
            fields=None,
            limit=100,
            max_results=None,
        )
        assert result["count"] == 2

    @pytest.mark.asyncio
    async def test_query_with_fields(self, mock_client, isabl_query):
        """Test query with field selection."""
        mock_client.query_all.return_value = {
            "count": 1,
            "next": None,
            "results": [{"pk": 1, "results": {}}],
        }

        await isabl_query(
            "analyses",
            fields=["pk", "results"]
        )

        mock_client.query_all.assert_called_once_with(
            endpoint="analyses",
            filters={},
            fields=["pk", "results"],
            limit=100,
            max_results=None,
        )

    @pytest.mark.asyncio
    async def test_query_with_limit(self, mock_client, isabl_query):
        """Test query with custom limit."""
        mock_client.query_all.return_value = {"count": 50, "next": None, "results": []}

        await isabl_query("experiments", limit=50)

        mock_client.query_all.assert_called_once_with(
            endpoint="experiments",
            filters={},
            fields=None,
            limit=50,
            max_results=None,
        )

    @pytest.mark.asyncio
    async def test_query_has_more_pagination(self, mock_client, isabl_query):
        """Test query indicates when more results exist."""
        mock_client.query_all.return_value = {
            "count": 500,
            "next": None,
            "results": [{"pk": i} for i in range(100)],
        }

        result = await isabl_query("experiments")

        assert result["has_more"] is False

    @pytest.mark.asyncio
    async def test_query_empty_results(self, mock_client, isabl_query):
        """Test query with no results."""
        mock_client.query_all.return_value = {
            "count": 0,
            "next": None,
            "results": [],
        }

        result = await isabl_query("experiments", filters={"status": "NONEXISTENT"})

        assert result["count"] == 0
        assert result["results"] == []
        assert result["has_more"] is False

    @pytest.mark.asyncio
    async def test_query_none_filters_treated_as_empty(self, mock_client, isabl_query):
        """Test that None filters are treated as empty dict."""
        mock_client.query_all.return_value = {"count": 0, "results": []}

        await isabl_query("experiments", filters=None)

        mock_client.query_all.assert_called_once_with(
            endpoint="experiments",
            filters={},
            fields=None,
            limit=100,
            max_results=None,
        )

    @pytest.mark.asyncio
    async def test_query_with_custom_output_fields_and_url(self, mock_client, isabl_query):
        """Test projection with dotted fields and derived analysis URL."""
        mock_client.query_all.return_value = {
            "count": 1,
            "next": None,
            "results": [
                {
                    "pk": 518730,
                    "status": "FAILED",
                    "storage_url": "/work/isabl/analyses/518730",
                    "application": {"name": "CONPAIR_INDIVIDUAL"},
                }
            ],
        }
        mock_client.analysis_browse_url = MagicMock(
            return_value="http://localhost:8000/api/v1/?analysis=518730"
        )

        result = await isabl_query(
            "analyses",
            output_fields=["pk", "application.name", "status", "url", "storage_url"],
        )

        assert result["results"] == [
            {
                "pk": 518730,
                "application.name": "CONPAIR_INDIVIDUAL",
                "status": "FAILED",
                "url": "http://localhost:8000/api/v1/?analysis=518730",
                "storage_url": "/work/isabl/analyses/518730",
            }
        ]

    @pytest.mark.asyncio
    async def test_query_table_format(self, mock_client, isabl_query):
        """Test markdown table formatting."""
        mock_client.query_all.return_value = {
            "count": 1,
            "next": None,
            "results": [{"pk": 1, "status": "FAILED"}],
        }

        result = await isabl_query(
            "analyses",
            output_fields=["pk", "status"],
            output_format="table",
        )

        assert result["output_format"] == "table"
        assert "| pk | status |" in result["output"]
        assert "| 1 | FAILED |" in result["output"]

    @pytest.mark.asyncio
    async def test_query_csv_format(self, mock_client, isabl_query):
        """Test CSV formatting."""
        mock_client.query_all.return_value = {
            "count": 1,
            "next": None,
            "results": [{"pk": 1, "status": "FAILED"}],
        }

        result = await isabl_query(
            "analyses",
            output_fields=["pk", "status"],
            output_format="csv",
        )

        assert result["output_format"] == "csv"
        assert "pk,status" in result["output"]
        assert "1,FAILED" in result["output"]


class TestIsablGetTree:
    """Tests for the isabl_get_tree tool."""

    @pytest.fixture
    def mock_client(self):
        """Create a mock API client."""
        return AsyncMock()

    @pytest.fixture
    def mock_mcp(self):
        """Create a mock MCP server."""
        return MagicMock()

    @pytest.fixture
    def isabl_get_tree(self, mock_mcp, mock_client):
        """Get the isabl_get_tree tool function."""
        from isabl_mcp.tools.data import register_data_tools

        tool_func = None

        def capture_tool():
            def decorator(func):
                nonlocal tool_func
                if func.__name__ == "isabl_get_tree":
                    tool_func = func
                return func
            return decorator

        mock_mcp.tool = capture_tool
        register_data_tools(mock_mcp, mock_client)
        return tool_func

    @pytest.mark.asyncio
    async def test_get_tree_by_system_id(self, mock_client, isabl_get_tree):
        """Test getting tree by system_id."""
        mock_tree = {
            "pk": 1,
            "system_id": "ISB_H000001",
            "samples": [
                {
                    "pk": 10,
                    "system_id": "ISB_S000001",
                    "experiments": [
                        {"pk": 100, "system_id": "ISB_E000001"}
                    ]
                }
            ]
        }
        mock_client.get_tree.return_value = mock_tree

        result = await isabl_get_tree("ISB_H000001")

        mock_client.get_tree.assert_called_once_with("ISB_H000001")
        assert result["system_id"] == "ISB_H000001"
        assert len(result["samples"]) == 1

    @pytest.mark.asyncio
    async def test_get_tree_by_pk(self, mock_client, isabl_get_tree):
        """Test getting tree by primary key."""
        mock_client.get_tree.return_value = {"pk": 123}

        result = await isabl_get_tree("123")

        mock_client.get_tree.assert_called_once_with("123")
        assert result["pk"] == 123

    @pytest.mark.asyncio
    async def test_get_tree_complex_hierarchy(self, mock_client, isabl_get_tree):
        """Test getting tree with multiple samples and experiments."""
        mock_tree = {
            "pk": 1,
            "system_id": "ISB_H000001",
            "samples": [
                {
                    "pk": 10,
                    "category": "TUMOR",
                    "experiments": [
                        {"pk": 100, "technique": {"method": "WGS"}},
                        {"pk": 101, "technique": {"method": "RNA-Seq"}},
                    ]
                },
                {
                    "pk": 11,
                    "category": "NORMAL",
                    "experiments": [
                        {"pk": 102, "technique": {"method": "WGS"}},
                    ]
                }
            ]
        }
        mock_client.get_tree.return_value = mock_tree

        result = await isabl_get_tree("ISB_H000001")

        assert len(result["samples"]) == 2
        assert len(result["samples"][0]["experiments"]) == 2
        assert len(result["samples"][1]["experiments"]) == 1


class TestIsablGetResults:
    """Tests for the isabl_get_results tool."""

    @pytest.fixture
    def mock_client(self):
        """Create a mock API client."""
        return AsyncMock()

    @pytest.fixture
    def mock_mcp(self):
        """Create a mock MCP server."""
        return MagicMock()

    @pytest.fixture
    def isabl_get_results(self, mock_mcp, mock_client):
        """Get the isabl_get_results tool function."""
        from isabl_mcp.tools.data import register_data_tools

        tool_func = None

        def capture_tool():
            def decorator(func):
                nonlocal tool_func
                if func.__name__ == "isabl_get_results":
                    tool_func = func
                return func
            return decorator

        mock_mcp.tool = capture_tool
        register_data_tools(mock_mcp, mock_client)
        return tool_func

    @pytest.mark.asyncio
    async def test_get_all_results(self, mock_client, isabl_get_results):
        """Test getting all results from an analysis."""
        mock_client.get_analysis_results.return_value = {
            "pk": 123,
            "status": "SUCCEEDED",
            "storage_url": "/data/analyses/123",
            "results": {
                "vcf": "/data/analyses/123/output.vcf",
                "bam": "/data/analyses/123/output.bam",
                "tsv": "/data/analyses/123/metrics.tsv",
            },
            "application": "MUTECT",
        }

        result = await isabl_get_results(123)

        mock_client.get_analysis_results.assert_called_once_with(123)
        assert result["pk"] == 123
        assert "vcf" in result["results"]
        assert "bam" in result["results"]
        assert "tsv" in result["results"]

    @pytest.mark.asyncio
    async def test_get_specific_result_key(self, mock_client, isabl_get_results):
        """Test getting a specific result key."""
        mock_client.get_analysis_results.return_value = {
            "pk": 123,
            "status": "SUCCEEDED",
            "storage_url": "/data/analyses/123",
            "results": {
                "vcf": "/data/analyses/123/output.vcf",
                "bam": "/data/analyses/123/output.bam",
            },
        }

        result = await isabl_get_results(123, result_key="vcf")

        assert result["results"] == {"vcf": "/data/analyses/123/output.vcf"}

    @pytest.mark.asyncio
    async def test_get_result_key_not_found(self, mock_client, isabl_get_results):
        """Test handling missing result key."""
        mock_client.get_analysis_results.return_value = {
            "pk": 123,
            "status": "SUCCEEDED",
            "results": {
                "vcf": "/data/analyses/123/output.vcf",
            },
        }

        result = await isabl_get_results(123, result_key="nonexistent")

        assert "error" in result["results"]
        assert "not found" in result["results"]["error"]
        assert "vcf" in result["results"]["error"]  # Should list available keys

    @pytest.mark.asyncio
    async def test_get_results_empty(self, mock_client, isabl_get_results):
        """Test handling analysis with no results."""
        mock_client.get_analysis_results.return_value = {
            "pk": 456,
            "status": "FAILED",
            "storage_url": None,
            "results": {},
        }

        result = await isabl_get_results(456)

        assert result["results"] == {}

    @pytest.mark.asyncio
    async def test_get_results_none_results(self, mock_client, isabl_get_results):
        """Test handling analysis where results is None."""
        mock_client.get_analysis_results.return_value = {
            "pk": 789,
            "status": "CREATED",
            "storage_url": None,
            "results": None,
        }

        result = await isabl_get_results(789, result_key="vcf")

        # Should not crash when results is None
        assert result["results"] is None


class TestIsablGetLogs:
    """Tests for the isabl_get_logs tool."""

    @pytest.fixture
    def mock_client(self):
        """Create a mock API client."""
        return AsyncMock()

    @pytest.fixture
    def mock_mcp(self):
        """Create a mock MCP server."""
        return MagicMock()

    @pytest.fixture
    def isabl_get_logs(self, mock_mcp, mock_client):
        """Get the isabl_get_logs tool function."""
        from isabl_mcp.tools.data import register_data_tools

        tool_func = None

        def capture_tool():
            def decorator(func):
                nonlocal tool_func
                if func.__name__ == "isabl_get_logs":
                    tool_func = func
                return func
            return decorator

        mock_mcp.tool = capture_tool
        register_data_tools(mock_mcp, mock_client)
        return tool_func

    @pytest.mark.asyncio
    async def test_get_all_logs(self, mock_client, isabl_get_logs):
        """Test getting all logs from an analysis."""
        mock_client.get_analysis_logs.return_value = {
            "head_job.log": "stdout content",
            "head_job.err": "stderr content",
            "head_job.sh": "#!/bin/bash\necho hello",
        }

        result = await isabl_get_logs(123)

        mock_client.get_analysis_logs.assert_called_once_with(
            analysis_pk=123,
            log_type="all",
            tail_lines=None,
        )
        assert "head_job.log" in result
        assert "head_job.err" in result
        assert "head_job.sh" in result

    @pytest.mark.asyncio
    async def test_get_stderr_only(self, mock_client, isabl_get_logs):
        """Test getting only stderr log."""
        mock_client.get_analysis_logs.return_value = {
            "head_job.err": "error output",
        }

        result = await isabl_get_logs(123, log_type="stderr")

        mock_client.get_analysis_logs.assert_called_once_with(
            analysis_pk=123,
            log_type="stderr",
            tail_lines=None,
        )

    @pytest.mark.asyncio
    async def test_get_stdout_only(self, mock_client, isabl_get_logs):
        """Test getting only stdout log."""
        mock_client.get_analysis_logs.return_value = {
            "head_job.log": "standard output",
        }

        await isabl_get_logs(123, log_type="stdout")

        mock_client.get_analysis_logs.assert_called_once_with(
            analysis_pk=123,
            log_type="stdout",
            tail_lines=None,
        )

    @pytest.mark.asyncio
    async def test_get_script_only(self, mock_client, isabl_get_logs):
        """Test getting only the script file."""
        mock_client.get_analysis_logs.return_value = {
            "head_job.sh": "#!/bin/bash\nmy_command",
        }

        await isabl_get_logs(123, log_type="script")

        mock_client.get_analysis_logs.assert_called_once_with(
            analysis_pk=123,
            log_type="script",
            tail_lines=None,
        )

    @pytest.mark.asyncio
    async def test_get_logs_with_tail(self, mock_client, isabl_get_logs):
        """Test getting last N lines of logs."""
        mock_client.get_analysis_logs.return_value = {
            "head_job.err": "last 50 lines",
        }

        await isabl_get_logs(123, log_type="stderr", tail_lines=50)

        mock_client.get_analysis_logs.assert_called_once_with(
            analysis_pk=123,
            log_type="stderr",
            tail_lines=50,
        )

    @pytest.mark.asyncio
    async def test_get_logs_error(self, mock_client, isabl_get_logs):
        """Test handling errors when getting logs."""
        mock_client.get_analysis_logs.return_value = {
            "error": "No storage_url for this analysis",
        }

        result = await isabl_get_logs(123)

        assert "error" in result
