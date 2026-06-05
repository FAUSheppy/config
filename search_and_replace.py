#!/usr/bin/env python3

import argparse
from pathlib import Path
import sys


def find_files(directory: Path, recursive: bool):
    if recursive:
        yield from (p for p in directory.rglob("*") if p.is_file())
    else:
        yield from (p for p in directory.iterdir() if p.is_file())

def process_file(file_path: Path, search: str, replace: str):
    try:
        content = file_path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return None

    if search not in content:
        return None

    changed_lines = []

    for lineno, line in enumerate(content.splitlines(), start=1):
        if search in line:
            changed_lines.append({
                "line": lineno,
                "old": line,
                "new": line.replace(search, replace),
            })

    return {
        "path": file_path,
        "count": content.count(search),
        "new_content": content.replace(search, replace),
        "changed_lines": changed_lines,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Search and replace text in files with confirmation."
    )
    parser.add_argument(
        "directory",
        help="Directory to search"
    )
    parser.add_argument(
        "search",
        help="String to search for"
    )
    parser.add_argument(
        "replace",
        help="Replacement string"
    )
    parser.add_argument(
        "-r",
        "--recursive",
        action="store_true",
        help="Search recursively"
    )
    parser.add_argument(
        "-y",
        "--yes",
        action="store_true",
        help="Skip confirmation"
    )

    args = parser.parse_args()

    directory = Path(args.directory)

    if not directory.is_dir():
        print(f"Error: '{directory}' is not a directory.", file=sys.stderr)
        sys.exit(1)

    changes = []

    for file_path in find_files(directory, args.recursive):
        result = process_file(file_path, args.search, args.replace)
        if result:
            changes.append(result)

    if not changes:
        print("No matches found.")
        return

    print("\nPlanned changes:\n")
    total_replacements = 0
    
    for change in changes:
        print("=" * 80)
        print(f"File: {change['path']}")
        print(f"Replacements: {change['count']}")
        print()
    
        for line_change in change["changed_lines"]:
            print(f"Line {line_change['line']}:")
            print(f"  - {line_change['old']}")
            print(f"  + {line_change['new']}")
            print()
    
        total_replacements += change["count"]

    if not args.yes:
        try:
            response = input("\nApply these changes? [y/N]: ").strip().lower()
        except KeyboardInterrupt:
            print("Aborted")
            sys.exit(1)

        if response.lower() not in ("y", "yes"):
            print("Aborted.")
            return

    for change in changes:
        change["path"].write_text(
            change["new_content"],
            encoding="utf-8"
        )

    print(
        f"Completed. Modified {len(changes)} file(s), "
        f"{total_replacements} replacement(s)."
    )


if __name__ == "__main__":
    main()
