#!/usr/bin/env python3
import argparse
import os
import re
import shutil
import subprocess
from pathlib import Path


ATTENTION = "\033[01;37mATTENTION:\033[00m"
ALERTS_LABEL = "\033[01;37mALERTS:\033[00m"
EXPORTED_LABEL = "\033[01;37mExported files\033[00m"
REMOVED_LABEL = "\033[01;37mRemoved files:\033[00m"
UPDATES_LABEL = "\033[01;37mUpdate files:\033[00m"


def run_command(command):
    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=False,
    )
    return result.stdout.splitlines()


def get_rev_id(rev=None):
    command = ["git", "rev-parse"]
    if rev:
        command.append(rev)
    else:
        command.append("HEAD")
    output = run_command(command)
    return output[0] if output else ""


def matches_any_regex(file_path, regexes):
    for regex in regexes:
        if regex.search(file_path):
            return True
    return False


def get_file_alerts(file_path, alert_regexes):
    file_alerts = []
    for alert_regex, file_alert in alert_regexes:
        if alert_regex.search(file_path):
            file_alerts.append(file_alert % file_path)
    return file_alerts


def commit_hash(value):
    if not re.fullmatch(r"[a-f0-9]{40}", value, re.IGNORECASE):
        raise argparse.ArgumentTypeError("must be a valid Git commit hash")
    return value


def parse_args():
    description = f"""\
Export files changed between two revisions of a Git repository.

{ATTENTION} Files are exported as they are in the actual state of the repository (committed or uncommitted).
Provided start/end revisions are used just to find modifications in the project which happened between them.
They do not change the actual revision of the project.
To export files in versions from a specific revision or branch, update the project accordingly by git checkout.
In most cases, you will export the last version of files (you are working on) for FTP update.

{ATTENTION} By default *.js and *.less (placed in directories .../js/sources/*.js,
.../js/libs/sources/*.js, .../css/less/*.less and .../css/libs/less/*.less) are NOT exported.
Use option --export-sources to export also *.js and *.less source files.

{ATTENTION} There is the explicit list of ignored files which are NOT exported (see gitexport.py > ignored_regexes).
Then *.js and *.less source files are NOT exported too (see the previous paragraph).
Use option --export-ignored to export also these ignored files and *.js and *.less source files.

{ATTENTION} There is the explicit whitelist of files which are ALWAYS exported (see gitexport.py > exported_regexes),
even when they match the ignored files or the *.js and *.less source rule.

{ATTENTION} Be aware that revisions in your local repository can have different local order
than they have in repositories of your colleagues."""
    epilog = """\
Examples:
%(prog)s 9864038c3eb54387fd205d2b541ada89827ba2ef 2b8f5a6fcf6c41bfbf3d63f7a5e0b7cabe75e764 /tmp/export
    Exports all files changed from rev 9864038c3eb54387fd205d2b541ada89827ba2ef to 2b8f5a6fcf6c41bfbf3d63f7a5e0b7cabe75e764 (inclusive) into directory /tmp/export.
    The *.js and *.less sources are NOT exported.

%(prog)s 9864038c3eb54387fd205d2b541ada89827ba2ef 2b8f5a6fcf6c41bfbf3d63f7a5e0b7cabe75e764 /tmp/export --export-sources
    Exports all files changed from rev 9864038c3eb54387fd205d2b541ada89827ba2ef to 2b8f5a6fcf6c41bfbf3d63f7a5e0b7cabe75e764 (inclusive) into directory /tmp/export.
    The *.js and *.less sources are exported too.

%(prog)s 9864038c3eb54387fd205d2b541ada89827ba2ef 2b8f5a6fcf6c41bfbf3d63f7a5e0b7cabe75e764 /tmp/export --export-ignored
    Exports all files changed from rev 9864038c3eb54387fd205d2b541ada89827ba2ef to 2b8f5a6fcf6c41bfbf3d63f7a5e0b7cabe75e764 (inclusive) into directory /tmp/export.
    The ignored files and *.js and *.less sources are exported too."""
    parser = argparse.ArgumentParser(
        description=description,
        epilog=epilog,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("start_rev", metavar="START_REV", type=commit_hash, help="start revision (full commit hash)")
    parser.add_argument("end_rev", metavar="END_REV", type=commit_hash, help="end revision (full commit hash)")
    parser.add_argument("export_dir", metavar="EXPORT_DIR", type=Path, help="existing writable export directory")
    parser.add_argument("--export-sources", action="store_true", help="export also *.js and *.less source files")
    parser.add_argument(
        "--export-ignored",
        action="store_true",
        help="export also ignored files and *.js and *.less source files",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    rev1 = args.start_rev
    rev2 = args.end_rev
    export_dir = args.export_dir

    curr_rev = get_rev_id().strip()
    status_output = run_command(["git", "status", "--porcelain"])
    if status_output:
        curr_rev += " \033[01;37mwith uncommitted changes\033[00m"

    if not export_dir.exists() or not os.access(export_dir, os.W_OK):
        print(f"Directory {export_dir} does not exist or it is not writable")
        return 1
    if not export_dir.is_dir():
        print(f"{export_dir} is not a directory")
        return 1

    dir_files = [item for item in export_dir.iterdir()]
    if dir_files:
        print(f"{ATTENTION} Directory {export_dir} is not empty!")
        print("Press ENTER to continue or CTRL+C to exit")
        try:
            input()
        except KeyboardInterrupt:
            return 0

    print("Processing...")

    modified_map = {}
    removed_map = {}
    diff_output = run_command(["git", "diff", "--name-status", f"{rev1}^..{rev2}"])
    for item in diff_output:
        parts = item.split("\t")
        if len(parts) < 2:
            print("Invalid item in output of git diff")
            print(item)
            return 1

        status = parts[0][0].upper()
        if status in ("A", "M"):
            file_path = parts[1]
            modified_map[file_path] = True
            removed_map.pop(file_path, None)
        elif status == "D":
            file_path = parts[1]
            removed_map[file_path] = True
            modified_map.pop(file_path, None)
        # rename
        elif status == "R":
            old_file = parts[1]
            new_file = parts[2]
            removed_map[old_file] = True
            modified_map.pop(old_file, None)
            modified_map[new_file] = True
            removed_map.pop(new_file, None)
        else:
            print("Invalid item in output of git diff")
            print(item)
            return 1

    modified = sorted(modified_map.keys())
    removed = sorted(removed_map.keys())

    ds = os.sep
    vendors_regex = re.compile(re.escape(f"{ds}vendors{ds}"))
    sources_regex = re.compile(
        re.escape(ds)
        + r"(?:css|js)(?:"
        + re.escape(f"{ds}libs")
        + r")?(?:"
        + re.escape(f"{ds}less")
        + r"|"
        + re.escape(f"{ds}sources")
        + r")"
        + re.escape(ds)
    )
    updates_regex = re.compile(re.escape(f"{ds}updates{ds}"))
    # takes precedence over ignored_regexes and the *.js/*.less source rule
    exported_regexes = [
        re.compile(r"^\.prodcontainer/"),
    ]
    ignored_regexes = [
        re.compile(r"^\.[a-zA-Z]+/?"),
        re.compile(r"^misc/"),
        re.compile(r"^docs/"),
        re.compile(r"^AGENTS\.md"),
        re.compile(r"^CLAUDE\.md"),
        re.compile(r"^book\.json"),
        re.compile(r"^book\.readme"),
        re.compile(r"^default\.gitconfig"),
        re.compile(r"^gitexport\.py"),
        re.compile(r"^gulpfile\.js"),
        re.compile(r"^package-lock\.json"),
        re.compile(r"^package\.json"),
        re.compile(r"^tsconfig\.json"),
        re.compile(r"^readme\.md", re.IGNORECASE),
        re.compile(r"^pyproject\.toml"),
        re.compile(r"^pyrightconfig\.json"),
    ]
    alert_regexes = [
        (
            re.compile(r"^\.htaccess"),
            'In file %s search for "ATTENTION: For Apache 2.4.52" and consider that warning!',
        ),
    ]

    alerts = []
    updates = []
    filtered_modified = []
    for file_path in modified:
        extension = Path(file_path).suffix.lstrip(".").lower()
        is_exported = matches_any_regex(file_path, exported_regexes)
        is_source_file = (
            not is_exported
            and not args.export_sources
            and not args.export_ignored
            and not vendors_regex.search(file_path)
            and sources_regex.search(file_path)
            and extension in ("less", "js")
        )
        is_ignored = (
            not is_exported
            and not args.export_ignored
            and not vendors_regex.search(file_path)
            and matches_any_regex(file_path, ignored_regexes)
        )

        if is_source_file or is_ignored:
            continue

        filtered_modified.append(file_path)
        if not vendors_regex.search(file_path):
            if updates_regex.search(file_path):
                updates.append(file_path)
            alerts.extend(get_file_alerts(file_path, alert_regexes))

    modified = filtered_modified

    toplevel_output = run_command(["git", "rev-parse", "--show-toplevel"])
    root = Path(toplevel_output[0]) if toplevel_output else Path.cwd()

    if modified:
        print()
        print(f"{EXPORTED_LABEL} (in version from revision {curr_rev}):")
        for file_path in modified:
            source_path = root / file_path
            if not source_path.exists():
                print(
                    f"{ATTENTION} File {file_path} does not exist in actual revision ({curr_rev})!"
                )
                continue
            if not os.access(source_path, os.R_OK):
                print(
                    f"{ATTENTION} File {file_path} is not available (check the rights)!"
                )
                continue
            if not source_path.is_file():
                print(f"{ATTENTION}  {file_path} is not a file!")
                continue

            target_path = export_dir / file_path.lstrip(ds)
            target_path.parent.mkdir(parents=True, exist_ok=True)
            try:
                shutil.copy2(source_path, target_path)
            except OSError:
                print(f"{ATTENTION} Copying of file {file_path} has failed!")
                continue
            print(file_path)

    if removed:
        print()
        print(REMOVED_LABEL)
        for file_path in removed:
            print(file_path)

    if updates:
        print()
        print(f"{UPDATES_LABEL} (in version from revision {curr_rev})")
        for file_path in updates:
            source_path = root / file_path
            if not source_path.exists():
                print(
                    f"{ATTENTION} File {file_path} does not exist in actual revision ({curr_rev})!"
                )
                continue
            if not os.access(source_path, os.R_OK):
                print(
                    f"{ATTENTION} File {file_path} is not available (check the rights)!"
                )
                continue
            if not source_path.is_file():
                print(f"{ATTENTION} {file_path} is not a file!")
                continue
            print(file_path)

    if alerts:
        print()
        print(ALERTS_LABEL)
        for alert in alerts:
            print(alert)

    user_name = "unknown user"
    output = run_command(["git", "config", "user.name"])
    if output:
        user_name = output[0]

    full_user_name = user_name
    if user_name:
        match = re.search(
            r"[a-z0-9._\-]+@[a-z0-9._\-]+\.[a-z]{2,4}", user_name, re.IGNORECASE
        )
        if match:
            user_name = match.group(0).split("@", 1)[0]
        user_name = re.sub(r"[^a-z0-9]+", "_", user_name, flags=re.IGNORECASE).upper()

    project_name = os.getenv("DOCKER_WORKDIR_LOCAL_BASENAME")
    if not project_name:
        project_name = root.name
    project_name = re.sub(r"[^a-z0-9]+", "_", project_name, flags=re.IGNORECASE).upper()

    filename = "EXPORT_REV"
    if user_name:
        filename += f"_{user_name}"
    if project_name:
        filename += f"_{project_name}"

    output = run_command(["git", "log", "-1", "--format=%B", rev2])
    output.insert(0, "")
    output.insert(
        0,
        f"Exported from {root}{ds} (in version from revision {curr_rev}) by {full_user_name}:",
    )
    output.append(f"Export was done from revision {rev1} to revision {rev2}.")
    output.append("")
    output.append(
        f'ATTENTION (if you are not the user "{full_user_name}") then you have to export'
    )
    output.append(
        f"also all your revisions which were pushed after the creation of {rev2}."
    )
    output.append(
        f'If you have your own  "EXPORT_REV_" file on FTP then export from {rev2}.'
    )

    (export_dir / filename).write_text("\n".join(output).strip(), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
