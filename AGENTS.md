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

## Všeobecný popis

Tento projekt slúži na vývoj pomocných Python skriptov. Skripty sú písané:

- pre Python 3.10+ (viď aj `pyproject.toml`)
- tak, aby každý z nich mohol byť spustiteľný aj samostatne (napr. `python ./src/runtools/dockerinfo.py`)

Viď aj `README.md`.

## AI agenti

Viď `docs/ai-agents.md`.

## Rôzne

### Načítanie URL adries chránených pomocou hesla

Pri načítaní URL adries chránených pomocou hesla použi `curl`. Napríklad pri basic HTTP authentication použi `curl -u <user>:<pwd> https://example.sk/some/protected/page`
