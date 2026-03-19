# Data Management & Import

Tools and patterns to import, register, validate and manage raw and reference data in Isabl.

## Contents

- [Import Engines & Commands](./import-engines-commands/) — High-level import classes and CLI entrypoints for registering experiments and reference assets.
- [File handling & Preprocessing](./file-handling-preprocessing/) — File-level utilities: matching, ownership checks, movement/copying/symlinking, and BED preprocessing/indexing.
- [Storage & Instance Management](./storage-instance-management/) — Helpers to provision storage directories, update storage URLs, and manage analysis storage lifecycle.
- [Reference & BED Management](./reference-bed-management/) — Importing and registering reference genomes and technique BED assets, including compression and indexing for fast queries.
