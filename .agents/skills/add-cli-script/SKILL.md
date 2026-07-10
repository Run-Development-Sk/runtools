---
name: add-cli-script
description: Adding a new helper Python CLI script to the runtools project according to project conventions. Use when you need to create a new independently executable tool and expose it as a console command.
---

# add-cli-script

A new helper tool belongs in `src/runtools/<name>.py` and is exposed as a
console command via `pyproject.toml` → `[project.scripts]`. Every script must
also be executable standalone (`python ./src/runtools/<name>.py`).

## Conventions (pattern based on existing scripts)

- The target version is Python 3.10+ (see `pyproject.toml`).
- Prefer the standard library; add a new dependency via the package manager (pip),
  not by manually editing `pyproject.toml`.
- `main()` returns an int (exit code): `0` on success, non-zero on error.
- The end of the file always has `if __name__ == "__main__": raise SystemExit(main())`.
- `print()` is intended as user-facing output in these CLI tools.
- For `subprocess.run(...)`, use an explicit `check=` and handle the return code.
- When working with files, verify existence and permissions (pattern in `gitexport.py`).

## Script template

```python
#!/usr/bin/env python3
import sys


def print_help():
    print("python3 <name>.py [ARGS]")
    print()
    print("Brief description of what the tool does.")


def main():
    argv = sys.argv[1:]

    if "-h" in argv or "--help" in argv:
        print_help()
        return 0

    # ... tool logic ...

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## Registering the console command

Add a line to `pyproject.toml` in the `[project.scripts]` section:

```toml
<name> = "runtools.<name>:main"
```

After installation (`pipx install --force …` or `pip install -e .`), the
command is available globally as `<name>`.

## Checklist

- [ ] File `src/runtools/<name>.py` with `main() -> int` and `raise SystemExit(main())`
- [ ] The script is also executable standalone: `python ./src/runtools/<name>.py`
- [ ] The command is registered in `pyproject.toml` → `[project.scripts]`
- [ ] The tool is added to the list of commands in `README.md`
- [ ] New dependencies (if any) are added via the package manager, not manually

## Anti-pattern

- ❌ Don't place logic outside `main()` such that it runs already on module import.
- ❌ Don't hardcode passwords/tokens; download password-protected URLs via `curl -u …` (see `AGENTS.md`).
- ❌ Don't add a dependency by manually editing `pyproject.toml` – use the package manager.
