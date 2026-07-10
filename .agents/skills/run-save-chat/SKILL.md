---
name: run-save-chat
description: >-
  Literally (verbatim) save the entire chat history – all prompts and agent
  responses – to a .md file. Without a specified name, it asks whether to auto-generate
  it or have the user enter it; handles the directory (default tmp/), appends the .md extension,
  and always adds a suffix with the agent's name. Use for "save chat", "save entire
  conversation to .md".
---

# run-save-chat

Skill for **literally saving the entire chat history** – all prompts and agent responses – to a Markdown file. Content is saved **verbatim** – exactly as it was written/printed, without summarization, shortening, or modifications.

## When to use

- "save chat", "save entire conversation to .md",
- the entry point is also the command `/run.save-chat`.

## Input

- Optional argument = specification of the target file (name, potentially with a folder).
- If the argument is missing, the agent **asks the user** whether to auto-generate the filename or have the user enter it (see below).

## 1. Determine agent identifier (suffix)

Suffix = short identifier of the running agent/CLI:

| Agent            | Suffix   |
| ---------------- | -------- |
| Auggie           | `auggie` |
| Claude Code      | `claude` |
| Antigravity      | `agy`    |
| Codex            | `codex`  |

## 2. Determine target path (algorithm)

Follow this order:

1. **Without argument** -> ask the user whether the agent should auto-generate the filename or if the user wants to enter it:
   - **Agent generates** -> create a short descriptive name (slug) from the main topic of the conversation, using only characters `[a-zA-Z0-9\-]` (kebab-case, e.g., `tax-analyze`). This is treated as "name without folder" -> target folder is `tmp/`.
   - **User enters** -> wait for the name (potentially with a folder) and proceed with step 2 below as if it were the original argument.
2. **With argument** -> split it into folder part and filename:
   - contains `/` (has a folder) -> target folder = specified folder,
   - does not contain `/` (only name) -> target folder = `tmp/`.
3. **Extension**: remove the trailing `.md` from the name if present -> you get the `stem`. If the name did not have an extension, still proceed with the `stem` (same procedure); `.md` will be appended in step 5. (This resolves "without extension -> append `.md`".)
4. **Agent suffix**: add `-<suffix>` (e.g., `-auggie`) to the `stem`. If `stem` already ends with `-<suffix>`, do not double it.
5. **Final path** = `<target folder>/<stem>-<suffix>.md`.
6. If the target folder does not exist, create it.

### Examples

| Argument                                  | Suffix   | Resulting path                                       |
| ----------------------------------------- | -------- | ---------------------------------------------------- |
| *(none)*                                  | `auggie` | `tmp/tax-analyze-auggie.md` (slug auto-generated)    |
| `my-chat.md`                              | `auggie` | `tmp/my-chat-auggie.md`                              |
| `my-chat`                                 | `auggie` | `tmp/my-chat-auggie.md`                              |
| `.agents/user-prompts/my-chat.md`         | `auggie` | `.agents/user-prompts/my-chat-auggie.md`             |
| `.agents/user-prompts/my-chat`            | `claude` | `.agents/user-prompts/my-chat-claude.md`             |

## 3. Save all prompts and responses

Write the **literal** (verbatim) content of the entire conversation in chronological order to the final path. **For each turn** (user prompt and the subsequent agent response), repeat the same format as below – i.e., as many `**Prompt:**` / `**Response:**` blocks as there were turns in the chat. The first line of the file is empty, headers are bold, and **each non-empty line of the prompt and response is indented by 4 spaces to the right**:

```
**Prompt:**

    <literal text of 1st prompt – each line indented by 4 spaces>

**Response:**

    <literal text of 1st response – each line indented by 4 spaces>

**Prompt:**

    <literal text of 2nd prompt – each line indented by 4 spaces>

**Response:**

    <literal text of 2nd response – each line indented by 4 spaces>
```

- **The entire chat history is saved** – all prompts and responses from the beginning of the conversation to the last turn, in the order they occurred.
- Prompts and responses are written **verbatim** (Markdown as-is), without summarization, shortening, or modification – only with a 4-space indentation added at the beginning of each non-empty line (empty lines remain empty).
- The 4-space indentation applies to **all** lines of content, including headings, lists, tables, and code blocks – so that they can be visually distinguished from the structural headers `**Prompt:**` and `**Response:**` (and the empty separator lines).
- Do not add anything else (no additional heading, metadata, or comment) besides the `**Prompt:**` and `**Response:**` headers (and the empty separator lines).
- Template of a single block format: `.agents/user-prompts/ai-namespacing-auggie.md`.
- If the file already exists, warn the user and ask whether to overwrite.
- After saving, notify the user of the resulting path.

## Hard Rules

- Prompts and responses are **verbatim** – no paraphrasing or additions (the only allowed modification is the 4-space line indentation).
- The **entire** chat history is saved, not just the last turn.
- The agent suffix is **always** added.
- Never save secrets to the file (`.agents/rules/run.secret-safety.md`).

## Related

- `.agents/commands/run.save-chat.md` – paired command `/run.save-chat` (entry point to this skill).
- `.agents/skills/run-save-response/SKILL.md` – equivalent for saving only the last prompt and response.
- `docs/ai-agents.md` – source of truth on unified agent configuration.
- `.agents/rules/run.secret-safety.md` – no secrets in files or prompts.
