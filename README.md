# claude-code-settings

個人 Claude Code 環境設定，包含 settings、skills、slash commands、subagents 等。

## 結構

```
.
├── CLAUDE.md                 # 全域 / 專案備忘錄（Claude 每次會載入）
├── .claude/
│   ├── settings.json         # 共用設定（會 commit）
│   ├── settings.local.json   # 本機設定（.gitignore，不 commit）
│   ├── skills/               # 自訂 skills，每個 skill 一個資料夾
│   │   └── <skill>/SKILL.md
│   ├── commands/             # 自訂 slash commands（/<name>）
│   │   └── <name>.md
│   └── agents/               # 自訂 subagents
│       └── <name>.md
└── README.md
```

## 使用

把這個 repo clone 到本機後，將 `.claude/` 內容套用到目標環境：

- 想全域生效：複製或 symlink 到 `~/.claude/`
- 只想用在單一專案：複製或 symlink 到該專案的 `.claude/`

```bash
# 範例：symlink 到 user-level
ln -s "$(pwd)/.claude/skills"   ~/.claude/skills
ln -s "$(pwd)/.claude/commands" ~/.claude/commands
ln -s "$(pwd)/.claude/agents"   ~/.claude/agents
```

## 新增內容

- **Skill**：新增 `.claude/skills/<name>/SKILL.md`，內含 frontmatter（`name`、`description`）與 skill 內文。
- **Slash command**：新增 `.claude/commands/<name>.md`，檔名即為指令名。
- **Subagent**：新增 `.claude/agents/<name>.md`，內含 frontmatter 設定該 agent 的角色與工具。
