# Signals & Automation (CLI)

Commands and signal integration to trigger or rerun automated workflows from the CLI or web frontend.

## Source Documents

- **Rerun failed asynchronous signals (jobs) selectively** — Documents rerun_signals(filters) which triggers reruns of previously failed signals based on provided filters. This is useful for recovering from transient failures in asynchronous tasks managed by the Isabl signaling system.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/commands.py)
- **Execute signals triggered from the web frontend** — Explains run_web_signals(filters) which runs signals that were initiated via the Isabl frontend, optionally constrained by filters. This bridges frontend-triggered events to backend signal execution for tasks such as reprocessing or manual starts.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/commands.py)
- **Run arbitrary signals on analyses or experiments** — Defines a CLI function to execute arbitrary signals against analyses or experiments by using import strings. The function accepts an endpoint, filter criteria, and a list of signals to run, allowing targeted programmatic triggers inside Isabl.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/commands.py)
- **Signal to resume interrupted analysis executions** — This signal triggers resumption of a previously started analysis, instructing the system to continue execution from its current state. It is intended for use when analyses were paused, failed transiently, or need to be continued without wiping existing results.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/signals.py)
- **Force wipe and restart analysis execution** — This signal forces an analysis to be wiped and restarted from scratch, clearing prior results and re-queuing execution. It's used when a full rerun is required due to corruption, configuration changes, or to ensure reproducibility.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/signals.py)
- **Trigger analysis execution signals via web** — This function emits web-facing signals to trigger analysis execution, with optional flags to restart or force a run. It provides a central entry point so web UI or API calls can request resume, restart, or forced re-execution for an analysis.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/signals.py)
