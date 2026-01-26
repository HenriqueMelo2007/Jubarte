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
