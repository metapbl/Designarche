# Slop signs on every platform

Read this for every audit, together with the platform file. Each sign carries its grade (see Grades in SKILL.md) and what to do instead. The platform file adds the signs that only exist there.

## Slop signs

Facts and content
- `must-fix` Invented facts: metrics, testimonials, customer logos, star ratings, user counts or case studies nobody supplied — Instead: ask whether it is real; if not, remove it or leave a clearly marked slot.
- `must-fix` Placeholder data that looks real (`$123,456`, `John Doe`, lorem ipsum in a shipped screen) — Instead: real sample data from the product, or an honest empty state.

Accessibility
- `must-fix` Normal text under 4.5:1 against its background, or large text, icons and control edges under 3:1 — Instead: pick role colors that pass; measure with `scripts/contrast.py`.
- `must-fix` Keyboard focus that is invisible or missing on something you can operate — Instead: a visible focus indicator on every interactive element, as the platform draws it.
- `must-fix` Color as the only signal (red/green status with no text, icon or shape) — Instead: add a label, icon or pattern.
- `must-fix` Motion that cannot be reduced, or content that only appears through animation — Instead: honor the system's reduce-motion setting and keep content visible without it.

Color and surfaces
- `should-fix` Purple-to-blue or violet-to-pink gradients on backgrounds, cards or buttons — Instead: a single neutral surface; save the accent for elements that carry meaning.
- `should-fix` Gradient or shimmering text in headings, numbers or the logo — Instead: solid text in the primary text role.
- `should-fix` Colored glows, neon outlines or blurred color clouds behind content — Instead: show depth with surface steps and thin, low-contrast borders.
- `should-fix` Highlights on so many elements that none of them leads — Instead: spend the accent on one or two things per screen.
- `should-fix` Text set in several almost-identical shades of one color — Instead: two or three text roles taken from one neutral scale.
- `should-fix` Raw color values inside components instead of role names — Instead: role tokens (text, surface, accent, danger) defined in one place.

Type
- `should-fix` Very heavy headings (800–900) used for hierarchy — Instead: size and spacing for hierarchy, regular or medium weight.
- `should-fix` Small labels in tracked uppercase (`DASHBOARD`, `PAID THIS MONTH`) — Instead: sentence case at normal tracking.
- `should-fix` Many sizes and weights on one screen — Instead: a few steps from one scale.
- `should-fix` Numbers in mixed formats side by side (`$48,210` next to `$124,860.40`) — Instead: one format; tabular figures where numbers line up.
- `should-fix` One italic word for emphasis inside a heading — Instead: plain text; emphasis through placement or weight.

Icons
- `should-fix` Emoji used as icons, status or decoration (🚀 🔥 📈 ✅) — Instead: one icon set from the platform, or no icon.
- `should-fix` A sparkle ✨ on anything to do with AI — Instead: a plain icon only where it explains something, or none.
- `should-fix` Icons in mixed sizes, strokes and colors — Instead: one size, one stroke, the text role color.

Spacing and layout
- `should-fix` Spacing values off any scale (13 px here, 7 px there) — Instead: steps from one spacing scale.
- `should-fix` Sibling rows or cards with different heights, gaps or padding — Instead: one height, one gap, one padding.
- `should-fix` A card inside a card inside a card — Instead: one level of grouping; separate with space or a divider.
- `should-fix` A row of equal cards that all show the same kind of chart — Instead: one main view and compact supporting numbers.

Copy
- `should-fix` A personal greeting as the page title (`Hi Alex, great to see you! 👋`) — Instead: title the page by what it shows.
- `should-fix` Hype words (supercharge, seamless, unlock, magic, revolutionize) and exclamation marks — Instead: say plainly what the thing does.
- `should-fix` A headline you could paste onto a competitor's page unchanged — Instead: name what this product does and for whom, in its own vocabulary.
- `should-fix` A change with nothing to compare against (`Up 12%!`) — Instead: state the baseline (`+12% compared with last month`).
- `should-fix` Long, chatty placeholder text (`Type here to find anything you want...`) — Instead: one word that names the field.

Components
- `should-fix` Everything shaped as a full pill: search, buttons, cards — Instead: corner radius by size, as the platform does.
- `should-fix` `NEW`, `PRO`, `Beta 🚀` badges scattered everywhere — Instead: none, or one quiet text badge where it is true.
- `should-fix` A sparkline or mini chart added to every number — Instead: the number, its label and its change.
- `should-fix` Decorative status dots or glowing pills that carry no state — Instead: plain text; a dot only when it shows a real state.

Motion
- `should-fix` Pulsing, breathing or glowing animation on elements that are not live data — Instead: keep them still.
- `should-fix` The same hover effect (lift, scale, glow) on every control — Instead: what the platform's standard control does on hover.
- `should-fix` Bouncy springs and overshoot on ordinary UI, or everything flying in on load — Instead: one short ease-out, and only where motion explains a change.

Template look
- `consider` A neutral gray screen, the default font and one stock blue button, on a product whose world is warm, bright or particular — Instead: let the direction line choose a tint and an accent from the product's world.
- `consider` Every screen in the product built from the same layout, palette and type regardless of what it does — Instead: let each screen's job shape its layout.

---

Several signs above draw on ideas from unslop by Damir Sokolovsky (CC BY 4.0) and Hallmark (MIT), rewritten in our own words. Full credits are in the repository's NOTICE file.
