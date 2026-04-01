# Sample Pairing & Roles

Validators that enforce correct target/reference pairing, single-target constraints and normal/control assignments.

## Source Documents

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
- **Ensure experiments represent NORMAL control samples** — Raises an error if any provided experiments are not labeled as NORMAL samples. This is useful for pipelines that require normal/control samples (e.g., germline or somatic comparisons) to ensure correct sample role assignment.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Validate individual identity across sample pairs** — Checks that target and reference experiments belong to the correct individuals according to pipeline matching rules. For matched pipelines it enforces that pairs come from the same individual; for unmatched pipelines it requires pairs to be from different individuals.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
- **Validate paired DNA targets and reference experiments** — Validates target-reference tuples intended for DNA-based applications. It ensures pairing rules for base DNA pipelines are satisfied (e.g., correct sample roles and compatible metadata) before running paired analyses.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/app.py)
