---
name: run-add-agent-asset
description: >-
  Adding and modifying agent artifacts (skills, rules, slash commands,
  subagents) in accordance with the unified configuration of AI agents described in
  docs/ai-agents.md. Use when "create/edit skill | rule | command | subagent",
  "add agent artifact".
---

# run-add-agent-asset

Skill for safely adding new agent artifacts so that they work across all agents (Auggie, Claude Code, Antigravity, Codex).
**The source of truth is `docs/ai-agents.md`** – this skill is only a procedure and checklist; do not duplicate symlink or format details, refer to it instead.

## When to use

- "create/edit skill", "add rule", "new slash command", "new subagent",
- "add agent artifact" / "modify agent configuration".

## 1. Determine artifact type

- **rule** – always/frequently valid guardrails (`.agents/rules/run.<name>.md`),
- **skill** – repeatable procedure/workflow (`.agents/skills/run-<name>/SKILL.md`),
- **command** – short entry point `/run.<name>` (`.agents/commands/run.<name>.md`),
- **subagent** – isolated specialist with its own prompt (`.agents/agents/run.<name>.*`).

If it is not a new type of artifact, **new symlinks are not needed** – existing ones in `docs/ai-agents.md` already ensure cross-tool discovery.

## 2. Conventions

- **namespace prefix** – all local/shared/project-owned artifacts (rules, commands, skills, subagents) are namespaced with `run.` / `run-` to mark them as project-owned and avoid collisions with third-party or vendor-provided artifacts (e.g. `speckit-*`, which stay unprefixed and must never be renamed); use `run.<name>` for commands/rules/subagents (files) and `run-<name>` for skill directories,
- kebab-case for the part of the name after the prefix (e.g., `run.deploy-staging`, `run-review-pr`),
- avoid double-prefixing (`run.run.<name>`, `run-run-<name>`) – if a requested name already carries a `run.` or `run-` prefix, strip that prefix first and then apply the correct prefix for the artifact type (`run.` for command/rule/subagent files, `run-` for skill directories),
- content and `description` **in English**,
- keep `description` brief and clear – the agent decides on activation based on it during `agent_requested` / `model_decision`.

## 3. Cookbook by type

### Rule (`.agents/rules/run.<name>.md`)
- Combined frontmatter: `description` + `type:` (Auggie: `always_apply|agent_requested`, `manual` is skipped by CLI – only works in IDE extensions) + `trigger:` (Antigravity: `always_on|glob|model_decision|manual`). Unknown keys are ignored by each agent.
- Claude Code and Codex do not have a rules folder -> if the `always_apply|always_on` rule should apply to them as well, add a `@.agents/rules/run.<name>.md` import to `AGENTS.md`.

### Skill (`.agents/skills/run-<name>/SKILL.md`)
- Directory + `SKILL.md` with **mandatory** frontmatter `name` (= `run-<name>`) and `description`.
- Optional subdirectories `scripts/`, `references/`, `assets/`.
- No registration is needed elsewhere – agents auto-discover skills.

### Command (`.agents/commands/run.<name>.md`)
- File `run.<name>.md` -> `/run.<name>`; an additional subdirectory adds a further namespace (`frontend/run.component.md` -> `/frontend:run.component`).
- Frontmatter with a `description` field (folded scalar, e.g., `description: >-`).
- **Codex** does not support slash commands – use the corresponding skill directly there; the command should be a thin entry point referencing the skill.

### Subagent (`.agents/agents/`)
- Add **both** formats for the same agent, sharing the `run.<name>` base name:
  - `run.<name>.md` (Claude Code, Auggie): YAML frontmatter `name`, `description`, optionally `color` (Auggie), `tools`, `model` (Claude); body = system prompt,
  - `run.<name>.toml` (Codex): `name`, `description`, `developer_instructions` (system prompt), optionally `model`, `sandbox_mode`.
- Antigravity does not support file-based subagents yet (only `define_subagent` at runtime) – do not edit anything extra for it.

## 4. Documentation and Registry Sync (DoD)

- new **always-apply rule** -> add to the list of "Always applicable cross-cutting rules" in `AGENTS.md` and add a `@`-import,
- **new type of artifact/agent requiring a new symlink** -> add a line to the symlink table **and** to the `ln -s` block in `docs/ai-agents.md`,
- if a new command/skill was created that is an entry point to another, link them with a reference and matching names (e.g., command `/run.<name>` <-> skill `run-<name>`).

## 5. Verification Checklist (cross-tool)

After creation, verify that the artifact is visible to each relevant agent:

- **Auggie** – skills natively from `.agents/skills`; commands/agents/rules via `.augment/*` symlinks,
- **Claude Code** – via `.claude/*` symlinks; rules only via `@`-import in `AGENTS.md`,
- **Antigravity** – `.agents/*` natively; commands via symlink `workflows -> commands`; does not read subagents from files,
- **Codex** – `.agents/skills` and `AGENTS.md` natively; subagents from `.codex/agents` (`.toml`) via symlink; does not support commands; rules only by reference from `AGENTS.md`.

## Related

- `docs/ai-agents.md` – **source of truth** about unified configuration and symlinks.
- `.agents/rules/run.secret-safety.md` – never include secrets in artifacts – neither in files nor in prompts.
- `.agents/commands/run.add-agent-asset.md` – paired command `/run.add-agent-asset` (entry point to this skill).
