#!/usr/bin/env bash
# setup-skills.sh — Link Hermes skills from repo into AppData
#
# Run this after cloning hermes-outreach on a fresh machine.
# Creates directory junctions so Hermes finds skills in the repo
# while they appear to live in the standard AppData location.
#
# Usage:  bash scripts/setup-skills.sh
#         (no sudo needed — junctions are user-level)

set -euo pipefail

# ---- paths ----
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
HERMES_SKILLS="${HERMES_HOME:-$HOME/.hermes}/skills"

# ---- helpers ----
junction() {
  local name="$1"      # skill name (e.g. funnel-audit-session)
  local category="$2"  # "" for standalone, "productivity" or "software-development"

  local target="$REPO_ROOT/skills/$name"
  local linkto="$HERMES_SKILLS"

  if [ -n "$category" ]; then
    linkto="$linkto/$category"
    mkdir -p "$linkto"
  fi
  linkto="$linkto/$name"

  # Remove if it exists and is a real directory (not a junction)
  if [ -d "$linkto" ] && [ ! -L "$linkto" ]; then
    echo "Removing existing directory: $linkto"
    rm -rf "$linkto"
  fi

  if [ -L "$linkto" ] || [ -d "$linkto" ]; then
    echo "  ✅  Already linked: $name"
    return
  fi

  # Convert to Windows-native paths for PowerShell
  local win_linkto
  local win_target
  win_linkto=$(echo "$linkto" | sed 's|^/c/|C:\\|; s|/|\\|g')
  win_target=$(echo "$target" | sed 's|^/c/|C:\\|; s|/|\\|g')

  echo "  🔗  Linking $name → $target"
  powershell.exe -Command "New-Item -ItemType Junction -Path \"$win_linkto\" -Target \"$win_target\" -Force" > /dev/null
}

echo "=== Hermes Outreach — Skill Setup ==="
echo ""

# ---- standalone ----
junction "funnel-audit-session" ""

# ---- productivity category ----
junction "cold-outreach-pipeline" "productivity"

# ---- software-development category ----
junction "haytham-email-draft" "software-development"
junction "pipeline-tick" "software-development"
junction "git-recovery" "software-development"
junction "project-bootstrapping" "software-development"

echo ""
echo "=== Done. Verify with: hermes skills list ==="