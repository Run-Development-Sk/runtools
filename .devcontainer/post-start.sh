#!/bin/bash
# this script is used as "postStartCommand" in devcontainer.json

# create scratchpad file if it does not exist
echo "" && echo "Creating scratchpad file..."
SCRATCHPAD_DIR="$(dirname "${BASH_SOURCE[0]}")/../tmp"
SCRATCHPAD_FILE="${SCRATCHPAD_DIR}/tmp.txt"
if [ ! -f "${SCRATCHPAD_FILE}" ]; then
    mkdir -p "${SCRATCHPAD_DIR}"
    echo "This is your scratchpad..." > "${SCRATCHPAD_FILE}"
fi

# AI agents: materialize the symlinked rules dir that auggie can't read as a symlink
bash "$(dirname "${BASH_SOURCE[0]}")/post-start-ai-agents.sh"
