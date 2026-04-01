"""Integration-style tests for MCP server tools.

These tests verify that tools work together correctly and handle
real-world scenarios with shared fixtures.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch


class TestQueryAndResultsWorkflow:
    """Tests for typical query -> get results workflow."""

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
        """Register all tools and return them as a dict."""
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
    async def test_query_then_get_results(
        self, mock_client, all_tools, sample_analyses_list, sample_analysis_data
    ):
        """Test querying for analyses then getting results."""
        # Step 1: Query for succeeded analyses
        mock_client.query_all.return_value = {
            "count": 2,
            "next": None,
            "results": sample_analyses_list[:2],  # Two SUCCEEDED analyses
        }

        query_result = await all_tools["isabl_query"](
            "analyses",
            filters={"status": "SUCCEEDED", "projects": 102}
        )

        assert query_result["count"] == 2

        # Step 2: Get results for each analysis
        mock_client.get_analysis_results.return_value = {
            "pk": 1000,
            "status": "SUCCEEDED",
            "storage_url": "/data/analyses/1000",
            "results": {"vcf": "/data/analyses/1000/output.vcf"},
            "application": "MUTECT",
        }

        for analysis in query_result["results"]:
            result = await all_tools["isabl_get_results"](analysis["pk"])
            assert result["status"] == "SUCCEEDED"
            assert "vcf" in result["results"]

    @pytest.mark.asyncio
    async def test_query_failed_analyses_then_get_logs(
        self, mock_client, all_tools, sample_analyses_list
    ):
        """Test querying for failed analyses then getting logs."""
        # Query for failed analyses
        mock_client.query_all.return_value = {
            "count": 1,
            "next": None,
            "results": [sample_analyses_list[2]],  # The FAILED analysis
        }

        query_result = await all_tools["isabl_query"](
            "analyses",
            filters={"status": "FAILED"}
        )

        assert query_result["count"] == 1

        # Get logs for the failed analysis
        mock_client.get_analysis_logs.return_value = {
            "head_job.err": "Error: Out of memory\nSegmentation fault",
        }

        logs = await all_tools["isabl_get_logs"](
            query_result["results"][0]["pk"],
            log_type="stderr"
        )

        assert "Error" in logs["head_job.err"]

    @pytest.mark.asyncio
    async def test_get_tree_then_query_analyses(
        self, mock_client, all_tools, sample_individual_tree
    ):
        """Test getting individual tree then querying related analyses."""
        # Get individual tree
        mock_client.get_tree.return_value = sample_individual_tree

        tree = await all_tools["isabl_get_tree"]("ISB_H000001")

        assert len(tree["samples"]) == 2

        # Collect all experiment PKs
        experiment_pks = []
        for sample in tree["samples"]:
            for exp in sample["experiments"]:
                experiment_pks.append(exp["pk"])

        # Query analyses for these experiments
        mock_client.query_all.return_value = {
            "count": 5,
            "next": None,
            "results": [
                {"pk": 1, "status": "SUCCEEDED", "targets": [{"pk": 100}]},
                {"pk": 2, "status": "SUCCEEDED", "targets": [{"pk": 101}]},
            ],
        }

        analyses = await all_tools["isabl_query"](
            "analyses",
            filters={"targets__in": experiment_pks}
        )

        assert analyses["count"] == 5


class TestMergeResultsWorkflow:
    """Tests for merge_results in real scenarios."""

    @pytest.fixture
    def mock_client(self):
        """Create a mock API client."""
        return AsyncMock()

    @pytest.fixture
    def mock_mcp(self):
        """Create a mock MCP server."""
        return MagicMock()

    @pytest.fixture
    def merge_results(self, mock_mcp, mock_client):
        """Get the merge_results tool function."""
        from isabl_mcp.tools.aggregation import register_aggregation_tools

        tools = {}

        def capture_tool():
            def decorator(func):
                tools[func.__name__] = func
                return func
            return decorator

        mock_mcp.tool = capture_tool
        register_aggregation_tools(mock_mcp, mock_client)
        return tools["merge_results"]

    @pytest.mark.asyncio
    async def test_merge_cohort_vcfs(self, mock_client, merge_results):
        """Test merging VCF files from a cohort analysis."""
        # Simulate getting VCFs from multiple analyses
        mock_client.get_analysis_results.side_effect = [
            {
                "pk": i,
                "storage_url": f"/data/analyses/{i}",
                "status": "SUCCEEDED",
                "results": {"vcf": f"/data/analyses/{i}/somatic.vcf.gz"},
            }
            for i in range(1, 11)  # 10 analyses
        ]

        result = await merge_results(
            list(range(1, 11)),
            "vcf",
            output_format="paths"
        )

        assert result["total_requested"] == 10
        assert result["files_found"] == 10
        assert all(f["path"].endswith(".vcf.gz") for f in result["files"])


class TestProjectSummaryWorkflow:
    """Tests for project_summary with realistic data."""

    @pytest.fixture
    def mock_client(self):
        """Create a mock API client."""
        return AsyncMock()

    @pytest.fixture
    def mock_mcp(self):
        """Create a mock MCP server."""
        return MagicMock()

    @pytest.fixture
    def project_summary(self, mock_mcp, mock_client):
        """Get the project_summary tool function."""
        from isabl_mcp.tools.aggregation import register_aggregation_tools

        tools = {}

        def capture_tool():
            def decorator(func):
                tools[func.__name__] = func
                return func
            return decorator

        mock_mcp.tool = capture_tool
        register_aggregation_tools(mock_mcp, mock_client)
        return tools["project_summary"]

    @pytest.mark.asyncio
    async def test_large_project_summary(self, mock_client, project_summary):
        """Test summarizing a large project."""
        mock_client.get_project_summary.return_value = {
            "project": {
                "pk": 1,
                "title": "Large Cancer Genomics Study",
                "short_title": "LCGS",
            },
            "counts": {
                "experiments": 5000,
                "analyses": {
                    "total": 25000,
                    "by_status": {
                        "SUCCEEDED": 20000,
                        "FAILED": 1000,
                        "STARTED": 500,
                        "SUBMITTED": 1000,
                        "STAGED": 2000,
                        "CREATED": 500,
                    },
                    "by_application": {
                        "BWA": 5000,
                        "MUTECT": 5000,
                        "STRELKA": 5000,
                        "STAR": 5000,
                        "QC_METRICS": 5000,
                    },
                },
            },
            "storage_usage_gb": 50000.0,  # 50 TB
        }

        result = await project_summary(1)

        assert result["counts"]["experiments"] == 5000
        assert result["counts"]["analyses"]["total"] == 25000
        assert sum(result["counts"]["analyses"]["by_status"].values()) == 25000


class TestAppToolsWorkflow:
    """Tests for app discovery workflow."""

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
    async def test_discover_app_then_get_template(
        self, mock_client, app_tools, sample_application_data
    ):
        """Test discovering an app and then generating a template."""
        # First, search for apps
        mock_client.query.return_value = {
            "results": [sample_application_data]
        }

        search_result = await app_tools["get_apps"]("MUTECT", detailed=True)

        assert search_result["match_type"] == "exact"
        assert search_result["app"]["name"] == "MUTECT"

        # The app uses pairs (tumor-normal), generate paired template
        template = await app_tools["get_app_template"](
            app_type="paired",
            include_dependencies=True
        )

        assert "options.PAIRS" in template
        assert "get_dependencies" in template
        assert "utils.get_result" in template


class TestEdgeCases:
    """Tests for edge cases and error handling."""

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
    async def test_query_with_complex_filters(self, mock_client, all_tools):
        """Test query with complex nested filters."""
        mock_client.query_all.return_value = {"count": 0, "results": []}

        await all_tools["isabl_query"](
            "experiments",
            filters={
                "projects": 102,
                "technique__method": "WGS",
                "sample__category": "TUMOR",
                "created__gte": "2024-01-01",
                "created__lte": "2024-12-31",
            }
        )

        call_args = mock_client.query_all.call_args
        filters = call_args[1]["filters"]
        assert filters["technique__method"] == "WGS"
        assert filters["sample__category"] == "TUMOR"

    @pytest.mark.asyncio
    async def test_query_with_special_characters(self, mock_client, all_tools):
        """Test query handles special characters in filters."""
        mock_client.query_all.return_value = {"count": 0, "results": []}

        # Query with identifier that might have special characters
        await all_tools["isabl_query"](
            "individuals",
            filters={"identifier": "PATIENT-001_v2"}
        )

        call_args = mock_client.query_all.call_args
        assert call_args[1]["filters"]["identifier"] == "PATIENT-001_v2"

    @pytest.mark.asyncio
    async def test_get_results_with_nested_result_structure(
        self, mock_client, all_tools
    ):
        """Test getting results with deeply nested structure."""
        mock_client.get_analysis_results.return_value = {
            "pk": 123,
            "status": "SUCCEEDED",
            "storage_url": "/data/analyses/123",
            "results": {
                "primary": {
                    "path": "/data/analyses/123/primary.vcf",
                    "index": "/data/analyses/123/primary.vcf.idx",
                    "metadata": {
                        "variant_count": 15000,
                        "filtered_count": 500,
                    },
                },
                "secondary": "/data/analyses/123/secondary.tsv",
            },
        }

        result = await all_tools["isabl_get_results"](123, result_key="primary")

        assert "primary" in result["results"]
        assert result["results"]["primary"]["path"] == "/data/analyses/123/primary.vcf"

    @pytest.mark.asyncio
    async def test_unicode_in_project_title(self, mock_client, all_tools):
        """Test handling unicode characters in project data."""
        mock_client.get_project_summary.return_value = {
            "project": {
                "pk": 1,
                "title": "Genome Analysis - Phase III",
                "short_title": "GA3",
            },
            "counts": {
                "experiments": 10,
                "analyses": {"total": 50, "by_status": {}, "by_application": {}},
            },
            "storage_usage_gb": 100.0,
        }

        result = await all_tools["project_summary"](1)

        assert "Phase III" in result["project"]["title"]

    @pytest.mark.asyncio
    async def test_very_long_log_content(self, mock_client, all_tools):
        """Test handling very long log content."""
        # Simulate a very long log file
        long_log = "Log line\n" * 100000  # 100k lines

        mock_client.get_analysis_logs.return_value = {
            "head_job.err": long_log,
        }

        result = await all_tools["isabl_get_logs"](123, log_type="stderr")

        # Should return the content (client handles truncation)
        assert "head_job.err" in result

    @pytest.mark.asyncio
    async def test_zero_limit_query(self, mock_client, all_tools):
        """Test query with zero limit still works."""
        mock_client.query_all.return_value = {"count": 100, "results": []}

        result = await all_tools["isabl_query"]("experiments", limit=0)

        # Should still make the call
        mock_client.query_all.assert_called_once()

    @pytest.mark.asyncio
    async def test_large_analysis_id(self, mock_client, all_tools):
        """Test handling very large analysis IDs."""
        mock_client.get_analysis_results.return_value = {
            "pk": 999999999,
            "status": "SUCCEEDED",
            "storage_url": "/data/analyses/999999999",
            "results": {},
        }

        result = await all_tools["isabl_get_results"](999999999)

        assert result["pk"] == 999999999
