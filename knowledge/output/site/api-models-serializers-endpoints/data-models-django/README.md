# Data Models (Django)

Database models representing Individuals, Samples, Experiments, Analyses, Projects and related domain objects.

## Source Documents

- **Aliquot Model: Managing Sample Aliquots** — Django model representing sample aliquots used in Isabl. It inherits from BaseBioModel, includes a foreign key to the Sample model, and enforces uniqueness of (sample, identifier) to uniquely identify aliquots.
  [Source](https://github.com/papaemmelab/isabl_api/blob/master/isabl_api/models/aliquot.py)
- **Analysis Model: Tracking Application Runs and Results** — Defines the Analysis model used to represent instances of Applications run on sequencing objects. It includes links to projects or individuals, relationships to other analyses, targets/references, application type, status lifecycle timestamps, runtime/wait metrics, results as JSON, and permissions for downloading results.
  [Source](https://github.com/papaemmelab/isabl_api/blob/master/isabl_api/models/analysis.py)
- **Application Model: Registering Analytical Tools** — Describes the Application model for registering analysis tools in Isabl, including fields for name, version, linked genome assembly, application_class (executor), configuration (settings), and results specification. Uniqueness is enforced for name/version/assembly and a slug is maintained for instances.
  [Source](https://github.com/papaemmelab/isabl_api/blob/master/isabl_api/models/application.py)
- **Assembly Model: Recording Genome Assemblies** — Simple model for tracking genome assemblies used in Isabl. It stores a unique assembly name (e.g., GRCh37), a reference_data JSON dictionary for assembly assets, and an optional species field to denote origin species.
  [Source](https://github.com/papaemmelab/isabl_api/blob/master/isabl_api/models/assembly.py)
- **TimeStampedModel: Common Created and Modified Fields** — Abstract Django model that provides standard auditing fields (created, modified, created_by) and a bulk update manager. It also includes helper methods to get model names, API create/update/read-only fields, search fields, serializer fields, and absolute URLs.
  [Source](https://github.com/papaemmelab/isabl_api/blob/master/isabl_api/models/base.py)
- **BaseModel: Shared Fields and Utilities for Models** — Abstract BaseModel that extends TimeStampedModel with common fields like notes, storage_url, storage_usage, custom_fields, uuid, and a free-form data JSON. It also supplies methods for readonly/create/update/search field lists, optimized queryset construction, and a clean hook.
  [Source](https://github.com/papaemmelab/isabl_api/blob/master/isabl_api/models/base.py)
- **Abstract model providing unique slug field** — An abstract Django model that provides a single slug field for derived models. It defines convenience methods like __str__, get_readonly_fields, and get_search_fields to standardize how slugged models are represented and searched.
  [Source](https://github.com/papaemmelab/isabl_api/blob/master/isabl_api/models/base.py)
- **Abstract biological base model for entities** — An abstract base class for biological entities (Individual, Sample, Experiment) that centralizes common fields like identifier, system_id and submission. It implements utilities for child relationships, search/create/readonly field lists, and auto-creates a system_id on first save while avoiding force_insert issues.
  [Source](https://github.com/papaemmelab/isabl_api/blob/master/isabl_api/models/base.py)
- **CustomField model for extensible metadata fields** — Model that registers user-defined custom fields for supported models. It stores target model name, field_name (validated for format), optional verbose_name, and a configuration JSON blob; uniqueness is enforced per model+field_name and a clean() method validates entries.
  [Source](https://github.com/papaemmelab/isabl_api/blob/master/isabl_api/models/base.py)
- **Center model tracking sample generating centers** — A simple model for tracking centers (institutions) where data are generated. It inherits BaseSlugModel and stores name and acronym with a uniqueness constraint on the pair and an index on the slug.
  [Source](https://github.com/papaemmelab/isabl_api/blob/master/isabl_api/models/center.py)
- **Client settings model with JSON preferences** — Model for storing client-specific unstructured settings using a JSONField and a slug identifier. It is timestamped and includes a clean() method for validation of the slug or settings as needed.
  [Source](https://github.com/papaemmelab/isabl_api/blob/master/isabl_api/models/client.py)
- **Disease model for tracking disease metadata** — A lightweight model for tracking diseases that stores a disease name and an acronym. It inherits BaseSlugModel, enforces uniqueness between name and acronym, and adds an index on the slug for quick lookups.
  [Source](https://github.com/papaemmelab/isabl_api/blob/master/isabl_api/models/disease.py)
- **Experiment model managing experimental data objects** — Model for representing experimental data, linking Sample/Aliquot, Technique, Platform, Center and Projects. It includes JSON fields for raw_data, results and bam_files, enforces uniqueness over sample/aliquot/technique/identifier, and provides helper methods for obtaining the related individual, optimizing querysets, analytics retrieval, and caching analytics metadata.
  [Source](https://github.com/papaemmelab/isabl_api/blob/master/isabl_api/models/experiment.py)
- **Group model tracking organizational groups or teams** — A minimal model to represent groups/teams with name and acronym fields that inherits BaseSlugModel. The model enforces uniqueness of the name/acronym pair and indexes the slug for efficient lookups.
  [Source](https://github.com/papaemmelab/isabl_api/blob/master/isabl_api/models/group.py)
- **Individual model representing organisms or patients** — Top-level biological entity model used to represent organisms (patients, mice, etc.) that includes fields like center, species, gender, and birth_year. It inherits BaseBioModel, enforces uniqueness on species/center/identifier, indexes those fields, and documents PHI handling and an example to change primary key sequence start.
  [Source](https://github.com/papaemmelab/isabl_api/blob/master/isabl_api/models/individual.py)
- **Platform model for experimental sequencing platforms** — Model for describing experimental platforms via manufacturer, system and version fields. It inherits BaseSlugModel and enforces uniqueness across the manufacturer/system/version triplet while indexing those fields for efficient lookups.
  [Source](https://github.com/papaemmelab/isabl_api/blob/master/isabl_api/models/platform.py)
- **User preferences model for Isabl API** — Defines a simple TimeStampedModel used to store per-user preferences. Key fields include a OneToOne created_by reference to the user and an unstructured JSONField called preferences. The model exposes helper methods for checking superuser status and retrieving permissions and groups.
  [Source](https://github.com/papaemmelab/isabl_api/blob/master/isabl_api/models/preferences.py)
- **Project model for managing studies** — Describes the Project model used to manage study metadata and access in Isabl. It includes descriptive fields (title, description), contact emails (principal_investigator, owner, analyst, coordinator), organizational links (group), and a JSONField to manage sharing settings. The model also defines a custom permission allowing users to see all projects.
  [Source](https://github.com/papaemmelab/isabl_api/blob/master/isabl_api/models/project.py)
- **Sample model for biological sample management** — Defines the Sample model (inherits BaseBioModel) used to record biospecimen information. Important fields include a foreign key to Individual, optional disease link, a required category, and collection_days with validation. The model enforces uniqueness and indexing across (individual, category, identifier) to avoid duplicate sample records.
  [Source](https://github.com/papaemmelab/isabl_api/blob/master/isabl_api/models/sample.py)
- **Automation signal tracking model and fields** — A compact BaseSlugModel used to track automation signals in Isabl. It records an import_string, the target_endpoint (schema/type), and target_id (instance identifier), and enforces uniqueness across these three fields. The model includes an index on slug and exposes a failure_traceback method to inspect signal errors.
  [Source](https://github.com/papaemmelab/isabl_api/blob/master/isabl_api/models/signal.py)
- **Bulk submission model for Excel-based imports** — Model designed to support bulk creation of instances from an uploaded Excel submission form. It tracks a short description, processed timestamp, associated projects (ManyToMany), result file path, and the uploaded submission_form which is validated. The model is intended to record both the input form and the outcomes of processing.
  [Source](https://github.com/papaemmelab/isabl_api/blob/master/isabl_api/models/submission.py)
- **Sequencing Technique model with reference data** — Represents sequencing or experimental techniques as a BaseSlugModel with method, name, and category fields. It also contains a reference_data JSONField for attaching reference assets or metadata. The model enforces uniqueness on (method, name) and indexes the pair for efficient lookup.
  [Source](https://github.com/papaemmelab/isabl_api/blob/master/isabl_api/models/technique.py)
