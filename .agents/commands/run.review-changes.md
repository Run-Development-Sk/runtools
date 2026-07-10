---
description: >-
  Review/revise changes made by an AI agent - staged files, specific commit(s),
  or branch changes against main - and report remarks only (read-only, no edits/commits).
  Source code is reviewed against architectural and language/framework-specific quality
  criteria for the identified type; non-code changes are evaluated for correctness/completeness
  against the original user request.
---

# /run.review-changes – Review AI agent changes

Follow the procedure according to the **`run-review-changes`** skill
(`.agents/skills/run-review-changes/SKILL.md`). The command and the skill have the same
output; this command is the entry point for Claude Code, Auggie, and Antigravity. (Codex does
not support slash commands – use the `run-review-changes` skill directly there.)

In short (details in the skill):

1. If not already specified, ask the user whether to review **staged files**, **commit
   hash(es)**, or **branch changes against main** (pull request style), and ask for the
   **original request/prompt** that led to the changes.
2. Determine the diff (`git diff --cached` for staged files; `git show`/`git diff` for the
   given commit hash(es); `git diff main...HEAD` for branch changes) without modifying the
   working tree/index.
3. Classify each changed file as source code or not.
4. Source code -> review against architectural and language/framework-specific quality
   criteria appropriate to the identified type (correctness, design, idioms, security,
   performance, error handling, readability, tests). Non-code -> evaluate correctness and
   completeness against the original request.
5. Report remarks only, grouped by file/commit, plus an overall summary.

Hard rule: this is **read-only** – the agent only writes remarks; it never edits, adds,
removes, stages, unstages, or commits anything.

If the user provided an argument (change source and/or original request), narrow the
procedure accordingly instead of asking again.
