---
description: >-
  Solve a complex task by comparing proposals from multiple CLI subagents
  (claude/auggie/codex/agy) with different LLM models and present a recommended solution.
  Runs only on request; intermediate outputs remain in tmp/ for verification.
---

# /run.compare-solutions – Compare proposals from multiple subagents

Thin entry point – **the entire procedure, CLI table, and Output Contract are in `.agents/agents/run.compare-solutions.md`** (do not duplicate them here). The command and the sub-agent have the same output; this command is the entry point for Claude Code, Auggie, and Antigravity. (Codex does not support slash commands – invoke the `run.compare-solutions` sub-agent directly there. Antigravity does not read file-based sub-agents – refer to the content of `.agents/agents/run.compare-solutions.md`.)

In short (details in the sub-agent):

1. Check CLI availability and **verify valid model-IDs** (`auggie model list`, `agy models`; `claude`/`codex` via `--help`).
2. Propose an agent × model matrix (**default `claude` and `auggie`**), warn about credit multiplication, and **wait for user confirmation**.
3. Prepare the prompt in a file with the **Output Contract** (exact text in the sub-agent) and run the orchestration script (`--check` before fan-out cheaply verifies auth/flags):
   ```bash
   .agents/agents/scripts/run.compare-solutions-fanout.sh \
     --prompt-file tmp/run.compare-solutions/prompt.md  claude auggie
   ```
4. Compare and analyze outputs; present a **recommended solution** (a proposal, not execution of changes) and provide the path to the `tmp/` folder containing the individual solutions.

Hard rules: only on request (never automatically), **no recursive execution** of the orchestrator, subagents only propose (they do not edit the repo), never include secrets in the prompt or argv (`.agents/rules/run.secret-safety.md`).

If the user provided an argument (task, which CLIs, how many, which models), narrow the procedure accordingly.
