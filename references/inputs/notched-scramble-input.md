# Notched-Border Floating Label + Live Validation + Scramble Password Reveal

- **ID:** `notched-scramble-input`
- **Category:** `inputs`
- **Tags:** `text-input, floating-label, notched-border, live-validation, password-reveal, scramble, form`
- **Motion Vibe:** Snappy, tactile, precision-tech
- **Best For:** Login/signup forms, account settings, password creation, API key/secret inputs, onboarding flows
- **Dependencies:** Pure CSS + lightweight `requestAnimationFrame` helper (no animation library required)
- **Source / Inspiration:** Curated Instagram Reel micro-interaction study (custom notched-border + scramble variant)

## Visual & Interactive Overview

A high-craft text and password input combining a smooth notched-border floating label, debounced live validation with SVG path draw-in status icons and inline password rule pills, and a progressive left-to-right character-scramble effect when toggling password visibility.

## Component API / Props

- `label: string`
- `type?: "text" | "email" | "password"`
- `value: string` and `onChange: (value: string) => void` (or uncontrolled/ref-forwarded integration with form libraries)
- `validate?: (value: string) => { valid: boolean; message?: string }`
- `passwordRules?: Array<{ label: string; test: (value: string) => boolean }>`
- `validateOn?: "change" | "blur"` (default: `"change"` debounced ~250ms after first interaction, immediate on blur/submit)
- `disabled?: boolean`

## Visual Anatomy & Theme Adaptation

- Inherit the host project's font family, input height, border radius, and theme tokens (surface background, neutral border, focus accent, success green, error red).
- Reserve vertical space or animate helper/error height smoothly so validation state transitions produce zero cumulative layout shift (CLS).
- Right-side icon cluster: place the validation status icon to the left of the password visibility toggle when `type="password"` is active, and add matching right padding on the `<input>` so text never collides with the icons.

## States & Motion Specification

### 1. Notched-Border Floating Label

- **Resting state (empty & unfocused):** Label sits vertically centered inside the input at normal body size and muted text color with `pointer-events: none`.
- **Active state (focused, non-empty, or browser-autofilled):** Label translates upward onto the top border and scales down (`scale(0.82)`, `transform-origin: left center`), shifting to the active accent color or the current valid/invalid status color.
- **Notch cutout:** Give the floated label `4px` to `6px` horizontal padding with a background matching the surrounding container surface (for example `var(--surface)` or `bg-card`) so it cleanly breaks the top border. If the input sits over a gradient or variable background, use a `<fieldset>` and `<legend>` cutout instead of a solid fill.
- **Motion:** Animate `transform` and `color` only over `200ms` with `cubic-bezier(0.22, 1, 0.36, 1)` so the transition stays GPU-composited with zero font-size jitter.

### 2. Live Validation Animations

- **State lifecycle:** Track `idle`, `valid`, and `invalid`. Never show error styling before the user has interacted (`dirty` or `blurred`).
- **Timing:** Debounce validation by `250ms` during typing after first interaction; validate immediately on `blur` or form submit.
- **Border & focus ring:** Smoothly interpolate border color and focus ring over `200ms` across neutral, accent, success, and error states.
- **Status icon (SVG draw-in):** Render an inline SVG checkmark (`valid`) or X/alert icon (`invalid`) animated with `stroke-dasharray` / `stroke-dashoffset` draw-in paired with a subtle scale pop (`0.8` to `1`).
- **Micro-shake:** Trigger a subtle horizontal shake (`+-4px` over `300ms`) only on invalid `blur` or failed submit, never on every keystroke.
- **Helper text & password rule pills:** Animate helper/error messages in with `opacity` and `translateY(-4px -> 0)`. For password fields with rules, display compact inline rule pills (such as `8+ chars`, `uppercase`, `number`, `symbol`) that spring-scale into the success color as each rule passes, paired with a smooth strength bar.

### 3. Character-Scramble Password Reveal FX

- **Toggle button:** Place an accessible `<button type="button">` on the far right inside the input with dynamic `aria-label` ("Show password" / "Hide password") and `aria-pressed={isVisible}`. Animate the eye icon with a diagonal SVG slash that draws or erases smoothly on toggle.
- **Scramble animation:** On visibility toggle, run a `~240ms` `requestAnimationFrame` loop cycling random glyph characters (`!@#$%^&*0123456789ABCDEF`) that progressively lock in from left to right into either plaintext characters (on reveal) or masked bullets (`•`, on hide).
- **Visual overlay isolation:** Render the scramble effect strictly in a synchronized visual overlay layer (or ephemeral display mask) and never mutate the real controlled input `value`.

## Edge Cases & Sharp Edges

- **Never corrupt controlled state:** Mutating the actual input `value` during the scramble causes live validation, password managers, or pressing Enter mid-animation to read scrambled characters. Always keep the real `<input>` value pure.
- **Interrupt on typing:** Immediately cancel any active `requestAnimationFrame` scramble loop if the user types or pastes during the transition.
- **Caret preservation:** Store `selectionStart` and `selectionEnd` before toggling input `type` between `"password"` and `"text"`, keep focus on the input, and restore the selection range immediately afterward so the cursor never jumps.
- **Browser autofill collision:** Handle `:-webkit-autofill` (via CSS pseudo-class and/or `animationstart` detection) so autofilled values trigger the floated label state immediately without overlapping text.
- **Theme surface matching:** In apps with light/dark modes or nested cards, bind the notch label's background to the card/container surface CSS variable rather than a hardcoded page background.

## Accessibility & Reduced Motion

- **ARIA & keyboard:** Associate helper/error messages via `aria-describedby`, toggle `aria-invalid` when invalid, keep the reveal toggle reachable via `Tab` and triggerable with `Enter` or `Space`, and announce live validation messages politely (`aria-live="polite"`).
- **Reduced motion:** Under `prefers-reduced-motion: reduce`, disable glyph scramble cycling and invalid micro-shake, falling back to a quick `120ms` opacity crossfade.
