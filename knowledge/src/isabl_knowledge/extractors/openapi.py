"""Extractor for OpenAPI/Swagger specifications."""

from __future__ import annotations

import json
from pathlib import Path

from isabl_knowledge.config import SourceConfig
from isabl_knowledge.extractors.base import BaseExtractor
from isabl_knowledge.models import Document


class OpenAPIExtractor(BaseExtractor):
    """Extract documents from an OpenAPI/Swagger JSON spec file."""

    def extract(self) -> list[Document]:
        """Parse OpenAPI spec into one document per endpoint + one per schema."""
        spec_path = self.source.url
        if not spec_path:
            return []

        path = Path(spec_path)
        if not path.exists():
            raise FileNotFoundError(f"OpenAPI spec not found: {spec_path}")

        spec = json.loads(path.read_text())

        # Detect OpenAPI version
        is_v3 = spec.get("openapi", "").startswith("3.")
        base_url = self._get_base_url(spec, is_v3)

        documents = []
        documents.extend(self._extract_endpoints(spec, is_v3, base_url))
        documents.extend(self._extract_schemas(spec, is_v3))

        return documents

    def _get_base_url(self, spec: dict, is_v3: bool) -> str:
        if is_v3:
            servers = spec.get("servers", [])
            return servers[0]["url"] if servers else ""
        return spec.get("basePath", "")

    def _extract_endpoints(
        self, spec: dict, is_v3: bool, base_url: str
    ) -> list[Document]:
        """Create one document per endpoint (path + method)."""
        docs = []
        paths = spec.get("paths", {})

        for path, methods in paths.items():
            for method, details in methods.items():
                if method in ("parameters", "servers", "summary", "description"):
                    continue

                operation_id = details.get("operationId", "")
                summary = details.get("summary", "")
                description = details.get("description", "")
                tags = details.get("tags", [])

                # Build content
                content_parts = [
                    f"# {method.upper()} {base_url}{path}",
                    "",
                ]

                if summary:
                    content_parts.append(f"**{summary}**")
                    content_parts.append("")

                if description:
                    content_parts.append(description)
                    content_parts.append("")

                # Parameters
                params = details.get("parameters", [])
                if params:
                    content_parts.append("## Parameters")
                    content_parts.append("")
                    for p in params:
                        p = self._resolve_ref(spec, p)
                        name = p.get("name", "")
                        location = p.get("in", "")
                        required = p.get("required", False)
                        p_desc = p.get("description", "")
                        p_type = self._get_param_type(p, is_v3)
                        req = " (required)" if required else ""
                        content_parts.append(
                            f"- `{name}` ({location}, {p_type}){req}: {p_desc}"
                        )
                    content_parts.append("")

                # Request body (v3)
                if is_v3 and "requestBody" in details:
                    body = self._resolve_ref(spec, details["requestBody"])
                    content_parts.append("## Request Body")
                    content_parts.append("")
                    body_desc = body.get("description", "")
                    if body_desc:
                        content_parts.append(body_desc)
                    for media_type, media in body.get("content", {}).items():
                        schema = media.get("schema", {})
                        schema_text = self._schema_to_text(spec, schema)
                        if schema_text:
                            content_parts.append(f"\n**{media_type}:**\n{schema_text}")
                    content_parts.append("")

                # Responses
                responses = details.get("responses", {})
                if responses:
                    content_parts.append("## Responses")
                    content_parts.append("")
                    for status, resp in responses.items():
                        resp = self._resolve_ref(spec, resp)
                        r_desc = resp.get("description", "")
                        content_parts.append(f"- **{status}**: {r_desc}")

                        # Show response schema
                        if is_v3:
                            for media_type, media in resp.get("content", {}).items():
                                schema = media.get("schema", {})
                                schema_text = self._schema_to_text(spec, schema, indent=2)
                                if schema_text:
                                    content_parts.append(schema_text)
                        else:
                            schema = resp.get("schema", {})
                            schema_text = self._schema_to_text(spec, schema, indent=2)
                            if schema_text:
                                content_parts.append(schema_text)
                    content_parts.append("")

                doc_id = f"{self.source.name}/endpoint:{method.upper()}:{path}"
                title = summary or f"{method.upper()} {path}"

                docs.append(
                    Document(
                        doc_id=doc_id,
                        source_type="openapi_endpoint",
                        source_url=f"{base_url}{path}",
                        content="\n".join(content_parts),
                        tags=tags,
                        metadata={
                            "method": method.upper(),
                            "path": path,
                            "operation_id": operation_id,
                        },
                    )
                )

        return docs

    def _extract_schemas(self, spec: dict, is_v3: bool) -> list[Document]:
        """Create one document per schema/model definition."""
        docs = []

        if is_v3:
            schemas = spec.get("components", {}).get("schemas", {})
        else:
            schemas = spec.get("definitions", {})

        for name, schema in schemas.items():
            content_parts = [f"# Schema: {name}", ""]

            description = schema.get("description", "")
            if description:
                content_parts.append(description)
                content_parts.append("")

            # Properties
            properties = schema.get("properties", {})
            required_fields = set(schema.get("required", []))

            if properties:
                content_parts.append("## Fields")
                content_parts.append("")
                for prop_name, prop in properties.items():
                    prop = self._resolve_ref(spec, prop)
                    prop_type = prop.get("type", "object")
                    prop_desc = prop.get("description", "")
                    read_only = prop.get("readOnly", False)
                    enum = prop.get("enum")
                    req = " (required)" if prop_name in required_fields else ""
                    ro = " (read-only)" if read_only else ""

                    extras = []
                    if enum:
                        extras.append(f"enum: {enum}")
                    if prop.get("format"):
                        extras.append(f"format: {prop['format']}")
                    if "$ref" in prop:
                        extras.append(f"ref: {prop['$ref'].split('/')[-1]}")

                    extra_str = f" [{', '.join(extras)}]" if extras else ""
                    content_parts.append(
                        f"- `{prop_name}` ({prop_type}{req}{ro}){extra_str}: {prop_desc}"
                    )
                content_parts.append("")

            doc_id = f"{self.source.name}/schema:{name}"

            docs.append(
                Document(
                    doc_id=doc_id,
                    source_type="openapi_schema",
                    source_url="",
                    content="\n".join(content_parts),
                    tags=["api-schema", name.lower()],
                    metadata={
                        "kind": "schema",
                        "name": name,
                    },
                )
            )

        return docs

    def _resolve_ref(self, spec: dict, obj: dict) -> dict:
        """Resolve a $ref pointer to its definition."""
        ref = obj.get("$ref")
        if not ref:
            return obj

        parts = ref.lstrip("#/").split("/")
        resolved = spec
        for part in parts:
            resolved = resolved.get(part, {})
        return resolved

    def _get_param_type(self, param: dict, is_v3: bool) -> str:
        if is_v3:
            schema = param.get("schema", {})
            return schema.get("type", "string")
        return param.get("type", "string")

    def _schema_to_text(self, spec: dict, schema: dict, indent: int = 0) -> str:
        """Convert a schema to a readable text summary."""
        schema = self._resolve_ref(spec, schema)
        prefix = "  " * indent

        if not schema:
            return ""

        if "properties" in schema:
            lines = []
            for name, prop in schema["properties"].items():
                prop = self._resolve_ref(spec, prop)
                p_type = prop.get("type", "object")
                lines.append(f"{prefix}- `{name}`: {p_type}")
            return "\n".join(lines)

        if schema.get("type") == "array":
            items = self._resolve_ref(spec, schema.get("items", {}))
            item_type = items.get("type", items.get("title", "object"))
            return f"{prefix}Array of {item_type}"

        s_type = schema.get("type", "")
        if s_type:
            return f"{prefix}{s_type}"

        return ""
