# DEVLOG settings

The devlog skill reads this file before every entry. Edit it freely.

## Project
name: My Project
description: One line on what the project is.

## Output
language: en          # language the entries are written in, e.g. en, ko, ja
folder: devlog        # where entries, map.json and dashboard.html live
dashboard: manual     # manual = build only when asked, auto = rebuild after every entry

## Tags
# Pick from these when tagging an entry. Add your own.
- backend
- frontend
- data
- infra
- study

## Never record
# Anything here stays out of the log, even if it was in the conversation.
- API keys, tokens, passwords
- Internal URLs and server addresses
- Real names of teammates (use roles instead)
- Customer or personal data

## Extra rules (optional)
# Your own house rules, e.g. "Results must link the commit hash".
