---
name: ui-vault
description: Personal UI and micro-interaction repository. Use when building, designing, or polishing frontend screens, forms, inputs, buttons, modals, or animations; when the user invokes /ui-vault (such as "/ui-vault text input", "/ui-vault list", or "/ui-vault suggest"); when asking for UI or animation ideas that fit their project; or when saving, browsing, or applying components from their UI library.
---

# UI Vault

A personal, stack-agnostic repository of curated UI components and micro-interactions. Use this vault to browse saved UIs by category, recommend fitting patterns for the user's current project, implement blueprints adapted to the host codebase, and store new patterns over time.

## When to Use

- The user invokes `/ui-vault` with a category, component type, ID, or subcommand (for example `/ui-vault text input`, `/ui-vault list`, `/ui-vault buttons`, `/ui-vault suggest`).
- The user is building or refining a frontend screen, form, dashboard, or interactive component and wants polished UI or animation suggestions.
- The user asks to browse, search, inspect, or apply a saved UI component or animation from their library.
- The user shares an animation, video, reel, reference, or newly built component and asks to save or store it in the vault for future projects.

## Command Router (`/ui-vault`)

When invoked directly (via `/ui-vault ...` or natural-language equivalents), route the argument as follows:

- `/ui-vault` or `/ui-vault list` or `/ui-vault all` -> Run **Workflow 1 (Browse All)** showing category counts and all saved UIs.
- `/ui-vault <category or keyword>` (e.g., `/ui-vault text input`, `/ui-vault inputs`, `/ui-vault password`, `/ui-vault buttons`) -> Run **Workflow 1 (Browse by Category / Tag)** matching via the Category & Alias Map and Catalog `Tags`.
- `/ui-vault inspect <id>` or `/ui-vault <exact-id>` -> Read `references/<category>/<id>.md` and display the full specification summary plus quick apply/prompt options.
- `/ui-vault suggest` -> Run **Workflow 2 (Suggest for Current Project)**.
- `/ui-vault apply <id>` -> Run **Workflow 3 (Apply a Saved Pattern)**.
- `/ui-vault save <notes>` -> Run **Workflow 4 (Store a New UI or Animation)**.

## Category & Alias Map

Normalize natural-language queries to these canonical categories before filtering the Catalog:

| Canonical Category | Common Aliases & Keywords |
| --- | --- |
| `inputs` | input, text input, text inputs, textfield, text field, form, forms, password, search, select, textarea, otp |
| `buttons` | button, buttons, btn, cta, toggle, switch, chip, pill |
| `navigation` | nav, navbar, sidebar, tabs, menu, breadcrumb, command palette, dock |
| `cards` | card, cards, bento, tile, pricing, preview |
| `modals` | modal, modals, dialog, drawer, sheet, popover, dropdown, tooltip |
| `feedback` | toast, alert, banner, notification, badge, validation, empty state |
| `loaders` | loader, loaders, loading, spinner, skeleton, progress, shimmer |
| `data-display` | table, list, chart, kpi, stat, timeline, accordion |
| `transitions` | transition, page transition, scroll, hero, reveal, parallax, background |

## Catalog

Read only the referenced spec file when a pattern is inspected or selected for implementation.

| ID | Category | Pattern | Tags | Motion Vibe | Best For | Dependencies | Spec Path |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `notched-scramble-input` | `inputs` | Notched-Border Floating Label + Live Validation + Scramble Password Reveal | text-input, floating-label, live-validation, password-reveal, scramble, form | Snappy, tactile, precision-tech | Auth forms, signup flows, settings, API key or password fields | Pure CSS + lightweight rAF | `references/inputs/notched-scramble-input.md` |

## Workflows

### 1. Browse & Display UIs by Category

Follow these steps when the user runs `/ui-vault <category>`, `/ui-vault list`, or asks what UIs are available:

1. If the user asked for all UIs (`list`, `all`, or bare `/ui-vault`), show a compact category overview with counts followed by a scannable table of every catalog entry grouped by category.
2. If the user provided a category or keyword (such as `text input` or `password`):
   - Resolve the query against the Category & Alias Map AND match against the Catalog `Tags` and `Pattern` columns.
   - Display every matching entry in a clean Markdown table containing: **ID**, **Pattern**, **Motion Vibe**, **Best For**, and **Dependencies**.
   - If the query matches a valid category that currently has 0 saved items, state clearly that the category is currently empty, list which categories have entries today, and offer to save a new component into that category.
3. End with concise next-step shortcuts using real IDs from the result (for example: `apply <id>`, `inspect <id>`, or `prompt <id>`).
4. Optional CLI helper for local environments with Python: run `python scripts/browse.py "<query>"` (or `--all` / `--categories`) to filter the Catalog table deterministically without manual scanning.

### 2. Suggest Patterns for the Current Project

Follow these steps when the user is building a UI or runs `/ui-vault suggest`:

1. Inspect the current project context: identify the page type (auth, dashboard, checkout, landing), visual tone (minimal, dark mode, enterprise, playful), and frontend stack (React, Next.js, Tailwind, CSS, Framer Motion).
2. Scan the Catalog table and match entries by `Best For`, `Tags`, `Motion Vibe`, and `Dependencies`.
3. Recommend 1 to 3 fitting entries. For each suggestion, explain why it fits the current screen and note any theme or dependency tradeoffs.
4. If no catalog entry fits cleanly, say so transparently instead of forcing an awkward match, and offer to design a custom pattern that can be saved afterward.
5. Wait for the user to pick a pattern (unless they already named one), then proceed to Workflow 3.

### 3. Apply a Saved Pattern

Follow these steps to implement a chosen vault entry in the user's codebase:

1. Read the full blueprint file at `references/<category>/<id>.md`. Never rely on the one-line catalog summary alone because easing curves, state lifecycles, edge cases, and accessibility rules live in the spec.
2. Inspect the target codebase's design tokens (surface colors, border colors, accent/status colors, border radius, typography) and form or state conventions (controlled props, ref forwarding, `react-hook-form`, etc.).
3. Translate the stack-agnostic spec into the project's exact stack while preserving motion curves, state lifecycles, `prefers-reduced-motion` fallbacks, and sharp-edge protections (such as autofill detection or caret preservation).
4. If the user asks for a reusable prompt instead of direct code edits, output a self-contained implementation prompt pre-filled with the blueprint's full specs and adapted to their target component.

### 4. Store a New UI or Animation

Follow these steps whenever the user asks to add a new UI component or micro-interaction to the vault:

1. Read `references/entry-template.md` and follow its standardized blueprint structure.
2. Distill the UI into a stack-agnostic specification covering visual anatomy, state lifecycle, exact motion timings and easing curves, accessibility and `prefers-reduced-motion` behavior, and subtle edge cases. Avoid hardcoding one-off project colors or single-framework boilerplate unless a specific library is strictly required.
3. Save the new spec file under `references/<category>/<kebab-case-id>.md` using a canonical category from the Category & Alias Map.
4. Add a concise single-row entry (including searchable `Tags`) to the Catalog table in `SKILL.md` so future `/ui-vault` lookups and suggestions discover it automatically.
5. Verify that the new file path in the Catalog matches the saved file path exactly.

## Gotchas

- Never inline full component specs or code snippets inside `SKILL.md`. Keep `SKILL.md` lean as a router and catalog so context stays small as the vault grows.
- Always keep the Catalog table in `SKILL.md` and the files under `references/` in sync whenever adding, renaming, or removing an entry.
- If the Catalog table grows past roughly 50 entries, split category tables into `references/<category>/INDEX.md`, keep only category counts and index pointers in `SKILL.md`, and update `scripts/browse.py` accordingly.
- Always adapt colors and surfaces to the active project's theme variables rather than hardcoding hex values from a demo.
- Never omit `prefers-reduced-motion` fallbacks or keyboard/ARIA behavior when applying a pattern.
