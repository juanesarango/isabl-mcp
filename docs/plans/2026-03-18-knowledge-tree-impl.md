# Knowledge Tree Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a pipeline that extracts knowledge from Isabl sources into a tree structure, served via MCP resources and a browsable GitHub repo.

**Architecture:** Config-driven pipeline (extract → summarize → build tree → render). Single `tree.json` artifact consumed by three renderers: MCP server, GitHub repo, static site.

**Tech Stack:** Python 3.10+, uv, click, pydantic, anthropic SDK, mcp, PyYAML, nbconvert

---

### Task 1: Scaffold the project

**Files:**
- Create: `knowledge/pyproject.toml`
- Create: `knowledge/src/isabl_knowledge/__init__.py`
- Create: `knowledge/src/isabl_knowledge/cli.py`
- Create: `knowledge/src/isabl_knowledge/config.py`
- Create: `knowledge/knowledge.yaml`
- Create: `knowledge/tests/__init__.py`
- Create: `knowledge/tests/conftest.py`

**Step 1: Initialize the uv project**

```bash
cd /Users/arangooj/isabl/isabl-ai-integration
mkdir -p knowledge/src/isabl_knowledge knowledge/tests
```

**Step 2: Create pyproject.toml**

```toml
[project]
name = "isabl-knowledge"
version = "0.1.0"
description = "Knowledge tree generator for the Isabl genomics platform"
requires-python = ">=3.10"
license = "MIT"
dependencies = [
    "click>=8.0.0",
    "pyyaml>=6.0",
    "pydantic>=2.0.0",
    "pydantic-settings>=2.0.0",
    "anthropic>=0.40.0",
    "mcp>=1.0.0",
    "httpx>=0.27.0",
    "nbconvert>=7.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "pytest-asyncio>=0.23.0",
]

[project.scripts]
isabl-knowledge = "isabl_knowledge.cli:cli"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/isabl_knowledge"]

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_functions = ["test_*"]
```

**Step 3: Create config.py with pydantic model for knowledge.yaml**

```python
"""Configuration for the knowledge tree pipeline."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import yaml
from pydantic import BaseModel


class SourceConfig(BaseModel):
    """A source to extract knowledge from."""
    name: str
    type: str  # github_python, github_django, github_apps, gitbook, jupyter
    repo: Optional[str] = None
    repos: Optional[list[str]] = None
    url: Optional[str] = None
    paths: Optional[list[str]] = None
    extract: Optional[list[str]] = None
    base_class: Optional[str] = None


class TreeConfig(BaseModel):
    """Tree generation settings."""
    max_depth: int = 4
    max_nodes: int = 100
    orientation: str = "capabilities and use cases, not code internals"


class OutputConfig(BaseModel):
    """Output settings."""
    github_repo: Optional[str] = None
    site: Optional[str] = None


class KnowledgeConfig(BaseModel):
    """Top-level pipeline configuration."""
    name: str
    sources: list[SourceConfig]
    tree: TreeConfig = TreeConfig()
    output: OutputConfig = OutputConfig()


def load_config(path: Path) -> KnowledgeConfig:
    """Load pipeline configuration from a YAML file."""
    with open(path) as f:
        raw = yaml.safe_load(f)
    return KnowledgeConfig(**raw)
```

**Step 4: Create cli.py with click commands**

```python
"""CLI for the Isabl knowledge tree pipeline."""

from pathlib import Path

import click

from isabl_knowledge.config import load_config


@click.group()
@click.option(
    "--config", "-c",
    default="knowledge.yaml",
    type=click.Path(exists=True, path_type=Path),
    help="Path to knowledge.yaml config file.",
)
@click.pass_context
def cli(ctx, config: Path):
    """Isabl Knowledge Tree - extract, organize, and serve platform knowledge."""
    ctx.ensure_object(dict)
    ctx.obj["config"] = load_config(config)


@cli.command()
@click.pass_context
def extract(ctx):
    """Extract content from all configured sources."""
    cfg = ctx.obj["config"]
    click.echo(f"Extracting from {len(cfg.sources)} sources...")
    for source in cfg.sources:
        click.echo(f"  - {source.name} ({source.type})")
    click.echo("Extract not yet implemented.")


@cli.command()
@click.pass_context
def summarize(ctx):
    """Generate LLM summaries for extracted documents."""
    click.echo("Summarize not yet implemented.")


@cli.command()
@click.pass_context
def tree(ctx):
    """Build the knowledge tree from summaries."""
    click.echo("Tree building not yet implemented.")


@cli.command()
@click.pass_context
def publish(ctx):
    """Render and publish the knowledge tree."""
    click.echo("Publish not yet implemented.")


@cli.command()
@click.pass_context
def build(ctx):
    """Run the full pipeline: extract → summarize → tree → publish."""
    ctx.invoke(extract)
    ctx.invoke(summarize)
    ctx.invoke(tree)
    ctx.invoke(publish)


@cli.command()
@click.pass_context
def serve(ctx):
    """Start the knowledge MCP server."""
    click.echo("MCP server not yet implemented.")
```

**Step 5: Create knowledge.yaml with placeholder sources**

```yaml
name: isabl-knowledge

sources:
  - name: isabl_cli
    type: github_python
    repo: isabl-io/isabl_cli
    extract: [docstrings, cli_commands]

  - name: docs
    type: gitbook
    url: https://docs.isabl.io

tree:
  max_depth: 4
  max_nodes: 100
  orientation: "capabilities and use cases, not code internals"

output:
  github_repo: isabl-knowledge-tree
```

**Step 6: Create `__init__.py`**

```python
"""Isabl Knowledge Tree - extract, organize, and serve platform knowledge."""
```

**Step 7: Create test conftest and config test**

Create `knowledge/tests/conftest.py`:
```python
"""Shared fixtures for knowledge tree tests."""

from pathlib import Path

import pytest

from isabl_knowledge.config import KnowledgeConfig, SourceConfig, TreeConfig


@pytest.fixture
def sample_config():
    """Minimal pipeline config for testing."""
    return KnowledgeConfig(
        name="test-knowledge",
        sources=[
            SourceConfig(
                name="test_source",
                type="github_python",
                repo="test/repo",
                extract=["docstrings"],
            ),
        ],
        tree=TreeConfig(),
    )


@pytest.fixture
def config_yaml_path(tmp_path):
    """Create a temporary knowledge.yaml for testing."""
    config_file = tmp_path / "knowledge.yaml"
    config_file.write_text(
        """
name: test-knowledge
sources:
  - name: test_source
    type: github_python
    repo: test/repo
    extract: [docstrings]
tree:
  max_depth: 3
  max_nodes: 50
"""
    )
    return config_file
```

Create `knowledge/tests/test_config.py`:
```python
"""Tests for configuration loading."""

from isabl_knowledge.config import load_config, KnowledgeConfig


def test_load_config(config_yaml_path):
    config = load_config(config_yaml_path)
    assert isinstance(config, KnowledgeConfig)
    assert config.name == "test-knowledge"
    assert len(config.sources) == 1
    assert config.sources[0].name == "test_source"
    assert config.tree.max_depth == 3
    assert config.tree.max_nodes == 50


def test_config_defaults(sample_config):
    assert sample_config.tree.max_depth == 4
    assert sample_config.tree.max_nodes == 100
    assert sample_config.output.github_repo is None
```

**Step 8: Install and run tests**

```bash
cd knowledge && uv venv && uv pip install -e ".[dev]"
uv run pytest -v
```

Expected: 2 tests pass.

**Step 9: Verify CLI works**

```bash
uv run isabl-knowledge --config knowledge.yaml extract
```

Expected: prints source list with "Extract not yet implemented."

**Step 10: Commit**

```bash
git add knowledge/
git commit -m "feat: scaffold knowledge tree pipeline with CLI and config"
```

---

### Task 2: Document model and extraction base

**Files:**
- Create: `knowledge/src/isabl_knowledge/models.py`
- Create: `knowledge/src/isabl_knowledge/extractors/__init__.py`
- Create: `knowledge/src/isabl_knowledge/extractors/base.py`
- Create: `knowledge/tests/test_models.py`

**Step 1: Write test for document model**

Create `knowledge/tests/test_models.py`:
```python
"""Tests for document models."""

from isabl_knowledge.models import Document


def test_document_creation():
    doc = Document(
        doc_id="cli/get_experiments",
        source_type="github_docstring",
        source_url="https://github.com/isabl-io/isabl_cli",
        content="# get_experiments\n\nQuery experiments from Isabl.",
    )
    assert doc.doc_id == "cli/get_experiments"
    assert doc.title == ""  # empty until summarized
    assert doc.tags == []
    assert doc.summary == ""


def test_document_with_metadata():
    doc = Document(
        doc_id="api/experiments",
        source_type="openapi",
        source_url="https://github.com/isabl-io/isabl_api",
        content="GET /api/v1/experiments/",
        metadata={"method": "GET", "path": "/api/v1/experiments/"},
    )
    assert doc.metadata["method"] == "GET"
```

**Step 2: Run test to verify it fails**

```bash
cd knowledge && uv run pytest tests/test_models.py -v
```

Expected: FAIL — `ModuleNotFoundError: No module named 'isabl_knowledge.models'`

**Step 3: Create document model**

Create `knowledge/src/isabl_knowledge/models.py`:
```python
"""Data models for extracted documents and tree nodes."""

from __future__ import annotations

from pydantic import BaseModel, Field


class Document(BaseModel):
    """An extracted document from any source."""
    doc_id: str
    source_type: str
    source_url: str
    content: str
    title: str = ""
    summary: str = ""
    tags: list[str] = Field(default_factory=list)
    questions: list[str] = Field(default_factory=list)
    metadata: dict = Field(default_factory=dict)


class TreeNode(BaseModel):
    """A node in the knowledge tree."""
    id: str
    title: str
    summary: str = ""
    children: list[TreeNode] = Field(default_factory=list)
    documents: list[str] = Field(default_factory=list)
```

**Step 4: Run tests to verify they pass**

```bash
cd knowledge && uv run pytest tests/test_models.py -v
```

Expected: 2 tests PASS.

**Step 5: Create extractor base class**

Create `knowledge/src/isabl_knowledge/extractors/__init__.py`:
```python
"""Source extractors for the knowledge tree pipeline."""
```

Create `knowledge/src/isabl_knowledge/extractors/base.py`:
```python
"""Base class for source extractors."""

from __future__ import annotations

import abc

from isabl_knowledge.config import SourceConfig
from isabl_knowledge.models import Document


class BaseExtractor(abc.ABC):
    """Base class for extracting documents from a source."""

    def __init__(self, source: SourceConfig):
        self.source = source

    @abc.abstractmethod
    def extract(self) -> list[Document]:
        """Extract documents from the source. Returns a list of Documents."""
        ...
```

**Step 6: Commit**

```bash
git add knowledge/
git commit -m "feat: add document model and extractor base class"
```

---

### Task 3: Gitbook extractor

This is the easiest extractor and gives the highest-value content for the knowledge tree.

**Files:**
- Create: `knowledge/src/isabl_knowledge/extractors/gitbook.py`
- Create: `knowledge/tests/test_gitbook_extractor.py`

**Step 1: Write tests for gitbook extractor**

Create `knowledge/tests/test_gitbook_extractor.py`:
```python
"""Tests for the Gitbook docs extractor."""

from unittest.mock import patch, MagicMock

from isabl_knowledge.config import SourceConfig
from isabl_knowledge.extractors.gitbook import GitbookExtractor


@pytest.fixture
def gitbook_source():
    return SourceConfig(
        name="docs",
        type="gitbook",
        url="https://docs.isabl.io",
    )


import pytest


def test_gitbook_extractor_creates_documents(gitbook_source):
    """Test that the extractor produces Document objects from fetched pages."""
    fake_pages = {
        "/": "<h1>Isabl</h1><p>Welcome to Isabl docs.</p>",
        "/quick-start": "<h1>Quick Start</h1><p>Get started with Isabl.</p>",
    }

    with patch.object(GitbookExtractor, "_fetch_pages", return_value=fake_pages):
        extractor = GitbookExtractor(gitbook_source)
        docs = extractor.extract()

    assert len(docs) == 2
    assert all(d.source_type == "gitbook" for d in docs)
    assert any("Quick Start" in d.content for d in docs)
    assert all(d.doc_id.startswith("docs/") for d in docs)


def test_gitbook_extractor_skips_empty_pages(gitbook_source):
    """Test that empty or trivial pages are skipped."""
    fake_pages = {
        "/": "<h1>Isabl</h1><p>Content here.</p>",
        "/empty": "",
        "/tiny": "<p>x</p>",
    }

    with patch.object(GitbookExtractor, "_fetch_pages", return_value=fake_pages):
        extractor = GitbookExtractor(gitbook_source)
        docs = extractor.extract()

    # Should skip empty and very short pages
    assert len(docs) == 1
```

**Step 2: Run test to verify it fails**

```bash
cd knowledge && uv run pytest tests/test_gitbook_extractor.py -v
```

Expected: FAIL — module not found.

**Step 3: Implement the Gitbook extractor**

Create `knowledge/src/isabl_knowledge/extractors/gitbook.py`:
```python
"""Extractor for Gitbook documentation sites."""

from __future__ import annotations

import re
from html.parser import HTMLParser
from urllib.parse import urljoin

import httpx

from isabl_knowledge.config import SourceConfig
from isabl_knowledge.extractors.base import BaseExtractor
from isabl_knowledge.models import Document

# Minimum content length to keep a page (skip near-empty pages)
MIN_CONTENT_LENGTH = 50


class _HTMLToMarkdown(HTMLParser):
    """Minimal HTML to markdown converter."""

    def __init__(self):
        super().__init__()
        self.result = []
        self._tag_stack = []

    def handle_starttag(self, tag, attrs):
        self._tag_stack.append(tag)
        if tag in ("h1", "h2", "h3", "h4"):
            level = int(tag[1])
            self.result.append("\n" + "#" * level + " ")
        elif tag == "li":
            self.result.append("\n- ")
        elif tag == "p":
            self.result.append("\n\n")
        elif tag == "code":
            self.result.append("`")
        elif tag == "pre":
            self.result.append("\n```\n")
        elif tag == "a":
            href = dict(attrs).get("href", "")
            self.result.append("[")
            self._tag_stack.append(("a_href", href))

    def handle_endtag(self, tag):
        if tag == "code":
            self.result.append("`")
        elif tag == "pre":
            self.result.append("\n```\n")
        elif tag == "a":
            # Pop until we find the a_href marker
            href = ""
            while self._tag_stack:
                item = self._tag_stack.pop()
                if isinstance(item, tuple) and item[0] == "a_href":
                    href = item[1]
                    break
            self.result.append(f"]({href})")
        elif self._tag_stack:
            self._tag_stack.pop()

    def handle_data(self, data):
        self.result.append(data)

    def get_markdown(self) -> str:
        text = "".join(self.result).strip()
        # Collapse multiple blank lines
        return re.sub(r"\n{3,}", "\n\n", text)


def html_to_markdown(html: str) -> str:
    """Convert HTML to simple markdown."""
    parser = _HTMLToMarkdown()
    parser.feed(html)
    return parser.get_markdown()


class GitbookExtractor(BaseExtractor):
    """Extract documentation pages from a Gitbook site."""

    def __init__(self, source: SourceConfig):
        super().__init__(source)
        self.base_url = source.url.rstrip("/") if source.url else ""

    def extract(self) -> list[Document]:
        """Fetch all pages and convert to Documents."""
        pages = self._fetch_pages()
        documents = []

        for path, html in pages.items():
            markdown = html_to_markdown(html)
            if len(markdown) < MIN_CONTENT_LENGTH:
                continue

            slug = path.strip("/") or "index"
            doc = Document(
                doc_id=f"{self.source.name}/{slug}",
                source_type="gitbook",
                source_url=f"{self.base_url}{path}",
                content=markdown,
                metadata={"path": path},
            )
            documents.append(doc)

        return documents

    def _fetch_pages(self) -> dict[str, str]:
        """Fetch pages from the Gitbook site. Returns {path: html_content}."""
        pages = {}
        visited = set()
        to_visit = ["/"]

        with httpx.Client(follow_redirects=True, timeout=30) as client:
            while to_visit:
                path = to_visit.pop(0)
                if path in visited:
                    continue
                visited.add(path)

                url = urljoin(self.base_url, path)
                try:
                    resp = client.get(url)
                    resp.raise_for_status()
                except httpx.HTTPError:
                    continue

                pages[path] = resp.text

                # Find internal links to crawl
                for match in re.finditer(r'href="(/[^"]*)"', resp.text):
                    link = match.group(1).split("#")[0].split("?")[0]
                    if link not in visited and not link.startswith("/api"):
                        to_visit.append(link)

        return pages
```

**Step 4: Run tests to verify they pass**

```bash
cd knowledge && uv run pytest tests/test_gitbook_extractor.py -v
```

Expected: 2 tests PASS.

**Step 5: Commit**

```bash
git add knowledge/
git commit -m "feat: add Gitbook documentation extractor"
```

---

### Task 4: Python docstring extractor

Extract SDK reference from isabl_cli by parsing Python source files with AST.

**Files:**
- Create: `knowledge/src/isabl_knowledge/extractors/github_python.py`
- Create: `knowledge/tests/test_python_extractor.py`

**Step 1: Write tests**

Create `knowledge/tests/test_python_extractor.py`:
```python
"""Tests for the Python/GitHub extractor."""

import textwrap
from pathlib import Path

import pytest

from isabl_knowledge.config import SourceConfig
from isabl_knowledge.extractors.github_python import PythonExtractor


@pytest.fixture
def python_source():
    return SourceConfig(
        name="isabl_cli",
        type="github_python",
        repo="isabl-io/isabl_cli",
        extract=["docstrings"],
    )


@pytest.fixture
def sample_python_file(tmp_path):
    """Create a sample Python file with docstrings."""
    code = textwrap.dedent('''
        """Module for querying experiments."""

        def get_experiments(projects=None, technique__method=None):
            """Get experiments from Isabl.

            Args:
                projects: Project PK or list of PKs.
                technique__method: Filter by sequencing method (WGS, RNA-Seq).

            Returns:
                List of experiment dictionaries.
            """
            pass


        class ExperimentManager:
            """Manages experiment queries and caching."""

            def count(self):
                """Return the number of experiments."""
                pass
    ''')
    f = tmp_path / "experiments.py"
    f.write_text(code)
    return f


def test_extract_from_file(python_source, sample_python_file):
    """Test extracting docstrings from a single Python file."""
    extractor = PythonExtractor(python_source)
    docs = extractor._extract_file(sample_python_file, "experiments.py")

    # Should extract module, function, and class docstrings
    assert len(docs) >= 2
    assert any("get_experiments" in d.doc_id for d in docs)
    assert any("projects" in d.content for d in docs)


def test_skip_undocumented(python_source, tmp_path):
    """Functions without docstrings should be skipped."""
    code = "def no_docs():\n    pass\n"
    f = tmp_path / "empty.py"
    f.write_text(code)

    extractor = PythonExtractor(python_source)
    docs = extractor._extract_file(f, "empty.py")
    assert len(docs) == 0
```

**Step 2: Run test to verify it fails**

```bash
cd knowledge && uv run pytest tests/test_python_extractor.py -v
```

**Step 3: Implement the Python extractor**

Create `knowledge/src/isabl_knowledge/extractors/github_python.py`:
```python
"""Extractor for Python source files (docstrings, function signatures)."""

from __future__ import annotations

import ast
import subprocess
import tempfile
from pathlib import Path

from isabl_knowledge.config import SourceConfig
from isabl_knowledge.extractors.base import BaseExtractor
from isabl_knowledge.models import Document


class PythonExtractor(BaseExtractor):
    """Extract docstrings and signatures from Python source files."""

    def extract(self) -> list[Document]:
        """Clone the repo and extract from all .py files."""
        repo = self.source.repo
        if not repo:
            return []

        with tempfile.TemporaryDirectory() as tmp:
            clone_dir = Path(tmp) / "repo"
            subprocess.run(
                ["git", "clone", "--depth", "1", f"https://github.com/{repo}.git", str(clone_dir)],
                capture_output=True,
                check=True,
            )

            documents = []
            for py_file in sorted(clone_dir.rglob("*.py")):
                rel_path = str(py_file.relative_to(clone_dir))
                # Skip test files, migrations, setup files
                if any(skip in rel_path for skip in ["test", "migration", "setup.py", "conftest"]):
                    continue
                docs = self._extract_file(py_file, rel_path)
                documents.extend(docs)

            return documents

    def _extract_file(self, file_path: Path, rel_path: str) -> list[Document]:
        """Extract documented functions, classes, and module docstrings from a file."""
        try:
            source = file_path.read_text()
            tree = ast.parse(source)
        except (SyntaxError, UnicodeDecodeError):
            return []

        documents = []

        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                docstring = ast.get_docstring(node)
                if not docstring:
                    continue

                sig = self._get_signature(node)
                content = f"# {node.name}\n\n```python\n{sig}\n```\n\n{docstring}"

                documents.append(Document(
                    doc_id=f"{self.source.name}/{rel_path}:{node.name}",
                    source_type="github_docstring",
                    source_url=f"https://github.com/{self.source.repo}/blob/main/{rel_path}",
                    content=content,
                    metadata={"kind": "function", "name": node.name, "file": rel_path},
                ))

            elif isinstance(node, ast.ClassDef):
                docstring = ast.get_docstring(node)
                if not docstring:
                    continue

                # Collect method summaries
                methods = []
                for item in node.body:
                    if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        method_doc = ast.get_docstring(item)
                        if method_doc:
                            sig = self._get_signature(item)
                            methods.append(f"### {item.name}\n\n```python\n{sig}\n```\n\n{method_doc}")

                content = f"# class {node.name}\n\n{docstring}"
                if methods:
                    content += "\n\n## Methods\n\n" + "\n\n".join(methods)

                documents.append(Document(
                    doc_id=f"{self.source.name}/{rel_path}:{node.name}",
                    source_type="github_docstring",
                    source_url=f"https://github.com/{self.source.repo}/blob/main/{rel_path}",
                    content=content,
                    metadata={"kind": "class", "name": node.name, "file": rel_path},
                ))

        return documents

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
```

**Step 4: Run tests**

```bash
cd knowledge && uv run pytest tests/test_python_extractor.py -v
```

Expected: 2 tests PASS.

**Step 5: Commit**

```bash
git add knowledge/
git commit -m "feat: add Python docstring extractor"
```

---

### Task 5: Wire extractors into CLI

**Files:**
- Modify: `knowledge/src/isabl_knowledge/cli.py`
- Create: `knowledge/src/isabl_knowledge/extractors/registry.py`
- Create: `knowledge/tests/test_cli.py`

**Step 1: Write CLI test**

Create `knowledge/tests/test_cli.py`:
```python
"""Tests for the CLI."""

from click.testing import CliRunner

from isabl_knowledge.cli import cli


def test_cli_help():
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "extract" in result.output
    assert "build" in result.output


def test_extract_command(config_yaml_path):
    runner = CliRunner()
    result = runner.invoke(cli, ["--config", str(config_yaml_path), "extract"])
    assert result.exit_code == 0
    assert "Extracting" in result.output
```

**Step 2: Create extractor registry**

Create `knowledge/src/isabl_knowledge/extractors/registry.py`:
```python
"""Registry mapping source types to extractor classes."""

from __future__ import annotations

from isabl_knowledge.config import SourceConfig
from isabl_knowledge.extractors.base import BaseExtractor
from isabl_knowledge.extractors.gitbook import GitbookExtractor
from isabl_knowledge.extractors.github_python import PythonExtractor


EXTRACTORS: dict[str, type[BaseExtractor]] = {
    "github_python": PythonExtractor,
    "gitbook": GitbookExtractor,
}


def get_extractor(source: SourceConfig) -> BaseExtractor:
    """Get the appropriate extractor for a source config."""
    cls = EXTRACTORS.get(source.type)
    if cls is None:
        raise ValueError(f"Unknown source type: {source.type}. Available: {list(EXTRACTORS.keys())}")
    return cls(source)
```

**Step 3: Update cli.py extract command to use registry and save documents**

Update the `extract` command in `cli.py`:
```python
import json

@cli.command()
@click.option("--output-dir", "-o", default="data", type=click.Path(path_type=Path))
@click.pass_context
def extract(ctx, output_dir: Path):
    """Extract content from all configured sources."""
    cfg = ctx.obj["config"]
    output_dir.mkdir(parents=True, exist_ok=True)

    all_docs = []
    for source in cfg.sources:
        click.echo(f"Extracting: {source.name} ({source.type})...")
        try:
            from isabl_knowledge.extractors.registry import get_extractor
            extractor = get_extractor(source)
            docs = extractor.extract()
            all_docs.extend(docs)
            click.echo(f"  → {len(docs)} documents")
        except ValueError as e:
            click.echo(f"  → Skipped: {e}")

    # Save extracted documents
    out_file = output_dir / "documents.json"
    out_file.write_text(json.dumps([d.model_dump() for d in all_docs], indent=2))
    click.echo(f"\nTotal: {len(all_docs)} documents saved to {out_file}")
```

**Step 4: Run tests**

```bash
cd knowledge && uv run pytest tests/test_cli.py -v
```

Expected: 2 tests PASS.

**Step 5: Commit**

```bash
git add knowledge/
git commit -m "feat: wire extractors into CLI with registry"
```

---

### Task 6: Summarizer (LLM pass 1)

**Files:**
- Create: `knowledge/src/isabl_knowledge/summarizer.py`
- Create: `knowledge/tests/test_summarizer.py`

**Step 1: Write tests**

Create `knowledge/tests/test_summarizer.py`:
```python
"""Tests for the LLM summarizer."""

from unittest.mock import patch, MagicMock

import pytest

from isabl_knowledge.models import Document
from isabl_knowledge.summarizer import summarize_document, summarize_documents


@pytest.fixture
def sample_doc():
    return Document(
        doc_id="cli/get_experiments",
        source_type="github_docstring",
        source_url="https://github.com/test/repo",
        content="# get_experiments\n\nQuery experiments from Isabl by project, technique, or status.",
    )


def test_summarize_document_calls_llm(sample_doc):
    """Test that summarize_document returns a document with title, summary, tags, questions."""
    mock_response = MagicMock()
    mock_response.content = [MagicMock(text="""{
        "title": "Query Experiments from Isabl",
        "summary": "Function to retrieve experiments filtered by project, technique, or status.",
        "tags": ["experiments", "querying", "SDK"],
        "questions": ["How do I get experiments for a project?"]
    }""")]

    with patch("isabl_knowledge.summarizer.get_client") as mock_client:
        mock_client.return_value.messages.create.return_value = mock_response
        result = summarize_document(sample_doc)

    assert result.title == "Query Experiments from Isabl"
    assert result.summary != ""
    assert len(result.tags) > 0
    assert len(result.questions) > 0
    # Original fields preserved
    assert result.doc_id == sample_doc.doc_id
    assert result.content == sample_doc.content
```

**Step 2: Implement summarizer**

Create `knowledge/src/isabl_knowledge/summarizer.py`:
```python
"""LLM-based document summarizer."""

from __future__ import annotations

import json
import logging

from anthropic import Anthropic

from isabl_knowledge.models import Document

logger = logging.getLogger(__name__)

SUMMARIZE_PROMPT = """Analyze this document from the Isabl genomics platform and produce a JSON object with:
- "title": descriptive title (5-10 words)
- "summary": 2-3 sentence summary explaining what this document covers
- "tags": 3-5 topic tags
- "questions": 3-5 questions this document answers

The audience is researchers, bioinformaticians, and engineers learning about Isabl.

Document:
{content}

Respond with only the JSON object, no markdown fencing."""


def get_client() -> Anthropic:
    """Get an Anthropic client."""
    return Anthropic()


def summarize_document(doc: Document, model: str = "claude-sonnet-4-20250514") -> Document:
    """Summarize a single document using an LLM."""
    client = get_client()
    prompt = SUMMARIZE_PROMPT.format(content=doc.content[:4000])

    response = client.messages.create(
        model=model,
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}],
    )

    text = response.content[0].text
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        logger.warning(f"Failed to parse LLM response for {doc.doc_id}")
        return doc

    doc.title = data.get("title", "")
    doc.summary = data.get("summary", "")
    doc.tags = data.get("tags", [])
    doc.questions = data.get("questions", [])
    return doc


def summarize_documents(docs: list[Document], model: str = "claude-sonnet-4-20250514") -> list[Document]:
    """Summarize all documents."""
    results = []
    for i, doc in enumerate(docs):
        logger.info(f"Summarizing {i + 1}/{len(docs)}: {doc.doc_id}")
        results.append(summarize_document(doc, model=model))
    return results
```

**Step 3: Run tests**

```bash
cd knowledge && uv run pytest tests/test_summarizer.py -v
```

Expected: PASS.

**Step 4: Commit**

```bash
git add knowledge/
git commit -m "feat: add LLM-based document summarizer"
```

---

### Task 7: Tree builder (LLM pass 2)

**Files:**
- Create: `knowledge/src/isabl_knowledge/tree_builder.py`
- Create: `knowledge/tests/test_tree_builder.py`

**Step 1: Write tests**

Create `knowledge/tests/test_tree_builder.py`:
```python
"""Tests for the knowledge tree builder."""

from unittest.mock import patch, MagicMock

import pytest

from isabl_knowledge.models import Document, TreeNode
from isabl_knowledge.tree_builder import build_tree


@pytest.fixture
def summarized_docs():
    return [
        Document(
            doc_id="cli/get_experiments",
            source_type="github_docstring",
            source_url="https://github.com/test",
            content="...",
            title="Query Experiments",
            summary="How to query experiments.",
            tags=["experiments", "querying"],
        ),
        Document(
            doc_id="apps/mutect2",
            source_type="github_apps",
            source_url="https://github.com/test",
            content="...",
            title="MuTect2 Variant Caller",
            summary="Somatic variant calling pipeline.",
            tags=["variant-calling", "pipelines"],
        ),
    ]


def test_build_tree_returns_tree_node(summarized_docs):
    """Test that build_tree returns a valid TreeNode."""
    mock_response = MagicMock()
    mock_response.content = [MagicMock(text="""{
        "id": "root",
        "title": "Isabl Genomics Platform",
        "summary": "Complete platform knowledge",
        "children": [
            {
                "id": "0001",
                "title": "Data Querying",
                "summary": "How to find and retrieve data",
                "documents": ["cli/get_experiments"]
            },
            {
                "id": "0002",
                "title": "Analysis Pipelines",
                "summary": "Available genomic analysis pipelines",
                "documents": ["apps/mutect2"]
            }
        ]
    }""")]

    with patch("isabl_knowledge.tree_builder.get_client") as mock_client:
        mock_client.return_value.messages.create.return_value = mock_response
        tree = build_tree(summarized_docs)

    assert isinstance(tree, TreeNode)
    assert tree.id == "root"
    assert len(tree.children) == 2
    assert tree.children[0].documents == ["cli/get_experiments"]
```

**Step 2: Implement tree builder**

Create `knowledge/src/isabl_knowledge/tree_builder.py`:
```python
"""Build a knowledge tree from summarized documents."""

from __future__ import annotations

import json
import logging

from anthropic import Anthropic

from isabl_knowledge.models import Document, TreeNode

logger = logging.getLogger(__name__)

TREE_PROMPT = """You are organizing documentation for the Isabl genomics platform into a navigable knowledge tree.

Given these {count} documents (each with doc_id, title, summary, tags), create a hierarchical tree structure:

- Max 4 levels deep
- Max 100 nodes
- Group by capabilities and use cases, not code structure
- Each leaf node should list the doc_ids of relevant documents
- Each node needs: id (dotted notation like "0001.0002"), title, summary, and optionally children or documents

Documents:
{documents}

Return a JSON object representing the root TreeNode. No markdown fencing."""


def get_client() -> Anthropic:
    """Get an Anthropic client."""
    return Anthropic()


def build_tree(docs: list[Document], model: str = "claude-sonnet-4-20250514") -> TreeNode:
    """Build a knowledge tree from summarized documents."""
    client = get_client()

    doc_summaries = json.dumps([
        {"doc_id": d.doc_id, "title": d.title, "summary": d.summary, "tags": d.tags}
        for d in docs
    ], indent=2)

    prompt = TREE_PROMPT.format(count=len(docs), documents=doc_summaries)

    response = client.messages.create(
        model=model,
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}],
    )

    text = response.content[0].text
    data = json.loads(text)
    return TreeNode(**data)
```

**Step 3: Run tests**

```bash
cd knowledge && uv run pytest tests/test_tree_builder.py -v
```

Expected: PASS.

**Step 4: Commit**

```bash
git add knowledge/
git commit -m "feat: add LLM-based knowledge tree builder"
```

---

### Task 8: GitHub repo renderer

**Files:**
- Create: `knowledge/src/isabl_knowledge/renderers/__init__.py`
- Create: `knowledge/src/isabl_knowledge/renderers/github_repo.py`
- Create: `knowledge/tests/test_github_renderer.py`

**Step 1: Write tests**

Create `knowledge/tests/test_github_renderer.py`:
```python
"""Tests for the GitHub repo renderer."""

from pathlib import Path

from isabl_knowledge.models import Document, TreeNode
from isabl_knowledge.renderers.github_repo import render_tree_to_repo


def test_render_creates_folder_hierarchy(tmp_path):
    """Test that render creates folders with README.md files."""
    tree = TreeNode(
        id="root",
        title="Isabl Platform",
        summary="Root node",
        children=[
            TreeNode(
                id="0001",
                title="Data Querying",
                summary="How to query data",
                documents=["cli/get_experiments"],
            ),
            TreeNode(
                id="0002",
                title="Pipelines",
                summary="Analysis pipelines",
                children=[
                    TreeNode(
                        id="0002.0001",
                        title="Variant Calling",
                        summary="Somatic variants",
                        documents=["apps/mutect2"],
                    ),
                ],
            ),
        ],
    )

    docs = {
        "cli/get_experiments": Document(
            doc_id="cli/get_experiments",
            source_type="docstring",
            source_url="https://github.com/test",
            content="# get_experiments\n\nQuery experiments.",
            title="Query Experiments",
            summary="How to query experiments.",
        ),
    }

    render_tree_to_repo(tree, docs, tmp_path)

    # Root README
    assert (tmp_path / "README.md").exists()
    root_content = (tmp_path / "README.md").read_text()
    assert "Isabl Platform" in root_content

    # Child folders
    assert (tmp_path / "data-querying" / "README.md").exists()
    assert (tmp_path / "pipelines" / "variant-calling" / "README.md").exists()

    # Document references in leaf READMEs
    leaf = (tmp_path / "data-querying" / "README.md").read_text()
    assert "cli/get_experiments" in leaf or "Query Experiments" in leaf
```

**Step 2: Implement renderer**

Create `knowledge/src/isabl_knowledge/renderers/__init__.py`:
```python
"""Renderers for the knowledge tree."""
```

Create `knowledge/src/isabl_knowledge/renderers/github_repo.py`:
```python
"""Render a knowledge tree as a GitHub-browsable folder hierarchy."""

from __future__ import annotations

import re
from pathlib import Path

from isabl_knowledge.models import Document, TreeNode


def slugify(title: str) -> str:
    """Convert a title to a folder-safe slug."""
    slug = title.lower().strip()
    slug = re.sub(r"[^a-z0-9\s-]", "", slug)
    slug = re.sub(r"[\s]+", "-", slug)
    return slug.strip("-")


def render_tree_to_repo(
    tree: TreeNode,
    documents: dict[str, Document],
    output_dir: Path,
) -> None:
    """Render a tree as folders with README.md files."""
    output_dir.mkdir(parents=True, exist_ok=True)
    _render_node(tree, documents, output_dir, is_root=True)


def _render_node(
    node: TreeNode,
    documents: dict[str, Document],
    parent_dir: Path,
    is_root: bool = False,
) -> None:
    """Recursively render a tree node."""
    if is_root:
        node_dir = parent_dir
    else:
        node_dir = parent_dir / slugify(node.title)
        node_dir.mkdir(parents=True, exist_ok=True)

    # Build README content
    lines = [f"# {node.title}\n"]
    if node.summary:
        lines.append(f"{node.summary}\n")

    # List children as links
    if node.children:
        lines.append("## Contents\n")
        for child in node.children:
            child_slug = slugify(child.title)
            lines.append(f"- [{child.title}](./{child_slug}/) — {child.summary}")
        lines.append("")

    # List linked documents
    if node.documents:
        lines.append("## Source Documents\n")
        for doc_id in node.documents:
            doc = documents.get(doc_id)
            if doc:
                lines.append(f"- **{doc.title or doc.doc_id}** — {doc.summary}")
                if doc.source_url:
                    lines.append(f"  [Source]({doc.source_url})")
            else:
                lines.append(f"- {doc_id}")
        lines.append("")

    readme = node_dir / "README.md"
    readme.write_text("\n".join(lines))

    # Recurse into children
    for child in node.children:
        _render_node(child, documents, node_dir)
```

**Step 3: Run tests**

```bash
cd knowledge && uv run pytest tests/test_github_renderer.py -v
```

Expected: PASS.

**Step 4: Commit**

```bash
git add knowledge/
git commit -m "feat: add GitHub repo renderer for knowledge tree"
```

---

### Task 9: Wire full pipeline in CLI

**Files:**
- Modify: `knowledge/src/isabl_knowledge/cli.py`

**Step 1: Update all CLI commands to use real implementations**

Update `cli.py` to wire `summarize`, `tree`, `publish`, and `build` commands with the real implementations, loading/saving `documents.json` and `tree.json` between steps.

**Step 2: Run end-to-end test with config**

```bash
cd knowledge
# Extract from gitbook only (doesn't need git clone)
uv run isabl-knowledge --config knowledge.yaml extract
# Check output
cat data/documents.json | python -m json.tool | head -20
```

**Step 3: Commit**

```bash
git add knowledge/
git commit -m "feat: wire full pipeline into CLI commands"
```

---

### Task 10: Knowledge MCP server

**Files:**
- Create: `knowledge/src/isabl_knowledge/mcp_server.py`
- Create: `knowledge/tests/test_mcp_server.py`

**Step 1: Write tests**

Create `knowledge/tests/test_mcp_server.py`:
```python
"""Tests for the knowledge MCP server."""

import json
from pathlib import Path

import pytest

from isabl_knowledge.mcp_server import create_knowledge_server


@pytest.fixture
def tree_data(tmp_path):
    """Create sample tree.json and documents.json for testing."""
    tree = {
        "id": "root",
        "title": "Isabl Platform",
        "summary": "Root",
        "children": [
            {
                "id": "0001",
                "title": "Querying Data",
                "summary": "How to query",
                "documents": ["cli/get_experiments"],
            },
        ],
    }
    docs = [
        {
            "doc_id": "cli/get_experiments",
            "source_type": "docstring",
            "source_url": "https://github.com/test",
            "content": "# get_experiments\n\nQuery experiments.",
            "title": "Query Experiments",
            "summary": "How to query experiments.",
            "tags": ["querying"],
            "questions": ["How do I get experiments?"],
            "metadata": {},
        },
    ]

    (tmp_path / "tree.json").write_text(json.dumps(tree))
    (tmp_path / "documents.json").write_text(json.dumps(docs))
    return tmp_path


def test_create_server(tree_data):
    """Test that the MCP server loads tree and documents."""
    server = create_knowledge_server(tree_data)
    assert server is not None
```

**Step 2: Implement MCP server**

Create `knowledge/src/isabl_knowledge/mcp_server.py`:
```python
"""Knowledge tree MCP server."""

from __future__ import annotations

import json
import logging
from pathlib import Path

from mcp.server.fastmcp import FastMCP

from isabl_knowledge.models import Document, TreeNode

logger = logging.getLogger(__name__)


def create_knowledge_server(data_dir: Path) -> FastMCP:
    """Create an MCP server that serves the knowledge tree."""
    mcp = FastMCP("Isabl Knowledge")

    # Load tree
    tree_file = data_dir / "tree.json"
    tree_data = json.loads(tree_file.read_text())
    tree = TreeNode(**tree_data)

    # Load documents
    docs_file = data_dir / "documents.json"
    docs_list = json.loads(docs_file.read_text())
    docs = {d["doc_id"]: Document(**d) for d in docs_list}

    # Build node index for fast lookup
    node_index: dict[str, TreeNode] = {}
    _index_nodes(tree, node_index)

    @mcp.tool()
    async def get_tree() -> dict:
        """Get the top-level knowledge tree with node summaries.

        Returns the root node with its immediate children.
        Use get_node() to drill into a specific branch.
        """
        return {
            "id": tree.id,
            "title": tree.title,
            "summary": tree.summary,
            "children": [
                {"id": c.id, "title": c.title, "summary": c.summary}
                for c in tree.children
            ],
        }

    @mcp.tool()
    async def get_node(node_id: str) -> dict:
        """Get a specific node's details, children, and linked documents.

        Args:
            node_id: The node ID (e.g., "0001", "0001.0002")
        """
        node = node_index.get(node_id)
        if not node:
            return {"error": f"Node {node_id} not found"}

        result = {
            "id": node.id,
            "title": node.title,
            "summary": node.summary,
        }

        if node.children:
            result["children"] = [
                {"id": c.id, "title": c.title, "summary": c.summary}
                for c in node.children
            ]

        if node.documents:
            result["documents"] = []
            for doc_id in node.documents:
                doc = docs.get(doc_id)
                if doc:
                    result["documents"].append({
                        "doc_id": doc.doc_id,
                        "title": doc.title,
                        "summary": doc.summary,
                        "tags": doc.tags,
                        "questions": doc.questions,
                    })

        return result

    @mcp.tool()
    async def get_document(doc_id: str) -> dict:
        """Get the full content of a source document.

        Args:
            doc_id: The document ID (e.g., "cli/get_experiments")
        """
        doc = docs.get(doc_id)
        if not doc:
            return {"error": f"Document {doc_id} not found"}
        return doc.model_dump()

    return mcp


def _index_nodes(node: TreeNode, index: dict[str, TreeNode]) -> None:
    """Recursively index all nodes by ID."""
    index[node.id] = node
    for child in node.children:
        _index_nodes(child, index)
```

**Step 3: Run tests**

```bash
cd knowledge && uv run pytest tests/test_mcp_server.py -v
```

Expected: PASS.

**Step 4: Wire `serve` command in CLI**

```python
@cli.command()
@click.option("--data-dir", "-d", default="output", type=click.Path(exists=True, path_type=Path))
@click.pass_context
def serve(ctx, data_dir: Path):
    """Start the knowledge MCP server."""
    from isabl_knowledge.mcp_server import create_knowledge_server
    server = create_knowledge_server(data_dir)
    click.echo("Starting Isabl Knowledge MCP server...")
    server.run()
```

**Step 5: Commit**

```bash
git add knowledge/
git commit -m "feat: add knowledge tree MCP server"
```
