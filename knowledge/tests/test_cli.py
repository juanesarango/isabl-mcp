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
