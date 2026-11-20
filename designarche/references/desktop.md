# Desktop apps (Windows, macOS, Linux)

Read this for any desktop GUI, whatever the toolkit (Qt/PySide6, WinUI, WPF, AppKit/SwiftUI, GTK, Tauri, Electron). Use [slop-signs.md](slop-signs.md) as well. For the Graphite/Paper theme in PySide6, see [pyside6-theme.md](pyside6-theme.md).

On the desktop the strongest slop sign is a web page pretending to be an app: web habits in a window. The test for every choice is "what does the platform's own standard control do here?"

## Rules

Platform first
- Use the toolkit's standard controls and the operating system's dialogs (open, save, color, print, confirm). Build a custom control only when no standard one does the job.
- Follow the OS you run on. On Windows, Windows conventions; on macOS, Mac conventions; on Linux, the desktop's (GNOME or KDE). A cross-platform toolkit does not excuse one OS's habits on another.
- Respect system settings: light/dark mode, high contrast, accent color (as an option, see SKILL.md), text size, reduced motion.

Spacing (use named steps, never one-off values)
- Windows 11: 8 between buttons and between a control and its header, 12 between a control and its label and between content areas, 16 from a surface edge to its text (effective pixels).
- macOS: about 20 pt window margins and between groups, 8 pt between related controls.
- KDE: Kirigami spacing units (small inside a group, large between groups and at window edges).
- GNOME: libadwaita's widgets and spacing; do not invent your own.
- Everywhere: related items close together, groups further apart.

Type
- Use the system font and the platform's type ramp: Segoe UI Variable on Windows (body 14 / 20 line), the system font on macOS (body 13 pt, nothing under 10 pt), the desktop font on Linux.
- Follow the user's text-size setting; do not hard-code sizes that ignore it.
- GNOME: no italics and no all-caps for UI text.

Shape and color
- Corner radius: on Windows 8 for windows, flyouts and dialogs, 4 for buttons and list highlights. On macOS the OS draws windows; follow the control style. Do not round everything to a pill.
- A gray fill on a button reads as "disabled" on Windows; an enabled default button is outlined or lightly filled, never solid gray.
- Keep color for the accent, selection, state and data. The window itself stays in the system's neutral materials or the theme's surfaces.

Windows, dialogs and feedback
- Use the OS title bar and window frame. Remember window size and position between runs.
- Settings open in their own window or the platform's settings pattern, not as a modal panel inside the main window.
- Confirm only irreversible actions; prefer undo, or the trash, for deletions.
- Progress: nothing for work under about 0.2 s, a spinner up to about 2 s, a progress bar beyond that. Simple apps need no first-run wizard or tour; an empty view shows an icon, one line and the action that fills it.
- Notifications use the system's notification mechanism, not web-style toasts in the corner of the window.

Pointer and keyboard
- Pointer: an arrow over buttons and list rows; a hand only over real links. An I-beam only where text can be edited or selected.
- Hover: plain push buttons in most desktop styles change little or nothing on hover; list rows and toolbar icon buttons show a light highlight. Match the platform's standard control.
- Everything works from the keyboard: Tab order follows reading order, Enter and Esc do what the platform expects in dialogs, menus and common actions have the platform's shortcuts (Ctrl on Windows and Linux, Cmd on macOS).
- Text input works with input method editors (for example Korean, Japanese, Chinese composition).

## Slop signs

Platform and accessibility
- `must-fix` A control or action that cannot be reached or used from the keyboard — Instead: standard controls with a working Tab order and the platform's shortcuts.
- `must-fix` Text sizes fixed in pixels so the system text-size setting has no effect — Instead: sizes from the platform's type ramp that scale with the setting.
- `must-fix` The app ignores high-contrast mode, leaving text or controls invisible — Instead: system colors or theme roles that switch with high contrast.
- `must-fix` Text input that breaks input-method composition (Korean, Japanese, Chinese) — Instead: the toolkit's standard text fields, tested with an IME.

Web habits in a window
- `should-fix` A hand-drawn title bar or window frame, or CSS-style fake window shadows and rounded corners — Instead: the OS title bar and frame (or the toolkit's supported custom title bar API, kept native in behavior).
- `should-fix` A pointing-hand cursor over buttons or list rows — Instead: the arrow cursor; the hand only for links.
- `should-fix` Settings shown as a dimmed modal panel inside the main window, or modals over a blurred backdrop — Instead: a separate settings window or the platform's settings pattern, and plain system dialogs.
- `should-fix` Toast pop-ups in the window corner for routine feedback — Instead: inline status, a status bar, or system notifications for background events.
- `should-fix` Page-style fade or slide transitions between views, skeleton screens for work that finishes in a blink — Instead: switch views directly; show progress only when work takes long enough to notice.
- `should-fix` A web font or a single fixed font on every OS — Instead: the system font of each platform.
- `should-fix` Window size and position forgotten on every launch — Instead: save and restore them.

Mobile habits on the desktop
- `should-fix` A hamburger menu hiding the main commands, a bottom tab bar or a floating action button — Instead: a menu bar or toolbar, a sidebar for navigation, commands where the platform puts them.
- `should-fix` Oversized touch-style controls and spacing in a mouse-first app — Instead: the platform's standard control sizes and density.

Generic look
- `should-fix` A solid gray-filled enabled button on Windows (it reads as disabled) — Instead: outlined or lightly filled enabled buttons; gray fill only for disabled.
- `should-fix` Custom-styled versions of standard controls that look like none of the platforms — Instead: the toolkit's native style or one consistent theme built on it.
- `should-fix` A first-run wizard or a guided tour in a simple utility — Instead: a useful empty state with one clear action.
- `consider` A brand color painted over standard controls everywhere — Instead: brand accent on selection and primary actions only; let standard controls keep their platform look.

## Check

1. Screenshots of the main window and the key dialogs in every color mode the app supports.
   - PySide6 with Graphite/Paper: the screenshot step in [pyside6-theme.md](pyside6-theme.md) (step 5).
   - Other toolkits: the toolkit's own widget-grab or test screenshot feature, or the OS screenshot tool. If you cannot run the app, ask the user for screenshots of each mode.
2. Contrast for each text role on each surface with `python scripts/contrast.py <text> <background>`.
3. Keyboard pass: reach and use every control with Tab, Shift+Tab, Enter, Space and Esc; check menus and shortcuts.
4. Open the app at a larger system text size and in high-contrast mode (Windows) if the platform has it; nothing may be cut off or invisible.
5. Walk the Slop signs above and in slop-signs.md against the screenshots and the code.
6. Optional automated accessibility checkers: Accessibility Insights / Axe.Windows (Windows), the Xcode accessibility audit (macOS), Accerciser (Linux). Report which ones ran.
7. Say which OS you actually ran. Do not claim a pass for an OS you did not run.
