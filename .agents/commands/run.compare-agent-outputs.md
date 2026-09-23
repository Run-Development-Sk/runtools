---
description: >-
  Entry point to the run-compare-agent-outputs skill – compare already existing
  agent outputs from files and recommend a solution, without running any agents.
---

# /run.compare-agent-outputs – Compare existing agent outputs

Thin entry point – **the entire procedure is in the skill `.agents/skills/run-compare-agent-outputs/SKILL.md`** (do not duplicate it here). Codex does not support slash commands – invoke the skill directly there.

Argument = the files to compare (a list, a glob, or a directory); without an argument, the skill asks.

```
/run.compare-agent-outputs tmp/my-task-analysis-*.md
```

The outputs are read as they are – no agent is launched and no credits are spent. If the proposals **do not exist yet** and are supposed to be generated, use `/run.compare-subagent-outputs`.
