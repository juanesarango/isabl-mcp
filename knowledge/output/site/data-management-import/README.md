# Data Management & Import

Tools and workflows for discovering, importing, registering and organizing raw and reference data in Isabl storage.

## Contents

- [Import Engines & CLI wrappers](./import-engines-cli-wrappers/) — Importer classes and the CLI wrappers that drive bulk and local import operations for experiments, BEDs and reference data.
- [Storage Management](./storage-management/) — Compute and create storage directories, patch instance storage URLs, and register files into instance storage.
- [File Transfer & Linking](./file-transfer-linking/) — Helpers to copy/move/symlink files and expose experiment or analysis outputs into project or delivery directories.
- [BED & Reference File Processing](./bed-reference-file-processing/) — Prepare and register BED and other reference resources (sorting, bgzip, tabix) and commands to register technique-specific resources.
- [Validation & Path Matching](./validation-path-matching/) — Utilities for detecting supported raw file types, matching paths to experiments, ownership/readability checks, regex helpers and per-file annotation hooks.
