# Terminal programs (CLI and TUI)

Read this for command-line tools and full-screen terminal interfaces, in any language (Python with Click, Typer or Textual; Rust with clap or Ratatui; Go with Cobra or Bubble Tea; Node; shell-free scripts). Use [slop-signs.md](slop-signs.md) as well; the color, copy and emoji signs there apply to terminal output too.

For a thorough guide written by others, see the Command Line Interface Guidelines at https://clig.dev (read it there; it is not copied here).

In the terminal the slop signs are decoration and chatter: banners, emoji, color everywhere, spinners in log files, and messages that talk instead of inform.

## Rules

Output
- Print what the user asked for and little else. Success can be quiet; a short confirmation is enough when something changed.
- Results go to standard output, messages and errors to standard error, so piping the result stays clean.
- Offer machine-readable output (`--json` or a plain one-item-per-line mode) when others may script the tool.
- Plain text first. Color only to point at what matters (errors, warnings, the key value), never as the only carrier of meaning.

Color, symbols and animation
- Turn color and animation off when output is not a terminal, when `NO_COLOR` is set, when `TERM=dumb`, or when the user passes `--no-color`.
- Pick colors that read on both dark and light terminal backgrounds, or stick to the terminal's own named colors so the user's theme decides.
- Symbols and emoji only where they add structure, and with a plain-text fallback.
- Spinners and progress bars only on an interactive terminal, and only for work that takes long enough to notice.

Help and errors
- `-h` and `--help` work everywhere and start with one usage line and a short description, then the most common examples.
- Errors say what went wrong, why if known, and what to do next, in plain words, with a non-zero exit code. No stack trace unless asked for (`--verbose` or a debug flag).
- Destructive actions ask for confirmation on an interactive terminal and accept a flag (`--yes`, `--force`) for scripts.

Layout (TUI and wide output)
- Work at 80 columns and wrap or truncate cleanly when narrower; use the full width only when the terminal has it.
- Keyboard first: arrow keys and the common shortcuts, a visible key hint line, `q` or Esc to leave, Ctrl+C always exits.
- Use the terminal's own background; do not paint a fixed background color over the user's theme.

## Slop signs

Accessibility and robustness
- `must-fix` Color or animation codes written into pipes, files or CI logs (no TTY check, `NO_COLOR` ignored) — Instead: detect the terminal and honor `NO_COLOR`, `TERM=dumb` and `--no-color`.
- `must-fix` Meaning carried only by color (red and green with no word or symbol) — Instead: add a word or a symbol to every colored state.
- `must-fix` Errors that print a raw stack trace or nothing at all, or exit with code 0 on failure — Instead: a plain message on standard error, a hint, and a non-zero exit code.
- `must-fix` A TUI that cannot be left with q, Esc or Ctrl+C, or that leaves the terminal broken after exit — Instead: always restore the terminal and honor Ctrl+C.

Decoration and chatter
- `should-fix` An ASCII-art banner or logo printed on every run — Instead: nothing, or one line with the version when asked (`--version`).
- `should-fix` Emoji on every line (🚀 Starting…, ✅ Done!, 🎉) — Instead: plain words; a single symbol only where it marks status.
- `should-fix` Rainbow output: every line or key in a different color — Instead: default text, color only for errors, warnings and the one value that matters.
- `should-fix` Chatty narration ("Let's get started!", "Awesome, all done!") — Instead: report what happened in a few words, or stay quiet on success.
- `should-fix` Results mixed with progress messages on standard output — Instead: results on standard output, everything else on standard error.
- `should-fix` A fixed dark background painted over the user's terminal theme — Instead: the terminal's own background and colors.
- `should-fix` Help text that is a wall of every flag with no usage line or examples — Instead: usage, a one-line description, common examples, then the full list.
- `consider` No machine-readable output for a tool that others will script — Instead: a `--json` or line-per-item mode.

## Check

1. Run the common commands in a real terminal and capture the output as text (and as screenshots for a TUI) on a dark and a light terminal theme.
   - If you cannot run the program, ask the user for the output or screenshots, and judge the rest from the code.
2. Pipe the output to a file (`> out.txt`) and with `NO_COLOR=1` set: no color codes, no spinners, the result unchanged.
3. Run with `--help`, with a wrong argument and with a missing file: the help reads well, errors are plain, exit codes are non-zero on failure.
4. For a TUI, run at 80 × 24 and in a narrower window; check key hints, quitting and that the terminal is restored after exit.
5. If you have screenshots, measure the main text and accent colors against the background with `python scripts/contrast.py <text> <background>`.
6. Walk the Slop signs above and in slop-signs.md against the output and the code.
