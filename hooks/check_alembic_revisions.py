import re
import subprocess
import sys

revision_regex = re.compile(r"([A-z0-9_-]+)(\s\(head\))")


def main():
    heads = _get_heads()
    print("HEADS:", *heads, sep="\n")

    if len(heads) > 1:
        print("There are more than one head revision. Fix it merging it or setting in order.")
        sys.exit(1)

    current = _get_current()

    if current not in heads:
        print("Current revision is not in heads. Run 'alembic upgrade head' to fix it.")
        sys.exit(1)
    print("Revisions are in order.")


def _get_heads() -> list[str]:
    return [head.group(1) for head in revision_regex.finditer(_run_alembic_heads())]


def _run_alembic_heads() -> str:
    result = subprocess.run(["alembic", "heads"], capture_output=True, text=True)
    if result.returncode != 0:
        print("Error:", result.stderr)
        sys.exit(result.returncode)
    return result.stdout


def _get_current() -> str | None:
    if res := revision_regex.search(_run_alembic_current()):
        return res.group(1)
    return None


def _run_alembic_current() -> str:
    result = subprocess.run(["alembic", "current"], capture_output=True, text=True)
    if result.returncode != 0:
        print("Error:", result.stderr)
        sys.exit(result.returncode)
    return result.stdout


if __name__ == "__main__":
    main()
