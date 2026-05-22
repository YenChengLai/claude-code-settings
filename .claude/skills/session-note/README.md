# Session Note skill

Trigger an AI to distill the current session into one structured markdown note,
written to a single central vault — not into whatever project you happen to be in.

Design intent: **low recording friction + strictly consistent structure.** The
power of notes comes from accumulation; accumulation requires that recording stay
effortless and that everything land in one place. Future indexing, search, and a
knowledge graph are all rebuildable from each note's consistent frontmatter.

---

## Install (user level — does not touch your team's project setup)

Claude Code loads skills from two independent sources at once:

- User level: `~/.claude/skills/` — applies to every session, every project.
- Project level: `<project>/.claude/skills/` — e.g. your team's
  `everything-ai-tools` symlink created by `setup.sh`.

This skill is personal, so install it at the user level. It then works
everywhere, and it never mixes with — or gets clobbered by — the team's
project-level `setup.sh` symlinks.

```bash
# Clone or place this folder somewhere stable, e.g. ~/tools/session-note
mkdir -p ~/.claude/skills
ln -s ~/tools/session-note ~/.claude/skills/session-note
```

For Antigravity, point its skill-loading path at the same folder (or symlink it
the same way). One `SKILL.md`, both tools.

### Do I need to install it per project?

No. Because it lives at the user level, you install it once and it is available
in every project and even in sessions with no project open. It follows *you*, not
a repo — which is exactly right for a personal productivity tool. (Your team's
`setup.sh` is project-level by design, because team conventions bind to a
specific repo. This skill is the opposite case.)

---

## Set your vault location (one environment variable)

The skill writes every note to a fixed vault, resolved from `SESSION_NOTES_DIR`,
falling back to `~/notes`. Point it at whatever you want to be your single home
for notes — ideally a Git repo or an Obsidian vault:

```bash
# in ~/.bashrc / ~/.zshrc
export SESSION_NOTES_DIR="$HOME/obsidian/ai-notes"
```

Why an env var instead of hard-coding the path in the skill:

- The skill stays free of your personal paths (clean to share later).
- Switching machines means changing one variable, not editing the skill.
- The vault is just a folder of markdown — make it an Obsidian vault, a Git repo,
  or both, and it syncs / versions for free.

Recommended: `git init` the vault and push to GitHub, or open it as an Obsidian
vault. Either way the skill keeps writing plain `.md` files into it.

---

## Use

In any session, when you've reached a point worth keeping:

> note this session

or

> /note

The AI reviews the session, distills the main and sub-problems, writes one note
into your vault, and reports the filename plus a one-line summary. One session,
one file.

---

## What a note looks like

A markdown file with YAML frontmatter on top and a fixed body structure below.
See `examples/2026-05-21-eventlet-asyncio-deadlock.md`.

The frontmatter fields are the foundation — keep them complete every time:

| Field | Purpose | Future use |
|-------|---------|------------|
| `title` | one-line title | list / search display |
| `date` | date | timeline sorting |
| `source` | originating tool | source filtering |
| `category` | top-level class | folders / filtering |
| `tags` | topic tags | cross-note classification |
| `entities` | concrete terms | **knowledge-graph nodes** |
| `status` | resolution state | finding open problems |
| `related` | linked notes | **knowledge-graph edges** |

---

## Future extensions (all downstream — don't build them now)

Because every note has identical structure, each of these can later be a small
standalone tool that scans `$VAULT/`:

1. Index / full-text search — parse all frontmatter into an `INDEX.md`, or wire
   up `ripgrep`.
2. Semantic search — embed each note for fuzzy queries.
3. Auto-linking — on write, compare `entities` / `tags` overlap and backfill the
   `related` field. Once this runs, the graph's edges grow on their own.
4. Knowledge-graph view — feed `entities` (nodes) + `related` (edges) into
   Cytoscape.js / D3.
5. Periodic review — scan notes with `date` in the last 7 days and have the AI
   produce a weekly recap.

The point: none of these change how you record today. Accumulate first; build a
given feature only when you actually feel the need for that one.
