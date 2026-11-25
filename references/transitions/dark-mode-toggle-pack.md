# Dark Mode Toggle Pack (6 Theme-Switch Transitions)

- **ID:** `dark-mode-toggle-pack`
- **Category:** `transitions`
- **Tags:** `dark-mode, theme-toggle, toggle, button, view-transitions, clip-path, 3d-flip, conic-mask, stagger, light-dark`
- **Motion Vibe:** Expressive, tactile, adaptable (ranges from clean editorial to playful showcase)
- **Best For:** Full-page light/dark theme switches, settings cards, profile panels, dashboards, portfolios, and interactive widgets
- **Dependencies:** Pure CSS + lightweight JS (View Transitions API with clip-path/overlay fallback; CSS `@property` for Clock Sweep)
- **Source / Inspiration:** `@ui_motion_prompts` - Dark Mode Toggle Part 1 (one tap, six ways)

## Visual & Interactive Overview

A curated pack of six distinct light/dark theme transition animations triggered from a sun/moon toggle button. Each variant pairs a synchronized surface transition (radial portal, curtain wipe, staggered rows, 3D card flip, eclipse disc, or clock sweep) with bespoke icon choreography.

## Variant Selection Guide

Choose the variant that fits the host screen rather than using all six at once:

| Variant | Best Scope | Visual Feel |
| --- | --- | --- |
| `portal-open` | Full app, dashboard, SaaS | Crisp circular wave radiating from the clicked button |
| `curtain-drop` | Editorial pages, minimal apps | Smooth top-to-bottom theme curtain with falling icon |
| `line-by-line` | Settings panels, lists, dense forms | Calm, legible row-by-row stagger without heavy masking |
| `theme-flip` | Standalone cards, tiles, widgets (avoid on full pages) | Playful 3D flip revealing the opposite theme on the back |
| `eclipse-slide` | Portfolios, hero sections, showcases | Dramatic oversized disc gliding across the surface |
| `clock-sweep` | Creative tools, interactive demos | Radial clock-hand sweep synchronized with a 360deg icon spin |

## Component API / Props

- `variant: "portal-open" | "curtain-drop" | "line-by-line" | "theme-flip" | "eclipse-slide" | "clock-sweep"`
- `theme: "light" | "dark"`
- `onToggle: (nextTheme: "light" | "dark") => void`
- `durationMs?: number` (default `480` to `620` depending on variant)
- `disabled?: boolean`

## Visual Anatomy & Theme Adaptation

- Drive all colors from host theme tokens (`--surface`, `--surface-elevated`, `--text-primary`, `--text-muted`, `--border`, `--accent`) switched via a root class or `data-theme="dark"` attribute.
- For full-page transitions (`portal-open`, `curtain-drop`, `eclipse-slide`, `clock-sweep`), prefer the native **View Transitions API** (`document.startViewTransition`) so the browser snapshots old and new states automatically without duplicating DOM trees.
- For scoped containers or browsers without View Transitions support, clone or layer an incoming theme overlay above the current surface, animate its mask/clip-path, commit the real theme state on finish, and remove the overlay.
- For `theme-flip`, keep both front (light) and back (dark) faces synced to the same interactive state (switches, inputs, badges) so controls never reset mid-flip.

## States & Motion Specification

### 1. Portal Open (`portal-open`)

- **Trigger:** Capture the toggle button's center coordinates `(x, y)` and compute `maxRadius = Math.hypot(Math.max(x, width - x), Math.max(y, height - y))`.
- **Surface motion:** Animate `::view-transition-new(root)` (or incoming overlay) from `clip-path: circle(0px at x y)` to `clip-path: circle(${maxRadius}px at x y)`.
- **Icon motion:** Subtle scale pop (`0.85 -> 1`) and `30deg` tilt between sun and moon.
- **Timing:** `540ms` with `cubic-bezier(0.22, 1, 0.36, 1)`.

### 2. Curtain Drop (`curtain-drop`)

- **Surface motion:** Incoming theme wipes top-to-bottom via `clip-path: inset(0 0 100% 0)` -> `inset(0 0 0% 0)`.
- **Icon motion:** Outgoing icon drops/fades out while incoming moon/sun drops in from `-10px` with a slight spring overshoot (`translateY(-10px) -> translateY(2px) -> 0`).
- **Timing:** `500ms` with `cubic-bezier(0.22, 1, 0.36, 1)` for the curtain; `420ms` springy curve for the icon drop.

### 3. Line by Line (`line-by-line`)

- **Surface motion:** Container background transitions smoothly while direct child rows/sections transition color, background, and border with an incremental `transition-delay` (`45ms` to `60ms` per row index from top to bottom).
- **Icon motion:** Sun rays scale down (`scale(0)`) and tuck inward toward the center while the crescent mask slides in to carve the moon (and reverses smoothly back to sun).
- **Timing:** `280ms` per row with `45ms` stagger step, `cubic-bezier(0.22, 1, 0.36, 1)`.

### 4. Theme Flip (`theme-flip`)

- **Surface motion:** Wrap card in `perspective: 1100px`; inner container uses `transform-style: preserve-3d` and rotates `rotateY(0deg)` <-> `rotateY(180deg)`. Both faces set `backface-visibility: hidden`, with the dark face pre-rotated `rotateY(180deg)`.
- **Depth polish:** Add a brief subtle `scale(0.97)` midpoint or elevated shadow during rotation to reinforce physical depth.
- **Timing:** `620ms` with `cubic-bezier(0.34, 1.25, 0.64, 1)` (gentle overshoot settle).

### 5. Eclipse Slide (`eclipse-slide`)

- **Surface motion:** An oversized circular clip or disc (`~180%` to `220%` of container width so its leading edge forms a gentle arc) glides horizontally across the surface from offscreen left/right to full coverage, revealing the incoming theme behind its curved edge.
- **Icon motion:** Moon shadow disc slides smoothly across the sun circle in the same direction as the surface eclipse.
- **Timing:** `580ms` with `cubic-bezier(0.25, 0.9, 0.3, 1)`.

### 6. Clock Sweep (`clock-sweep`)

- **Surface motion:** Register `@property --sweep-angle { syntax: "<angle>"; inherits: false; initial-value: 0deg; }` and animate `--sweep-angle` from `0deg` to `360deg` inside `mask-image: conic-gradient(#000 0deg var(--sweep-angle), transparent var(--sweep-angle) 360deg)` (centered on the container or toggle).
- **Icon motion:** Sun/moon button spins a full `360deg` (`rotate(0deg -> 360deg)`) in lockstep with the sweep angle.
- **Timing:** `600ms` with `cubic-bezier(0.4, 0, 0.2, 1)`.

## Edge Cases & Sharp Edges

- **Rapid double-taps:** Track an incrementing transition ID or cancel any active Web Animation / View Transition before starting the next toggle so overlays never get stuck or flash stale themes.
- **View Transitions API fallback:** Feature-detect `document.startViewTransition`; on unsupported browsers, fall back cleanly to either a scoped overlay clip animation or a smooth `200ms` token fade.
- **Zero FOUC on initial load:** Apply the saved `localStorage` or `prefers-color-scheme` theme synchronously before first paint (for example via an inline head script) and disable theme transitions until after hydration.
- **3D Flip interaction bugs:** Set `pointer-events: none` and `aria-hidden="true"` (plus `inert` where supported) on the hidden back face so screen readers and keyboard tabs never focus invisible controls.
- **Clock Sweep `@property` support:** If CSS Houdini `@property` is unavailable, gracefully fall back to a `180ms` opacity crossfade instead of leaving the incoming layer stuck invisible.
- **Scrollbars and fixed headers:** When using View Transitions on full pages, ensure `::view-transition-old(root)` and `::view-transition-new(root)` disable default crossfade mixing (`animation: none; mix-blend-mode: normal;`) and stack `::view-transition-new(root)` above old so the clip-path reveals cleanly.

## Accessibility & Reduced Motion

- **ARIA & keyboard:** Use a native `<button type="button">` with `aria-pressed={isDark}` and dynamic `aria-label` (for example `"Switch to dark mode"` / `"Switch to light mode"`). Support `Enter` and `Space` activation and preserve focus ring visibility across both themes.
- **Reduced motion:** Under `prefers-reduced-motion: reduce`, bypass circular portals, curtain wipes, 3D flips, eclipse glides, conic sweeps, and icon spins, falling back to a calm `150ms` opacity/color transition (or instant theme swap).
