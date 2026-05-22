---
name: session-note
description: >
  Distill the current AI session — the main problem and any sub-problems explored
  so far — into a single markdown note with structured frontmatter, then write it
  to a fixed personal notes vault. Use when the user says "note this session",
  "take a note", "session note", "/note", "summarize this and save it", or similar.
  Works in any project or with no project. Not limited to work: also covers
  learning, reading, personal growth, and ideas. The note is always written to one
  central vault, never to the current project's directory.
---

# Session Note skill

## What this skill does

Distills the current session into one durable note that "future you, who has
forgotten the details" can still understand, and writes it into a single
central vault. The value of notes comes from accumulation and **consistency** —
consistent frontmatter, consistent vocabulary (so tags and entities aggregate
across notes), and consistent placement. The skill enforces all three so that
future indexing, search, and knowledge-graph features can be rebuilt from the
files themselves without ever going back to fill in missing data.

## Where notes go (read this first)

Notes are NEVER written to the current project's `./notes/`. They are always
written to a single fixed vault so knowledge accumulates in one place.

Resolve the destination directory:
1. The environment variable `SESSION_NOTES_DIR`, if set.
2. Otherwise, fall back to `~/notes`.

Treat the resolved path as `$VAULT`. Within `$VAULT`, notes live under five
category subdirectories — one per `category` value:

- `$VAULT/work/`
- `$VAULT/learning/`
- `$VAULT/reading/`
- `$VAULT/personal/`
- `$VAULT/idea/`

Create the relevant subdirectory on demand. Never write notes into the project
working directory, regardless of which project the session is running in.

## The vault index (`$VAULT/_index.md`)

`_index.md` is the controlled-vocabulary view this skill reads on every
trigger. It contains:

- **Active vocabulary** for `tags` and `entities`. Reuse existing terms first;
  only introduce new ones when no existing term fits.
- **Recent notes list** so you can detect when the current session overlaps
  with a prior note and offer to update it.

**Notes are the canonical data; `_index.md` is a derived view.** Two pieces of
machinery keep them aligned:

1. **The skill's per-trigger fast path** (step 10 below): a best-effort
   incremental update of `_index.md` so that the next trigger immediately
   sees the new tags / entities. Fast, AI-driven, may drift slightly.
2. **The rebuild script** (`scripts/rebuild-index.py`, sitting next to this
   SKILL.md): deterministically regenerates `_index.md` from all notes,
   sorts and deduplicates entries, and validates that every note has a
   well-formed frontmatter block, the right category, and a conformant
   filename. `sync.sh` in the vault runs this before every push — so any
   drift the skill introduced gets normalized, and broken notes block the
   push entirely.

Net effect: AI mutations to `_index.md` are a cache, not a contract.
Don't agonize over them.

If `_index.md` does not exist (fresh vault), create a minimal skeleton with
empty Tags / Entities / Notes sections — the next rebuild will populate it.

## When to trigger

User-initiated only; never run automatically. Trigger phrases include: "note
this session", "take a note", "session note", "/note", "summarize and save".
The user keeps the judgment of "is this worth keeping" — the skill only does
the writing.

## Steps

1. **Resolve `$VAULT`.** Read `SESSION_NOTES_DIR`; fall back to `~/notes`.
   Create the directory if needed.

2. **Read `$VAULT/_index.md`.** Initialize it from the skeleton above if it
   doesn't exist. Note the active tags, entities, and the recent notes list.

3. **Review the session.** Read the conversation so far. Identify the main
   problem and any sub-problems. Distill — do not transcribe.

4. **Check for an existing note to update.** Look at the most-recent entry in
   the Notes section of `_index.md`. If its topic clearly overlaps with the
   current session, ask the user:

   > Found a related recent note: "<title>" at `<path>`. Do you want to
   > **update** that note, or start a **new** one?

   - If the user picks **update**, load the existing file and treat this as
     an update of the same note.
   - If the user picks **new**, or there is no plausible overlap, proceed to
     create a new note.

5. **Classify.** Pick `category`: one of `work` / `learning` / `reading` /
   `personal` / `idea`. To stay consistent with past classifications, lean on
   how similar topics appear in the Notes section of `_index.md`. Ask one
   short question only if genuinely ambiguous.

6. **Extract structured fields** — **prefer existing vocabulary from
   `_index.md`**:
   - `title`: one-line description, recognizable at a glance later.
   - `tags`: 3–6 entries. Reuse existing tags where possible; only introduce
     a new tag if no existing one fits. Lowercase, kebab-case, ≤3 words.
   - `entities`: concrete technical terms / concepts / tools / people that
     appeared. Reuse existing entity names where possible; otherwise
     introduce a new one in its natural proper-noun form (disambiguate when
     two distinct things would otherwise collide).
   - `status`: `resolved` / `open` / `partial` / `reference`.
   - `related`: leave as `[]`; a future tool will fill it in.

7. **Write the body** with this fixed structure (omit a section if empty,
   but keep the order):
   - `## Problem / context`
   - `## Conclusion / solution`
   - `## Key concepts`
   - `## Follow-ups` (open items as `- [ ]` checkboxes)
   - `## Source` (session link or 1–2 quoted excerpts)

8. **Filename and path.**
   - **New note:** `$VAULT/<category>/YYYY-MM-DD-kebab-slug.md`. Build the
     slug from a few key English words in the title. If the filename
     collides, modify the slug to be unique (e.g., append a short suffix).
   - **Update:** reuse the existing file's path; do not rename.

9. **Write or rewrite the file.** Frontmatter + body.
   - **New:** create it fresh.
   - **Update:** rewrite the existing file as a coherent unified note that
     merges the new session's information with what was already there. Do
     **not** append — merge.

10. **Update `_index.md` (fast-path cache).** Apply exactly these three
    structured mutations — nothing else. Do NOT reorder, deduplicate, or
    "clean up" the file; that's the rebuild script's job.

    a. For each tag in the new note that is not already in the Tags section,
       append it as a new bullet at the end of that section.
    b. For each entity in the new note that is not already in the Entities
       section, append it as a new bullet at the end of that section.
    c. In the Notes section, insert a new line at the top (for a new note),
       or rewrite the existing line in place (for an update). Format:
       `- YYYY-MM-DD — <category> — <title> → <category>/<slug>.md`

    The next time `sync.sh` runs (before push), `rebuild-index.py` will
    normalize order, deduplicate, and validate the whole vault. So the goal
    here is just to keep `_index.md` useful for the *next* trigger before
    the next sync — not to perfectly maintain it.

11. **Report back.** Tell the user the filename, whether this was a new note
    or an update, and a one-line summary. Then stop. Do not over-explain.

## Frontmatter spec (field names are strict — keep them identical every time)

```yaml
---
title: <one-line title>
date: <YYYY-MM-DD>
source: <claude-code | antigravity | claude-web | other>
category: <work | learning | reading | personal | idea>
tags: [tag1, tag2, tag3]
entities: ["concrete term 1", "concrete term 2"]
status: <resolved | open | partial | reference>
related: []
---
```

`date` is the original creation date and stays unchanged across updates.

## Design principles

- **Distill, don't transcribe.** The note is for future-you who has forgotten
  the details; it must stand on its own.
- **Never skimp on frontmatter.** The body can be long or short, but the
  structured fields must be complete and consistent every single time — that
  consistency is the one precondition for ever building an index or knowledge
  graph on top of these notes.
- **Plain text, free, portable.** Produce only markdown. No database, no paid
  service, no project-local state.
- **Single destination.** Always write to `$VAULT`, never the current project.
  Scattered notes cannot accumulate into knowledge.
- **Single index, explicit vocabulary, mechanical sync.** Tags and entities
  live in one `_index.md` that the rebuild script derives deterministically
  from all notes. The skill's per-trigger updates to it are a best-effort
  cache; the script is the source of truth. This avoids drift (`notetaking`
  vs `note-taking` vs `notes`) that would otherwise quietly break aggregation.
- **Don't over-engineer downstream features.** No full-text search,
  embeddings, or knowledge-graph view inside this skill — those are
  downstream concerns for after the data has accumulated. The frontmatter
  spec and the index file are the only structural commitments; everything
  else can be added when actually needed.
