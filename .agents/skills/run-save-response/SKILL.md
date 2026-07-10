---
name: run-save-response
description: >-
  Literally (verbatim) save the last prompt and agent response to a .md file.
  Without a specified name, it asks whether to auto-generate it or have the user enter it;
  handles the directory (default tmp/), appends the .md extension, and always adds a suffix
  with the agent's name. Use for "save response", "rewrite last response to .md",
  "save response".
---

# run-save-response

Skill for **literally saving the last prompt and agent response** to a Markdown file. Content is saved **verbatim** – exactly as it was written/printed, without summarization, shortening, or modifications.

## When to use

- "save last response", "rewrite response to .md", "save response",
- the entry point is also the command `/run.save-response`.

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
   - **Agent generates** -> create a short descriptive name (slug) from the topic of the last response, using only characters `[a-zA-Z0-9\-]` (kebab-case, e.g., `tax-analyze`). This is treated as "name without folder" -> target folder is `tmp/`.
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
| `my-tax-analyze.md`                       | `auggie` | `tmp/my-tax-analyze-auggie.md`                       |
| `my-tax-analyze`                          | `auggie` | `tmp/my-tax-analyze-auggie.md`                       |
| `.agents/user-prompts/my-tax-analyze.md`  | `auggie` | `.agents/user-prompts/my-tax-analyze-auggie.md`      |
| `.agents/user-prompts/my-tax-analyze`     | `claude` | `.agents/user-prompts/my-tax-analyze-claude.md`      |

## 3. Save prompt and response

Write the **literal** (verbatim) content in exactly this format to the final path (the first line of the file is empty, headers are bold, and **each non-empty line of the prompt and response is indented by 4 spaces to the right**):

```
**Prompt:**

    <literal text of last prompt – each line indented by 4 spaces>

**Response:**

    <literal text of last response – each line indented by 4 spaces>
```

- Both the prompt and response are written **verbatim** (Markdown as-is), without summarization, shortening, or modification – only with a 4-space indentation added at the beginning of each non-empty line (empty lines remain empty).
- The 4-space indentation applies to **all** lines of content, including headings, lists, tables, and code blocks – so that they can be visually distinguished from the structural headers `**Prompt:**` and `**Response:**` (and the empty separator lines).
- Do not add anything else (no additional heading, metadata, or comment) besides the `**Prompt:**` and `**Response:**` headers (and the empty separator lines).
- Template of correctly formatted output: `.agents/user-prompts/ai-namespacing-auggie.md`.
- If the file already exists, warn the user and ask whether to overwrite.
- After saving, notify the user of the resulting path.

## Hard Rules

- The prompt and response are **verbatim** – no paraphrasing or additions (the only allowed modification is the 4-space line indentation).
- The agent suffix is **always** added.
- Never save secrets to the file (`.agents/rules/run.secret-safety.md`).

## Related

- `.agents/commands/run.save-response.md` – paired command `/run.save-response` (entry point to this skill).
- `docs/ai-agents.md` – source of truth on unified agent configuration.
- `.agents/rules/run.secret-safety.md` – no secrets in files or prompts.
