---
description: >-
  Entry point to the run-remove-devcontainer-addon skill – remove an integrated
  devcontainer add-on per the `## Removal` section of its descriptor.
---

# /run.remove-devcontainer-addon – Remove a devcontainer add-on

Follow the procedure according to the **`run-remove-devcontainer-addon`** skill
(`.agents/skills/run-remove-devcontainer-addon/SKILL.md`). The command and the skill have the
same output; this command is the entry point for Claude Code, Auggie, and Antigravity. (Codex
does not support slash commands – use the `run-remove-devcontainer-addon` skill directly
there.)

In short (details in the skill):

1. Resolve the target add-on from the argument (`<add-on>` or `<add-on>.md`, with or without a
   path prefix). If no argument was given, list the add-ons currently integrated in the project
   (via their `.devcontainer/<add-on>.md` descriptors) and ask the user to pick one.
2. Read that descriptor's `## Installation` and `## Removal` sections.
3. Build a concrete removal plan: files/folders to delete, appended snippets to strip from
   scripts/`.gitignore`, and any other Removal-section steps (e.g. restoring a symlink) –
   distinguishing files wholly owned by the add-on from shared files that must keep their
   project-specific content.
4. Show the plan and get explicit confirmation before deleting or editing anything.
5. Apply the plan and report a summary, including any manual follow-up left for the user (e.g.
   rebuild the devcontainer).

Hard rule: never commit, stage, unstage, or otherwise change git state – this only edits/deletes
working-tree files, and nothing is removed without confirmation first.

If the user already named the add-on, do not ask again – proceed with that add-on.
