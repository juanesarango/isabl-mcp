# Data Import & Storage Management

Tools and import engines to associate raw files with experiments, register reference resources (BEDs, genomes), create storage directories, symlink/move files, and validate ownership/readability.

## Contents

- [Importers & Import Workflows](./importers-import-workflows/) — Local import engines and batch import features to discover, match and commit raw files to experiments and to register reference resources for assemblies/techniques.
- [File Operations, Linking & Delivery](./file-operations-linking-delivery/) — Filesystem operations used during import and delivery: symlinks, copying, moving, symlinking experiments into project directories and exposing analysis outputs to targets.
- [Storage Directories & Path Management](./storage-directories-path-management/) — Helpers to compute and create hashed or structured storage directories, claim storage URLs for instances, update storage metadata and to soft-delete or trash analysis storage.
- [BED, Reference Files & Preprocessing](./bed-reference-files-preprocessing/) — Tools to process BED files (sort/bgzip/tabix), import and register technique/assembly reference data and prepare capture kit resources for pipelines.
- [Validation During Import](./validation-during-import/) — Checks performed by importers such as file-type detection, ownership/readability assertions and raw-data inspection for matching and QC.
