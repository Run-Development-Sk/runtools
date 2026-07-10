---
description: >-
  Default to English for generated code and documentation text regardless of
  the prompt's language, with narrow exceptions for documentation only; agent
  chat responses instead always follow the language of the user's prompt.
  Applies to all agents and all skills in this workspace.
type: always_apply
trigger: always_on
---

# Rule: English by default

Applies to all agents and all skills in this workspace.

## Code

- Source code, identifiers, and code comments are **always exclusively in
  English** - no exceptions, regardless of the prompt's language (whether
  given directly or via a file).

## Documentation and other text

- Default to English, regardless of the prompt's language (direct or via a
  file).
- Exceptions (documentation text only, never code):
  - the user **explicitly** requests another language,
  - the target document is **already entirely written** in another
    language - continue in that language to keep the document consistent.

## Agent chat responses

- The agent's chat responses (conversational text to the user) are **always
  in the language of the user's prompt**, regardless of the English-by-default
  rules above for code and documentation - these apply only to generated
  code/documentation content, not to the conversational response itself.
