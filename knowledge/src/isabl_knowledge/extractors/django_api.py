"""Extractor for Django REST Framework APIs (models, serializers, views, URLs)."""

from __future__ import annotations

import ast
import re
import subprocess
import tempfile
from pathlib import Path

from isabl_knowledge.config import SourceConfig
from isabl_knowledge.extractors.base import BaseExtractor
from isabl_knowledge.models import Document


class DjangoAPIExtractor(BaseExtractor):
    """Extract structured API knowledge from a Django REST Framework project."""

    def extract(self) -> list[Document]:
        """Clone repo and extract models, serializers, views, and URL config."""
        repo = self.source.repo
        if not repo:
            return []

        with tempfile.TemporaryDirectory() as tmp:
            clone_dir = Path(tmp) / "repo"
            branch_args = []
            if self.source.extract and len(self.source.extract) > 0:
                # Use first extract entry as branch name if it looks like one
                for e in self.source.extract:
                    if e.startswith("branch:"):
                        branch_args = ["-b", e.split(":", 1)[1]]
                        break

            subprocess.run(
                [
                    "git", "clone", "--depth", "1",
                    *branch_args,
                    f"https://github.com/{repo}.git",
                    str(clone_dir),
                ],
                capture_output=True,
                check=True,
            )

            documents = []
            documents.extend(self._extract_models(clone_dir))
            documents.extend(self._extract_serializers(clone_dir))
            documents.extend(self._extract_views(clone_dir))
            documents.extend(self._extract_urls(clone_dir))

            return documents

    def _find_files(self, clone_dir: Path, pattern: str) -> list[Path]:
        """Find Python files matching a pattern, excluding tests/migrations."""
        results = []
        for py_file in sorted(clone_dir.rglob("*.py")):
            rel = str(py_file.relative_to(clone_dir))
            if any(skip in rel for skip in ["test", "migration", "setup.py", "conftest", "manage.py"]):
                continue
            if pattern in py_file.name or pattern in rel:
                results.append(py_file)
        return results

    def _extract_models(self, clone_dir: Path) -> list[Document]:
        """Extract Django model definitions."""
        docs = []
        model_files = self._find_files(clone_dir, "model")

        for file_path in model_files:
            try:
                source = file_path.read_text()
                tree = ast.parse(source)
            except (SyntaxError, UnicodeDecodeError):
                continue

            rel_path = str(file_path.relative_to(clone_dir))

            for node in ast.walk(tree):
                if not isinstance(node, ast.ClassDef):
                    continue

                # Check if it looks like a Django model
                bases = [ast.unparse(b) for b in node.bases]
                is_model = any(
                    "Model" in b or "Base" in b
                    for b in bases
                )
                if not is_model:
                    continue

                docstring = ast.get_docstring(node) or ""
                fields = self._extract_model_fields(node, source)
                meta = self._extract_meta(node)
                methods = self._extract_methods(node)

                content_parts = [f"# Model: {node.name}"]
                if bases:
                    content_parts.append(f"\nInherits from: {', '.join(bases)}")
                if docstring:
                    content_parts.append(f"\n{docstring}")

                if fields:
                    content_parts.append("\n## Fields\n")
                    for name, field_type, field_args in fields:
                        content_parts.append(f"- `{name}`: {field_type}({field_args})")

                if meta:
                    content_parts.append(f"\n## Meta\n\n{meta}")

                if methods:
                    content_parts.append("\n## Methods\n")
                    for mname, msig, mdoc in methods:
                        content_parts.append(f"### {mname}\n\n```python\n{msig}\n```")
                        if mdoc:
                            content_parts.append(f"\n{mdoc}")

                docs.append(
                    Document(
                        doc_id=f"{self.source.name}/{rel_path}:model:{node.name}",
                        source_type="django_model",
                        source_url=f"https://github.com/{self.source.repo}/blob/master/{rel_path}",
                        content="\n".join(content_parts),
                        tags=["model", node.name.lower()],
                        metadata={
                            "kind": "model",
                            "name": node.name,
                            "file": rel_path,
                            "bases": bases,
                        },
                    )
                )

        return docs

    def _extract_model_fields(
        self, class_node: ast.ClassDef, source: str
    ) -> list[tuple[str, str, str]]:
        """Extract field definitions from a model class."""
        fields = []
        for node in class_node.body:
            if not isinstance(node, ast.Assign):
                continue
            for target in node.targets:
                if not isinstance(target, ast.Name):
                    continue
                if target.id.startswith("_"):
                    continue

                # Check if RHS is a field call
                if isinstance(node.value, ast.Call):
                    func_name = ast.unparse(node.value.func)
                    if any(kw in func_name.lower() for kw in [
                        "field", "foreign", "many", "one", "char", "text",
                        "integer", "boolean", "date", "json", "file", "slug",
                        "url", "email", "uuid", "auto", "decimal", "float",
                    ]):
                        args = ast.unparse(node.value).split("(", 1)
                        field_args = args[1].rstrip(")") if len(args) > 1 else ""
                        # Truncate long args
                        if len(field_args) > 120:
                            field_args = field_args[:120] + "..."
                        fields.append((target.id, func_name, field_args))
        return fields

    def _extract_meta(self, class_node: ast.ClassDef) -> str:
        """Extract Meta class info."""
        for node in class_node.body:
            if isinstance(node, ast.ClassDef) and node.name == "Meta":
                lines = []
                for item in node.body:
                    if isinstance(item, ast.Assign):
                        try:
                            lines.append(ast.unparse(item))
                        except Exception:
                            pass
                return "\n".join(lines)
        return ""

    def _extract_methods(
        self, class_node: ast.ClassDef
    ) -> list[tuple[str, str, str]]:
        """Extract documented methods from a class."""
        methods = []
        for node in class_node.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if node.name.startswith("_") and node.name != "__str__":
                    continue
                docstring = ast.get_docstring(node) or ""
                sig = self._get_signature(node)
                methods.append((node.name, sig, docstring))
        return methods

    def _extract_serializers(self, clone_dir: Path) -> list[Document]:
        """Extract DRF serializer definitions."""
        docs = []
        serializer_files = self._find_files(clone_dir, "serial")

        for file_path in serializer_files:
            try:
                source = file_path.read_text()
                tree = ast.parse(source)
            except (SyntaxError, UnicodeDecodeError):
                continue

            rel_path = str(file_path.relative_to(clone_dir))

            for node in ast.walk(tree):
                if not isinstance(node, ast.ClassDef):
                    continue

                bases = [ast.unparse(b) for b in node.bases]
                is_serializer = any("Serializer" in b for b in bases)
                if not is_serializer:
                    continue

                docstring = ast.get_docstring(node) or ""
                meta = self._extract_meta(node)
                fields = self._extract_serializer_fields(node)

                content_parts = [f"# Serializer: {node.name}"]
                if bases:
                    content_parts.append(f"\nInherits from: {', '.join(bases)}")
                if docstring:
                    content_parts.append(f"\n{docstring}")
                if meta:
                    content_parts.append(f"\n## Meta\n\n```python\n{meta}\n```")
                if fields:
                    content_parts.append("\n## Declared Fields\n")
                    for fname, fval in fields:
                        content_parts.append(f"- `{fname}`: {fval}")

                docs.append(
                    Document(
                        doc_id=f"{self.source.name}/{rel_path}:serializer:{node.name}",
                        source_type="django_serializer",
                        source_url=f"https://github.com/{self.source.repo}/blob/master/{rel_path}",
                        content="\n".join(content_parts),
                        tags=["serializer", node.name.lower()],
                        metadata={
                            "kind": "serializer",
                            "name": node.name,
                            "file": rel_path,
                        },
                    )
                )

        return docs

    def _extract_serializer_fields(
        self, class_node: ast.ClassDef
    ) -> list[tuple[str, str]]:
        """Extract declared fields from a serializer."""
        fields = []
        for node in class_node.body:
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and not target.id.startswith("_"):
                        try:
                            value = ast.unparse(node.value)
                            if len(value) > 150:
                                value = value[:150] + "..."
                            fields.append((target.id, value))
                        except Exception:
                            pass
        return fields

    def _extract_views(self, clone_dir: Path) -> list[Document]:
        """Extract DRF view/viewset definitions."""
        docs = []
        view_files = self._find_files(clone_dir, "view")

        for file_path in view_files:
            try:
                source = file_path.read_text()
                tree = ast.parse(source)
            except (SyntaxError, UnicodeDecodeError):
                continue

            rel_path = str(file_path.relative_to(clone_dir))

            for node in ast.walk(tree):
                if not isinstance(node, ast.ClassDef):
                    continue

                bases = [ast.unparse(b) for b in node.bases]
                is_view = any(
                    kw in b for b in bases
                    for kw in ["View", "ViewSet", "Mixin", "APIView"]
                )
                if not is_view:
                    continue

                docstring = ast.get_docstring(node) or ""
                methods = self._extract_methods(node)
                attrs = self._extract_class_attrs(node)

                content_parts = [f"# View: {node.name}"]
                if bases:
                    content_parts.append(f"\nInherits from: {', '.join(bases)}")
                if docstring:
                    content_parts.append(f"\n{docstring}")
                if attrs:
                    content_parts.append("\n## Attributes\n")
                    for aname, aval in attrs:
                        content_parts.append(f"- `{aname}` = {aval}")
                if methods:
                    content_parts.append("\n## Methods\n")
                    for mname, msig, mdoc in methods:
                        content_parts.append(f"### {mname}\n\n```python\n{msig}\n```")
                        if mdoc:
                            content_parts.append(f"\n{mdoc}")

                docs.append(
                    Document(
                        doc_id=f"{self.source.name}/{rel_path}:view:{node.name}",
                        source_type="django_view",
                        source_url=f"https://github.com/{self.source.repo}/blob/master/{rel_path}",
                        content="\n".join(content_parts),
                        tags=["view", node.name.lower()],
                        metadata={
                            "kind": "view",
                            "name": node.name,
                            "file": rel_path,
                        },
                    )
                )

        return docs

    def _extract_class_attrs(
        self, class_node: ast.ClassDef
    ) -> list[tuple[str, str]]:
        """Extract class-level attribute assignments."""
        attrs = []
        for node in class_node.body:
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and not target.id.startswith("_"):
                        try:
                            value = ast.unparse(node.value)
                            if len(value) > 150:
                                value = value[:150] + "..."
                            attrs.append((target.id, value))
                        except Exception:
                            pass
        return attrs

    def _extract_urls(self, clone_dir: Path) -> list[Document]:
        """Extract URL routing configuration."""
        docs = []
        url_files = self._find_files(clone_dir, "url")

        for file_path in url_files:
            try:
                source = file_path.read_text()
            except (UnicodeDecodeError,):
                continue

            rel_path = str(file_path.relative_to(clone_dir))

            # Extract URL patterns using regex (AST is tricky for this)
            patterns = re.findall(
                r'(?:url|path|re_path)\s*\(\s*["\']([^"\']+)["\']',
                source,
            )

            if not patterns:
                continue

            content_parts = [
                f"# URL Configuration: {rel_path}",
                "",
                "## URL Patterns",
                "",
            ]

            for pattern in patterns:
                content_parts.append(f"- `{pattern}`")

            content_parts.append(f"\n## Full Source\n\n```python\n{source}\n```")

            docs.append(
                Document(
                    doc_id=f"{self.source.name}/{rel_path}:urls",
                    source_type="django_urls",
                    source_url=f"https://github.com/{self.source.repo}/blob/master/{rel_path}",
                    content="\n".join(content_parts),
                    tags=["urls", "routing"],
                    metadata={
                        "kind": "urls",
                        "file": rel_path,
                        "pattern_count": len(patterns),
                    },
                )
            )

        return docs

    def _get_signature(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> str:
        """Reconstruct a function signature string from AST."""
        args = []
        defaults_offset = len(node.args.args) - len(node.args.defaults)

        for i, arg in enumerate(node.args.args):
            name = arg.arg
            annotation = ""
            if arg.annotation:
                annotation = f": {ast.unparse(arg.annotation)}"
            default_idx = i - defaults_offset
            default = ""
            if default_idx >= 0:
                default = f"={ast.unparse(node.args.defaults[default_idx])}"
            args.append(f"{name}{annotation}{default}")

        if node.args.vararg:
            args.append(f"*{node.args.vararg.arg}")
        if node.args.kwonlyargs:
            if not node.args.vararg:
                args.append("*")
            for j, kw in enumerate(node.args.kwonlyargs):
                kw_default = ""
                if j < len(node.args.kw_defaults) and node.args.kw_defaults[j]:
                    kw_default = f"={ast.unparse(node.args.kw_defaults[j])}"
                args.append(f"{kw.arg}{kw_default}")
        if node.args.kwarg:
            args.append(f"**{node.args.kwarg.arg}")

        ret = ""
        if node.returns:
            ret = f" -> {ast.unparse(node.returns)}"

        prefix = "async def" if isinstance(node, ast.AsyncFunctionDef) else "def"
        return f"{prefix} {node.name}({', '.join(args)}){ret}"
