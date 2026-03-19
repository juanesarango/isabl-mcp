# Validation & Preconditions

Pre-flight and domain-specific validation hooks to ensure correct inputs, file availability and metadata consistency.

## Source Documents

- **Validate application settings and configuration correctness** — Explains validate_settings which should ensure application settings are correctly configured. Implementations must raise an AssertionError when settings are invalid; the settings argument is an ApplicationSettings object behaving like a dictionary.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Validate target and reference experiment combinations** — Documents validate_experiments which must assert whether a (targets, references) tuple is valid for an application. This prevents nonsensical analyses (e.g., running variant calling on imaging data) by raising AssertionError for invalid combinations.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Validate that experiments have registered BAMs** — validate_bams checks a set of experiments and raises an error if any of them lack a registered BAM file. It's a pre-flight validation step intended to ensure required input files are present before launching analyses.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Validate experiments have required BED files** — validate_bedfiles verifies that each supplied experiment has a registered BED file of a given type (defaulting to 'targets'). It raises an error if any experiment is missing the specified bedfile type, ensuring inputs for interval-based analyses are present.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Validate reference genome presence and indexes** — Checks that the specified reference genome exists in Isabl and that the required index files for downstream tools are present. This validation prevents pipeline runs from starting without the necessary reference assets and will raise an error listing missing or incomplete indexes.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Validate experiments include raw sequencing data** — Verifies that each experiment in the provided list has associated raw data files registered in Isabl (e.g., FASTQ/BAM). If any experiment lacks raw data, the function raises an error to stop downstream processing that depends on input files.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Ensure experiments use a single raw data type** — Confirms that all experiments passed to a workflow contain only one type of raw data (for example, all FASTQ or all BAM files) to avoid mixing incompatible inputs. This check helps ensure that pipelines expecting a uniform input format do not receive heterogeneous file types.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Validate that raw data are FASTQ files only** — Validates that every experiment's raw data is FASTQ format and rejects experiments containing other file types. This is used by fastq-only pipelines to ensure input compatibility and to avoid unintended processing of incompatible file formats.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Validate that targets and references form a pair** — Checks that the provided targets and references are organized as pairs with matching structure (e.g., tuples of target/reference). This ensures that workflows expecting paired inputs receive correctly shaped input and prevents mismatches during pairing operations.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Validate exactly one target sample provided** — Ensures that exactly one target sample is supplied to a command or workflow. This validation is useful for single-sample analyses where multiple targets would be invalid and could cause unintended behavior.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Validate single target and no references passed** — Checks that exactly one target is supplied and that no references are provided in the same command. This is used for commands that operate on a single sample without comparing or pairing it with other samples.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Validate at least one target and one reference present** — Verifies that the invocation includes at least one target and at least one reference, which is necessary for comparative analyses or paired workflows. If either side is empty, the function raises an error to prevent incomplete comparisons.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Ensure targets are not also listed as references** — Confirms that there is no overlap between the targets and references lists, preventing a sample from being used both as the subject and as a reference. This avoids logical errors in comparative workflows and ensures clear separation of roles.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Validate experiments use expected experimental methods** — Verifies that each experiment's declared experimental method matches one of the allowed/expected methods provided. This prevents running pipelines on incompatible experiment types and ensures metadata consistency across analyses.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Validate experiments come from PDX samples only** — Describes a function that checks whether a set of experiments originate from patient-derived xenograft (PDX) samples. It enforces that only PDX sample types are accepted by downstream applications or commands.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Validate experiments contain DNA data only** — Documents a function that ensures a collection of experiments represent DNA-derived data. The validation prevents non-DNA experiments from being passed to DNA-specific analyses or applications.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Validate experiments contain RNA data only** — Explains a function that verifies experiments are RNA-derived before allowing RNA-specific workflows to run. It prevents mismatched data types from entering RNA processing pipelines.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Validate target-reference tuples for DNA pipelines** — Covers a function that validates pairs of target and reference experiments used by DNA analysis applications. It ensures that targets and references are properly structured and appropriate for base DNA workflows (e.g., tumor-normal pairing or other expected pairings).
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Validate targets and references share same bedfile** — Describes a validation function that ensures both targets and references were processed with the same genomic technique manifested as a shared bedfile. This check prevents combining experiments with different capture regions or assay designs.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Validate sequencing platform consistency across samples** — Explains a function that ensures targets and references were sequenced on the same platform. This validation protects analyses from platform-specific biases or incompatibilities when combining data.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Validate experiments match application's species setting** — Documents a function that checks whether the species annotation on experiments matches the expected species configured for the application. It prevents cross-species mix-ups which could break references, annotations, or downstream tools.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Validate experiments are from NORMAL sample type** — Covers a function that enforces that all provided experiments originate from NORMAL samples. The function raises an error if any experiment is not annotated as NORMAL, which is important for analyses that require normal controls.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Validate individual identities for target-reference pairs** — Describes a function that checks individual/sample identity relationships between targets and references. It enforces that pairs are from the same individual for matched pipelines and from different individuals for unmatched pipelines, ensuring correct pairing semantics for analysis.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Validate experiments originate from specific source material** — Explains a function that verifies experiments were derived from a given source material (e.g., blood, tissue, FFPE). It helps enforce that analyses expecting a particular source only receive compatible experiments.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Validate a filesystem path is a file** — validate_is_file checks that a provided path points to a regular file and raises an error otherwise. It is a simple utility intended to guard functions that require file inputs.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Validate a filesystem path is a directory** — validate_is_dir ensures the provided path refers to an existing directory and raises an error if it does not. This utility is used to verify directory inputs for functions that expect folder paths.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Validate experiments use expected experimental methods** — Verifies that each experiment's declared experimental method matches one of the allowed/expected methods provided. This prevents running pipelines on incompatible experiment types and ensures metadata consistency across analyses.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
