"""CLI for the Isabl knowledge tree pipeline."""

import json
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
        except Exception as e:
            click.echo(f"  → Skipped: {e}")

    out_file = output_dir / "documents.json"
    out_file.write_text(json.dumps([d.model_dump() for d in all_docs], indent=2))
    click.echo(f"\nTotal: {len(all_docs)} documents saved to {out_file}")


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
    """Run the full pipeline: extract -> summarize -> tree -> publish."""
    ctx.invoke(extract)
    ctx.invoke(summarize)
    ctx.invoke(tree)
    ctx.invoke(publish)


@cli.command()
@click.pass_context
def serve(ctx):
    """Start the knowledge MCP server."""
    click.echo("MCP server not yet implemented.")
