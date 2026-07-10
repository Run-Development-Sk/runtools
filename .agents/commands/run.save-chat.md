---
description: >-
  Literally save the entire chat history – all prompts and agent responses – to
  a .md file. Without arguments, it asks whether to auto-generate the name or
  have the user enter it; names without a folder go to tmp/, with a folder stay in place;
  appends missing extension and always adds a suffix with the agent's name.
---

# /run.save-chat – Save entire chat history to .md

Follow the procedure according to the **`run-save-chat`** skill (`.agents/skills/run-save-chat/SKILL.md`). The command and the skill have the same output; this command is the entry point for Claude Code, Auggie, and Antigravity. (Codex does not support slash commands – use the `run-save-chat` skill directly there.)

In short (details in the skill):

1. Determine the agent's suffix (`auggie` / `claude` / `agy` / `codex`).
2. Determine the target path:
   - without an argument -> ask the user whether to auto-generate the name (slug `[a-zA-Z0-9\-]` from the conversation topic, folder `tmp/`) or if they want to enter it,
   - name without a folder -> folder `tmp/`,
   - name with a folder -> stays in that folder,
   - missing extension -> append `.md`.
3. Add the suffix `-<agent>` before `.md` (e.g., `my-chat-auggie.md`).
4. Write the **literal** (verbatim) content of the entire conversation – **all** prompts and responses in chronological order, each turn under bold headers `**Prompt:**` / `**Response:**` (as many blocks as there were turns), where **each non-empty line of the prompt and response is indented by 4 spaces to the right** (format template: `.agents/user-prompts/ai-namespacing-auggie.md`, exact format in the skill); if the folder is missing, create it; if the file exists, ask about overwriting; announce the resulting path.

Hard rules: prompts and responses are verbatim (the only modification is the 4-space line indentation), the entire chat history is saved (not just the last turn), the agent suffix is always added, no secrets in the file (`.agents/rules/run.secret-safety.md`).

If the user provided an argument (name, potentially with a folder), narrow the procedure accordingly.
