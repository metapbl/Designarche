# Mobile apps (iOS, iPadOS, Android)

Read this for phone and tablet apps, native (SwiftUI, UIKit, Jetpack Compose, Views) or cross-platform (Flutter, React Native). Use [slop-signs.md](slop-signs.md) as well. A mobile website is a web page: use [web.md](web.md), and this file for touch and screen-size rules.

On mobile the slop signs are a web page squeezed into an app, and one platform's habits shipped to the other. A cross-platform framework still runs on a specific phone: follow that phone's platform.

## Rules

Platform first
- Use the platform's navigation and controls: on iOS a tab bar, navigation stack and the system's sheets and alerts; on Android Material components, the top app bar or navigation bar, and the system Back behavior. Flutter and React Native apps adopt the platform's look on each OS (Cupertino or Material widgets, or adaptive components) rather than one design for both.
- Keep system gestures working: edge-swipe back on iOS, predictive Back on Android. Do not hijack them.
- Respect the safe areas and insets: notch, Dynamic Island, status bar, home indicator, navigation bar and the on-screen keyboard. Inputs stay visible above the keyboard.
- Use the platform's icon set (SF Symbols on iOS, Material Symbols on Android), one style throughout.

Touch and type
- Touch targets at least 44 × 44 pt on iOS and 48 × 48 dp on Android, with space between neighbors.
- Text follows the system text size: Dynamic Type on iOS, `sp` units on Android. Layouts must not clip or overlap at large sizes; aim to stay usable at 200%.
- iOS body text is 17 pt by default, nothing under 11 pt. Android uses the Material type scale.

Color and appearance
- Colors through roles: semantic system colors on iOS, Material color roles on Android, or the app's tokens. Light and dark are both first-class, and contrast holds in both.
- Android 12+ may use dynamic color from the wallpaper; keep a static scheme as fallback.
- Offer higher contrast when the system's Increase Contrast setting is on, if the default colors do not meet it.

Motion and adaptivity
- When Reduce Motion is on, replace slides, zooms and parallax with fades or no animation.
- Tablets get a layout built for their width (size classes, window size classes), not a stretched phone screen. Rotation and split-screen or multi-window must not break the layout.

## Slop signs

Accessibility
- `must-fix` Touch targets under 44 pt (iOS) or 48 dp (Android) — Instead: grow the tappable area to the minimum, even if the icon stays small.
- `must-fix` Text in fixed sizes that ignore Dynamic Type or `sp` scaling, or layouts that clip at large text — Instead: system text styles that scale, and layouts that wrap.
- `must-fix` Icon buttons and images with no accessibility label, so VoiceOver or TalkBack read nothing useful — Instead: a label that says what the control does.
- `must-fix` Content under the notch, status bar, home indicator or keyboard — Instead: honor the safe areas and keyboard insets.
- `must-fix` System back gesture disabled or overridden — Instead: let the platform's back behavior work.

Web or wrong-platform habits
- `should-fix` Web-shaped controls (HTML-style buttons, custom toggles, hover-only hints) — Instead: the platform's native controls.
- `should-fix` iOS patterns on Android or Android patterns on iOS (a floating action button on iOS, an iOS-style back chevron and tab bar on Android) — Instead: each OS's own navigation and controls.
- `should-fix` A hamburger drawer hiding the main destinations of a small app — Instead: a tab bar (iOS) or navigation bar (Android) with the main destinations.
- `should-fix` Mixed icon sets, or emoji standing in for icons — Instead: SF Symbols or Material Symbols, one style.
- `should-fix` Hard-coded hex colors and a dark mode made by inverting colors — Instead: semantic colors or color roles with real dark variants.
- `should-fix` A stretched phone layout on a tablet — Instead: a two-pane or wider layout from the platform's size classes.
- `should-fix` A splash screen with a long animation, or an onboarding carousel before the app does anything — Instead: the system launch screen and the app's real first screen.
- `consider` A custom design that looks the same on both platforms — Instead: shared brand and content, platform-native controls and navigation.

## Check

1. Screenshots of the key screens in every appearance the app supports (light and dark, or the only one), on a phone size and, if the app supports it, a tablet size.
   - If you can run a simulator or emulator, capture from it (Xcode's simulator, the Android emulator, or the framework's test screenshot tooling).
   - If you cannot, ask the user for those screenshots, and judge the rest from the code.
2. Contrast for each text color on its background with `python scripts/contrast.py <text> <background>`, in both appearances.
3. Large text: the largest accessibility text size (iOS) or font scale 200% (Android); nothing clips or overlaps.
4. Screen reader: every control has a label and the reading order makes sense (VoiceOver, TalkBack), as far as you can check from the code or the user's run.
5. Walk the Slop signs above and in slop-signs.md against the screenshots and the code.
6. Optional tools: Xcode Accessibility Inspector and the accessibility audit in UI tests (iOS), Accessibility Scanner and Compose UI tests (Android). Report which ran.
7. Say which device or simulator you ran. Do not claim a pass for a platform you did not run.
