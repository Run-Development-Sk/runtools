# AI agents

Devcontainer feature [`_agents`](https://github.com/RunDevelopmentSk/devcontainers).
Adds `claude`, `codex`, `agy` and `auggie` CLI AI agents in the form of a [unified configuration](../docs/ai-agents.md).

## Installation

Copy the contents of the `_agents` folder into the project folder.

Add the following to the end of the `.devcontainer/.post-create.sh` file:

```sh
# install AI agents
bash "$(dirname "${BASH_SOURCE[0]}")/post-create-agents.sh"
```

Add the following to the `.gitignore` file:

```sh
#
# AI agents
#
# ignore local overrides (per-developer notes/settings, never commit)
*.local.md
*.local.json
*.local.toml
```

Rebuild the devcontainer.

## Removal

Delete everything that was added.

Rebuild the devcontainer.
