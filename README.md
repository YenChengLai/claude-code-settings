# claude-code-settings

Personal Claude Code environment settings, designed to be installed across
multiple machines (work, home) at varying granularity — full overlay at home,
single-skill mount at work.

## What's in here

- `.claude/skills/session-note/` — distill the current AI session into a single
  structured markdown note in a fixed vault. See
  [its README](.claude/skills/session-note/README.md).
- `scripts/install.sh` — idempotent installer that symlinks items from this
  repo into `~/.claude/`.
- `.claude/settings.json` — repo-local default settings. **Not** auto-symlinked
  (Claude Code may rewrite the file and break the symlink). Copy it manually if
  you want it as your user-level config.

## Install on a new machine

```bash
# Clone anywhere stable
git clone git@github.com:YenChengLai/claude-code-settings.git ~/tools/claude-code-settings
cd ~/tools/claude-code-settings

# Option A — full install (personal machine):
# symlink every skill / command / agent in the repo into ~/.claude/
./scripts/install.sh

# Option B — single skill install (e.g. work machine, where you only want
# to opt into specific tools and leave the rest of ~/.claude/ alone)
./scripts/install.sh session-note
```

Then point the `session-note` skill at your notes vault by setting an env var
in your shell rc:

```bash
# ~/.bashrc or ~/.zshrc
export SESSION_NOTES_DIR="$HOME/path/to/your/notes"
```

Open a new shell (or `source` the rc) and you're set. In any Claude Code
session, say `note this session` or `/note` to save a note.

## Adding a new skill / command / agent

1. Drop the file(s) into the right subfolder:
   - Skill: `.claude/skills/<name>/SKILL.md` (frontmatter must include `name`
     and `description`).
   - Command: `.claude/commands/<name>.md` (filename becomes the slash command
     name).
   - Agent: `.claude/agents/<name>.md` (frontmatter must include `name` and
     `description`; optionally `tools` and `model`).
2. Commit and push.
3. On each machine, re-run the installer:
   - `./scripts/install.sh` to pick up everything (existing symlinks are left
     alone; only new items get linked).
   - `./scripts/install.sh <name>` to opt in to one specific skill.

## Why two install modes

- **Home machine** — I want everything I version-control to be active. Full mode.
- **Work machine** — `~/.claude/` may already hold settings I want to keep, and
  the project I work in already symlinks the team's tooling. So I opt in to
  specific personal skills only.

Both modes work by symlinking individual items into `~/.claude/<subdir>/`. The
whole `~/.claude/` directory is never replaced, so this coexists with anything
else you already have there.

## Layout

```
.
├── .claude/
│   ├── settings.json          # repo-local default; manual copy only
│   ├── skills/
│   │   └── session-note/      # SKILL.md + README + example note
│   ├── commands/              # (empty for now)
│   └── agents/                # (empty for now)
├── scripts/
│   └── install.sh             # idempotent installer (full / single)
├── CLAUDE.md                  # Claude's memory when editing this repo
└── README.md
```
