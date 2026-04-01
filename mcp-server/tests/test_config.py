"""Tests for configuration and token resolution."""

import json
import pytest
from unittest.mock import patch

from isabl_mcp.config import (
    _resolve_token,
    _resolve_url_and_token,
    _DEFAULT_API_URL,
    Settings,
)


class TestTokenResolution:
    def test_explicit_token_takes_precedence(self, tmp_path):
        """Env var token wins over settings.json."""
        settings_file = tmp_path / "settings.json"
        settings_file.write_text(json.dumps({
            "http://localhost:8000/api/v1/": {"api_token": "file-token"}
        }))

        with patch("isabl_mcp.config.ISABL_SETTINGS_PATH", settings_file):
            result = _resolve_token("http://localhost:8000/api/v1/", "env-token")

        assert result == "env-token"

    def test_falls_back_to_settings_file(self, tmp_path):
        """When no env token, reads from settings.json."""
        settings_file = tmp_path / "settings.json"
        settings_file.write_text(json.dumps({
            "http://localhost:8000/api/v1/": {"api_token": "file-token"}
        }))

        with patch("isabl_mcp.config.ISABL_SETTINGS_PATH", settings_file):
            result = _resolve_token("http://localhost:8000/api/v1/", "")

        assert result == "file-token"

    def test_trailing_slash_matching(self, tmp_path):
        """URL matching works with or without trailing slash."""
        settings_file = tmp_path / "settings.json"
        settings_file.write_text(json.dumps({
            "http://localhost:8000/api/v1/": {"api_token": "file-token"}
        }))

        with patch("isabl_mcp.config.ISABL_SETTINGS_PATH", settings_file):
            result = _resolve_token("http://localhost:8000/api/v1", "")

        assert result == "file-token"

    def test_no_settings_file(self, tmp_path):
        """Returns empty string when settings.json doesn't exist."""
        missing = tmp_path / "nonexistent" / "settings.json"

        with patch("isabl_mcp.config.ISABL_SETTINGS_PATH", missing):
            result = _resolve_token("http://localhost:8000/api/v1/", "")

        assert result == ""

    def test_no_matching_url(self, tmp_path):
        """Returns empty when URL not in settings.json."""
        settings_file = tmp_path / "settings.json"
        settings_file.write_text(json.dumps({
            "https://prod.isabl.io/api/v1/": {"api_token": "prod-token"}
        }))

        with patch("isabl_mcp.config.ISABL_SETTINGS_PATH", settings_file):
            result = _resolve_token("http://localhost:8000/api/v1/", "")

        assert result == ""

    def test_malformed_settings_file(self, tmp_path):
        """Handles corrupt settings.json gracefully."""
        settings_file = tmp_path / "settings.json"
        settings_file.write_text("not valid json{{{")

        with patch("isabl_mcp.config.ISABL_SETTINGS_PATH", settings_file):
            result = _resolve_token("http://localhost:8000/api/v1/", "")

        assert result == ""


class TestUrlAndTokenAutoDiscovery:
    def test_auto_discovers_url_and_token(self, tmp_path):
        """When no env vars set, discovers both URL and token from settings.json."""
        settings_file = tmp_path / "settings.json"
        settings_file.write_text(json.dumps({
            "https://prod.isabl.io/api/v1/": {"api_token": "prod-token"}
        }))

        with (
            patch("isabl_mcp.config.ISABL_SETTINGS_PATH", settings_file),
            patch.dict("os.environ", {}, clear=True),
        ):
            url, token = _resolve_url_and_token(_DEFAULT_API_URL, "")

        assert url == "https://prod.isabl.io/api/v1/"
        assert token == "prod-token"

    def test_explicit_env_url_skips_auto_discovery(self, tmp_path):
        """When ISABL_API_URL is set, don't auto-discover URL."""
        settings_file = tmp_path / "settings.json"
        settings_file.write_text(json.dumps({
            "https://prod.isabl.io/api/v1/": {"api_token": "prod-token"}
        }))

        with (
            patch("isabl_mcp.config.ISABL_SETTINGS_PATH", settings_file),
            patch.dict("os.environ", {"ISABL_API_URL": "http://custom:8000/api/v1/"}, clear=True),
        ):
            url, token = _resolve_url_and_token("http://custom:8000/api/v1/", "")

        # URL stays as given, token not found for custom URL
        assert url == "http://custom:8000/api/v1/"
        assert token == ""

    def test_explicit_token_skips_file(self, tmp_path):
        """When ISABL_API_TOKEN is set, don't read settings.json."""
        settings_file = tmp_path / "settings.json"
        settings_file.write_text(json.dumps({
            "https://prod.isabl.io/api/v1/": {"api_token": "prod-token"}
        }))

        with patch("isabl_mcp.config.ISABL_SETTINGS_PATH", settings_file):
            url, token = _resolve_url_and_token(_DEFAULT_API_URL, "my-env-token")

        assert url == _DEFAULT_API_URL
        assert token == "my-env-token"

    def test_multi_url_uses_first_and_warns(self, tmp_path):
        """When multiple URLs in settings.json, uses first and logs warning."""
        settings_file = tmp_path / "settings.json"
        settings_file.write_text(json.dumps({
            "https://prod.isabl.io/api/v1/": {"api_token": "prod-token"},
            "https://staging.isabl.io/api/v1/": {"api_token": "staging-token"},
        }))

        with (
            patch("isabl_mcp.config.ISABL_SETTINGS_PATH", settings_file),
            patch.dict("os.environ", {}, clear=True),
        ):
            url, token = _resolve_url_and_token(_DEFAULT_API_URL, "")

        # Uses first entry
        assert url == "https://prod.isabl.io/api/v1/"
        assert token == "prod-token"

    def test_empty_settings_file(self, tmp_path):
        """Empty settings.json returns defaults."""
        settings_file = tmp_path / "settings.json"
        settings_file.write_text("{}")

        with (
            patch("isabl_mcp.config.ISABL_SETTINGS_PATH", settings_file),
            patch.dict("os.environ", {}, clear=True),
        ):
            url, token = _resolve_url_and_token(_DEFAULT_API_URL, "")

        assert url == _DEFAULT_API_URL
        assert token == ""


class TestSettings:
    def test_settings_auto_discovers_from_file(self, tmp_path):
        """Settings model auto-discovers URL and token from settings.json."""
        settings_file = tmp_path / "settings.json"
        settings_file.write_text(json.dumps({
            "https://prod.isabl.io/api/v1/": {"api_token": "auto-token"}
        }))

        with (
            patch("isabl_mcp.config.ISABL_SETTINGS_PATH", settings_file),
            patch.dict("os.environ", {}, clear=True),
        ):
            s = Settings()

        assert s.api_url == "https://prod.isabl.io/api/v1/"
        assert s.api_token == "auto-token"

    def test_settings_env_overrides_file(self, tmp_path):
        """Env vars take precedence over settings.json."""
        settings_file = tmp_path / "settings.json"
        settings_file.write_text(json.dumps({
            "https://prod.isabl.io/api/v1/": {"api_token": "file-token"}
        }))

        with (
            patch("isabl_mcp.config.ISABL_SETTINGS_PATH", settings_file),
            patch.dict("os.environ", {
                "ISABL_API_URL": "http://custom:8000/api/v1/",
                "ISABL_API_TOKEN": "env-token",
            }, clear=True),
        ):
            s = Settings()

        assert s.api_url == "http://custom:8000/api/v1/"
        assert s.api_token == "env-token"
