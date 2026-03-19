# Serialization & IsablDict Utilities

Utilities that convert API responses and nested Python objects into IsablDict wrappers and provide custom dict-like accessors and representations.

## Source Documents

- **Recursive conversion of objects to IsablDict** — isablfy converts arbitrary Python objects (including nested lists and dicts) into IsablDict instances recursively. It standardizes data structures returned from API calls or internal functions so downstream code can work with a consistent mapping type.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/api.py)
- **Recursive dictionary to IsablDict transformer** — Classmethod that converts a plain Python dictionary into IsablDict instances recursively, turning nested dictionaries into typed IsablDict objects. This helper ensures nested structures are consistently wrapped for API/CLI objects.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/api.py)
- **Constructor supports id-based retrieval** — Custom __init__ implementation that, when the first argument is an int or str, treats it as an identifier and retrieves the corresponding instance during construction. This enables convenient instantiation from an id value as well as normal construction via other args/kwargs.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/api.py)
- **Custom get checks custom fields first** — Override of the get method that prioritizes checking for custom fields before falling back to normal dictionary lookup or a provided default. This ensures user-defined/custom metadata fields are accessed consistently in Isabl objects.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/api.py)
- **Pop method prefers custom fields first** — Custom pop implementation that checks for and removes custom fields before falling back to standard dictionary pop behavior. It supports providing a default value and ensures custom metadata can be safely removed from Isabl objects.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/api.py)
- **Readable string representation for assemblies** — Custom __repr__ implementation that gives assembly objects a concise, informative string representation for easier inspection. This representation surfaces key attributes of assemblies to simplify debugging and logging in interactive sessions.
  [Source](https://github.com/papaemmelab/isabl_cli/blob/main/isabl_cli/api.py)
