# runtools

Helper Python scripts for RunDevelopment projects. After installation they
are available as console commands:

- `dockerinfo` – overview of Docker images, containers, volumes and build cache
- `gitexport` – export changes from a Git repository
- `gitmirror` – mirror a Git repository to another repository

## Installation

> **Note:** Python 3.12+ on Debian/Ubuntu systems blocks installing
> packages directly into the system Python (PEP 668). For CLI tools we
> recommend `pipx`, which handles this automatically.

### Via `pipx` (recommended)

`pipx` installs the package into an isolated virtual environment and makes
the console commands (`dockerinfo`, `gitexport`, `gitmirror`) globally
available in `PATH`.

**Installing `pipx`** (if you don't have it yet):

```bash
sudo apt install pipx
pipx ensurepath
```

After `ensurepath`, restart your terminal (or run `source ~/.bashrc`) for the
path change to take effect.

**Installing `runtools`:**

```bash
pipx install "runtools @ git+https://git@github.com/RunDevelopmentSk/runtools.git@main"
```

### Via `requirements.txt` (devcontainer / venv)

Add to `requirements.txt`:

```text
runtools @ git+https://git@github.com/RunDevelopmentSk/runtools.git@main
```

and install with `--break-system-packages` (suitable in a devcontainer or venv):

```bash
pip install -r requirements.txt --break-system-packages
```

### Manually (as a fallback)

If installation is not possible, it's entirely sufficient to download the required script from the folder [https://github.com/RunDevelopmentSk/runtools > `/src/runtools/`](https://github.com/RunDevelopmentSk/runtools/tree/main/src/runtools) and run it like any other Python script, e.g.:

```
python3 dockerinfo.py
```

## Updating

Since installation is always done from the `main` branch (without versioning), pip/pipx
may not detect a commit hash change on re-run.

### Via `pipx`

```bash
pipx install --force "runtools @ git+https://git@github.com/RunDevelopmentSk/runtools.git@main"
```

(`pipx upgrade runtools` is not reliable when installing from git without tags —
hence `--force`.)

### Via `requirements.txt`

```bash
pip install --upgrade --force-reinstall -r requirements.txt --break-system-packages
```
