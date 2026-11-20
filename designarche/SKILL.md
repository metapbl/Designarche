---
name: designarche
description: Keeps interfaces built by AI agents from looking machine-made ("AI slop") on any platform (web, desktop, mobile, terminal) and in any language or framework. Use when designing or building a new screen, reviewing or fixing an existing UI for generic AI-looking patterns, checking contrast and platform conventions, or applying the Graphite (dark) / Paper (light) theme to a PySide6 desktop app.
license: MIT
---

# designarche

Make each screen look like it was designed for its platform and its product, not generated.

Speak to the user in their language. Read only the reference file the task needs.

## Which part to use

| Task | Read |
|---|---|
| Apply or update the Graphite/Paper theme in a PySide6 (Python) desktop app | [references/pyside6-theme.md](references/pyside6-theme.md) |

This version ships the PySide6 theme. The shared principles, the per-platform rules and the slop audit are being added; until then, say so when asked for them instead of improvising rules.

## Ground rules

- Run bundled scripts with Python: `python scripts/<name>.py`, paths relative to this skill folder. Do not rely on a particular shell.
- Before changing an existing screen, show what you would change and wait for the user's answer.
- Do not call a screen finished without a check you actually ran (tests, screenshots, contrast numbers). If a check could not run, say what was not checked.
