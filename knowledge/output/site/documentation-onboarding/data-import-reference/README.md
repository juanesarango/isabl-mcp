# Data & Import Reference

Documentation focused on Isabl's data model and the principles and options for importing and retrieving data.

## Source Documents

- **Data Model: Individuals, Samples, and Experiments** — Explains Isabl's normalized data model where Individuals have Samples and Samples have Experiments, reducing redundancy and improving integrity. The document describes relationships, unique constraints, and provides a database diagram to show how metadata should be registered prior to importing data.
  [Source](https://docs.isabl.io/data-model)
- **Importing Raw Data with Isabl-CLI** — Describes how Isabl-CLI discovers and imports raw data by matching files to registered metadata and moving/symlinking them into a scalable storage layout. It documents supported default raw formats, how to extend formats (EXTRA_RAW_DATA_FORMATS), storage hashing for experiment paths, and explicit YAML-based imports with the relevant CLI flags.
  [Source](https://docs.isabl.io/import-data)
- **Retrieving and Filtering Data from Isabl APIs** — Explains how to use filters to subset and retrieve data from Isabl using the REST API, the CLI, or Python. Provides examples (curl and isabl CLI) showing field-value filters to fetch experiments, file types (e.g., BAM, VCF), and outputs produced by specific applications or statuses.
  [Source](https://docs.isabl.io/retrieve-data)
