# Assay, Platform & Species Checks

Validators for experimental method compatibility, platform matching, species constraints and source material checks (PDX, DNA/RNA).

## Source Documents

- **Validate experimental methods against expected list** — Verifies that the experimental method(s) associated with experiments match the set of methods allowed or expected by the pipeline or command. This ensures that only compatible experimental techniques are submitted for a given analysis.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Validate experiments are PDX-derived samples** — Checks that the provided experiments originate from patient-derived xenograft (PDX) samples. Intended to block workflows that require PDX material from running on non-PDX experiments by validating sample metadata.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Validate experiments contain DNA sequencing data** — Ensures the list of experiments supplied represent DNA-derived assays. Use this to guard DNA-only applications so non-DNA experiments (e.g., RNA-seq) are rejected before execution.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Validate experiments contain RNA sequencing data** — Verifies that the provided experiments are RNA-based assays. This prevents RNA-specific workflows from being run with non-RNA inputs by checking experiment metadata and raising errors on mismatches.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Validate targets and references share same technique** — Checks that target and reference experiments use the same technique, typically by comparing bedfiles or assay-specific configurations. This prevents combining experiments with incompatible capture/assay designs that would invalidate downstream comparisons.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Validate experiments sequenced on same platform** — Ensures that the target and reference experiments were sequenced on the same sequencing platform. This validation helps avoid platform-induced biases in comparative analyses by rejecting cross-platform pairings.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Validate experiments match application's species** — Verifies that all experiments are from the species expected by the application configuration. This prevents running species-specific pipelines (human, mouse, etc.) on incompatible species datasets by validating experiment species metadata.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Validate experiments originate from specific source material** — Ensures experiments come from a particular source material specified by the application (e.g., blood, tissue, FFPE). This validation prevents running source-specific workflows on samples from the wrong source by checking sample metadata.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
