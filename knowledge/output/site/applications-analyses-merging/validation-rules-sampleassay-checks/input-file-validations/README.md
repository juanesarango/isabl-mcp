# Input & File Validations

Checks that required files, reference indexes and raw inputs exist and match expected formats.

## Source Documents

- **Validate a given filesystem path is a file** — validate_is_file(path) checks that the provided path exists and is a regular file, raising an error if not. This utility is used to validate input files before attempting file-based operations within the CLI or pipeline.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Validate a given filesystem path is a directory** — validate_is_dir(path) ensures the supplied path exists and is a directory, raising an error otherwise. It is a helper used to confirm directory inputs (e.g., output folders) are present and correct before operations proceed.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Validate existence and indexes of reference genome** — Checks that a named reference genome exists in the Isabl environment and that the genome has the index files required by downstream pipelines. This validation is performed before launching analyses to ensure aligners and other tools have the necessary index artifacts available.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Ensure experiments contain raw sequencing data** — Validates that provided experiment records include raw data files before any processing steps are started. It prevents submitting experiments without raw inputs, avoiding wasted compute and confusing failures later in the pipeline.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Confirm raw data are FASTQ files only** — Validates that the raw data associated with the given experiments are exclusively FASTQ files. This check is intended for tools and workflows that require FASTQ input and will block runs if other file types are present.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Require experiments to contain single data type** — Ensures that all raw data for the supplied experiments are of the same data type (for example, all FASTQ or all BAM) so that a single pipeline can be selected and executed. This avoids mixing incompatible input types in a single job submission.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Validate experiments have registered BAMs** — validate_bams(experiments) checks that every experiment in the provided list has a registered BAM and raises an error if any are missing. It is intended as a pre-flight check before launching analyses that require BAM inputs.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Validate experiments have required BED files** — validate_bedfiles(experiments, bedfile_type='targets') verifies that each experiment has a registered BED file of the specified type (defaults to 'targets') and raises an error if any are missing. This ensures required interval definitions are present before analyses that depend on them.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
