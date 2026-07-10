# Coding AI Agents

The following coding AI agents are available in this devcontainer:

- `auggie` (**Augment Code** CLI)
- **Claude Code** (VS Code extension) and/or `claude` (Claude Code CLI)
- `agy` (**Antigravity** CLI)
- **Codex** (VS Code extension) and/or `codex` (Codex CLI)

You can download the current version for a given project from [github.com/RunDevelopmentSk/devcontainers](https://github.com/RunDevelopmentSk/devcontainers) > `_agents`.

Details on how to use individual AI agents are described below.

## Plans

Every agent is used through a personal account (your individual login with the provider, see
"Logging In" sestions below). Which **plan** pays for that usage is a separate choice:

- **Individual plan** – an individually paid, capped tier tied to your personal account (private
  use).
- **Company plan** – a shared, company-paid tier your personal account is added to as a member
  (work use); either metered API billing (pay per use) or a flat seat-based subscription (with
  pay-as-you-go overflow once included credits are exhausted).

The following notes summarize subscription options and their relative value, as of July 2026:

- `agy`
  - [Individual plan](accounts.google.com):
    - 1 seat
    - a small amount of free credits, with a weekly reset window
    - an API requests limit
  - [Company plan](https://console.cloud.google.com/) (metered API billing; personal account + project + billing + API enabled):
    - unlimited seats for shared credits
    - $300 of initial free credits included, then pay as you go
    - the most cost-effective setup is often to keep each user on a separate, individually-owned Company plan to multiply the $300 free credits and also reduce the API requests.
- `auggie`
  - [Company plan](https://app.augmentcode.com/) (seat-based subscription; $100/month plan):
    - 50 seats for shared credits
    - when purchased credits are exhausted, pay as you go
- `claude`
  - [Individual plan](https://claude.ai/):
    - 1 seat
    - free credits based on subscription plan, with 5-hour and weekly reset window
  - [Company plan](platform.claude.com) (metered API billing):
    - unlimited seats for shared credits
    - pay as you go
- `codex`
  - [Individual plan](https://chatgpt.com/) (Personal plan):
    - 1 seat
    - free credits based on subscription plan, with 5-hour and weekly reset window
  - [Company plan](https://chatgpt.com/) (seat-based subscription; Business plan):
    - unlimited seats for shared credits
    - pay as you go

Approximate value ranking, depending on the models in use (July 2026):

- `agy` > individually-owned Company plan > until the initial $300 is used up
- `codex` > Individual plan
- `claude` > Individual plan
- `auggie` > Company plan
- `claude` > Company plan
- `codex` > Company plan

## Unified Configuration (`.agents/` + `AGENTS.md`)

For all agents, **one source of truth** is used for project instructions, workspace rules, and skills across all agents:

- [`AGENTS.md`](../AGENTS.md) in the root directory – main project instructions in the standard [agents.md](https://agents.md/) format. Accepted by:
    - `auggie`
    - `claude` (symlink `CLAUDE.md`)
    - `agy`
    - `codex`
- [`.agents/rules/`](../.agents/rules/) – modular workspace rules. Accepted by:
    - `auggie` (symlink `.augment/rules`)
    - `claude` (reference in `AGENTS.md`)
    - `agy`
    - `codex` (reference in `AGENTS.md`)
- [`.agents/skills/`](../.agents/skills/) – cross-tool skills in the standard [agentskills.io](https://agentskills.io/) format. Accepted by:
    - `auggie`
    - `claude` (symlink `.claude/skills`)
    - `agy`
    - `codex`
- [`.agents/commands/`](../.agents/commands/) – custom slash commands shared across agents; each `<name>.md` file creates a `/name` command. Accepted by:
    - `auggie` (symlink `.augment/commands`)
    - `claude` (symlink `.claude/commands`)
    - `agy` (symlink `.agents/workflows`)
- [`.agents/agents/`](../.agents/agents/) – subagents shared across agents. Accepted by:
    - `auggie` (symlink `.augment/agents`), `.md` format
    - `claude` (symlink `.claude/agents`), `.md` format
    - `codex` (symlink `.codex/agents`), `toml` format
- [`.agents/mcp_config.json`](../.agents/mcp_config.json) – shared JSON configuration of MCP servers. Accepted by:
    - `agy`
    - `claude` (symlink `.mcp.json`)

The commands to create symbolic links are (the path to the linked folder or file is always relative to the location of the link):

```sh
ln -s AGENTS.md CLAUDE.md
ln -s ../.agents/skills .claude/skills
ln -s ../.agents/rules .augment/rules
ln -s .agents/mcp_config.json .mcp.json
ln -s ../.agents/commands .augment/commands
ln -s ../.agents/commands .claude/commands
ln -s commands .agents/workflows
ln -s ../.agents/agents .claude/agents
ln -s ../.agents/agents .augment/agents
ln -s ../.agents/agents .codex/agents
```

### Naming convention

Local/shared/project-owned rules, commands, skills, and subagents are namespaced with a `run.` / `run-` prefix so they are clearly distinguishable from third-party or vendor-provided artifacts (e.g. `speckit-*`), which stay unprefixed and must never be renamed:

- **rules** (`.agents/rules/run.<name>.md`), **commands** (`.agents/commands/run.<name>.md`), **subagents** (`.agents/agents/run.<name>.md` / `.toml`) use a dot-separated `run.<name>` file name,
- **skills** (`.agents/skills/run-<name>/SKILL.md`) use a hyphen-separated `run-<name>` directory name; the skill's frontmatter `name:` matches the directory name.

Avoid double-prefixing (`run.run.<name>`, `run-run-<name>`). A command that is a thin entry point to a skill shares the same base name across both prefix styles (e.g. command `/run.add-agent-asset` <-> skill `run-add-agent-asset`).

### Rules

Workspace rules are in `.agents/rules/*.md` (Markdown with optional YAML frontmatter). Discovery by agent:

| Agent       | Discovery                                                                             |
| ----------- | ------------------------------------------------------------------------------------- |
| Antigravity | natively reads `.agents/rules/*.md`                                                   |
| Auggie      | via symlink `.augment/rules → ../.agents/rules`                                       |
| Claude Code | has no rules folder; imports from `AGENTS.md` via `@.agents/rules/<file>.md` as needed|
| Codex       | has no rules folder; references from `AGENTS.md` via `.agents/rules/<file>.md` as needed|

Auggie and Antigravity use **different frontmatter keys**, but each ignores unknown keys – thus the files work in both from a single location. Auggie distinguishes `type: always_apply|agent_requested`; Antigravity uses `trigger: always_on|glob (+ globs:)|model_decision|manual`. For `agent_requested` / `model_decision`, the agent decides on activation based on the `description:`. Both frontmatter blocks can be combined in a single file.

Example of a compatible file:

```markdown
---
description: Short description of when the agent should consider this rule
type: agent_requested
trigger: model_decision
---

# Rule Name

- Specific rule or convention.
- …
```

### Subagents

Shared subagents are defined in `.agents/agents/`. Since Claude Code and Auggie use **Markdown** (`.md`) and Codex uses **TOML** (`.toml`), the directory contains both formats for each subagent (`<name>.md` + `<name>.toml`). Each agent selects files in the format it recognizes during discovery and ignores the others.

**Formats:**

- **`.md` (Claude Code, Auggie):** YAML frontmatter with `name` (Claude), `description` (both), `color` (Auggie) fields, optionally `tools` and `model` (Claude). The body of the file is the system prompt.
- **`.toml` (Codex):** `name`, `description`, `developer_instructions` (system prompt) fields, optionally `model`, `sandbox_mode`.

**Antigravity** currently does not support file-defined subagents (only dynamic creation via `define_subagent` tool at runtime). If Google officially introduces this, we will add it.

**Auggie** supports subagents via the same `.augment/agents/` directory (they can also be created via the `/agents` wizard in interactive mode).

### What remains agent-specific

The following files and directories cannot be unified into `.agents/` or symlinked (different formats, naming, or discovery mechanisms). Details on each item are in the [Auggie](#auggie), [Claude Code](#claude-code), [Antigravity](#antigravity), and [Codex](#codex) sections below.

| Agent            | Specific artifacts (not covered by unified configuration)                                                                                                                                              |
| ---------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Auggie**       | `.augment/settings.json` (+ `.local`), `.augmentignore`; MCP via `auggie mcp` subcommands or `--mcp-config`                                                                                           |
| **Claude Code**  | `CLAUDE.local.md` (private, gitignored), `.claude/settings.json` (+ `.local`; permissions/env/hooks)                                                                                                   |
| **Antigravity**  | `GEMINI.md` (alternative workspace context), `.agents/hooks.json` (lifecycle hooks)                                                                                                                  |
| **Codex**        | `AGENTS.override.md` (per-dir override), `.codex/config.toml` (model/sandbox/MCP/hooks), `.codex/hooks.json`, `.codex/rules/*.rules` (sandbox allow/block), `.agents/plugins/` + `plugins/` (plugins) |

**MCP**: shared JSON configuration is in `.agents/mcp_config.json` (for both Claude Code and Antigravity via the `.mcp.json` symlink above). Auggie configures MCP servers via `~/.augment/settings.json` (commands `auggie mcp add|add-json|list|remove`) or ad-hoc `--mcp-config`; sharing via `.agents/mcp_config.json` is not directly possible (different format). Codex uses TOML – `[mcp_servers]` in `.codex/config.toml` – sharing via symlink is not possible.

**Hooks** (lifecycle interceptors – `PreToolUse`, `PostToolUse`, `Stop` etc.):

| Agent           | File (project-level)                                                  | Format                                                              |
| --------------- | --------------------------------------------------------------------- | ------------------------------------------------------------------- |
| **Antigravity** | `.agents/hooks.json`                                                  | `{ "hooks": { "PreToolUse": [{ "matcher": "…", "hooks": […] }] } }` |
| **Claude Code** | `.claude/settings.json` (or `.claude/settings.local.json`)            | `{ "hooks": { "PreToolUse": [{ "matcher": "…", "hooks": […] }] } }` |
| **Codex**       | `.codex/hooks.json` **or** inline `[hooks]` in `.codex/config.toml`   | JSON (same schema) / TOML: `[[hooks.PreToolUse]]`                   |
| **Auggie**      | `.augment/settings.json` (or `.augment/settings.local.json`)          | `{ "hooks": { "PreToolUse": [{ "matcher": "…", "hooks": […] }] } }` |

The JSON schema for hooks is almost identical between Antigravity, Claude Code, and Auggie – only the file location differs. Codex also offers an equivalent TOML syntax; if both `hooks.json` and inline `[hooks]` exist in the same layer, Codex loads both and issues a warning – one per layer is recommended.

### Notes

- **Windows**: git symlinks work reliably on Linux/macOS. The devcontainer runs on Linux, so this issue is avoided. For a native Windows clone, `git config core.symlinks=true` is required, and the user must have `SeCreateSymbolicLinkPrivilege`:
  - Set `git config --global core.symlinks true` - this only needs to be done once globally, at the beginning.
  - Turn on "Settings" (`Win + I`) > "System" > "Advanced" > "For developers" - this only needs to be done once globally, at the beginning.
- **Local overrides**: files matching `*.local.md`, `*.local.json`, `*.local.toml` are in `.gitignore` – use them for your private notes/settings that do not belong in the repository.
- **Skill format**: each skill is a `.agents/skills/<name>/SKILL.md` directory with YAML frontmatter `name` and `description` (a common requirement for Auggie CLI, Codex, and Antigravity).
- **Antigravity tmp files**: Antigravity occasionally references files created in the `~/.gemini/antigravity-cli/brain` directory. To simplify access to these files, a symlink is created: `tmp/antigravity → ~/.gemini/antigravity-cli/brain`.
- **AI agent terminal label**: If you run multiple agents in separate VS Code terminals, rename each terminal (`F2`) to the agent's name so you can tell them apart at a glance.

The sections below describe installation, logging in, as well as all configuration options for individual agents.

## Auggie

### Installation

The CLI (`auggie`) is installed **automatically** in the devcontainer using `.devcontainer/post-create.sh` > `# install Auggie CLI (Augment Code)`.

### Logging In

You need to create a personal account on [app.augmentcode.com](https://app.augmentcode.com/). For private use, pay for one of the plans (Individual plan). **For work use**, request to have your personal user added to the [company users](https://app.augmentcode.com/account/team) (Company plan).

When logging into `auggie`, use the personal account created on [app.augmentcode.com](https://app.augmentcode.com/).

On the Company plan, you can track [credits consumed by individual users](https://app.augmentcode.com/account/analytics).

### Commands

Commands ("slash commands") for standard work with the `auggie` CLI are:

- **select model:** `/model`
- **set default model:** `/config` > `Default Model` > `Claude Sonnet ...`
- **allow full permissions:**
    - `auggie` has full permissions in the default configuration
    - controlled version: `/permissions` > `A` > `Locals settings (personal)` > ...
- **select conversation:** `/sessions`, here conversations can also be deleted
- **new conversation:** `/new`
- **rename conversation:** `/rename <name>`
- **save conversation:** saves automatically
- **compact conversation:** has no built-in command
- **create a copy of conversation:** `/fork`
- **copy last response:** `/copy`
- **save conversation to file:** has no built-in command, but you can use the added `/run.save-chat` command. Before running `/run.save-chat`, it is recommended to create a copy of the conversation using `/fork` so that the history of the original conversation remains untouched
- **code-review:** has no built-in command, but you can use the added `/run.review-changes` command or `/run-review-changes` skill
- **list and select skill:** `/skills`
- **show usage/credits:** no built-in command; view consumption on the [web dashboard](https://app.augmentcode.com/account/analytics)
- **exit work:** `/exit`

See also other added commands in `.agents/commands` and skills in `.agents/skills`.

Keyboard shortcuts:
- beginning of line: `Ctrl Shift A`
- end of line: `Ctrl Shift E`
- move back one word: `Alt B`
- move forward one word: `Alt F`
- delete from cursor to beginning of line: `Ctrl U`
- delete from cursor to end of line: `Ctrl Shift K`
- delete previous word: `Ctrl W`

### Configuration

Auggie can be configured as follows:

| File / folder                     | Purpose                                          | Note                                                                                                                                                                                                               |
| --------------------------------- | ------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `.augment/rules/*.md`             | Project rules                                    | Rules in `.augment/rules` are Markdown files; supported types are **always_apply** and **agent_requested**. Workspace rules are intended to be committed to the repository. ([docs.augmentcode.com][augment-1])   |
| `AGENTS.md`                       | Hierarchical rules                               | Can be in root and subdirectories; Auggie searches for it in the current and parent directories when working with a file. ([docs.augmentcode.com][augment-2], [agents.md](https://agents.md/))                   |
| `CLAUDE.md`                       | Hierarchical rules compatible with Claude Code   | Works similarly to `AGENTS.md`; only `AGENTS.md` and `CLAUDE.md` appear hierarchically, not `.augment/rules` in subdirectories. ([docs.augmentcode.com][augment-2])                                                |
| `.augment/skills/<name>/SKILL.md` | Skills                                           | Each skill is its own directory with `SKILL.md`; must have YAML frontmatter `name` and `description`. ([docs.augmentcode.com][augment-3])                                                                           |
| `.claude/skills/<name>/SKILL.md`  | Skills compatible with Claude Code               | Auggie can discover them as workspace skills. ([docs.augmentcode.com][augment-3])                                                                                                                                  |
| `.agents/skills/<name>/SKILL.md`  | Standard agentskills.io format                   | Also supported as workspace skills. ([docs.augmentcode.com][augment-3])                                                                                                                                            |
| `.augment/commands/*.md`          | Custom slash commands                            | Triggered via `/security-review` in interactive mode or `auggie command security-review`; e.g., `.augment/commands/security-review.md` → `/security-review`. ([docs.augmentcode.com][augment-4])                   |
| `.augment/commands/foo/bar.md`    | Namespaced commands                              | E.g., `.augment/commands/frontend/component.md` → `/frontend:component`. ([docs.augmentcode.com][augment-4])                                                                                                       |
| `.claude/commands/*.md`           | Claude-compatible commands                       | Auggie automatically recognizes them for compatibility with existing Claude Code setups. ([docs.augmentcode.com][augment-4])                                                                                       |
| `.augmentignore`                  | Files to exclude from indexing                  | Works similarly to `.gitignore`; Auggie indexes the workspace except for files in `.gitignore` and `.augmentignore`. You can also use `!` to include gitignored files. ([docs.augmentcode.com][augment-5])         |

[augment-1]: https://docs.augmentcode.com/cli/rules "Rules & Guidelines - Auggie"
[augment-2]: https://docs.augmentcode.com/cli/rules "Rules & Guidelines - Auggie"
[augment-3]: https://docs.augmentcode.com/cli/skills "Skills - Auggie CLI"
[augment-4]: https://docs.augmentcode.com/cli/custom-commands "Custom Commands - Auggie"
[augment-5]: https://docs.augmentcode.com/cli/setup-auggie/workspace-indexing "Workspace indexing - Auggie"

In the directory structure, it looks like this:

```
repo/
  .augmentignore
  AGENTS.md
  CLAUDE.md

  .augment/
    rules/
      general.md
      frontend/react.md
    skills/
      deploy-guide/
        SKILL.md
    commands/
      security-review.md
      frontend/
        component.md
    settings.json          # mostly Auggie/CLI and advanced shared settings
    settings.local.json    # local, do not commit
    agents/                # subagents, mostly Auggie/CLI
      code-review.md

  .claude/
    skills/
      some-skill/
        SKILL.md
    commands/
      some-command.md

  .agents/
    skills/
      some-standard-skill/
        SKILL.md
```

## Claude Code

### Installation

The VS Code extension is installed **automatically** in the devcontainer using `.devcontainer/devcontainer.json` > `"customizations"` > `"vscode"` > `"extensions"` > `"anthropic.claude-code"`.

The CLI (`claude`) is installed **automatically** in the devcontainer using `.devcontainer/post-create.sh` > `# install Claude Code CLI`.

### Logging In

You need to create a personal account on [platform.claude.com](https://platform.claude.com/). For private use, pay for one of the plans (Individual plan). **For work use**, request to have your personal user added to the [company users](https://platform.claude.com/settings/members) (Company plan; with the role `Claude Code` or `Developer`).

When logging into `claude` > `/login`, select `2. Anthropic Console account · API usage billing`, use the personal account created on [platform.claude.com](https://platform.claude.com/), and choose "Quantea Technologies" as the organization.

On the Company plan, you can track [credits consumed by individual users](https://platform.claude.com/cost?group_by=key_id).

### Commands

Commands ("slash commands") for standard work with the `claude` CLI are:

- **select model:** `/model`
- **set default model:** no separate action needed — the model selected via `/model` persists across sessions
- **allow full permissions:**
    - fast version: `claude --dangerously-skip-permissions`
    - slower version: `/config` > `Default permission mode` > `Auto`, or toggle on the fly using `Shift Tab`
    - controlled version: `/permissions` > `Allow`|`Ask`|`Deny`|... > `Bash`, `Bash(npm *)`, `Edit`, `Edit(src/**)`, `Write`, `Read`, `WebFetch`, `WebSearch`, `NotebookEdit`, `Skill`, `Workflow`, `Monitor`, ...
- **select conversation:** `/resume`
- **new conversation:** `/clear`
- **rename conversation:** `/rename`
- **save conversation:** saves automatically
- **compact conversation:** `/compact`
- **create a copy of conversation:** `/fork`
- **copy last response:** `/copy`, `/copy [N]` to select a specific response
- **save conversation to file:** `/export`
- **code-review:** `/code-review` or you can use the added `/run.review-changes` command or `/run-review-changes` skill
- **list and select skill:** `/skills`
- **show usage/credits:**
    - `/usage` – current 5h and week window token usage
    - web: [claude.ai](https://claude.ai/) → profile → Settings → Usage
- **exit work:** `/exit`

See also other added commands in `.agents/commands` and skills in `.agents/skills`.

### Configuration

Claude Code can be configured as follows:

| File / folder                     | Purpose                                                                                        | Note                                                                                                                                                       |
| --------------------------------- | ---------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `CLAUDE.md`                       | Main project instructions: architecture, build/test commands, coding conventions, workflow.    | Project `CLAUDE.md` can be in the root or as `.claude/CLAUDE.md`; Claude loads it as persistent instructions. ([Claude API Docs][claude-1])                  |
| `.claude/CLAUDE.md`               | Alternative location for project instructions.                                                 | Same purpose as root `CLAUDE.md`, just stored in `.claude/`. ([Claude API Docs][claude-1])                                                                 |
| `CLAUDE.local.md`                 | Your private project notes/preferences.                                                        | Claude loads it together with `CLAUDE.md`; should be in `.gitignore`. ([Claude API Docs][claude-1])                                                         |
| `.claude/rules/*.md`              | Modular rules, e.g., coding style, testing, security, API rules.                               | Rules can be split into subdirectories and can be path-scoped. ([Claude API Docs][claude-1])                                                               |
| `.claude/settings.json`           | Shared project settings: permissions, env, hooks, plugins, exclusion of sensitive files.       | Shared project settings stored in the repository. ([Claude API Docs][claude-2])                                                                            |
| `.claude/settings.local.json`     | Local overrides for a specific project.                                                        | Local settings, Claude Code sets them as gitignored when created. ([Claude API Docs][claude-2])                                                            |
| `.claude/skills/<skill>/SKILL.md` | Skills: repeatable workflows, checklists, and specialized knowledge.                           | Skills can be called via `/skill-name`; both `.claude/commands/*.md` and `.claude/skills/<name>/SKILL.md` create a slash command. ([Claude API Docs][claude-3]) |
| `.claude/commands/*.md`           | Legacy custom slash commands.                                                                  | Still supported, but custom commands have been merged with skills; new items are better placed in skills. ([Claude API Docs][claude-3])                      |
| `.claude/agents/*.md`             | Custom subagents with independent prompt, tool access, and permissions.                        | Project subagents live in `.claude/agents/`; used for specialized tasks and isolated context. ([Claude API Docs][claude-4])                                |
| `.mcp.json`                       | Project MCP servers shared with the team.                                                      | Project-scoped MCP configuration is saved in `.mcp.json` in the project root. ([Claude API Docs][claude-5])                                                 |
| `.gitignore`                      | Protection against committing local Claude files and sensitive data.                            | To block Claude Code from accessing sensitive files, also use `permissions.deny` in `.claude/settings.json`. ([Claude API Docs][claude-2])                 |

[claude-1]: https://docs.anthropic.com/en/docs/claude-code/memory "How Claude remembers your project - Claude Code Docs"
[claude-2]: https://docs.anthropic.com/en/docs/claude-code/settings "Claude Code settings - Claude Code Docs"
[claude-3]: https://docs.anthropic.com/en/docs/claude-code/skills "Extend Claude with skills - Claude Code Docs"
[claude-4]: https://docs.anthropic.com/en/docs/claude-code/sub-agents "Create custom subagents - Claude Code Docs"
[claude-5]: https://docs.anthropic.com/en/docs/claude-code/mcp "Connect Claude Code to tools via MCP - Claude Code Docs"

In the directory structure, it looks like this:

```
repo/
  CLAUDE.md
  CLAUDE.local.md          # local, do not commit
  .mcp.json                # shared MCP servers

  .claude/
    CLAUDE.md              # alternative to root CLAUDE.md
    settings.json          # shared project settings
    settings.local.json    # local project settings, do not commit

    rules/
      general.md
      frontend/react.md
      backend/api.md

    skills/
      deploy-staging/
        SKILL.md
        scripts/
        examples.md

    commands/              # legacy; still supported
      review.md
      fix-issue.md

    agents/
      code-reviewer.md
      debugger.md
      security-auditor.md
```

## Antigravity

### Installation

The VS Code extension is not installed (it does not exist).

The CLI (`agy`) is installed **automatically** in the devcontainer using `.devcontainer/post-create.sh` > `# install Antigravity CLI`.

### Logging In

You need to create a google account on [accounts.google.com](https://accounts.google.com) - i.e., having a standard personal google account is sufficient. **Antigravity can be used for free** via your personal google account (Individual plan), but you must expect limits and availability based on capacity, or you can pay for one of the [plans](https://antigravity.google/pricing). **For work use**, request to have your personal user added to the [company users](https://console.cloud.google.com/iam-admin/iam) (Company plan).

When logging into `agy`, select `2. Use a Google Cloud project`, use the personal account created on [accounts.google.com](https://accounts.google.com), and enter `project-605967c9-39ce-4929-b5b` as the project ID.

On the Company plan, you can track the [current price (consumption) for services used](https://console.cloud.google.com/billing/reports).

#### Initial Company plan setup

For the google account you decide to use for the Company plan, you need to do the following in the [Google Cloud Console](https://console.cloud.google.com/):

- [Create a project](https://console.cloud.google.com/projectcreate), e.g., `Run AI`.
- [Link a billing account to it](https://console.cloud.google.com/billing), e.g., `Run billing`.
- Enable `Agent platform API`: [console](https://console.cloud.google.com/apis/dashboard?cloudshell=true) (the `|>_|` icon in the top right) > `gcloud services enable aiplatform.googleapis.com`

### Commands

Commands ("slash commands") for standard work with the `agy` CLI are:

- **select model:** `/model`
- **set default model:** no separate action needed — the model selected via `/model` persists across sessions
- **allow full permissions:**
    - fast version: `agy --dangerously-skip-permissions`
    - slower version: `/config` > `Tools Permission` > `always-proceed`
    - controlled version: `/permissions` > `Project` > `allowlist` > `command(*)`, `read_file(*)`, `write_file(*)`, `read_url(*)`, `mcp(*)`
- **select conversation:** `/resume`
- **new conversation:** `/clear`
- **rename conversation:** `/rename`
- **save conversation:** saves automatically
- **compact conversation:** has no built-in command
- **create a copy of conversation:** `/fork`
- **copy last response:** `/copy`
- **save conversation to file:** has no built-in command, but you can use the added `/run-save-chat` skill. Before running `/run-save-chat`, it is recommended to create a copy of the conversation using `/fork` so that the history of the original conversation remains untouched
- **code-review:** has no built-in command, but you can use the added `/run-review-changes` skill
- **list and select skill:** `/skills`
- **show usage/credits:** `/usage` – current session's token usage and remaining credits
- **exit work:** `/exit`

See also other added commands in `.agents/commands` and skills in `.agents/skills`.

### Configuration

Antigravity can be configured as follows:

| File / folder                     | Purpose                                                                                   | Note                                                                                                                                                                                                                                |
| --------------------------------- | ----------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `GEMINI.md`                       | Workspace context / general project instructions for Gemini/Antigravity CLI.              | Antigravity CLI supports workspace context files `GEMINI.md` as well as `AGENTS.md`. ([Google Antigravity][agy-1])                                                                                                                   |
| `AGENTS.md`                       | Tool-agnostic project instructions for coding agents.                                     | Antigravity CLI reads `AGENTS.md` from the active workspace; AGENTS.md is a general open format for agent instructions. ([Google Antigravity][agy-1], [agents.md](https://agents.md/))                                              |
| `.agents/agents.md`               | Definition of the team/personas, e.g., PM, engineer, QA, DevOps.                          | Google codelab uses `.agents/agents.md` to centrally define specialized agent personas. ([Google Codelabs][agy-2])                                                                                                                  |
| `.agents/rules/*.md`              | Workspace rules: project rules for code style, architecture, testing, and security.       | Workspace rules live in `.agents/rules/`; global rules are in `~/.gemini/GEMINI.md`. ([Google Antigravity][agy-3])                                                                                                                  |
| `.agents/skills/<skill>/SKILL.md` | Project skills: repeatable abilities/workflows packaged as a directory with `SKILL.md`.   | Antigravity currently defaults to `.agents/skills`; a skill is a folder containing `SKILL.md`. ([Google Antigravity][agy-4], [medium][agy-5])                                                                                       |
| `.agents/workflows/*.md`          | Workspace workflows / custom slash commands.                                              | Workflows are saved Markdown files and are run via `/workflow-name`; workspace workflows live in `.agents/workflows/`. ([Google Antigravity][agy-3])                                                                                |
| `.agents/hooks.json`              | Hooks: local shell scripts run at specified points in the agent execution cycle.          | Hooks are configured in `hooks.json` in the customization directory, e.g., `.agents/` in the workspace. ([Google Antigravity][agy-6])                                                                                               |
| `.agents/mcp_config.json`         | Project MCP configuration, mainly for Antigravity CLI / workspace setup.                  | Antigravity uses a separate `mcp_config.json`; IDE documentation mentions global `~/.gemini/antigravity/mcp_config.json`, while CLI/workspace guides also mention project MCP under `.agents/`. ([Google Antigravity][agy-7])       |

[agy-1]: https://antigravity.google/docs/gcli-migration "Migrating from Gemini CLI"
[agy-2]: https://codelabs.developers.google.com/autonomous-ai-developer-pipelines-antigravity "Build Autonomous Developer Pipelines using agents.md and skills.md in Antigravity  |  Google Codelabs"
[agy-3]: https://antigravity.google/docs/rules-workflows "Google Antigravity - Rules"
[agy-4]: https://antigravity.google/docs/skills "Agent Skills"
[agy-5]: https://medium.com/google-cloud/tutorial-getting-started-with-antigravity-skills-864041811e0d "Tutorial : Getting Started with Google Antigravity Skills"
[agy-6]: https://antigravity.google/docs/hooks "Hooks"
[agy-7]: https://antigravity.google/docs/mcp "Antigravity Editor: MCP Integration"

In the directory structure, it looks like this:

```
repo/
  GEMINI.md
  AGENTS.md

  .agents/
    agents.md

    rules/
      code-style.md
      testing.md
      security.md

    skills/
      deploy-staging/
        SKILL.md
        scripts/
        resources/
        examples/

    workflows/
      review.md
      fix-issue.md
      startcycle.md

    hooks.json
    mcp_config.json          # mainly Antigravity CLI / project MCP; IDE MCP is often global
```

## Codex

### Installation

The VS Code extension is installed **automatically** in the devcontainer using `.devcontainer/devcontainer.json` > `"customizations"` > `"vscode"` > `"extensions"` > `"openai.chatgpt"`.

The CLI (`codex`) is installed **automatically** in the devcontainer using `.devcontainer/post-create.sh` > `# install Codex CLI`.

### Logging In

You need to create a personal account on [chatgpt.com](https://chatgpt.com/). **Codex can also be used for free** via your personal GPT account (Individual plan), but you must expect limits and availability based on capacity, or you can pay for one of the [plans](https://chatgpt.com/#pricing). **For work use**, request to have your personal user added to the [company users](https://chatgpt.com/admin/members) (Company plan).

When logging into `codex`, select `1. Sign in with ChatGPT` (or `2. Sign in with Device Code` if the first option does not work), use the personal account created on [chatgpt.com](https://chatgpt.com/), and select `Run Development's Workspace` when logging in via the browser.

On the Company plan, you can track [credits consumed by individual users](https://chatgpt.com/admin/usage).

### Commands

Commands ("slash commands") for standard work with the `codex` CLI are:

- **select model:** `/model`
- **set default model:** no separate action needed — the model selected via `/model` persists across sessions
- **allow full permissions:**
    - fast version: `codex --dangerously-bypass-approvals-and-sandbox`
    - slower version: `/permissions` > `Full Access`
- **select conversation:** `/resume`
- **new conversation:** `/new`, `/clear`
- **rename conversation:** `/rename`
- **save conversation:** saves automatically
- **compact conversation:** `/compact`
- **create a copy of conversation:** `/fork`
- **copy last response:** `/copy`
- **save conversation to file:** has no built-in command, but you can use the added `$run-save-chat` skill. Before running `$run-save-chat`, it is recommended to create a copy of the conversation using `/fork` so that the history of the original conversation remains untouched
- **code-review:** has no built-in command, but you can use the added `$run-review-changes` skill
- **list and select skill:** `/skills` or start typing by `$`
- **show usage/credits:**
    - `/status` – current 5h and week window token usage
    - `/statusline` – customization of a persistent status line showing live usage in the terminal
- **exit work:** `/exit`

See also other added skills in `.agents/skills`. The added commands in `.agents/commands` are not supported in the `codex` CLI.

### Configuration

| File / folder                                | Purpose                                                                                                                   | Note                                                                                                                                                                                                   |
| -------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `AGENTS.md`                                  | Main project instructions for Codex: build/test commands, architecture, conventions, what “done” means.                   | Codex reads `AGENTS.md` before starting work; it looks for it in the project from the root to the current directory and aggregates instructions hierarchically. ([OpenAI Developers][codex-1])         |
| `AGENTS.override.md`                         | Optional override for instructions in a given directory.                                                                  | Has priority over `AGENTS.md` during discovery; Codex takes at most one instruction file per directory. ([OpenAI Developers][codex-1])                                                                 |
| `*/AGENTS.md`                                | Instructions for a specific subdirectory, module, or service.                                                             | Files closer to the active workplace are loaded later, so they can override more general rules from the root. ([OpenAI Developers][codex-1])                                                            |
| `.codex/config.toml`                         | Project settings for Codex: model, approvals, sandbox, MCP servers, inline hooks, skill overrides, subagent settings.     | Codex uses `~/.codex/config.toml` for user config and `.codex/config.toml` for project overrides; project `.codex/` layers are loaded only in trusted projects. ([OpenAI Developers][codex-2])          |
| `.codex/hooks.json`                          | Lifecycle hooks for the project, e.g., prompt validation, logging, checks after a tool call, or at the end of a turn.     | Codex looks for hooks alongside active config layers as `hooks.json` or inline `[hooks]` in `config.toml`; project hooks are loaded only in trusted projects. ([OpenAI Developers][codex-3])           |
| `.codex/rules/*.rules`                       | Rules for allowing/prompting/blocking commands outside the sandbox.                                                       | `.rules` are experimental command rules; Codex scans `rules/` alongside the active config layer, including `<repo>/.codex/rules/`. ([OpenAI Developers][codex-4])                                      |
| `.codex/agents/*.toml`                       | Project custom subagents / custom agents with their own model, sandbox, MCP, skills, and developer instructions.          | Project custom agents are separate TOML files in `.codex/agents/`; mandatory fields are `name`, `description`, `developer_instructions`. ([OpenAI Developers][codex-5])                                |
| `.agents/skills/<skill>/SKILL.md`            | Repo skills: repeatable workflows, runbooks, checklists, and specialized procedures.                                      | Codex reads repo skills from `.agents/skills` from the current directory to the repository root; a skill is a folder with `SKILL.md` and optional `scripts/`, `references/`, `assets/`. ([OpenAI Developers][codex-6]) |
| `.agents/plugins/marketplace.json`           | Repo marketplace plugin catalog for the team/project.                                                                     | A repo-scoped marketplace can be saved to `$REPO_ROOT/.agents/plugins/marketplace.json`; entries point to plugin folders, often under `./plugins/`. ([OpenAI Developers][codex-7])                      |
| `plugins/<plugin>/.codex-plugin/plugin.json` | Manifest of a Codex plugin.                                                                                               | A plugin must have a manifest `.codex-plugin/plugin.json`; it can package skills, MCP servers, hooks, app integrations, and assets. ([OpenAI Developers][codex-7])                                     |
| `plugins/<plugin>/skills/<skill>/SKILL.md`   | Skills packaged in a plugin.                                                                                              | A plugin manifest can point to a `skills` directory and thus distribute one or more skills. ([OpenAI Developers][codex-7])                                                                             |
| `plugins/<plugin>/hooks/hooks.json`          | Hooks packaged in a plugin.                                                                                               | A plugin can contain lifecycle hooks; the user must review and trust them before execution. ([OpenAI Developers][codex-7])                                                                             |
| `plugins/<plugin>/.mcp.json`                 | MCP servers packaged in a plugin.                                                                                         | In a standard project, MCP is configured via `.codex/config.toml`; a plugin can have its own `.mcp.json` pointed to by the manifest. ([OpenAI Developers][codex-8])                                    |
| `plugins/<plugin>/.app.json`                 | App / connector mappings for the plugin.                                                                                  | A plugin structure can contain `.app.json` for app or connector integrations. ([OpenAI Developers][codex-7])                                                                                           |

[codex-1]: https://developers.openai.com/codex/guides/agents-md "Custom instructions with AGENTS.md – Codex | OpenAI Developers"
[codex-2]: https://developers.openai.com/codex/config-basic "Config basics – Codex | OpenAI Developers"
[codex-3]: https://developers.openai.com/codex/hooks "Hooks – Codex | OpenAI Developers"
[codex-4]: https://developers.openai.com/codex/rules "Rules – Codex | OpenAI Developers"
[codex-5]: https://developers.openai.com/codex/subagents "Subagents – Codex | OpenAI Developers"
[codex-6]: https://developers.openai.com/codex/skills "Agent Skills – Codex | OpenAI Developers"
[codex-7]: https://developers.openai.com/codex/plugins/build "Build plugins – Codex | OpenAI Developers"
[codex-8]: https://developers.openai.com/codex/mcp "Model Context Protocol – Codex | OpenAI Developers"

In the directory structure, it looks like this:

```
repo/
  AGENTS.md
  AGENTS.override.md          # optional, temporary override
  services/
    api/
      AGENTS.md               # optional, subdirectory-specific

  .codex/
    config.toml               # project Codex config; trusted projects only
    hooks.json
    rules/
      default.rules
    agents/
      code-reviewer.toml
      explorer.toml

  .agents/
    skills/
      deploy-staging/
        SKILL.md
        scripts/
        references/
        assets/
      review-changes/
        SKILL.md
    plugins/
      marketplace.json

  plugins/
    my-plugin/
      .codex-plugin/
        plugin.json
      skills/
        my-skill/
          SKILL.md
      hooks/
        hooks.json
      .mcp.json
      .app.json
      assets/
```
