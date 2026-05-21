# claude-code-settings

Personal Claude Code environment settings, including settings, skills, slash commands, subagents, and more.

## Structure

```
.
├── CLAUDE.md                 # Project memory (Claude loads this every session)
├── .claude/
│   ├── settings.json         # Shared settings (committed)
│   ├── settings.local.json   # Local-only settings (gitignored)
│   ├── skills/               # Custom skills, one folder per skill
│   │   └── <skill>/SKILL.md
│   ├── commands/             # Custom slash commands (/<name>)
│   │   └── <name>.md
│   └── agents/               # Custom subagents
│       └── <name>.md
└── README.md
```

## Usage

After cloning this repo, apply the `.claude/` contents to your target environment:

- For user-level (global) use: copy or symlink into `~/.claude/`
- For a single project: copy or symlink into that project's `.claude/`

```bash
# Example: symlink into the user-level config
ln -s "$(pwd)/.claude/skills"   ~/.claude/skills
ln -s "$(pwd)/.claude/commands" ~/.claude/commands
ln -s "$(pwd)/.claude/agents"   ~/.claude/agents
```

## Adding new content

- **Skill**: create `.claude/skills/<name>/SKILL.md` with frontmatter (`name`, `description`) followed by the skill body.
- **Slash command**: create `.claude/commands/<name>.md`; the filename becomes the command name.
- **Subagent**: create `.claude/agents/<name>.md` with frontmatter defining the agent's role and tools.
