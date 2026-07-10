---
type: always_apply
trigger: always_on
---

# Instructions for AI agents

This file is a **shared source of truth** for all AI agents in the project
(Auggie, Claude Code, Antigravity, Codex). Auggie, Antigravity
and Codex read it natively; Claude Code reads it via the symlink `CLAUDE.md → AGENTS.md`.

Configuration details of individual agents and the unified structure are in
[`docs/ai-agents.md`](docs/ai-agents.md).

Before working, check:

- `.agents/rules/*.md` – modular workspace rules

## Always applicable cross-cutting rules

- @.agents/rules/run.language-policy.md
- @.agents/rules/run.secret-safety.md

## General description

This project is used for developing helper Python scripts. The scripts are written:

- for Python 3.10+ (see also `pyproject.toml`)
- so that each of them can also be run standalone (e.g. `python ./src/runtools/dockerinfo.py`)

See also `README.md`.

## AI agents

See `docs/ai-agents.md`.

## Miscellaneous

### Fetching password-protected URLs

When fetching password-protected URLs, use `curl`. For example, for basic HTTP authentication use `curl -u <user>:<pwd> https://example.sk/some/protected/page`
