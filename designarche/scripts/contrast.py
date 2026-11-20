"""WCAG 2.2 contrast ratio of two colors.

Usage: python contrast.py <text color> <background color>
Colors are #rgb or #rrggbb. Prints the ratio and whether it meets
4.5:1 (normal text) and 3:1 (large text, icons, control boundaries).
"""

import re
import sys


def luminance(color: str) -> float:
    if not re.fullmatch(r"#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})", color):
        raise ValueError(f"not a #rgb or #rrggbb color: {color}")
    digits = color[1:]
    if len(digits) == 3:
        digits = "".join(c * 2 for c in digits)
    channels = [int(digits[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    r, g, b = (c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in channels)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def ratio(fg: str, bg: str) -> float:
    dark, light = sorted((luminance(fg), luminance(bg)))
    return (light + 0.05) / (dark + 0.05)


def main() -> None:
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    try:
        value = ratio(sys.argv[1], sys.argv[2])
    except ValueError as error:
        sys.exit(str(error))
    # Compare the unrounded ratio: 4.497 must not pass as 4.50.
    verdict = lambda need: "pass" if value >= need else "fail"
    print(f"{value:.2f}:1 text={verdict(4.5)} large={verdict(3)}")


if __name__ == "__main__":
    main()
