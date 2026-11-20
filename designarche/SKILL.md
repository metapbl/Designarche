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
| Apply or update the Graphite/Paper theme in a PySide6 (Python) desktop app | [references/pyside6-theme.md](references/pyside6-theme.md) |

Pick the platform the screen runs on. If no file fits exactly, use the closest one and say so in the first line of your reply.

## Shared principles

These hold on every platform. The platform file gives the concrete values.

- **Follow the platform first.** Use the platform's own controls, spacing, type and behavior before any style of your own.
- **Colors only through role names.** Components refer to roles such as text, surface, accent and danger, never to raw color values. How the roles are stored follows the stack's own way (CSS variables, a theme object, a token file).
- **Chrome color follows the content.** If the content is colorful (photos, video, charts, user media), keep the surrounding chrome neutral. If the content is mostly text or monochrome, the brand color may tint the accent and the shell.
- **Accent color.** Use a fixed brand accent by default. Following the system accent color is an option the product may offer. Without a brand color, use the system accent.
- **Hover and cursor.** Do what the platform's standard controls do. The same hover effect on every control is a slop sign.

## Grades

Every finding gets one grade.

| Grade | Meaning |
|---|---|
| `must-fix` | Breaks accessibility or a platform rule, or shows invented facts (fake numbers, testimonials, logos, features) |
| `should-fix` | A slop sign: a generic, machine-made pattern that has a better, specific alternative |
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

1. Read [the platform file](#which-file-to-read) for the screen. Look at the code and, when you can, at screenshots of the running screen.
2. List every finding with its location (`file:line`, or the screen area), its grade and what to do instead.
3. **Stop.** Change nothing until the user answers.
4. If the screen is nearly clean (no `must-fix` and at most two `should-fix`), say that no problems were found, give two or three suggestions, and change nothing.
5. Fix only the items the user approved: `must-fix` first, then `should-fix`. Fix `consider` items only when the user picked them. Report each item as fixed or failed, with the reason for a failure.
6. Run **Check**.

## Check

Run after a build or a fix.

1. Take screenshots of every color mode the app has (dark and light, or the only one it has), as the platform file's Check section describes.
2. Measure contrast for each text color on its background with `python scripts/contrast.py <text color> <background color>` (paths are relative to this skill folder). Normal text needs 4.5:1; large text, icons and control boundaries need 3:1.
3. Go through the platform file's Check list.
4. The result passes when no `must-fix` is left. Otherwise list what remains, and ask before fixing again; do not loop on your own.
5. If a check could not run (no screenshot tool, no display, a platform you cannot run), do not report a pass. Say what was not checked.
6. Screenshots may show real user data. Keep them out of version control and tell the user so.

## Ground rules

- Run bundled scripts with Python: `python scripts/<name>.py`, paths relative to this skill folder. Do not rely on a particular shell.
- Do not call a screen finished without a check you actually ran.
