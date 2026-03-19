# Validation & Input Guards

Rich set of pre-flight checks and validators to ensure correct experiments, sample roles, data types, species, assembly compatibility, bed/bam presence, pairing rules and other constraints before launching analyses.

## Source Documents

- **Validate application settings and configuration** — validate_settings should assert that application settings are correctly configured and raise an AssertionError when misconfigured. It receives an ApplicationSettings object (Munch-like) and is used to fail fast if required parameters or resources are missing.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Validate target and reference experiment combinations** — validate_experiments enforces that the combination of target and reference experiments makes sense for the application and should raise an AssertionError if not. This prevents nonsensical analyses (for example, running variant calling on imaging experiments) by using metadata-driven rules.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Validate experiments have registered BAMs** — validate_bams(experiments) checks that every experiment in the provided list has a registered BAM and raises an error if any are missing. It is intended as a pre-flight check before launching analyses that require BAM inputs.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Validate experiments have required BED files** — validate_bedfiles(experiments, bedfile_type='targets') verifies that each experiment has a registered BED file of the specified type (defaults to 'targets') and raises an error if any are missing. This ensures required interval definitions are present before analyses that depend on them.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Validate a given filesystem path is a file** — validate_is_file(path) checks that the provided path exists and is a regular file, raising an error if not. This utility is used to validate input files before attempting file-based operations within the CLI or pipeline.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Validate a given filesystem path is a directory** — validate_is_dir(path) ensures the supplied path exists and is a directory, raising an error otherwise. It is a helper used to confirm directory inputs (e.g., output folders) are present and correct before operations proceed.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Validate existence and indexes of reference genome** — Checks that a named reference genome exists in the Isabl environment and that the genome has the index files required by downstream pipelines. This validation is performed before launching analyses to ensure aligners and other tools have the necessary index artifacts available.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Ensure experiments contain raw sequencing data** — Validates that provided experiment records include raw data files before any processing steps are started. It prevents submitting experiments without raw inputs, avoiding wasted compute and confusing failures later in the pipeline.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Require experiments to contain single data type** — Ensures that all raw data for the supplied experiments are of the same data type (for example, all FASTQ or all BAM) so that a single pipeline can be selected and executed. This avoids mixing incompatible input types in a single job submission.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Confirm raw data are FASTQ files only** — Validates that the raw data associated with the given experiments are exclusively FASTQ files. This check is intended for tools and workflows that require FASTQ input and will block runs if other file types are present.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Validate that targets and references form a pair** — Checks that the provided targets and references represent paired entries (e.g., an equal-length tuple or matched pairing) required for pairwise analyses. This ensures correctness for workflows that compare each target to a corresponding reference.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Enforce exactly one target sample provided** — Validates that the targets list contains exactly one sample, which is necessary for single-sample workflows or commands that operate on a single target. It prevents accidental multi-sample submissions to commands that expect a single input.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **One target allowed and no references present** — Ensures that exactly one target is provided and that no references have been passed alongside it. This validation is used for single-sample analyses that must not include any reference samples in the same request.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Require at least one target and one reference sample** — Validates that the request includes at least one target and at least one reference sample, a common prerequisite for comparative or differential analyses. This check prevents running pairwise or comparative workflows without sufficient samples.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Ensure targets are not duplicated as references** — Checks that no sample listed as a target is also included among references to avoid self-comparisons and logical errors in analysis. This guard prevents confusing or invalid analyses where the same sample would be compared to itself.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Validate experimental methods against expected list** — Verifies that the experimental method(s) associated with experiments match the set of methods allowed or expected by the pipeline or command. This ensures that only compatible experimental techniques are submitted for a given analysis.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Validate experiments are PDX-derived samples** — Checks that the provided experiments originate from patient-derived xenograft (PDX) samples. Intended to block workflows that require PDX material from running on non-PDX experiments by validating sample metadata.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Validate experiments contain DNA sequencing data** — Ensures the list of experiments supplied represent DNA-derived assays. Use this to guard DNA-only applications so non-DNA experiments (e.g., RNA-seq) are rejected before execution.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Validate experiments contain RNA sequencing data** — Verifies that the provided experiments are RNA-based assays. This prevents RNA-specific workflows from being run with non-RNA inputs by checking experiment metadata and raising errors on mismatches.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Validate paired DNA targets and reference experiments** — Validates target-reference tuples intended for DNA-based applications. It ensures pairing rules for base DNA pipelines are satisfied (e.g., correct sample roles and compatible metadata) before running paired analyses.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Validate targets and references share same technique** — Checks that target and reference experiments use the same technique, typically by comparing bedfiles or assay-specific configurations. This prevents combining experiments with incompatible capture/assay designs that would invalidate downstream comparisons.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Validate experiments sequenced on same platform** — Ensures that the target and reference experiments were sequenced on the same sequencing platform. This validation helps avoid platform-induced biases in comparative analyses by rejecting cross-platform pairings.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Validate experiments match application's species** — Verifies that all experiments are from the species expected by the application configuration. This prevents running species-specific pipelines (human, mouse, etc.) on incompatible species datasets by validating experiment species metadata.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Ensure experiments represent NORMAL control samples** — Raises an error if any provided experiments are not labeled as NORMAL samples. This is useful for pipelines that require normal/control samples (e.g., germline or somatic comparisons) to ensure correct sample role assignment.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Validate individual identity across sample pairs** — Checks that target and reference experiments belong to the correct individuals according to pipeline matching rules. For matched pipelines it enforces that pairs come from the same individual; for unmatched pipelines it requires pairs to be from different individuals.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Validate experiments originate from specific source material** — Ensures experiments come from a particular source material specified by the application (e.g., blood, tissue, FFPE). This validation prevents running source-specific workflows on samples from the wrong source by checking sample metadata.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
