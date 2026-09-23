---
description: >-
  Only modify the project when the prompt unambiguously asks for a change.
  Questions asking for a solution, proposal, analysis or information are
  answered in chat only - nothing is written, edited, deleted or applied.
  Language-independent: intent is judged by meaning, not by keyword language.
  Applies to all agents and all skills in this workspace.
type: always_apply
trigger: always_on
---

# Rule: change the project only on an explicit request

## Two kinds of prompts

- **Question / consultation** - the user asks for a solution, a proposal, a design, an
  analysis, a review, an explanation, an estimate, a comparison, or any other
  information ("how would you...", "what is the best way...", "why does...",
  "is it possible...", "review this", "what do you think", "ako by si...",
  "aké sú možnosti...").
- **Change request** - the user unambiguously asks for the project to be modified
  ("fix", "change", "add", "remove", "rename", "refactor", "implement",
  "tune it", "apply it", "oprav", "uprav", "dolaď", "pridaj", "odstráň",
  "zapracuj").

Intent is decided by **meaning, not by the language of the prompt** - the same
rules apply to Slovak, Czech, English, or any other language.

## Behaviour

- **Question -> answer only.** No file is created, edited, deleted, moved, or
  renamed; no command with side effects is run; nothing is staged or committed;
  no configuration is applied; no state-changing call is made to **any**
  external system reachable through an API, tool, or MCP server – databases,
  ticketing/PM systems, web services and the like (e.g. Odoo PM via RPC).
  The proposal stays in the chat response.
- **Change request -> carry out the change** in full, as the prompt describes.
- **Unclear intent -> treat it as a question.** Answer, state what change you
  would make, and ask whether to apply it. Never resolve the ambiguity by
  writing to the project.
- A question about earlier work, or a remark that something is wrong, is **not**
  a change request on its own - describe the fix and wait for the go-ahead.
- Read-only inspection (reading files, searching, `git status`/`git diff`,
  running tests or linters that do not rewrite files, read-only calls to any
  external API – e.g. Odoo PM via RPC) is always allowed while answering a
  question.

## Scope of a change request

An approved change covers what the prompt asks for. Do not extend it with
unrequested "while I was there" edits - fixes of adjacent code, reformatting,
dependency bumps, or cleanups. Mention such findings in the response instead.
