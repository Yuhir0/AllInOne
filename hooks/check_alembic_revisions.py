import re
import subprocess
import sys

# Change the regex to match the revision format of your project
revision_regex = re.compile(r"\d{14}")


def main():
    heads = revision_regex.findall(_run_alembic_heads())
    print("HEADS:", *heads, sep="\n")

    if len(heads) > 1:
        print("There are more than one head revision. Fix it merging it or setting in order.")
        sys.exit(1)

    current = revision_regex.search(_run_alembic_current()).group(0)

    if current not in heads:
        print("Current revision is not in heads. Run 'alembic upgrade head' to fix it.")
        sys.exit(1)

    print("Revisions are in order.")


def _run_alembic_heads() -> str:
    result = subprocess.run(["alembic", "heads"], capture_output=True, text=True)
    if result.returncode != 0:
        print("Error:", result.stderr)
        sys.exit(result.returncode)
    return result.stdout


def _run_alembic_current() -> str:
    result = subprocess.run(["alembic", "current"], capture_output=True, text=True)
    if result.returncode != 0:
        print("Error:", result.stderr)
        sys.exit(result.returncode)
    return result.stdout


if __name__ == "__main__":
    main()
