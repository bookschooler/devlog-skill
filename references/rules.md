# Writing rules

These rules apply to every entry. When a rule and the user's `DEVLOG.md` disagree, `DEVLOG.md` wins.

## 1. Results are project work only

The **Results** section lists only what changed in the project named in `DEVLOG.md`:
code written or fixed, files created, experiments run, documents produced, decisions applied.

- Learning, reading and explanations go in **Learned**, not in Results.
- Write each result as an outcome you could point at: "Added retry to the upload API (`api/upload.py`)",
  not "Worked on the upload API".
- If nothing changed in the project, write `No project changes this session.`

## 2. Learned: definition → when → role

Each concept learned gets three short lines, always in this order:

```
### <Concept>
- Definition: what it is, in plain words (spell out abbreviations the first time)
- When: the situation where it comes up or is used
- Role here: what it did (or would do) in this project
```

If the conversation never covered one of the three, write `(not covered)` rather than inventing it.

## 3. Source grades

Every factual claim in Learned and Decisions that came from an outside source gets a grade,
written as `[A1]`, `[C2]` and so on, next to the source.

Letter — how trustworthy the source is:

| Grade | Source |
|---|---|
| A | Official docs, specs, papers, the project's own code or data |
| B | Well-known secondary sources (established textbooks, vendor engineering blogs) |
| C | Community answers, personal blogs, forum posts |
| D | Unverified: the agent's own background knowledge, hearsay, no source given |

Number — how far it was confirmed in this session:

| Grade | Meaning |
|---|---|
| 1 | Checked here: code ran, output seen, doc opened and read |
| 2 | Agrees with at least one other independent source, not run here |
| 3 | Not confirmed |

Anything graded D or 3 should also appear under **Open questions** if a decision depends on it.

## 4. Nothing that wasn't in the conversation

Write only what the conversation actually contains. No filling gaps with general knowledge,
no guessing file names, numbers, dates or reasons. If the reason for a decision was never stated,
write `Reason: not stated` — that gap is useful information.

## 5. Respect "Never record"

Skip anything matching the "Never record" list in `DEVLOG.md` (for example secrets, API keys,
personal data, internal URLs, teammates' names). When unsure, leave it out and mention in your
reply that something was omitted, without repeating it.

Always skip, regardless of settings: passwords, tokens, keys, connection strings.

## 6. The map (map.json)

The map traces how curiosity turned into decisions:

```
root (project)
└─ Task          what you set out to do
   └─ Question   a follow-up question that came up while doing it ("why does…?", "what if…?")
      └─ Insight what you found out
         └─ Decision what you chose to do because of it
```

- A Question can lead to another Question (that's the rabbit hole). Keep the chain.
- Not every chain reaches a Decision. Leave it open; it shows up as unfinished on the dashboard.
- Every node has `date`; Insight and Decision nodes may carry `source` with a grade.
