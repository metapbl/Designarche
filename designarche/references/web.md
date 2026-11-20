# Web apps and websites

Read this for anything rendered in a browser: sites, landing pages, web apps, dashboards, extension popups, Electron or Tauri views styled as web pages. Use [slop-signs.md](slop-signs.md) as well. If the web view lives inside a desktop app, [desktop.md](desktop.md) wins where the two disagree.

## Rules

Structure
- Real HTML first: headings in order, `button` for actions and `a` for navigation, `label` tied to every input, `lang` on the root, alt text on meaningful images and empty alt on decorative ones.
- Every color and font comes from a token (CSS custom properties or the framework's theme). No literal colors or font families past the token definitions.
- Support light and dark with `prefers-color-scheme` (or the product's own switch) by swapping tokens, not by restyling components.

Layout
- Design from narrow to wide: it must work at 360 px, and at 1920 px the content sits in a capped, centered column: extra width becomes margin, not longer lines.
- No horizontal scrolling of the page. Use `overflow-x: clip` where clipping is needed (not `hidden`, which breaks sticky positioning) and never size things to `100vw`.
- Grid tracks that hold images use `minmax(0, 1fr)`; long words and URLs wrap (`overflow-wrap: break-word`, `min-width: 0` on flex and grid children).
- One spacing scale (for example 4 px steps). Related things close, groups apart.
- On a 1280 × 800 screen a landing page's first view already holds its headline, one supporting sentence and its main action. Keep copy short; one idea per screen.

Type
- One or two families, a few sizes from one scale, regular and medium weights. Body text 16 px or more on phones, line length about 60–75 characters.
- Labels, table heads and navigation in sentence case at normal tracking.

Interaction
- Every interactive element shows `:focus-visible` immediately. Do not remove outlines without a replacement.
- Hover changes color or surface; pressing may scale down slightly. No lift-and-glow on every card.
- Touch targets at least 44 × 44 px on touch screens.
- Forms: visible labels (not placeholder-only), errors next to the field in words, the submit button says what it does.

Motion
- Animate only `transform` and `opacity`; never `transition: all`, never width, height, top or left.
- Every animation has a `prefers-reduced-motion: reduce` fallback, and content is visible with scripting off or before scripts run.

## Slop signs

Accessibility and robustness
- `must-fix` Interactive elements without a visible keyboard focus state, or outlines removed with nothing in their place — Instead: a `:focus-visible` style on every interactive element.
- `must-fix` Inputs with no label, icon buttons with no accessible name, `div` or `span` used as buttons — Instead: `label`, `aria-label` where there is no visible text, real `button` and `a` elements.
- `must-fix` Content hidden until a script or an entrance animation runs — Instead: content visible by default; animation only enhances.
- `must-fix` Animations with no reduced-motion fallback — Instead: a `prefers-reduced-motion: reduce` rule that removes or shortens them.
- `must-fix` The page scrolls sideways on a phone — Instead: fluid widths, wrapping, `overflow-x: clip`, no `100vw` widths.

Web-specific slop
- `should-fix` `transition: all`, or animating width, height, top or left — Instead: transition named properties; move with `transform`.
- `should-fix` Literal hex colors and font families scattered through components — Instead: tokens declared once and used by name.
- `should-fix` A tiny tracked-capitals "eyebrow" label above every heading — Instead: let the heading stand alone, or a plain sentence-case subtitle.
- `should-fix` Meta lines joined with middle dots and arrows glued to link text (`Read more →`) — Instead: plain, separate pieces of meta and descriptive link text.
- `should-fix` A fake browser or OS window drawn around a screenshot — Instead: the real product view, or the screenshot without fake chrome.
- `should-fix` Everything centered and stacked in one column (headline, text, buttons, image below) — Instead: a layout chosen for the content: a split, or text over a large product view.
- `should-fix` Three or more buttons, or chips and avatars piled under the hero actions — Instead: one primary and at most one secondary action.
- `should-fix` Parallax, scroll-triggered floating and elements that move as you scroll — Instead: a still layout; motion only to explain a change.
- `should-fix` Full-page text that runs edge to edge on a wide screen — Instead: a capped, centered container and a readable line length.
- `should-fix` Placeholder text used as the only label — Instead: a visible label above or beside the field.
- `consider` A visual or illustration on every section — Instead: one strong visual where it helps, usually the hero or the product itself.

## Check

1. Screenshots in light and dark at about 375, 768, 1280 and 1920 px wide.
   - If you have a browser tool, open the page there, switch the color scheme (emulate `prefers-color-scheme`) and capture each width.
   - If you do not, ask the user for those screenshots, or run the project's own end-to-end screenshot tests if it has them.
2. Contrast for each text color on its background with `python scripts/contrast.py <text> <background>`, using the token values.
3. Keyboard pass: Tab through the page; every control is reachable, its focus is visible, and Enter/Space work. Esc closes dialogs and menus.
4. Reduced motion: with reduced motion on, nothing important moves or is hidden.
5. At 360 px nothing scrolls sideways; at 1920 px the content stays capped.
6. Walk the Slop signs above and in slop-signs.md against the screenshots and the code.
7. Optional automated checks: an axe-based accessibility scan or a Lighthouse accessibility audit, if the project already has them. Report which ran.
