# Views & Endpoints

API views to read, stream and download analysis results, manage submissions, registration and user preferences.

## Source Documents

- **Frontend template view for Isabl UI** — A simple TemplateView subclass that renders the frontend template for the Isabl UI. It exposes a get_context_data method to inject custom context into the template rendering.
  [Source](https://github.com/papaemmelab/isabl_api/blob/master/example/views.py)
- **Project JIRA epic integration view** — Endpoint view that retrieves or creates a JIRA epic associated with a given project. The view is a BaseView subclass and exposes a get(request, pk) method to perform the lookup or creation using the project primary key.
  [Source](https://github.com/papaemmelab/isabl_api/blob/master/isabl_api/integrations/views.py)
- **Create or retrieve Jira ticket for project** — A BaseView subclass exposing a POST endpoint to get or create a JIRA ticket tied to a project's epic. The view accepts a project identifier and ensures a ticket exists under the project's epic, creating one if needed.
  [Source](https://github.com/papaemmelab/isabl_api/blob/master/isabl_api/integrations/views.py)
- **Google Drive directory integration for projects** — This BaseView subclass exposes a GET endpoint that retrieves or creates a Google Drive directory for a project. It maps a project (by primary key) to a Drive folder, creating the folder structure when it does not exist.
  [Source](https://github.com/papaemmelab/isabl_api/blob/master/isabl_api/integrations/views.py)
- **Base view enforcing analysis result download permissions** — BaseResultsView extends BaseView to add result-download-specific permission requirements by appending CanDownloadResults to the permission classes. It provides a get_analysis helper to check whether the requesting user is allowed to download the results for a particular analysis.
  [Source](https://github.com/papaemmelab/isabl_api/blob/master/isabl_api/views/analyses.py)
- **Read analysis result file (cat-like rendering)** — ReadAnalysisResult inherits from BaseResultsView and provides a GET endpoint to render the contents of a file located within an analysis output directory, similar to a UNIX cat. It relies on the base permission checks to ensure the user is authorized to view the file.
  [Source](https://github.com/papaemmelab/isabl_api/blob/master/isabl_api/views/analyses.py)
- **Download analysis result file endpoint** — DownloadAnalysisResult is a BaseResultsView that exposes a GET endpoint to render a file from an analysis output directory as a downloadable response. It ensures users have the required download permissions before serving the file.
  [Source](https://github.com/papaemmelab/isabl_api/blob/master/isabl_api/views/analyses.py)
- **Stream analysis result file (HTTP streaming)** — StreamAnalysisResult extends BaseResultsView and provides a GET endpoint for streaming a file from an analysis output directory, suitable for large files or continuous transfer. The view uses the base permission checks to confirm the requester may access the streamed content.
  [Source](https://github.com/papaemmelab/isabl_api/blob/master/isabl_api/views/analyses.py)
- **Bulk update analyses statuses efficiently** — BulkUpdateAnalyses is a BaseView that provides a PATCH endpoint for efficiently updating the status of multiple analyses in a single request. If an analysis status is set to SUBMITTED by the bulk operation, relevant time fields are reset to reflect the new submission state.
  [Source](https://github.com/papaemmelab/isabl_api/blob/master/isabl_api/views/analyses.py)
- **Base IGV view for genome visualization integration** — BaseIGVView extends BaseResultsView to render an IGV (Integrative Genomics Viewer) HTML interface using the igv.html template and TemplateHTMLRenderer. It exposes a render_igv helper for composing the IGV view and overrides dispatch to integrate with request handling and permission checks.
  [Source](https://github.com/papaemmelab/isabl_api/blob/master/isabl_api/views/analyses.py)
- **IGV Experiment view for genome visualization** — Defines a view that renders an Experiment in IGV (Integrative Genomics Viewer). It inherits from BaseIGVView and exposes a GET method that accepts a system_id to load the experiment data into IGV.
  [Source](https://github.com/papaemmelab/isabl_api/blob/master/isabl_api/views/analyses.py)
- **IGV Analysis view for analysis visualization** — Provides a view to render an Analysis in IGV. The view inherits from BaseIGVView and exposes a GET endpoint that accepts a primary key to identify the analysis to display in IGV.
  [Source](https://github.com/papaemmelab/isabl_api/blob/master/isabl_api/views/analyses.py)
- **Stream assembly reference file via API endpoint** — A view that serves files from an assembly reference collection. It inherits from BaseView and provides a GET method that takes a primary key to render or stream the referenced assembly file to the client.
  [Source](https://github.com/papaemmelab/isabl_api/blob/master/isabl_api/views/assemblies.py)
- **Base API view with JSON and auth defaults** — BaseView is a lightweight base class for API views that sets default renderers and enforces authentication. It inherits from Django REST Framework's APIView and configures JSONRenderer, a form-less renderer, and requires authenticated users by default.
  [Source](https://github.com/papaemmelab/isabl_api/blob/master/isabl_api/views/base.py)
- **Generic model-backed view with helper methods** — ModelView is a reusable generic view combining BaseView and GenericAPIView to support model-backed endpoints. It documents configurable attributes (model, serializer_class, lookup_field, ordering, permissions) and helper methods to resolve models, serializers, querysets, filters, pagination, and object retrieval at runtime.
  [Source](https://github.com/papaemmelab/isabl_api/blob/master/isabl_api/views/base.py)
- **Retrieve, update, and destroy model instances** — A composite view that provides retrieve, update, and delete operations for model instances. It inherits ModelView and Django REST Framework's RetrieveUpdateDestroyAPIView to offer standard CRUD endpoints for single objects.
  [Source](https://github.com/papaemmelab/isabl_api/blob/master/isabl_api/views/base.py)
- **Read-only retrieve view for single objects** — Provides a read-only endpoint to retrieve a single model instance. RetrieveView combines ModelView with DRF's RetrieveAPIView to enforce serializer/model resolution and authentication while allowing only GET retrieval.
  [Source](https://github.com/papaemmelab/isabl_api/blob/master/isabl_api/views/base.py)
- **List and create view with deduplication behavior** — ListCreateView implements listing of objects and creation with special get-or-create semantics. The GET method lists objects, while POST will either create new objects or return existing ones matched by primary key or unique-together constraints; if an existing object is returned, the posted data will not update it.
  [Source](https://github.com/papaemmelab/isabl_api/blob/master/isabl_api/views/base.py)
- **List view for querying model collections** — A simple view that lists model instances, combining ModelView with DRF's ListAPIView. It provides standard list behavior, inheriting authentication, serializer/model resolution, and filtering capabilities from ModelView.
  [Source](https://github.com/papaemmelab/isabl_api/blob/master/isabl_api/views/base.py)
- **Endpoint to authenticate and verify users** — AuthenticateUser is a small view that performs user authentication checks. It inherits from BaseView and exposes a GET method intended to authenticate or verify the current user session or token.
  [Source](https://github.com/papaemmelab/isabl_api/blob/master/isabl_api/views/base.py)
- **User Preferences Retrieve and Update API View** — Defines a view for retrieving and updating a user's preferences. It subclasses BaseView and RetrieveUpdateAPIView and uses the PreferencesSerializer. The get_object method resolves the preferences instance using request.user.
  [Source](https://github.com/papaemmelab/isabl_api/blob/master/isabl_api/views/base.py)
- **Send No-Reply Email via Mailgun Backend** — Implements an API endpoint that sends a no-reply email using the Django Mailgun backend. The view inherits from BaseView and exposes a post method that sends the message. The endpoint returns a value of 1 when the message is sent successfully.
  [Source](https://github.com/papaemmelab/isabl_api/blob/master/isabl_api/views/emails.py)
- **Public Registration Settings API View (AllowAny)** — Provides a public API endpoint to expose registration settings. The view inherits from Django REST Framework's APIView and sets permission_classes to AllowAny. A get method is implemented to retrieve the settings.
  [Source](https://github.com/papaemmelab/isabl_api/blob/master/isabl_api/views/registration.py)
- **Confirm Email Endpoint and Lookup Logic** — Defines the confirm-email endpoint used to validate and confirm user email addresses. The view inherits from APIView, allows any user (AllowAny), and implements get, get_object, and get_queryset methods to locate and operate on the relevant confirmation records. These methods encapsulate the logic for fetching the confirmation instance and handling GET confirmation requests.
  [Source](https://github.com/papaemmelab/isabl_api/blob/master/isabl_api/views/registration.py)
- **Download Submission Excel Template Endpoint** — Provides an endpoint to download the submission_form Excel template used for batch submissions. The view subclasses BaseView and implements a GET method to return the template file. This endpoint is intended for users preparing submission spreadsheets.
  [Source](https://github.com/papaemmelab/isabl_api/blob/master/isabl_api/views/submissions.py)
- **Process Submission Excel Form and Create Objects** — Accepts and processes a filled submission_form Excel file to create objects in the system. The view inherits from BaseView and exposes a POST endpoint that takes a primary key and the uploaded form, creates resources accordingly, and returns the submission object. The response includes a data field reporting any errors encountered during processing.
  [Source](https://github.com/papaemmelab/isabl_api/blob/master/isabl_api/views/submissions.py)
