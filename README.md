# devlog-skill

An [Agent Skill](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview) that turns
your conversation with a coding agent into a daily devlog: what you built, what you learned, why you
decided things — plus a "rabbit-hole map" of how follow-up questions led to insights and decisions.

한국어 설명은 [README.ko.md](README.ko.md)에 있어.

Works with any agent that reads `SKILL.md` folders and can read/write files. No hooks, no hosted services.

## Install

Copy this folder into your agent's skills directory, for example:

```bash
git clone https://github.com/bookschooler/devlog-skill ~/.claude/skills/devlog
```

```powershell
git clone https://github.com/bookschooler/devlog-skill "$HOME\.claude\skills\devlog"
```

For other agents, put the folder wherever that agent loads skills from.

## Use

At the end of a work session, say:

> write today's devlog  /  오늘 일지 써줘

On first run the agent creates `DEVLOG.md` in your project root. Edit it to set the project name,
log language, tags, and a **Never record** list (secrets, internal URLs, names…).

Build the dashboard any time:

```bash
python path/to/devlog/scripts/build_dashboard.py .
```

It writes `devlog/dashboard.html` — one self-contained page, standard-library Python only.

## What's inside

```
SKILL.md                 when to use it + the steps
references/rules.md      writing rules (results vs. learning, source grades, no invented facts)
templates/daily.md       one day's entry
templates/map.json       rabbit-hole map: root → task → question → insight → decision
templates/DEVLOG.md      per-user settings
scripts/build_dashboard.py  entries + map → dashboard.html
```

## License

MIT
