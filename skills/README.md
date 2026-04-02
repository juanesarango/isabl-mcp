# Isabl Skills

8 guided workflows for common Isabl tasks.

## Which Skill Should I Use?

| I want to... | Use this skill |
|--------------|----------------|
| Create a new bioinformatics pipeline | `/isabl:write-app` |
| Fix a failed analysis | `/isabl:debug-analysis` |
| Query experiments or analyses | `/isabl:query-data` |
| Get project status overview | `/isabl:project-report` |
| Combine results from multiple analyses | `/isabl:merge-results` |
| Add new sequencing data | `/isabl:submit-data` |
| Check what's running/failed | `/isabl:monitor-analyses` |
| Run multiple apps in sequence | `/isabl:run-pipeline` |

## Skills by Role

### For Bioinformaticians
- `/isabl:write-app` — Create AbstractApplication pipelines
- `/isabl:run-pipeline` — Chain multiple apps together
- `/isabl:debug-analysis` — Investigate failures

### For Analysts
- `/isabl:query-data` — Query patterns and filter syntax
- `/isabl:merge-results` — Aggregate results into DataFrames
- `/isabl:project-report` — Generate status reports

### For Both
- `/isabl:submit-data` — Register new sequencing data
- `/isabl:monitor-analyses` — Track analysis status

## Installation

```text
/plugin install github:juanesarango/isabl-mcp
```
