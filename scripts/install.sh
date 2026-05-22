#!/usr/bin/env bash
# Idempotent installer for personal Claude Code settings.
#
# Usage:
#   ./scripts/install.sh                # full: link every skill / command / agent
#                                       # under .claude/ into ~/.claude/
#   ./scripts/install.sh <skill_name>   # single: link only that one skill
#
# Notes:
#   - Items are symlinked one by one into ~/.claude/<subdir>/<name>.
#     The whole ~/.claude/ directory is never replaced, so anything you
#     already have there (settings.local.json, projects/, other skills, etc.)
#     stays put.
#   - Idempotent. Already-correct symlinks are left alone. Conflicting real
#     files or wrong-target symlinks get a timestamped .backup before the
#     new symlink is created.
#   - .claude/settings.json is intentionally NOT symlinked: Claude Code may
#     rewrite the file via delete-then-recreate, which would silently
#     replace the symlink with a real file. Copy it manually if you want.

set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TARGET_DIR="${HOME}/.claude"

link_one() {
  local src="$1"
  local dest="$2"

  if [[ -L "$dest" ]]; then
    local current
    current="$(readlink "$dest")"
    if [[ "$current" == "$src" ]]; then
      echo "= $dest -> $src (already linked)"
      return
    fi
    echo "~ $dest is a symlink to $current; backing up"
    mv "$dest" "$dest.backup.$(date +%s)"
  elif [[ -e "$dest" ]]; then
    echo "~ $dest exists; backing up"
    mv "$dest" "$dest.backup.$(date +%s)"
  fi

  ln -s "$src" "$dest"
  echo "+ $dest -> $src"
}

install_skill() {
  local name="$1"
  local src="$REPO_DIR/.claude/skills/$name"
  if [[ ! -d "$src" ]]; then
    echo "Error: skill '$name' not found at $src" >&2
    exit 1
  fi
  mkdir -p "$TARGET_DIR/skills"
  link_one "$src" "$TARGET_DIR/skills/$name"
}

install_full() {
  local subdir src_root item name
  for subdir in skills commands agents; do
    src_root="$REPO_DIR/.claude/$subdir"
    [[ -d "$src_root" ]] || continue
    mkdir -p "$TARGET_DIR/$subdir"
    shopt -s nullglob
    for item in "$src_root"/*; do
      name="$(basename "$item")"
      link_one "$item" "$TARGET_DIR/$subdir/$name"
    done
    shopt -u nullglob
  done
}

if [[ $# -eq 0 ]]; then
  install_full
else
  install_skill "$1"
fi

cat <<'EOF'

Done.

Reminders:
  - Set SESSION_NOTES_DIR in your shell rc (~/.bashrc or ~/.zshrc) to your
    notes vault path, then open a new shell or `source` the rc:
      export SESSION_NOTES_DIR="$HOME/path/to/your/notes"
  - .claude/settings.json is NOT auto-symlinked. If you want it as your
    user-level config, copy it manually:
      cp "<repo>/.claude/settings.json" ~/.claude/settings.json
EOF
