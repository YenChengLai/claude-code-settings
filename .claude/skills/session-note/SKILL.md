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
forgotten the details" can still understand, and appends it to a single central
vault. The value of notes comes from accumulation and consistency, so this
skill's most important job is to **enforce consistent frontmatter on every note**,
so that future indexing, search, and knowledge-graph features can all be rebuilt
from the files themselves without ever going back to fill in missing data.

## Where notes go (read this first)

Notes are NEVER written to the current project's `./notes/`. They are always
written to a single fixed vault so knowledge accumulates in one place.

Resolve the destination directory in this order:
1. The environment variable `SESSION_NOTES_DIR`, if set.
2. Otherwise, fall back to `~/notes`.

Treat the resolved path as `$VAULT`. Write every note under `$VAULT/`. Create
`$VAULT/` if it does not exist. Never write notes into the project working
directory, regardless of which project the session is running in.

## When to trigger

User-initiated only; never run automatically. Trigger phrases include: "note
this session", "take a note", "session note", "/note", "summarize and save".
The user keeps the judgment of "is this worth keeping" — the skill only does the
writing.

## Steps

1. **Review the session.** Read the conversation so far. Identify the main
   problem and any sub-problems that came up along the way. Distill — do not
   transcribe the whole conversation.

2. **Resolve `$VAULT`.** Read `SESSION_NOTES_DIR`; fall back to `~/notes`.
   Create the directory if needed.

3. **Classify.** Decide `category`: one of `work` / `learning` / `reading` /
   `personal` / `idea`. If genuinely unclear, ask the user one short question.

4. **Extract structured fields.** This is the core of the skill and must not be
   skipped:
   - `title`: one-line description, recognizable at a glance later.
   - `tags`: 3–6 lowercase topic tags for cross-note classification.
   - `entities`: concrete technical terms / concepts / tools / people that
     appeared (these become the nodes of a future knowledge graph).
   - `status`: `resolved` / `open` / `partial` / `reference`.
   - `related`: leave as an empty array `[]`; a future tool fills this in.

5. **Write the body** using this fixed structure (omit a section if empty, but
   keep the order):
   - `## Problem / context` — what the user was trying to solve.
   - `## Conclusion / solution` — the final answer (most-read section later).
   - `## Key concepts` — durable principles, mental models, gotchas worth keeping.
   - `## Follow-ups` — open items as `- [ ]` checkboxes.
   - `## Source` — a link to the session, or 1–2 quoted key excerpts.

6. **Pick the filename:** `$VAULT/YYYY-MM-DD-kebab-case-slug.md`. Build the slug
   from a few key English words in the title. The date prefix keeps files
   naturally sorted by time.

7. **Write the file.** Frontmatter + body. One session = one new file; never
   append to an existing note.

8. **Report back.** Tell the user the filename and a one-line summary, then stop.
   Do not over-explain.

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

## Design principles

- **Distill, don't transcribe.** The note is for future-you who has forgotten the
  details; it must stand on its own.
- **Never skimp on frontmatter.** The body can be long or short, but the
  structured fields must be complete and consistent every single time — that
  consistency is the one precondition for ever building an index or knowledge
  graph on top of these notes.
- **Plain text, free, portable.** Produce only markdown. No database, no paid
  service, no project-local state.
- **Single destination.** Always write to `$VAULT`, never the current project.
  Scattered notes cannot accumulate into knowledge.
- **Don't over-engineer.** No category folders, no index files, no search inside
  this skill — those are downstream concerns for after the data has accumulated.
  Adding them now only raises the friction of recording.
