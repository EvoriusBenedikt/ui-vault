# UI Vault

A personal, stack-agnostic Agent Skill and repository for storing curated UI components, micro-interactions, and animation specifications.

Designed for progressive disclosure under the open Agent Skills (`SKILL.md`) format: AI coding agents read only the lightweight catalog table when browsing or suggesting patterns, and load full blueprints from `references/` only when inspecting or implementing a specific component.

## Repository Structure

```text
ui-vault/
├── README.md
├── SKILL.md
├── scripts/
│   └── browse.py
└── references/
    ├── entry-template.md
    └── inputs/
        └── notched-scramble-input.md
```

## Quick Commands

Invoke the skill in any compatible AI agent using `/ui-vault` or natural language:

| Command | Action |
| --- | --- |
| `/ui-vault` or `/ui-vault list` | Show category counts and all saved UI patterns |
| `/ui-vault text input` | Filter saved UIs by category, alias, or tag (e.g., `inputs`, `password`, `buttons`) |
| `/ui-vault inspect <id>` | View the full motion spec, edge cases, and accessibility rules for a pattern |
| `/ui-vault suggest` | Recommend 1–3 fitting patterns from the vault for your current project |
| `/ui-vault apply <id>` | Implement the pattern adapted to your project's stack and theme tokens |
| `/ui-vault save <notes>` | Distill a new UI or animation into `references/` and register it in `SKILL.md` |

## Local CLI Browser (Optional)

Filter the catalog directly from your terminal with zero external dependencies (Python 3.10+):

```bash
# List all saved patterns
python scripts/browse.py --all

# Show item counts per category
python scripts/browse.py --categories

# Search by natural-language alias, category, or tag
python scripts/browse.py "text input"
python scripts/browse.py password --json
```

## Adding a New UI Pattern

1. Copy `references/entry-template.md` to `references/<category>/<kebab-case-id>.md`.
2. Fill in the stack-agnostic motion timings, state lifecycle, edge cases, and `prefers-reduced-motion` fallback.
3. Add a single-row entry (with searchable `Tags`) to the `## Catalog` table in `SKILL.md`.

Canonical categories: `inputs`, `buttons`, `navigation`, `cards`, `modals`, `feedback`, `loaders`, `data-display`, `transitions`.

## Using Across Agents

Clone this repository into your agent's skills directory (or symlink `ui-vault/` into each tool's skills folder) so all your projects share one version-controlled UI library:

```bash
git clone https://github.com/<your-username>/ui-vault.git
```
