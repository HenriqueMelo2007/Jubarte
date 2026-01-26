import subprocess
import sys


def run(cmd: list[str]):
    print(f"\n▶ {' '.join(cmd)}")
    subprocess.run(cmd, check=True)


def main():
    if len(sys.argv) < 2:
        print('Uso: python scripts/git_commit.py "type: message"')
        sys.exit(1)

    message = sys.argv[1]

    run(["pre-commit", "run", "--all-files"])
    run(["git", "add", "."])
    run(["git", "commit", "-m", message])

    if "--push" in sys.argv:
        run(["git", "push"])


if __name__ == "__main__":
    main()
