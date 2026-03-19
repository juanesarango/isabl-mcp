# Application Framework & Lifecycle

APIs, hooks and helpers to author, validate, run and collect results from Isabl Applications — the metadata-driven analysis units that submit jobs and record tracked analyses.

## Contents

- [Application Interface & Core Lifecycle](./application-interface-core-lifecycle/) — AbstractApplication contract, dependency resolution, command generation and the run orchestration used to create and submit analyses.
- [Results, Artifacts & Post-completion Hooks](./results-artifacts-post-completion-hooks/) — Hooks and helpers to collect per-analysis, per-individual and per-project results, attach logs/scripts, pattern-based result discovery, and to expose results via API.
- [Merging & Aggregation Workflows](./merging-aggregation-workflows/) — Project- and individual-level merge hooks, validation and the logic to create or submit aggregated merge analyses.
- [Validation & Input Guards](./validation-input-guards/) — Rich set of pre-flight checks and validators to ensure correct experiments, sample roles, data types, species, assembly compatibility, bed/bam presence, pairing rules and other constraints before launching analyses.
- [CLI Integration, Artifacts & Notifications](./cli-integration-artifacts-notifications/) — Helpers to expose applications as CLI commands, generate job scripts/log paths, patch status from jobs, send analytics after runs and notify project analysts.
