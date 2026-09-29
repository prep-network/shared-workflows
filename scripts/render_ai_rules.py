#!/usr/bin/env python3
"""Render shared ai-rules fragments into a downstream repo's rules files.

Looks up the manifest entry whose `repo` matches --repo, concatenates the
fragment files under <rules-root>/<group>/*.md for each group listed (sorted by
filename within a group, groups in the order listed in the manifest), then
writes that body to every entry in the target's `outputs`, each according to
its own mode:

  - mode: block — embed the fragments between BEGIN/END markers in an existing
    file, preserving everything outside the markers. Use this when the file is
    also hand-maintained (e.g. a repo's CLAUDE.md).
  - mode: whole-file — write the fragments as the entire file content, fully
    owned by this script. Use this for a dedicated stub the file's consumer
    composes into other output on its own (e.g. Laravel Boost's
    `.ai/guidelines/*.md`, which Boost folds into every agent file it generates
    on `boost:install`/`boost:update` — so this must NOT sit inside one of
    those generated files, or a Boost regen can wipe it).

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

# Laravel Boost derives a guideline's description from the text after the first
# "# " heading, so a whole-file guideline stub must start with one.
WHOLE_FILE_TITLE = "# Shared Team Guidelines"
WHOLE_FILE_NOTE = (
    "> Managed by [prep-network/shared-workflows](https://github.com/prep-network/shared-workflows) "
    "`ai-rules/` — edit there, not here; this file is regenerated on every sync "
    "and local edits will be overwritten."
)


def gather_fragments(groups: list[str], rules_root: pathlib.Path) -> str:
    """Concatenate every fragment file in the given groups into one body."""
    sections = []
    for group in groups:
        group_dir = rules_root / group
        fragments = sorted(group_dir.glob("*.md"))
        if not fragments:
            print(f"::warning::No fragments found in {group_dir}", file=sys.stderr)
        for fragment in fragments:
            sections.append(fragment.read_text().rstrip() + "\n")
    return "\n".join(sections).rstrip()


def upsert_block(file_path: pathlib.Path, block: str) -> None:
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


def write_whole_file(file_path: pathlib.Path, body: str) -> None:
    """Overwrite file_path entirely — the file is fully owned by this script."""
    content = f"{WHOLE_FILE_TITLE}\n\n{WHOLE_FILE_NOTE}\n\n{body}\n"
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(content)


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

    body = gather_fragments(target["groups"], args.rules_root)

    for output in target["outputs"]:
        mode = output.get("mode", "block")
        file_path = args.target_checkout / output["file"]

        if mode == "whole-file":
            write_whole_file(file_path, body)
        elif mode == "block":
            block = f"{BEGIN_MARKER}\n{body}\n{END_MARKER}\n"
            upsert_block(file_path, block)
        else:
            print(f"::error::Unknown mode '{mode}' for {args.repo}:{output['file']}", file=sys.stderr)
            sys.exit(1)

        print(f"Rendered groups {target['groups']} into {file_path} (mode: {mode})")


if __name__ == "__main__":
    main()
