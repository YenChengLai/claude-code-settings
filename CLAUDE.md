# CLAUDE.md

這個 repo 是個人的 Claude Code 環境設定。修改時請維持以下原則：

- `.claude/settings.json` 為共用設定，會被 commit；`settings.local.json` 為本機設定，已加入 `.gitignore`。
- 每個 skill 放在 `.claude/skills/<name>/SKILL.md`，必須有 frontmatter（`name`、`description`）。
- Slash command 放在 `.claude/commands/<name>.md`，檔名 = 指令名。
- Subagent 放在 `.claude/agents/<name>.md`，frontmatter 需設定 `name`、`description`，可加 `tools`、`model`。
