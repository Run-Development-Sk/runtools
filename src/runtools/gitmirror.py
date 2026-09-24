#!/usr/bin/env python3
"""Mirror a git repository to another repository."""

import argparse
import getpass
import os
import re
import shlex
import shutil
import stat
import subprocess
import sys
import tempfile


def normalize_repo(repo: str) -> str:
    """Adds the git@github.com: prefix and .git suffix if missing."""
    if not repo.startswith("git@github.com:"):
        repo = "git@github.com:" + repo
    if not repo.endswith(".git"):
        repo = repo + ".git"
    return repo


def get_local_name(repo_url: str) -> str:
    """Derives the local folder name from the repository URL.

    Example: git@github.com:RunDevelopmentSk/test.git -> test
    """
    name = repo_url.rstrip("/")
    if name.endswith(".git"):
        name = name[:-4]
    return name.split("/")[-1]


def run(cmd: list, cwd: str | None = None, env: dict | None = None) -> None:
    """Runs a command, prints it, and exits the script on error."""
    display = " ".join(cmd)
    if cwd:
        print(f"[{cwd}]$ {display}")
    else:
        print(f"$ {display}")
    result = subprocess.run(cmd, cwd=cwd, env=env)
    if result.returncode != 0:
        print(f"Error: command failed with return code {result.returncode}")
        sys.exit(1)


def ask_continue(path: str) -> bool:
    """Asks the user whether to overwrite an existing folder."""
    try:
        response = input(f"\nWarning: folder '{path}' already exists.\n" "Continue and overwrite it? [y/N] ")
    except EOFError:
        return False
    return response.strip().lower() == "y"


def ensure_removed(path: str, always: bool = False) -> None:
    """Removes the folder if it exists. If always=False, asks the user."""
    if os.path.exists(path):
        if not always and not ask_continue(path):
            print("Aborted.")
            sys.exit(0)
        shutil.rmtree(path)


def validate_mirror_repo(repo_url: str) -> None:
    """Verifies that the mirror-repo contains 'test' as a standalone word in its name.

    The word 'test' must be bounded by the start/end of the string or by a
    non-alphanumeric character (e.g. hyphen, slash, dot).
    Examples that PASS:  test, test-repo, my-test, my-test-repo
    Examples that FAIL: latest, contest, testing, attest
    """
    name = get_local_name(repo_url)
    if not re.search(r"(?<![a-zA-Z0-9])test(?![a-zA-Z0-9])", name, re.IGNORECASE):
        print(
            f"Error: mirror-repo '{name}' does not contain 'test' as a standalone word.\n"
            "This safety check prevents overwriting a production repository.\n"
            "Examples of valid names: test, test-01, test-repo, my-test, my-test-v2\n"
            "Use --force to skip this check."
        )
        sys.exit(1)


def confirm_force(name: str) -> bool:
    """Asks the user to type the mirror-repo name to confirm overwriting it."""
    try:
        response = input(
            f"All history of mirror-repo '{name}' will be irreversibly overwritten.\n"
            "Type the mirror-repo name to confirm: "
        )
    except EOFError:
        return False
    return response.strip() == name


def ask_ssh_passphrase() -> str:
    """Prompts the user for the SSH passphrase (hidden input)."""
    return getpass.getpass("SSH key passphrase (Enter = no passphrase): ")


def create_ssh_env(passphrase: str) -> tuple[dict, str]:
    """Creates an env with a temporary SSH_ASKPASS script.

    SSH/git calls this script whenever it needs the key's passphrase –
    so there's no need to know the key's path or run ssh-agent.
    Returns a tuple of (env, path_to_askpass_script).
    """
    with tempfile.NamedTemporaryFile(mode="w", suffix=".sh", delete=False, encoding="utf-8") as tf:
        tf.write(f"#!/bin/sh\nprintf '%s' {shlex.quote(passphrase)}\n")
        askpass_path = tf.name
    os.chmod(askpass_path, stat.S_IRWXU)  # chmod 700, only the owner can read/execute

    env = os.environ.copy()
    env["SSH_ASKPASS"] = askpass_path
    env["SSH_ASKPASS_REQUIRE"] = "force"  # use askpass even without an X server / terminal
    env.pop("DISPLAY", None)

    return env, askpass_path


def parse_args() -> argparse.Namespace:
    epilog = """\
Example:
    %(prog)s RunDevelopmentSk/drinkcentrum-is.git RunDevelopmentSk/test.git"""
    parser = argparse.ArgumentParser(
        description=__doc__,
        epilog=epilog,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("source_repo", metavar="source-repo", help="source repository (owner/name)")
    parser.add_argument("mirror_repo", metavar="mirror-repo", help="mirror repository (owner/name)")
    parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="skip the safety check requiring 'test' in the mirror-repo name",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    source_repo = normalize_repo(args.source_repo)
    mirror_repo = normalize_repo(args.mirror_repo)
    local_name = get_local_name(mirror_repo)

    # GitHub repository names are case-insensitive
    if source_repo.lower() == mirror_repo.lower():
        print("Error: source-repo and mirror-repo are the same repository.")
        sys.exit(1)

    if args.force:
        print("Warning: --force used, skipping the 'test' name safety check for mirror-repo.")
        if not confirm_force(local_name):
            print("Aborted.")
            sys.exit(0)
    else:
        validate_mirror_repo(mirror_repo)

    # Tmp folders with a __ prefix/suffix to avoid collisions
    tmp_init = f"__{local_name}_init__"
    tmp_bare = f"__{local_name}_bare__"
    tmp_src = f"__{local_name}_src__"

    print(f"Source repo : {source_repo}")
    print(f"Mirror repo : {mirror_repo}")
    print(f"Local target: ./{local_name}/")

    # --- SSH passphrase ---
    print()
    passphrase = ask_ssh_passphrase()
    ssh_env, askpass_path = create_ssh_env(passphrase)

    try:
        # --- Check whether the final folder already exists ---
        ensure_removed(local_name)

        # --- Step 1: Create an empty repository and push it to mirror-repo ---
        print("\n=== Step 1: Resetting mirror-repo history ===")
        for tmp in (tmp_init, tmp_bare):
            ensure_removed(tmp, always=True)

        os.makedirs(tmp_init)
        run(["git", "init"], cwd=tmp_init)
        run(["git", "branch", "-M", "main"], cwd=tmp_init)

        with open(os.path.join(tmp_init, "README.md"), "w", encoding="utf-8") as f:
            f.write("# New project\n")

        run(["git", "add", "."], cwd=tmp_init)
        run(["git", "commit", "-m", "Initial commit"], cwd=tmp_init)

        run(["git", "clone", "--bare", tmp_init, tmp_bare], env=ssh_env)
        run(["git", "remote", "set-url", "origin", mirror_repo], cwd=tmp_bare, env=ssh_env)
        run(["git", "push", "--mirror", "--force"], cwd=tmp_bare, env=ssh_env)

        shutil.rmtree(tmp_init)
        shutil.rmtree(tmp_bare)

        # --- Step 2: Clone source-repo and push it to mirror-repo ---
        print("\n=== Step 2: Mirroring source-repo to mirror-repo ===")
        ensure_removed(tmp_src, always=True)

        run(["git", "clone", "--mirror", source_repo, tmp_src], env=ssh_env)
        run(["git", "remote", "set-url", "origin", mirror_repo], cwd=tmp_src, env=ssh_env)

        # Remove read-only GitHub refs (refs/pull/*) before the mirror push,
        # so GitHub doesn't reject the push with "deny updating a hidden ref".
        hidden = subprocess.run(
            ["git", "for-each-ref", "--format=%(refname)", "refs/pull/"],
            cwd=tmp_src,
            capture_output=True,
            text=True,
        )
        for ref in hidden.stdout.split():
            subprocess.run(["git", "update-ref", "-d", ref], cwd=tmp_src, check=True)

        run(["git", "push", "--mirror", "--force"], cwd=tmp_src, env=ssh_env)

        shutil.rmtree(tmp_src)

        # --- Step 3: Local clone of mirror-repo with a reference to source ---
        print("\n=== Step 3: Creating a local clone of mirror-repo ===")
        run(["git", "clone", mirror_repo, local_name], env=ssh_env)
        run(["git", "remote", "add", "upstream", source_repo], cwd=local_name, env=ssh_env)
        # Disable push to upstream
        run(["git", "remote", "set-url", "--push", "upstream", "DISABLED"], cwd=local_name)

        print(f"\nDone! Mirror repo cloned to ./{local_name}/")
        print(f"  origin -> {mirror_repo}  (fetch + push)")
        print(f"  upstream -> {source_repo}  (fetch only, push DISABLED)")

    finally:
        os.unlink(askpass_path)


if __name__ == "__main__":
    main()
