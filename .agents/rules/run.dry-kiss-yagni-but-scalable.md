---
description: >-
  Do not restate or re-summarize the same information in documentation or code, keep the
  solution as simple as the task allows, build only what is required now, but
  keep expensive-to-reverse decisions open. Applies to all agents and skills;
  duplication that serves a distinct purpose (per-tool instructions,
  checklists, DoD repeats) is exempt.
type: always_apply
trigger: always_on
---

# Rule: DRY, KISS, YAGNI but scalable

AI agents tend to over-generate: restating the same information (even if rephrased), reaching for elaborate solutions, and building for needs nobody asked for - volume without added value. Applies to both documentation and code.

## DRY - do not repeat yourself

### When duplication is required (allowed)

Repetition is fine, and expected, when it serves a distinct purpose:

- content that must be spelled out separately per audience/tool/role (e.g. the per-agent instructions in `docs/ai-agents.md`, per-tool config blocks),
- checklists, DoD lists, or verification steps that are only useful when self-contained,
- index/pointer entries (e.g. `MEMORY.md`) that deliberately restate a one-line reference to fuller content held elsewhere,
- structurally required repetition (e.g. an artifact's name appearing in both its frontmatter and its file path).

### When duplication is not allowed

- Do not add a closing "summary of what changed / what was written" section that restates the body in different words - the reader already has the body.
- Do not restate the same requirement, fact, or explanation in multiple sections or artifacts just rephrased. Keep one source of truth and reference it from elsewhere, unless the content must be self-contained for a distinct purpose described above.
- Do not pad responses or files with recaps of previous turns/sections "for clarity" - trust the reader to have read what came before.
- In code: do not add comments that restate what the code already says; do not duplicate logic/abstractions that already exist elsewhere in the codebase - reuse or reference them instead.

## KISS - keep it stupid simple

- Pick the simplest solution that fully solves the task; readable and obvious beats clever and compact.
- Do not introduce an unnecessary abstraction, layer, wrapper, base class, or configuration option for a single call site - inline it and extract only when a second real caller appears.
- Prefer the mechanism already used in the project over a new dependency, framework, or pattern brought in for one problem.
- In documentation: flat structure, plain wording, no ceremony sections that exist only to look complete.
- Complexity the task genuinely requires - error handling, edge cases, security, a measured performance need - is not over-engineering; keep it.

## YAGNI - you aren't gonna need it

- Implement only what the current request asks for; a requirement that has not been stated does not exist yet.
- No speculative parameters, options, hooks, feature flags, or generalizations "for later", and no handling of cases that cannot occur today.
- No placeholder or dead code, unused exports, empty stubs, or documentation of behaviour that is not implemented.
- Anticipated future needs belong in the chat response (or a todo), not in the codebase.

## Scalability - do not design yourself into a corner

The counterweight to KISS and YAGNI: build for the scale you have, but keep the road to a bigger one open.

- Distinguish cheap and expensive reversals. Internal implementation, an in-memory algorithm, or a local helper can stay naive - it is rewritten in one place later. Data models and schemas, persisted or exchanged formats, public interfaces and API contracts, identifiers and naming, and integrations with external systems are expensive to change once in use - think those through even at today's small scale.
- Keep scale-sensitive choices localized to one call site or one module, so replacing them later touches one place. This alone is not a reason to add an abstraction or indirection layer.
- When the project's existing patterns already support the general case at no meaningful extra cost, do not bake in narrower assumptions such as fixed limits, counts, paths, or single-record operation.
- This is not a licence to pre-build the scalable version. Ship the simple one; just do not make the future one impossible.
- When the simple solution does close a door (an irreversible format, a one-way migration, a contract others will depend on), say so in the response and let the user decide.

## Rule of thumb

Before adding a paragraph, section, comment, abstraction, option, or file, ask: does it give the reader information they lack, or does the current task require this behaviour? If neither, leave it out - or replace it with a reference to the source of truth. Before choosing the simple solution, ask what it would cost to replace later; if that cost is high, pick the option that stays open.
