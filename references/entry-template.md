# <Pattern Name>

- **ID:** `<kebab-case-id>`
- **Category:** `<inputs | buttons | navigation | cards | modals | feedback | loaders | data-display | transitions>`
- **Tags:** `<comma-separated searchable keywords, e.g., text-input, floating-label, validation>`
- **Motion Vibe:** `<e.g., snappy, tactile, springy, subtle, editorial>`
- **Best For:** `<screens, flows, or component roles where this shines>`
- **Dependencies:** `<e.g., Pure CSS, CSS + rAF, Framer Motion>`
- **Source / Inspiration:** `<optional link or note on where this UI came from>`

## Visual & Interactive Overview

One or two sentences summarizing what the user sees and feels when interacting with this pattern.

## Component API / Props

- List the key props, slots, or callbacks the component should expose so it integrates cleanly with host apps.

## Visual Anatomy & Theme Adaptation

- Describe layout geometry and how surfaces, borders, and accent/status colors should map to the host project's design tokens.

## States & Motion Specification

### 1. <Core Interaction / Animation Name>

- **Resting state:** ...
- **Active / triggered state:** ...
- **Motion curve & timing:** Exact duration, easing curve or spring stiffness/damping, and GPU-composited properties (`transform`, `opacity`, `color`).

## Edge Cases & Sharp Edges

- Document concrete pitfalls (browser autofill, caret jumping, layout shift/CLS, rapid click/type interruption, dark/light surface mismatches).

## Accessibility & Reduced Motion

- **ARIA & keyboard:** Required roles, labels, focus management, and keyboard shortcuts.
- **Reduced motion:** Exact fallback behavior under `prefers-reduced-motion: reduce`.
