# Nextflow Single-Cell Alignment Isabl App

This folder contains a scaffold Isabl application class:

- `nextflow_single_cell_alignment_app.py`

It runs a Nextflow pipeline for a single target experiment and records standard
outputs in Isabl.

## What To Customize

Update `application_settings` in `NextflowSingleCellAlignment`:

- `pipeline_path`: path to your `.nf` pipeline entrypoint
- `nextflow_profile`: cluster/runtime profile (`standard`, `slurm`, etc.)
- `nextflow_extra_args`: additional params passed to Nextflow
- `aligned_bam_name` / `aligned_bai_name`: expected output filenames

## Important Notes

- FASTQ input inference comes from `experiment.raw_data` via `_get_fastq_pair()`.
  If your experiment schema differs, replace this method with explicit mapping.
- The command currently uses:
  - `--sample_id`
  - `--outdir`
  - `--fastq_1` and optional `--fastq_2`
  Update these flags to match your Nextflow pipeline.

## Register The App

Add your app class to your Isabl environment's `INSTALLED_APPLICATIONS`, for example:

```python
INSTALLED_APPLICATIONS = [
    "my_apps.nextflow_single_cell_alignment_app.NextflowSingleCellAlignment",
]
```

## Run Pattern

This scaffold is configured as a single-target app (`cli_options = [ii.options.TARGETS]`).
It will create one analysis per target experiment.
