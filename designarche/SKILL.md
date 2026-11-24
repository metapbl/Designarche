---
name: designarche
description: Keeps interfaces built by AI agents from looking machine-made ("AI slop") on any platform (web, desktop, mobile, terminal) and in any language or framework. Use when designing or building a new screen, reviewing or fixing an existing UI for generic AI-looking patterns, checking contrast and platform conventions, or applying the Graphite (dark) / Paper (light) theme to a PySide6 desktop app.
license: MIT
---

# designarche

Make each screen look like it was designed for its platform and its product, not generated.

Speak to the user in their language. Read only the reference files the task needs.

## Which file to read

| Task | Read |
|---|---|
| Any audit, and a last look after any build | [references/slop-signs.md](references/slop-signs.md) and the platform file |
| A website or web app (anything in a browser) | [references/web.md](references/web.md) |
| A phone or tablet app (iOS, Android, Flutter, React Native) | [references/mobile.md](references/mobile.md) |
| A desktop app (Windows, macOS, Linux; any toolkit) | [references/desktop.md](references/desktop.md) |
| A command-line tool or terminal UI (CLI, TUI) | [references/terminal.md](references/terminal.md) |
| Apply or update the Graphite/Paper theme in a PySide6 (Python) desktop app | [references/pyside6-theme.md](references/pyside6-theme.md) |

Pick the platform the screen runs on. If no file fits exactly, use the closest one and say so in the first line of your reply.

## Shared principles

These hold on every platform. The platform file gives the concrete values.

- **Follow the platform first.** Use the platform's own controls, spacing, type and behavior before any style of your own.
- **Colors only through role names.** Components refer to roles such as text, surface, accent and danger, never to raw color values. How the roles are stored follows the stack's own way (CSS variables, a theme object, a token file).
- **Chrome color follows the content.** If the content is colorful (photos, video, charts, user media), keep the surrounding chrome neutral. If the content is mostly text or monochrome, the brand color may tint the accent and the shell.
- **Content keeps its own colors.** Maps, photos, video and charts are judged as content, not as UI. Only the UI drawn on top of them (labels, buttons, pins, overlays) must use role colors and meet the contrast rules against what lies beneath.
- **Accent color.** Use a fixed brand accent by default. Following the system accent color is an option the product may offer. Without a brand color, use the system accent. The Graphite/Paper theme keeps its own fixed accent.
- **Hover and cursor.** Do what the platform's standard controls do. The same hover effect on every control is a slop sign.

## Grades

Every finding gets one grade.

| Grade | Meaning |
|---|---|
| `must-fix` | Fails accessibility, breaks platform behavior people rely on (keyboard use, the back gesture, system settings such as text size or high contrast, safe areas), or shows invented facts (fake numbers, testimonials, logos, features) |
| `should-fix` | A slop sign: a generic, machine-made pattern, or a look that departs from the platform's conventions, that has a better, specific alternative |
| `consider` | An improvement suggestion |

A screen passes when it has no `must-fix` left.

## Build a new screen

1. **Ask once.** Before building, ask in a single message what you need and cannot read from the project: what the product is and who uses it, the platform and stack, and any brand color or existing design. Do not ask again later, and never pick a random theme.
   - If the user said up front to just go ahead ("just do it", "그냥 해"), ask nothing. State what you inferred in the first line of your reply.
2. **Write a direction line** before deciding anything else: product · personality · world · signature, a few words each. Generic adjectives (clean, modern, sleek, minimal, intuitive, beautiful, elegant) are not allowed; replace each with a concrete word before settling the line. Every later decision follows this line.
3. **Read the platform file** for the platform (and the stack file, if there is one) and build to it.
4. In your first reply after building, show the direction line and name the platform file you read.
5. Run **Check**.

## Audit an existing screen

1. Read [the platform file](#which-file-to-read) for the screen. Look at the code and, when you can, at screenshots of the running screen. If something cannot be judged from what you have (for example whether the product has a brand color), ask instead of guessing.
2. If the screen is nearly clean (no `must-fix` and at most two `should-fix`), say that no problems were found, give two or three suggestions (including those `should-fix` items), change nothing and stop here.
3. Otherwise list every finding with its location (`file:line`, or the screen area), its grade and what to do instead.
4. **Stop.** Change nothing until the user answers. The question goes to the person using this session, even when another session or tool asked for the audit; send the requester only the results.
   - If the user wants to see a change before choosing, show a before/after preview (screenshots, or a temporary toggle that is removed afterwards) and still change nothing until they choose.
5. Fix only the items the user approved: `must-fix` first, then `should-fix`. Fix `consider` items only when the user picked them. Report each item as fixed or failed, with the reason for a failure.
6. Run **Check**.

## Check

Run after a build or a fix.

1. Take screenshots of every color mode the app has (dark and light, or the only one it has), as the platform file's Check section describes.
2. Measure contrast for each text color on its background with `python scripts/contrast.py <text color> <background color>` (paths are relative to this skill folder). Normal text needs 4.5:1; large text and meaningful icons need 3:1, and so does a control's boundary when that boundary is what makes the control recognizable.
3. Go through the platform file's Check list.
4. The result passes when no `must-fix` is left. Otherwise list what remains, including new `must-fix` findings the check uncovered, and ask before fixing again; fix only what the user approves and run Check once more. Do not loop on your own.
5. If a check could not run (no screenshot tool, no display, a platform you cannot run), do not report a pass for it. You may review the code instead (for example the reduced-motion rules or the tab order), but say that it was reviewed, not run, and list everything that was not checked.
6. Screenshots may show real user data. Save them outside version control, and tell the user where you saved them and that they should not be committed.

## Ground rules

- Run bundled scripts with Python: `python scripts/<name>.py`, paths relative to this skill folder. Do not rely on a particular shell.
- Do not call a screen finished without a check you actually ran.
