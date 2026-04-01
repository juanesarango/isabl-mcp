# Automation Signals & Orchestration

Signal-based helpers and invocation logic to resume, force or run web-triggered signals tied to analyses and imports.

## Source Documents

- **Trigger project-level analyses merge process** — Explains a helper that submits or triggers a project-level analyses merge when necessary. The function evaluates an analysis and, if conditions are met, initiates a merge process that consolidates analyses at the project scope.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/data.py)
- **Signal to resume paused or failed analyses** — resume_analysis_signal(analysis) emits a signal to resume execution of an existing analysis that was paused or failed. It is used by the web layer or orchestration code to request re-scheduling without wiping existing outputs.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/signals.py)
- **Signal to wipe analysis and restart execution** — force_analysis_signal(analysis) triggers a hard restart of an analysis by wiping its state and requesting a fresh execution. This signal is intended for cases where outputs or state are corrupted and a full re-run is required.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/signals.py)
- **Trigger analysis execution signals from web interface** — run_web_signals(analysis, restart=False, force=False) centralizes logic for emitting the appropriate execution-related signals based on provided flags. Depending on restart and force booleans it will call resume or force workflows so the web UI or API can request different types of re-runs.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/signals.py)
