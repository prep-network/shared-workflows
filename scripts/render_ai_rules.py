#!/usr/bin/env python3
"""Render shared ai-rules fragments into a downstream repo's rules file.

Looks up the manifest entry whose `repo` matches --repo, concatenates the
fragment files under <rules-root>/<group>/*.md for each group listed (sorted by
filename within a group, groups in the order listed in the manifest), and writes
the result between BEGIN/END markers in <target-checkout>/<file>. Content outside
the markers is preserved verbatim; the file is created if it doesn't exist yet.

Usage:
    render_ai_rules.py \
        --manifest ai-rules/manifest.yml \
        --rules-root ai-rules \
        --repo prep-network/events \
        --target-checkout /path/to/events/checkout
"""
import argparse
import pathlib
import re
import sys

import yaml

BEGIN_MARKER = (
    "<!-- BEGIN SHARED AI RULES (managed by prep-network/shared-workflows "
    "ai-rules/ — edit there, not here; this block is regenerated) -->"
)
END_MARKER = "<!-- END SHARED AI RULES -->"

BLOCK_PATTERN = re.compile(
    re.escape(BEGIN_MARKER) + r".*?" + re.escape(END_MARKER) + r"\n?",
    re.DOTALL,
)


def render_block(groups: list[str], rules_root: pathlib.Path) -> str:
    """Concatenate every fragment in the given groups into one marked block."""
    sections = []
    for group in groups:
        group_dir = rules_root / group
        fragments = sorted(group_dir.glob("*.md"))
        if not fragments:
            print(f"::warning::No fragments found in {group_dir}", file=sys.stderr)
        for fragment in fragments:
            sections.append(fragment.read_text().rstrip() + "\n")
    body = "\n".join(sections).rstrip()
    return f"{BEGIN_MARKER}\n{body}\n{END_MARKER}\n"


def upsert(file_path: pathlib.Path, block: str) -> None:
    """Replace the marked block in file_path, or prepend it if absent/missing."""
    existing = file_path.read_text() if file_path.exists() else ""
    if BLOCK_PATTERN.search(existing):
        # Use a replacement function, not a string: fragment content routinely
        # contains literal backslashes (e.g. PHP namespaces like App\View\App),
        # which re.sub would otherwise try to interpret as backreferences.
        new_content = BLOCK_PATTERN.sub(lambda _match: block, existing)
    elif existing.strip():
        new_content = block + "\n" + existing.lstrip("\n")
    else:
        new_content = block
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(new_content)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", required=True, type=pathlib.Path)
    parser.add_argument("--rules-root", required=True, type=pathlib.Path)
    parser.add_argument("--repo", required=True, help="owner/name, e.g. prep-network/events")
    parser.add_argument("--target-checkout", required=True, type=pathlib.Path)
    args = parser.parse_args()

    manifest = yaml.safe_load(args.manifest.read_text())
    target = next(
        (t for t in manifest["targets"].values() if t["repo"] == args.repo),
        None,
    )
    if target is None:
        print(f"::error::No ai-rules manifest target for repo {args.repo}", file=sys.stderr)
        sys.exit(1)

    block = render_block(target["groups"], args.rules_root)
    file_path = args.target_checkout / target["file"]
    upsert(file_path, block)
    print(f"Rendered groups {target['groups']} into {file_path}")


if __name__ == "__main__":
    main()
