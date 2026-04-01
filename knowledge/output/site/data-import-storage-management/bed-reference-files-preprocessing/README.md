# BED, Reference Files & Preprocessing

Tools to process BED files (sort/bgzip/tabix), import and register technique/assembly reference data and prepare capture kit resources for pipelines.

## Source Documents

- **Sort, compress and index BED files** — Utility function that sorts a BED file, compresses it with bgzip, and creates a tabix index. It prepares BED files for efficient querying and downstream usage in genomic workflows.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/data.py)
- **Register BED files to technique storage** — Registers targets and baits BED files into a technique's storage directory and updates the technique's data record via the API. It accepts assembly, species and optional description metadata and returns the updated technique object.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/data.py)
- **Local BED importer for techniques with processing** — An importer class for technique BED files that can preprocess BED files (sort, bgzip, tabix) and register them in a technique's storage directory. It offers process_bedfile to prepare the file and import_bedfiles to register targets/baits, assembly and species metadata, and update the technique instance via the API, plus a CLI wrapper.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/data.py)
- **Local reference data importer for assemblies and techniques** — An import engine class used to register reference resources (e.g., reference data files) for an assembly or technique. The class exposes import_data to move or symlink local reference data into Isabl storage and as_cli_command to expose the importer via a Click-based CLI.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/data.py)
- **Local reference genome importer CLI interface** — A minimal import engine specialized for importing a reference genome for an assembly. The class provides an as_cli_command method so the genome importer can be invoked from the command line via Click.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/data.py)
- **Supported Batch Systems for Job Submission** — Describes the batch systems Isabl supports out-of-the-box and how the CLI submits jobs to them. Lists supported systems (LSF, Slurm, SGE) and gives the import strings to reference the submission functions used by isabl_cli.
  [Source](https://docs.isabl.io/batch-systems)
