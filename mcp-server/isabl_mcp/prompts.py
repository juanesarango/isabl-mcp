"""MCP Prompts for the Isabl MCP Server.

Prompts are pre-built templates that guide the AI through common Isabl workflows.
They appear as selectable options in MCP clients (Cursor, Claude Code, etc.).
"""

from __future__ import annotations

from typing import Optional

from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts.base import Message, UserMessage, AssistantMessage


def register_prompts(mcp: FastMCP) -> None:
    """Register all Isabl prompts with the MCP server."""

    @mcp.prompt()
    def isabl_debug_analysis(analysis_id: int) -> list[Message]:
        """Debug a failed Isabl analysis step by step."""
        return [
            UserMessage(f"""Debug Isabl analysis {analysis_id}. Work through these steps:

1. Get analysis details: use isabl_query to fetch the analysis (endpoint="analyses", filters={{"pk": {analysis_id}}}) — check status, application name, targets
2. Read the error logs: use isabl_get_logs({analysis_id}, log_type="stderr") to see what went wrong
3. Read the command script: use isabl_get_logs({analysis_id}, log_type="script") to see what was executed
4. Check if input data exists: look at the target experiments and verify paths
5. Check dependencies: if the app depends on upstream analyses, verify those succeeded
6. Identify the root cause from the logs
7. Suggest a fix (re-run with --force, fix settings, fix input data, etc.)

Common error patterns:
- "File not found" → input path incorrect or missing
- "Permission denied" → storage directory permissions
- "Command not found" → tool_path setting is wrong
- "Memory allocation" → job needs more memory
- "Timeout" → job exceeded time limit"""),
        ]

    @mcp.prompt()
    def isabl_query_data(
        entity_type: str = "experiments",
        project_id: Optional[str] = None,
    ) -> list[Message]:
        """Query data from the Isabl API."""
        project_filter = ""
        if project_id:
            project_filter = f', filters={{"projects": {project_id}}}'

        return [
            UserMessage(f"""Help me query {entity_type} from Isabl.

Use the isabl_query tool to search. Available endpoints: experiments, analyses, projects, individuals, samples, applications, techniques.

Start with:
  isabl_query(endpoint="{entity_type}"{project_filter}, output_fields=["system_id", "status"])

Common filter patterns:
- By project: {{"projects": 102}}
- By status: {{"status": "FAILED"}}
- By application: {{"application__name": "MUTECT"}}
- By date: {{"created__gte": "2024-01-01"}}
- By technique: {{"technique__method": "WGS"}}

When showing IDs, prefer system_id over pk for readability."""),
        ]

    @mcp.prompt()
    def isabl_write_app(
        app_type: str = "single",
    ) -> list[Message]:
        """Guide through creating a new Isabl application."""
        return [
            UserMessage(f"""Help me create a new Isabl bioinformatics application ({app_type} sample analysis).

Steps:
1. First, use get_app_template("{app_type}") to get the boilerplate code
2. Then customize it by working through each method:
   - Define NAME, VERSION, ASSEMBLY, SPECIES
   - Choose cli_options (TARGETS for single, PAIRS for tumor-normal)
   - Define application_settings (tool paths, threads, memory)
   - Implement validate_experiments() to check input validity
   - Implement get_dependencies() if it depends on upstream results
   - Implement get_command() to generate the shell command
   - Implement get_analysis_results() to map output files
3. Register in INSTALLED_APPLICATIONS
4. Write tests

Also use search_knowledge("AbstractApplication") to find relevant documentation."""),
        ]

    @mcp.prompt()
    def isabl_project_report(project_id: int) -> list[Message]:
        """Generate a status report for an Isabl project."""
        return [
            UserMessage(f"""Generate a comprehensive status report for Isabl project {project_id}.

1. Use project_summary({project_id}) to get overall statistics
2. Use isabl_query("analyses", {{"targets__projects": {project_id}, "status": "FAILED"}}) to find failures
3. Use isabl_query("experiments", {{"projects": {project_id}}}, output_fields=["system_id", "technique.method"]) to break down by technique
4. Summarize:
   - Total experiments and their techniques
   - Analysis status breakdown (succeeded, failed, running, pending)
   - Which applications have been run
   - Any failed analyses that need attention
   - Storage usage"""),
        ]

    @mcp.prompt()
    def isabl_monitor_analyses(
        project_id: Optional[str] = None,
        status: str = "STARTED",
    ) -> list[Message]:
        """Monitor and track analysis status."""
        filters = f'"status": "{status}"'
        if project_id:
            filters += f', "targets__projects": {project_id}'

        return [
            UserMessage(f"""Monitor Isabl analyses with status {status}.

1. Query current analyses:
   isabl_query("analyses", {{{filters}}}, output_fields=["pk", "application.name", "status", "targets"])

2. For any FAILED analyses, check their logs:
   isabl_get_logs(analysis_id, log_type="stderr", tail_lines=20)

3. For STARTED analyses that seem stuck, check how long they've been running

4. Summarize:
   - How many analyses in each status
   - Any failures that need attention
   - Any stuck jobs (STARTED for too long)
   - Suggested actions for each issue"""),
        ]

    @mcp.prompt()
    def isabl_merge_results(
        result_key: str = "tsv",
    ) -> list[Message]:
        """Aggregate results from multiple analyses."""
        return [
            UserMessage(f"""Help me merge "{result_key}" results from multiple Isabl analyses.

Steps:
1. First, identify the analyses to merge. Ask me which project or analyses to use.
2. Query the analyses:
   isabl_query("analyses", filters, output_fields=["pk", "application.name", "status"])
3. Use merge_results(analysis_ids, "{result_key}") to collect the file paths
4. If output_format="preview", show the first few lines of each file
5. Suggest how to combine them (e.g., pandas concat for TSVs, bcftools merge for VCFs)"""),
        ]

    @mcp.prompt()
    def isabl_submit_data(
        data_type: str = "WGS",
    ) -> list[Message]:
        """Submit new sequencing data to Isabl."""
        return [
            UserMessage(f"""Help me submit new {data_type} sequencing data to Isabl.

The Isabl data model hierarchy is:
  Individual (patient) → Sample (tissue) → Experiment (sequencing run)

Steps:
1. Search for existing individuals/samples first to avoid duplicates:
   isabl_query("individuals", {{"identifier": "PATIENT_ID"}})
2. Create individual if needed (via isabl_cli or API)
3. Create sample linked to the individual
4. Create experiment with the FASTQ/BAM file paths
5. Verify the submission:
   isabl_get_tree("INDIVIDUAL_ID")

Use search_knowledge("submit data") for detailed documentation."""),
        ]

    @mcp.prompt()
    def isabl_run_pipeline(
        app_name: Optional[str] = None,
    ) -> list[Message]:
        """Run an Isabl application pipeline on experiments."""
        app_search = ""
        if app_name:
            app_search = f'\n2. Search for the app: get_apps("{app_name}", detailed=True)'

        return [
            UserMessage(f"""Help me run an Isabl pipeline on my experiments.

Steps:
1. Identify target experiments:
   isabl_query("experiments", {{"projects": PROJECT_ID}}, output_fields=["system_id", "technique.method"]){app_search}
3. Use search_knowledge("run pipeline") to understand the submission process
4. The typical CLI command pattern is:
   isabl APP_NAME --targets EXPERIMENT_IDS --commit

For paired analyses (tumor-normal):
   isabl APP_NAME --pairs TUMOR_ID NORMAL_ID --commit

5. After submission, monitor with:
   isabl_query("analyses", {{"status": "STARTED"}})"""),
        ]
