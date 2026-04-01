"""Example Isabl app that runs a Nextflow single-cell alignment pipeline."""

from __future__ import annotations

from typing import Any, Iterable, Optional

import isabl_cli as ii


class NextflowSingleCellAlignment(ii.AbstractApplication):
    """
    Run a Nextflow single-cell alignment workflow for one target experiment.

    This is a scaffold app intended to be customized for your local Nextflow
    pipeline interface (params/profile/container setup).
    """

    NAME = "nextflow_single_cell_alignment"
    VERSION = "0.1.0"
    SPECIES = "HUMAN"

    cli_help = "Run Nextflow single-cell alignment on one target experiment."
    cli_options = [ii.options.TARGETS]

    # Keep settings editable from the Isabl database.
    application_settings = {
        "nextflow_bin": "nextflow",
        "pipeline_path": "/path/to/your/single_cell_alignment.nf",
        "nextflow_profile": "standard",
        "nextflow_extra_args": "",
        # Optional output file name conventions produced by your pipeline.
        "aligned_bam_name": "aligned.bam",
        "aligned_bai_name": "aligned.bam.bai",
    }

    application_results = {
        "aligned_bam": {
            "frontend_type": "bam",
            "description": "Aligned single-cell BAM file.",
            "verbose_name": "Aligned BAM",
        },
        "aligned_bai": {
            "frontend_type": "text-file",
            "description": "Index for aligned BAM.",
            "verbose_name": "Aligned BAI",
        },
        "command_log": {
            "frontend_type": "ansi",
            "description": "Command output log.",
            "verbose_name": "Command Log",
        },
    }

    def validate_experiments(self, targets, references):
        """Validate target experiment selection for this app."""
        assert len(targets) == 1, "This app requires exactly one target experiment."
        assert not references, "This app does not use reference experiments."

    @staticmethod
    def _extract_urls_from_value(value: Any) -> Iterable[str]:
        """Recursively collect path-like values from experiment raw_data."""
        if isinstance(value, str):
            yield value
            return
        if isinstance(value, dict):
            url = value.get("url")
            if isinstance(url, str):
                yield url
            for nested in value.values():
                yield from NextflowSingleCellAlignment._extract_urls_from_value(nested)
            return
        if isinstance(value, list):
            for item in value:
                yield from NextflowSingleCellAlignment._extract_urls_from_value(item)

    def _get_fastq_pair(self, experiment: Any) -> tuple[Optional[str], Optional[str]]:
        """
        Try to infer R1/R2 FASTQ files from experiment.raw_data.

        If your data model differs, replace this method with your own mapping.
        """
        raw_data = getattr(experiment, "raw_data", {}) or {}
        all_urls = [u for u in self._extract_urls_from_value(raw_data) if "fastq" in u.lower()]

        r1 = next((u for u in all_urls if "_R1" in u or ".R1" in u or "_1.fastq" in u), None)
        r2 = next((u for u in all_urls if "_R2" in u or ".R2" in u or "_2.fastq" in u), None)

        if not r1 and all_urls:
            r1 = all_urls[0]
        return r1, r2

    def get_command(self, analysis, inputs, settings):
        """Build shell command that executes the Nextflow workflow."""
        target = analysis.targets[0]
        sample_id = getattr(target, "system_id", str(target.pk))
        outdir = analysis.storage_url

        fastq_1, fastq_2 = self._get_fastq_pair(target)
        assert fastq_1, (
            "Could not infer FASTQ input from experiment.raw_data. "
            "Customize _get_fastq_pair() for your data schema."
        )

        fastq_args = f"--fastq_1 '{fastq_1}'"
        if fastq_2:
            fastq_args += f" --fastq_2 '{fastq_2}'"

        return f"""
set -euo pipefail

{settings.nextflow_bin} run "{settings.pipeline_path}" \\
  -profile "{settings.nextflow_profile}" \\
  --sample_id "{sample_id}" \\
  --outdir "{outdir}" \\
  {fastq_args} \\
  {settings.nextflow_extra_args} \\
  -with-report "{outdir}/nextflow_report.html" \\
  -with-trace "{outdir}/nextflow_trace.txt" \\
  -with-timeline "{outdir}/nextflow_timeline.html" \\
  -with-dag "{outdir}/nextflow_dag.html"
""".strip()

    def get_analysis_results(self, analysis):
        """Return output artifacts recorded in Isabl for completed analyses."""
        storage_url = analysis.storage_url
        return {
            "aligned_bam": f"{storage_url}/{self.settings.aligned_bam_name}",
            "aligned_bai": f"{storage_url}/{self.settings.aligned_bai_name}",
            "command_log": f"{storage_url}/head_job.log",
        }
