---
description: >-
  Code comments describe the current state of the code, never the change that
  produced it - no references to previous solutions that no longer exist in
  the code. Write comments as if the code had been implemented this way from
  the start. Applies to all agents and all skills in this workspace.
type: always_apply
trigger: always_on
---

# Rule: timeless comments

- Write every comment (and doc comment) as if the current implementation had
  been written this way from the start.
- Do not explain the change being made ("changed to...", "now uses... instead
  of...", "refactored from...", "this replaces the old...") and do not justify
  why the edit is correct - that belongs in the chat response or the commit
  message, not in the code.
- Never reference a previous/worse/discarded solution that no longer exists in
  the code - the next reader has no idea it ever existed, so such a comment is
  noise to them.
- Exception: a comment may reference history when that is its actual purpose
  and it stays meaningful over time - e.g. a workaround note linking an
  upstream bug, or a migration/compatibility note for data produced by an
  older version.
