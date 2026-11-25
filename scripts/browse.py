#!/usr/bin/env python3
"""Zero-dependency CLI browser for the ui-vault Catalog in SKILL.md.

Usage:
  python scripts/browse.py --all
  python scripts/browse.py --categories
  python scripts/browse.py "text input"
  python scripts/browse.py inputs --json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

CATEGORY_ALIASES: dict[str, set[str]] = {
    "inputs": {
        "input",
        "inputs",
        "text input",
        "text inputs",
        "text-input",
        "textfield",
        "text field",
        "form",
        "forms",
        "password",
        "search",
        "select",
        "textarea",
        "otp",
    },
    "buttons": {"button", "buttons", "btn", "cta", "toggle", "switch", "chip", "pill"},
    "navigation": {
        "nav",
        "navigation",
        "navbar",
        "sidebar",
        "tabs",
        "menu",
        "breadcrumb",
        "command palette",
        "dock",
    },
    "cards": {"card", "cards", "bento", "tile", "pricing", "preview"},
    "modals": {
        "modal",
        "modals",
        "dialog",
        "drawer",
        "sheet",
        "popover",
        "dropdown",
        "tooltip",
    },
    "feedback": {
        "feedback",
        "toast",
        "alert",
        "banner",
        "notification",
        "badge",
        "validation",
        "empty state",
    },
    "loaders": {
        "loader",
        "loaders",
        "loading",
        "spinner",
        "skeleton",
        "progress",
        "shimmer",
    },
    "data-display": {
        "data-display",
        "data display",
        "table",
        "list",
        "chart",
        "kpi",
        "stat",
        "timeline",
        "accordion",
    },
    "transitions": {
        "transition",
        "transitions",
        "page transition",
        "scroll",
        "hero",
        "reveal",
        "parallax",
        "background",
    },
}


def strip_backticks(value: str) -> str:
    return value.strip().strip("`").strip()


def parse_catalog(skill_md_path: Path) -> list[dict[str, str]]:
    text = skill_md_path.read_text(encoding="utf-8")
    section_match = re.search(
        r"^## Catalog\s*$(.*?)(?=^## |\Z)", text, flags=re.MULTILINE | re.DOTALL
    )
    if not section_match:
        return []

    rows: list[dict[str, str]] = []
    headers: list[str] = []

    for raw_line in section_match.group(1).splitlines():
        line = raw_line.strip()
        if not line.startswith("|") or not line.endswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if not headers:
            headers = [c.lower().replace(" ", "_") for c in cells]
            continue
        if all(re.fullmatch(r":?-{3,}:?", c) for c in cells):
            continue
        if len(cells) != len(headers):
            continue
        entry = {h: strip_backticks(v) for h, v in zip(headers, cells)}
        rows.append(entry)
    return rows


def resolve_category(query: str) -> str | None:
    normalized = re.sub(r"\s+", " ", query.strip().lower())
    for canonical, aliases in CATEGORY_ALIASES.items():
        if normalized == canonical or normalized in aliases:
            return canonical
    return None


def filter_entries(entries: list[dict[str, str]], query: str) -> tuple[str | None, list[dict[str, str]]]:
    normalized = re.sub(r"\s+", " ", query.strip().lower())
    canonical = resolve_category(normalized)
    tokens = [t for t in re.split(r"[\s,/-]+", normalized) if t]

    matched: list[dict[str, str]] = []
    for item in entries:
        item_cat = item.get("category", "").lower()
        haystack = " ".join(
            [
                item.get("id", ""),
                item_cat,
                item.get("pattern", ""),
                item.get("tags", ""),
                item.get("best_for", ""),
            ]
        ).lower()

        if canonical and item_cat == canonical:
            matched.append(item)
        elif normalized in haystack or (tokens and all(t in haystack for t in tokens)):
            matched.append(item)

    return canonical, matched


def print_table(entries: list[dict[str, str]]) -> None:
    if not entries:
        print("No matching UI patterns found.")
        return
    print("| ID | Category | Pattern | Motion Vibe | Dependencies | Spec Path |")
    print("| --- | --- | --- | --- | --- | --- |")
    for e in entries:
        print(
            f"| `{e.get('id', '')}` | `{e.get('category', '')}` | "
            f"{e.get('pattern', '')} | {e.get('motion_vibe', '')} | "
            f"{e.get('dependencies', '')} | `{e.get('spec_path', '')}` |"
        )


def main() -> int:
    parser = argparse.ArgumentParser(description="Browse UI patterns stored in ui-vault.")
    parser.add_argument("query", nargs="*", help="Category, alias (e.g. 'text input'), tag, or ID.")
    parser.add_argument("--all", action="store_true", help="List all UI patterns in the vault.")
    parser.add_argument("--categories", action="store_true", help="Show item counts per category.")
    parser.add_argument("--json", action="store_true", help="Output JSON.")
    args = parser.parse_args()

    skill_md = Path(__file__).resolve().parent.parent / "SKILL.md"
    if not skill_md.exists():
        print(f"Error: SKILL.md not found at {skill_md}", file=sys.stderr)
        return 1

    entries = parse_catalog(skill_md)

    if args.categories:
        counts = Counter(e.get("category", "uncategorized") for e in entries)
        summary = {cat: counts.get(cat, 0) for cat in CATEGORY_ALIASES}
        for cat, count in counts.items():
            if cat not in summary:
                summary[cat] = count
        if args.json:
            print(json.dumps(summary, indent=2))
        else:
            for cat, count in summary.items():
                print(f"- {cat}: {count}")
        return 0

    query = " ".join(args.query).strip()
    if args.all or not query or query.lower() in {"all", "list"}:
        if args.json:
            print(json.dumps(entries, indent=2))
        else:
            print_table(entries)
        return 0

    canonical, matched = filter_entries(entries, query)
    if args.json:
        print(json.dumps({"query": query, "resolved_category": canonical, "results": matched}, indent=2))
    else:
        if canonical and not matched:
            print(f"Category `{canonical}` currently has 0 saved patterns.")
            return 0
        print_table(matched)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
