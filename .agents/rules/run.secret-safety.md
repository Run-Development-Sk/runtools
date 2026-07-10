---
description: >-
  Safe handling of secrets (API keys, tokens, passwords, private keys) -
  never print them in the output, logs, argv, or tickets; read only
  from the environment / secret manager. Applies to all agents and skills.
type: always_apply
trigger: always_on
---

# Rule: safe handling of secrets

Applies to all agents and all skills in this workspace.

## What is a secret

- API keys, tokens (OAuth/bearer), cookies, passwords, private keys, signing
  secrets, credential/session files, and values from the secret manager.
- Any values from `.env` files or from the process environment.

## Rules

- Secrets are **read exclusively from the environment** (e.g., `.env` file / secret
  manager), never hardcoded into scripts or documentation.
- **Never** print a secret value in the response, logs, error messages,
  command arguments, URLs, filenames, or tickets.
- Do not pass secrets via command line arguments (`argv`) – send them
  via the process environment; scripts should read them from env, not from parameters.
- When searching/grepping for potential secrets, do not print the found values – list only
  the filename, match count, or status "found / not found".
- If a secret appears in a previous context or tool output,
  do not repeat it – refer to it as "redacted".
