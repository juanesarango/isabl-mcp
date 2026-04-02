"""Tests for MCP prompts."""

import pytest

from mcp.server.fastmcp import FastMCP
from isabl_mcp.prompts import register_prompts


@pytest.fixture
def mcp_with_prompts():
    mcp = FastMCP("test")
    register_prompts(mcp)
    return mcp


def _text(message) -> str:
    """Extract text from a prompt Message (content may be str or TextContent)."""
    content = message.content
    if isinstance(content, str):
        return content
    return content.text


class TestPromptRegistration:
    def test_all_prompts_registered(self, mcp_with_prompts):
        prompts = mcp_with_prompts._prompt_manager._prompts
        expected = [
            "isabl_debug_analysis",
            "isabl_query_data",
            "isabl_write_app",
            "isabl_project_report",
            "isabl_monitor_analyses",
            "isabl_merge_results",
            "isabl_submit_data",
            "isabl_run_pipeline",
        ]
        for name in expected:
            assert name in prompts, f"Prompt {name} not registered"
        assert len(prompts) == 8

    @pytest.mark.asyncio
    async def test_debug_analysis_prompt(self, mcp_with_prompts):
        prompts = mcp_with_prompts._prompt_manager._prompts
        result = prompts["isabl_debug_analysis"].fn(analysis_id=12345)
        text = _text(result[0])
        assert "12345" in text
        assert "stderr" in text

    @pytest.mark.asyncio
    async def test_query_data_prompt_with_project(self, mcp_with_prompts):
        prompts = mcp_with_prompts._prompt_manager._prompts
        result = prompts["isabl_query_data"].fn(entity_type="analyses", project_id="102")
        text = _text(result[0])
        assert "analyses" in text
        assert "102" in text

    @pytest.mark.asyncio
    async def test_query_data_prompt_defaults(self, mcp_with_prompts):
        prompts = mcp_with_prompts._prompt_manager._prompts
        result = prompts["isabl_query_data"].fn()
        assert "experiments" in _text(result[0])

    @pytest.mark.asyncio
    async def test_write_app_prompt(self, mcp_with_prompts):
        prompts = mcp_with_prompts._prompt_manager._prompts
        result = prompts["isabl_write_app"].fn(app_type="paired")
        text = _text(result[0])
        assert "paired" in text
        assert "get_app_template" in text

    @pytest.mark.asyncio
    async def test_project_report_prompt(self, mcp_with_prompts):
        prompts = mcp_with_prompts._prompt_manager._prompts
        result = prompts["isabl_project_report"].fn(project_id=55)
        text = _text(result[0])
        assert "55" in text
        assert "project_summary" in text

    @pytest.mark.asyncio
    async def test_monitor_analyses_prompt(self, mcp_with_prompts):
        prompts = mcp_with_prompts._prompt_manager._prompts
        result = prompts["isabl_monitor_analyses"].fn(status="FAILED", project_id="102")
        text = _text(result[0])
        assert "FAILED" in text
        assert "102" in text

    @pytest.mark.asyncio
    async def test_merge_results_prompt(self, mcp_with_prompts):
        prompts = mcp_with_prompts._prompt_manager._prompts
        result = prompts["isabl_merge_results"].fn(result_key="vcf")
        assert "vcf" in _text(result[0])

    @pytest.mark.asyncio
    async def test_submit_data_prompt(self, mcp_with_prompts):
        prompts = mcp_with_prompts._prompt_manager._prompts
        result = prompts["isabl_submit_data"].fn(data_type="RNA-seq")
        assert "RNA-seq" in _text(result[0])

    @pytest.mark.asyncio
    async def test_run_pipeline_prompt(self, mcp_with_prompts):
        prompts = mcp_with_prompts._prompt_manager._prompts
        result = prompts["isabl_run_pipeline"].fn(app_name="MUTECT")
        text = _text(result[0])
        assert "MUTECT" in text
        assert "get_apps" in text
