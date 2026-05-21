# CLAUDE.md

This repo holds personal Claude Code environment settings. When editing, follow these conventions:

- `.claude/settings.json` is the shared, committed config; `settings.local.json` is local-only and listed in `.gitignore`.
- Each skill lives at `.claude/skills/<name>/SKILL.md` and must include frontmatter with `name` and `description`.
- Slash commands live at `.claude/commands/<name>.md`; the filename is the command name.
- Subagents live at `.claude/agents/<name>.md`; frontmatter must set `name` and `description`, and may set `tools` and `model`.
