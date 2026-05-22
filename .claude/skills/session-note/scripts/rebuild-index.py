#!/usr/bin/env python3
"""Rebuild $VAULT/_index.md from notes in the vault.

$VAULT is resolved from SESSION_NOTES_DIR (fallback: $HOME/notes).

Walks $VAULT/{work,learning,reading,personal,idea}/*.md, parses YAML
frontmatter from each, validates structure, aggregates tags and entities,
and writes a fresh _index.md. The notes themselves are the source of truth.

Usage:
    rebuild-index.py            # rebuild + write _index.md
    rebuild-index.py --check    # validate only; exit 1 on any error or drift

Exit codes:
    0 — success (or --check passed)
    1 — validation errors, or --check found drift
"""

import argparse
import os
import re
import sys
from pathlib import Path

CATEGORIES = ["work", "learning", "reading", "personal", "idea"]
REQUIRED_FIELDS = {
    "title",
    "date",
    "source",
    "category",
    "tags",
    "entities",
    "status",
    "related",
}
FILENAME_RE = re.compile(r"^\d{4}-\d{2}-\d{2}-[a-z0-9][a-z0-9-]*\.md$")
FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---", re.DOTALL)
# Split on commas that are NOT inside a double-quoted segment.
LIST_SPLIT_RE = re.compile(r',(?=(?:[^"]*"[^"]*")*[^"]*$)')


def parse_inline_list(raw):
    """Parse a YAML-flavored inline list like '[a, b, "c d"]'. Return None if not a list."""
    raw = raw.strip()
    if not (raw.startswith("[") and raw.endswith("]")):
        return None
    inner = raw[1:-1].strip()
    if not inner:
        return []
    items = []
    for part in LIST_SPLIT_RE.split(inner):
        item = part.strip()
        if (item.startswith('"') and item.endswith('"')) or (
            item.startswith("'") and item.endswith("'")
        ):
            item = item[1:-1]
        if item:
            items.append(item)
    return items


def parse_frontmatter(text):
    """Return dict of frontmatter fields, or None if no frontmatter block."""
    m = FRONTMATTER_RE.match(text)
    if not m:
        return None
    fields = {}
    for line in m.group(1).splitlines():
        if not line.strip() or ":" not in line:
            continue
        key, _, raw = line.partition(":")
        key = key.strip()
        raw = raw.strip()
        as_list = parse_inline_list(raw)
        if as_list is not None:
            fields[key] = as_list
        else:
            if (raw.startswith('"') and raw.endswith('"')) or (
                raw.startswith("'") and raw.endswith("'")
            ):
                raw = raw[1:-1]
            fields[key] = raw
    return fields


def resolve_vault():
    path = os.environ.get("SESSION_NOTES_DIR") or str(Path.home() / "notes")
    return Path(path).expanduser()


def collect_and_validate(vault):
    """Walk the vault and return (notes, tags, entities, errors)."""
    notes = []
    tags_seen = []
    entities_seen = []
    errors = []

    for category in CATEGORIES:
        cat_dir = vault / category
        if not cat_dir.is_dir():
            continue
        for md_path in sorted(cat_dir.glob("*.md")):
            rel_path = f"{category}/{md_path.name}"
            text = md_path.read_text(encoding="utf-8")
            fm = parse_frontmatter(text)
            if fm is None:
                errors.append(f"{rel_path}: no frontmatter block")
                continue

            missing = REQUIRED_FIELDS - set(fm.keys())
            if missing:
                errors.append(
                    f"{rel_path}: missing required fields: {', '.join(sorted(missing))}"
                )
            if fm.get("category") and fm["category"] != category:
                errors.append(
                    f"{rel_path}: category field '{fm['category']}' does not match folder '{category}'"
                )
            if not FILENAME_RE.match(md_path.name):
                errors.append(
                    f"{rel_path}: filename does not match YYYY-MM-DD-kebab-slug.md"
                )

            for tag in fm.get("tags") or []:
                if tag not in tags_seen:
                    tags_seen.append(tag)
            for ent in fm.get("entities") or []:
                if ent not in entities_seen:
                    entities_seen.append(ent)
            notes.append(
                {
                    "date": fm.get("date", ""),
                    "category": category,
                    "title": fm.get("title", "(untitled)"),
                    "path": rel_path,
                }
            )

    return notes, tags_seen, entities_seen, errors


def render_index(notes, tags, entities):
    """Generate the _index.md content."""
    out = []
    out.append("# session-note index")
    out.append("")
    out.append("Auto-rebuilt from `$VAULT/<category>/*.md` by")
    out.append("`scripts/rebuild-index.py`. Do not edit by hand — your changes will")
    out.append("be overwritten on the next rebuild. The notes themselves are the")
    out.append("source of truth.")
    out.append("")
    out.append("## Categories")
    out.append("")
    for c in CATEGORIES:
        out.append(f"- {c}")
    out.append("")
    out.append("## Tags (lowercase, kebab-case)")
    out.append("")
    for t in sorted(tags):
        out.append(f"- {t}")
    out.append("")
    out.append("## Entities (proper-noun form, disambiguated as needed)")
    out.append("")
    for e in sorted(entities):
        out.append(f"- {e}")
    out.append("")
    out.append("## Notes (most-recent-first)")
    out.append("")
    sorted_notes = sorted(notes, key=lambda n: (n["date"], n["path"]), reverse=True)
    for n in sorted_notes:
        out.append(
            f"- {n['date']} — {n['category']} — {n['title']} → {n['path']}"
        )
    return "\n".join(out) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--check",
        action="store_true",
        help="Validate only. Exit 1 on any error or if _index.md is out of date.",
    )
    args = ap.parse_args()

    vault = resolve_vault()
    if not vault.exists():
        print(f"Vault does not exist: {vault}", file=sys.stderr)
        sys.exit(1)

    notes, tags, entities, errors = collect_and_validate(vault)

    if errors:
        print("Validation errors:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        sys.exit(1)

    new_content = render_index(notes, tags, entities)
    index_path = vault / "_index.md"

    if args.check:
        if not index_path.exists():
            print(f"_index.md missing at {index_path}", file=sys.stderr)
            sys.exit(1)
        current = index_path.read_text(encoding="utf-8")
        if current != new_content:
            print(
                f"_index.md is out of date at {index_path} "
                f"(run rebuild-index.py without --check to refresh)",
                file=sys.stderr,
            )
            sys.exit(1)
        print(
            f"OK: {len(notes)} notes, {len(tags)} tags, {len(entities)} entities "
            f"(index in sync)"
        )
    else:
        index_path.write_text(new_content, encoding="utf-8")
        print(
            f"_index.md rebuilt: {len(notes)} notes, "
            f"{len(tags)} tags, {len(entities)} entities"
        )


if __name__ == "__main__":
    main()
