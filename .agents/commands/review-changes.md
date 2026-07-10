---
description: Checks uncommitted changes, summarizes them, and flags potential issues before committing.
---

# Review Changes

Check the current uncommitted changes in the repository and prepare an overview for code review.

## Steps

1. Show the list of changed files: `git status --short`
2. Show the diff of changed files: `git diff`
3. Check whether the changes:
   - Contain no debug output or `print()` calls intended only for development
   - Contain no commented-out code (prefer deleting over commenting out)
   - Contain no sensitive data (passwords, API keys, tokens)
   - Are consistent with the project conventions from `AGENTS.md`
4. Briefly summarize the changes: what changed and why
5. If there are issues, list them; if not, confirm that the changes look fine
