"""
gcommit — Automated Git Commit Helper with Pre-commit Enforcement

This script automates a safe Git commit workflow by ensuring that
pre-commit hooks run repeatedly until the repository is clean before
creating a commit.

Usage:
    poetry run gcommit "type: commit message" [--push]

Arguments:
    "type: commit message"
        The commit message to use when creating the commit.

Options:
    --push
        If provided, the script will run `git push` after committing.

Workflow:
    1. Runs `pre-commit run --all-files` up to 3 times (default)
       to allow auto-fixes to stabilize.
    2. Aborts if pre-commit keeps modifying files.
    3. Stages all changes (`git add .`).
    4. Creates a commit with the provided message.
    5. Optionally pushes to the current remote branch.

Requirements:
    - git
    - pre-commit installed and configured in the repository
    - poetry
"""

import subprocess
import sys


def run(cmd: list[str], allow_fail: bool = False) -> int:
    print(f"\n▶ {' '.join(cmd)}")
    result = subprocess.run(cmd)
    if result.returncode != 0 and not allow_fail:
        raise subprocess.CalledProcessError(result.returncode, cmd)
    return result.returncode


def run_precommit_until_clean(max_runs: int = 3):
    for i in range(max_runs):
        print(f"\n🔍 pre-commit run ({i + 1}/{max_runs})")
        code = run(["pre-commit", "run", "--all-files"], allow_fail=True)

        if code == 0:
            print("✅ pre-commit clean")
            return

    raise RuntimeError("❌ pre-commit keeps modifying files, aborting.")


def main():
    if len(sys.argv) < 2:
        print('Uso: gcommit "type: message" [--push]')
        sys.exit(1)

    message = sys.argv[1]
    push = "--push" in sys.argv

    run_precommit_until_clean()
    run(["git", "add", "."])
    run(["git", "commit", "-m", message])

    if push:
        run(["git", "push"])


if __name__ == "__main__":
    main()
