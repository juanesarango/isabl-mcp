#!/bin/bash
# Install Isabl skills for Claude Code (standalone)
#
# Preferred method: /plugin install github:juanesarango/isabl-skills
#   (installs MCP server + skills together)
#
# This script installs skills only. For MCP tools, also run:
#   claude mcp add isabl -- uvx isabl-mcp
#
# Usage: curl -fsSL https://raw.githubusercontent.com/juanesarango/isabl-skills/main/scripts/install.sh | bash

set -e

REPO="juanesarango/isabl-skills"
BRANCH="main"
SKILLS_DIR="$HOME/.claude/skills/isabl"
BASE_URL="https://raw.githubusercontent.com/$REPO/$BRANCH/skills"

# Skills to install
SKILLS=(
    "isabl-write-app.md"
    "isabl-debug-analysis.md"
    "isabl-query-data.md"
    "isabl-project-report.md"
    "isabl-merge-results.md"
    "isabl-submit-data.md"
    "isabl-monitor-analyses.md"
    "isabl-run-pipeline.md"
)

echo "Isabl Skills Installer"
echo "======================"
echo ""

# Create directory
mkdir -p "$SKILLS_DIR"

# Download each skill
echo "Installing ${#SKILLS[@]} skills to $SKILLS_DIR..."
echo ""

for skill in "${SKILLS[@]}"; do
    if curl -fsSL "$BASE_URL/$skill" -o "$SKILLS_DIR/$skill" 2>/dev/null; then
        echo "✓ $skill"
    else
        echo "✗ Failed to download $skill"
    fi
done

echo ""
echo "Done! Skills installed to $SKILLS_DIR"
echo ""
echo "Usage in Claude Code:"
echo "  /isabl-write-app       - Create a new Isabl application"
echo "  /isabl-debug-analysis  - Debug a failed analysis"
echo "  /isabl-query-data      - Query data from Isabl API"
echo "  /isabl-project-report  - Generate project status reports"
echo "  /isabl-merge-results   - Aggregate results across analyses"
echo "  /isabl-submit-data     - Submit new sequencing data"
echo "  /isabl-monitor-analyses - Track analysis status"
echo "  /isabl-run-pipeline    - Run multiple apps as pipeline"
echo ""
echo "To update, run this command again."
