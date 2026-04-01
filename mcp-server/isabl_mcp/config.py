"""Configuration for Isabl MCP Server."""

from __future__ import annotations

import json
import logging
import os
from pathlib import Path
from typing import Any, Dict, Tuple

from pydantic_settings import BaseSettings

logger = logging.getLogger(__name__)

ISABL_SETTINGS_PATH = Path.home() / ".isabl" / "settings.json"

# Sentinel to detect when api_url was NOT explicitly set by the user
_DEFAULT_API_URL = "http://localhost:8000/api/v1/"


def _load_isabl_settings() -> Dict[str, Any]:
    """Load ~/.isabl/settings.json if it exists."""
    if ISABL_SETTINGS_PATH.exists():
        try:
            return json.loads(ISABL_SETTINGS_PATH.read_text())
        except (json.JSONDecodeError, OSError) as e:
            logger.debug("Could not read %s: %s", ISABL_SETTINGS_PATH, e)
    return {}


def _resolve_token(api_url: str, explicit_token: str) -> str:
    """Resolve API token: env var first, then ~/.isabl/settings.json."""
    if explicit_token:
        return explicit_token

    isabl_settings = _load_isabl_settings()

    # Try exact match first, then try with/without trailing slash
    for url_variant in [api_url, api_url.rstrip("/") + "/", api_url.rstrip("/")]:
        entry = isabl_settings.get(url_variant)
        if isinstance(entry, dict) and entry.get("api_token"):
            logger.info("Using API token from %s for %s", ISABL_SETTINGS_PATH, url_variant)
            return entry["api_token"]

    return ""


def _resolve_url_and_token(
    api_url: str, explicit_token: str
) -> Tuple[str, str]:
    """Resolve both API URL and token from ~/.isabl/settings.json.

    If ISABL_API_URL is not set (uses default) and settings.json has exactly
    one entry, use that URL and its token. Otherwise, resolve token for the
    given URL.
    """
    url_from_env = os.environ.get("ISABL_API_URL", "")

    if explicit_token:
        return api_url, explicit_token

    isabl_settings = _load_isabl_settings()

    # If URL was not explicitly set and settings.json has entries, auto-discover
    if not url_from_env and api_url == _DEFAULT_API_URL and isabl_settings:
        # Filter to entries that have a valid api_token
        valid_entries = {
            url: entry
            for url, entry in isabl_settings.items()
            if isinstance(entry, dict) and entry.get("api_token")
        }

        if len(valid_entries) == 1:
            first_url = next(iter(valid_entries))
            logger.info(
                "Auto-discovered API URL and token from %s: %s",
                ISABL_SETTINGS_PATH,
                first_url,
            )
            return first_url, valid_entries[first_url]["api_token"]
        elif len(valid_entries) > 1:
            urls = list(valid_entries.keys())
            first_url = urls[0]
            logger.warning(
                "Multiple Isabl instances found in %s: %s. "
                "Using first: %s. Set ISABL_API_URL to choose a specific one.",
                ISABL_SETTINGS_PATH,
                ", ".join(urls),
                first_url,
            )
            return first_url, valid_entries[first_url]["api_token"]

    # Otherwise resolve token for the explicit URL
    token = _resolve_token(api_url, "")
    return api_url, token


class Settings(BaseSettings):
    """MCP Server settings loaded from environment variables.

    Auto-discovery order:
        1. ISABL_API_URL / ISABL_API_TOKEN environment variables
        2. ~/.isabl/settings.json (URL and token auto-discovered)

    Environment variables:
        ISABL_API_URL: Isabl API base URL
        ISABL_API_TOKEN: Authentication token
        ISABL_VERIFY_SSL: Whether to verify SSL certificates
        ISABL_TIMEOUT: HTTP request timeout in seconds
        ISABL_LOG_LEVEL: Logging level (DEBUG, INFO, WARNING, ERROR)
    """

    # Isabl API configuration
    api_url: str = _DEFAULT_API_URL
    api_token: str = ""

    # HTTP client settings
    verify_ssl: bool = True
    timeout: int = 30

    # Logging
    log_level: str = "INFO"

    model_config = {
        "env_prefix": "ISABL_",
        "env_file": ".env",
        "extra": "ignore",
    }

    def model_post_init(self, __context: Any) -> None:
        """Auto-discover URL and token from ~/.isabl/settings.json."""
        url, token = _resolve_url_and_token(self.api_url, self.api_token)
        if url != self.api_url:
            object.__setattr__(self, "api_url", url)
        if token and not self.api_token:
            object.__setattr__(self, "api_token", token)

    @property
    def isabl_api_url(self) -> str:
        return self.api_url

    @property
    def isabl_api_token(self) -> str:
        return self.api_token


settings = Settings()
