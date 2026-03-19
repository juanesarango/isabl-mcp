# Serializers

DRF serializers exposing model fields and specialized result/notification payloads used by the API and frontend.

## Source Documents

- **Serializer for project sharing permissions and flags** — A DRF serializer that models project sharing settings. It exposes can_read and can_share as lists of email addresses and an is_public boolean indicating whether the project and its results are publicly accessible. The serializer enforces email field types for entries in the user lists.
  [Source](https://github.com/papaemmelab/isabl_api/blob/master/isabl_api/serializers.py)
- **Serializer to control submission processing commit** — A minimal serializer that controls whether processing of a submission should commit the produced actions. It exposes a single boolean field commit with a default of False. This is intended to allow dry-run versus commit control when processing uploaded submission forms.
  [Source](https://github.com/papaemmelab/isabl_api/blob/master/isabl_api/serializers.py)
- **Bulk update serializer for analysis status and runner** — Serializer used to update multiple analysis records in bulk. It requires a status choice (STAGED or SUBMITTED), a list of analysis ids, and the ran_by field to capture the Linux user who executed the analyses. This standardizes the payload for bulk state transitions and audit information.
  [Source](https://github.com/papaemmelab/isabl_api/blob/master/isabl_api/serializers.py)
- **Serializer to register and configure Django validators** — Serializer that accepts a validator class (restricted to django.core.validators via a custom validator) and a dictionary of keyword arguments to configure it. Its Meta declares a validators list that references a builder function for the validator. This enables API-driven registration or configuration of Django validators.
  [Source](https://github.com/papaemmelab/isabl_api/blob/master/isabl_api/serializers.py)
- **Serializer for configuring custom model fields** — Defines the schema and validation for custom field configurations exposed via the API. Covers options like whether the field is used in submissions, the DRF field class to use, keyword arguments passed to the field, and custom validators applied to the field configuration.
  [Source](https://github.com/papaemmelab/isabl_api/blob/master/isabl_api/serializers.py)
- **Serializer for raw input file metadata** — Represents raw data files in API requests and responses, including the file URL, declared file type, auxiliary file metadata (e.g., PU, LB, PL for FASTQ), and optional checksum information. It standardizes how raw inputs are described so downstream processing can locate and verify files.
  [Source](https://github.com/papaemmelab/isabl_api/blob/master/isabl_api/serializers.py)
- **Serializer for reference data entries and URLs** — Provides a minimal serializer for reference data objects: a URL and an optional description. It standardizes how reference resources (e.g., genome FASTA, annotation files) are supplied in API payloads.
  [Source](https://github.com/papaemmelab/isabl_api/blob/master/isabl_api/serializers.py)
- **Serializer linking BAM files to analyses** — Describes BAM file resources via a URL and the primary key of the analysis that produced them. This serializer ties file locations to provenance by referencing the generating analysis record.
  [Source](https://github.com/papaemmelab/isabl_api/blob/master/isabl_api/serializers.py)
- **Serializer for analysis result metadata and UI hints** — Encodes result metadata consumed by both backend and frontend, including presentation type, verbose name, description, external links, optional flags, display logo/hiding options, ordering, and arbitrary JSON data. It is used to declare renderable results and control frontend rendering behavior.
  [Source](https://github.com/papaemmelab/isabl_api/blob/master/isabl_api/serializers.py)
- **Base model serializer with Isabl query fields** — A base serializer combining IsablQueryFieldsMixin with DRF's ModelSerializer to provide common query-related fields and behavior. Declares a pk field (optional) and is used as a foundation for model-specific serializers in the codebase.
  [Source](https://github.com/papaemmelab/isabl_api/blob/master/isabl_api/serializers.py)
- **Serializer for Tag objects and name management** — Implements a Tag serializer based on the base ModelSerializer, exposing the tag name and primary key. The Meta disables default validators on some fields to allow name updates and custom validation behavior.
  [Source](https://github.com/papaemmelab/isabl_api/blob/master/isabl_api/serializers.py)
- **Serializer exposing core user profile fields** — Provides a concise user serializer exposing first and last name, username, email, and primary key. It is intended for user listings and simple profile interactions within Isabl's API.
  [Source](https://github.com/papaemmelab/isabl_api/blob/master/isabl_api/serializers.py)
- **Serializer for user preferences and permissions** — Represents a user's preferences object along with group membership, permission lists, and a boolean is_superuser flag. Preferences are handled as JSON, while permissions and groups are lists — this serializer is used to read and update user-specific settings and access data.
  [Source](https://github.com/papaemmelab/isabl_api/blob/master/isabl_api/serializers.py)
- **Extended user details serializer including preferences** — Extends the base UserDetailsSerializer to include the user's preferences and basic profile fields. The serializer marks email as read-only and embeds PreferencesSerializer for the preferences attribute to present consolidated user information.
  [Source](https://github.com/papaemmelab/isabl_api/blob/master/isabl_api/serializers.py)
- **CustomRegisterSerializer adding first and last names** — Defines a registration serializer that extends RegisterSerializer by adding first_name and last_name fields. Both fields are CharFields with max_length 100 and no extra validators declared. This serializer is intended to capture basic user identity during registration flows.
  [Source](https://github.com/papaemmelab/isabl_api/blob/master/isabl_api/serializers.py)
- **Password reset serializer with email field** — A simple serializer for initiating password resets. It declares an email EmailField and references a password_reset_form_class (PasswordResetForm) used to handle validation/processing. The serializer inherits directly from serializers.Serializer rather than a model serializer.
  [Source](https://github.com/papaemmelab/isabl_api/blob/master/isabl_api/serializers.py)
- **Base Isabl model serializer with common fields** — Base ModelSerializer used across Isabl API resources that standardizes common fields and behavior. Declared fields include tags (TagSerializer, allow_null), data (JSONField), custom_fields (CustomFieldsField), and created_by (SlugRelatedField defaulting to current user). The Meta model is left as None and concrete serializers set their model and fields.
  [Source](https://github.com/papaemmelab/isabl_api/blob/master/isabl_api/serializers.py)
- **Client serializer including slug and settings** — Serializer for Client model that inherits from IsablSerializer and pulls its fields from models.Client.get_serializer_fields(). It explicitly declares a slug SlugField (unique identifier help_text) and a settings JSONField with a default empty dict. The Meta sets model to models.Client and uses model-driven field definitions.
  [Source](https://github.com/papaemmelab/isabl_api/blob/master/isabl_api/serializers.py)
- **Custom field serializer with configuration nested** — Serializer for CustomField model extending IsablSerializer and exposing model-defined fields plus a non-model nested configuration serializer. The Meta declares read_only_fields and fields via model helper methods and lists 'configuration' as a non-model serializer. The declared configuration field uses CustomFieldConfigurationSerializer.
  [Source](https://github.com/papaemmelab/isabl_api/blob/master/isabl_api/serializers.py)
- **Assembly serializer with species and reference data** — Serializer for Assembly model that includes assembly-specific fields and a non-model reference_data field. Meta pulls read-only fields and serializer fields from the model and declares 'reference_data' as a non-model serializer. Declared fields include name, species (ChoiceField using lazy_choices('species')), and reference_data as a DictField of reference assets.
  [Source](https://github.com/papaemmelab/isabl_api/blob/master/isabl_api/serializers.py)
- **Platform serializer delegating to model fields** — Serializer for the Platform model that inherits common IsablSerializer behavior and obtains its read-only and serializable fields from models.Platform helper methods. No additional custom fields are declared in the serializer file itself. The Meta configuration centralizes field selection to the model.
  [Source](https://github.com/papaemmelab/isabl_api/blob/master/isabl_api/serializers.py)
- **Center serializer mapping model-defined fields** — CenterSerializer maps the Center model into API representations by inheriting IsablSerializer and using model-provided field lists. The serializer does not declare extra fields itself; Meta uses models.Center.get_serializer_fields() and get_readonly_fields() to configure output. This centralizes field definitions in the model.
  [Source](https://github.com/papaemmelab/isabl_api/blob/master/isabl_api/serializers.py)
- **Signal serializer using model-provided fields** — Serializer for the Signal model that inherits common IsablSerializer behavior and relies on model helper methods for field and read-only configuration. No extra fields are declared in this snippet. The Meta ties the serializer to models.Signal and uses centralized model definitions.
  [Source](https://github.com/papaemmelab/isabl_api/blob/master/isabl_api/serializers.py)
- **Disease serializer exposing model fields and readonlys** — DiseaseSerializer provides API serialization for the Disease model by inheriting from IsablSerializer and pulling field lists from the model's helper functions. The serializer itself does not define additional fields in this excerpt; Meta uses models.Disease.get_serializer_fields() and get_readonly_fields(). This keeps model-to-API mapping centralized.
  [Source](https://github.com/papaemmelab/isabl_api/blob/master/isabl_api/serializers.py)
- **Group serializer mapping Group model fields** — Defines a serializer for the Group model by inheriting from IsablSerializer. It pulls the model, read-only fields, and the serializer fields dynamically from models.Group via helper methods.
  [Source](https://github.com/papaemmelab/isabl_api/blob/master/isabl_api/serializers.py)
- **Project serializer with sharing and group fields** — Serializer for the Project model that inherits from IsablSerializer and uses model-driven field lists. It declares a nested GroupSerializer for the group relation and a non-model serializer named 'sharing' handled by ProjectSharingSerializer.
  [Source](https://github.com/papaemmelab/isabl_api/blob/master/isabl_api/serializers.py)
- **Application serializer including assembly and results** — ApplicationSerializer maps the Application model and declares nested fields including an assembly (nullable) and a 'results' DictField that holds a results specification. The results field defaults to an empty dict and expects each entry to be validated by a ResultSerializer.
  [Source](https://github.com/papaemmelab/isabl_api/blob/master/isabl_api/serializers.py)
- **Submission serializer mapping Submission model fields** — A straightforward serializer for the Submission model that inherits from IsablSerializer. It sources its fields and read-only settings from models.Submission helper methods.
  [Source](https://github.com/papaemmelab/isabl_api/blob/master/isabl_api/serializers.py)
- **Technique serializer with reference data and method** — TechniqueSerializer serializes the Technique model and includes both model-driven fields and a non-model serializer 'reference_data'. It declares a name CharField, a reference_data DictField for technique assets, and a method ChoiceField populated from a lazy choices source.
  [Source](https://github.com/papaemmelab/isabl_api/blob/master/isabl_api/serializers.py)
- **Base bio serializer adding submission relation** — BaseBioSerializer extends IsablSerializer and adds a standardized submission relation used by biological entity serializers. It exposes a submission field as a PrimaryKeyRelatedField pointing to models.Submission, allowing null and defaulting to None.
  [Source](https://github.com/papaemmelab/isabl_api/blob/master/isabl_api/serializers.py)
- **Individual serializer with species and gender** — IndividualSerializer inherits from BaseBioSerializer and maps the Individual model using dynamic model helpers. It declares nested center data plus species and gender ChoiceFields, where gender defaults to 'UNKNOWN' and choices are provided by lazy choice lookups.
  [Source](https://github.com/papaemmelab/isabl_api/blob/master/isabl_api/serializers.py)
- **Sample serializer linking individual, disease, category** — SampleSerializer is a BaseBioSerializer-derived serializer for the Sample model that includes nested IndividualSerializer and DiseaseSerializer fields. It also exposes a category ChoiceField with choices loaded lazily from sample_categories.
  [Source](https://github.com/papaemmelab/isabl_api/blob/master/isabl_api/serializers.py)
- **Aliquot serializer referencing parent sample object** — AliquotSerializer extends BaseBioSerializer to serialize the Aliquot model and declares a nested SampleSerializer for its sample relationship. Field lists and read-only fields are obtained from the Aliquot model via its helper methods.
  [Source](https://github.com/papaemmelab/isabl_api/blob/master/isabl_api/serializers.py)
- **Compact _Application serializer exposing assembly name** — _Application is a minimal ModelSerializer for the Application model exposing a small set of fields (pk, name, version, assembly). The assembly field is serialized as a read-only CharField sourced from assembly.name to present the assembly label rather than the full object.
  [Source](https://github.com/papaemmelab/isabl_api/blob/master/isabl_api/serializers.py)
- **Experiment serializer for minimal experiment representation** — Defines a minimal ModelSerializer for the Experiment model. The serializer exposes only the primary key (pk) and the system_id fields for lightweight experiment representations.
  [Source](https://github.com/papaemmelab/isabl_api/blob/master/isabl_api/serializers.py)
- **Analysis serializer exposing pk and application field** — A concise ModelSerializer for the Analysis model that exposes the primary key and the application relationship. The declared application field uses a nested _Application() serializer representation.
  [Source](https://github.com/papaemmelab/isabl_api/blob/master/isabl_api/serializers.py)
- **Serializer aggregating analysis results and metadata** — Serializes Analysis objects with rich result-related fields including analyses, application, references, results, status, storage_url, targets, run_time and wait_time. It nests experiments for targets/references and includes a many-to-many analyses field (no longer artificially limited), allowing aggregated result views for downstream consumers.
  [Source](https://github.com/papaemmelab/isabl_api/blob/master/isabl_api/serializers.py)
- **Full experiment serializer with nested relationships** — A comprehensive Experiment serializer that inherits BaseBioSerializer and includes model-defined serializer fields plus aliquot_id and analytics. It embeds many related nested serializers (sample, technique, platform, center, projects, raw_data) and exposes computed/read-only fields like aliquot identifier, bam_files structure, and an appended results list of succeeded analyses.
  [Source](https://github.com/papaemmelab/isabl_api/blob/master/isabl_api/serializers.py)
- **Comprehensive Analysis serializer with nested links** — An Isabl-specific serializer for Analysis that combines model-derived fields with analytics extras and multiple nested relations. It includes nested application, project- and individual-level analysis links, targets/references as Experiment serializers, a read-only cached_fields JSON blob, an analyses linkage field, a ran_by slug field, and a status choice field with default 'CREATED'.
  [Source](https://github.com/papaemmelab/isabl_api/blob/master/isabl_api/serializers.py)
- **Base tree serializer for top-down hierarchical views** — A top-down ModelSerializer mixin designed to be a base for tree-like representations. It adds common fields used in hierarchical views: tags (read-only many TagSerializer), a flexible JSON data field, and created_by as a read-only slug-related username.
  [Source](https://github.com/papaemmelab/isabl_api/blob/master/isabl_api/serializers.py)
- **Experiment-focused tree serializer with aliquot id** — A TreeSerializer specialized for Experiment model hierarchical views. It includes technique, platform, center serializers and exposes aliquot_id as a read-only field sourced from the aliquot relationship for easy display in tree contexts.
  [Source](https://github.com/papaemmelab/isabl_api/blob/master/isabl_api/serializers.py)
- **Sample tree serializer embedding experiment summaries** — A TreeSerializer specialization for Sample objects that includes disease metadata and an experiment_set of nested ExperimentTreeSerializer entries. It provides a hierarchical view where each sample lists its related experiments in a read-only fashion.
  [Source](https://github.com/papaemmelab/isabl_api/blob/master/isabl_api/serializers.py)
- **Individual tree serializer including samples and center** — A TreeSerializer for the Individual model that embeds center metadata and a read-only sample_set using SampleTreeSerializer. It provides a hierarchical top-down view where an individual lists its samples and associated metadata for UI or API tree endpoints.
  [Source](https://github.com/papaemmelab/isabl_api/blob/master/isabl_api/serializers.py)
- **Serializer for sending emails and notifications** — A plain DRF Serializer for composing outbound emails: recipients (list of validated emails), subject, content and an html_template identifier. Each field carries specific length limits to enforce payload size constraints when sending notifications through Isabl.
  [Source](https://github.com/papaemmelab/isabl_api/blob/master/isabl_api/serializers.py)
