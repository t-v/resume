#!/usr/bin/env python3
"""Generate the static Quicksand fonts used by the PDF build.

Google only ships Quicksand as a variable font, and XeTeX cannot address the
named instances inside one: fontconfig resolves a bare "Quicksand" to the
variable font's default instance, which is Light, and an explicit
`BoldFont={Quicksand Bold}` fails to resolve. The PDF would end up entirely in
Light with no real bold.

So the two weights the PDF actually needs are instanced out into standalone
static fonts, with their name tables and OS/2 bits rewritten so that fontconfig
reports a plain "Quicksand" family with Regular and Bold styles.

The resulting .ttf files are committed to fonts/ so builds stay offline and
reproducible. Re-run this only to change the weights:

    python3 scripts/make-fonts.py

Requires fonttools:  pip install fonttools
"""

from __future__ import annotations

import sys
import urllib.request
from pathlib import Path

try:
    from fontTools.ttLib import TTFont
    from fontTools.varLib import instancer
except ImportError:
    sys.exit("fonttools is required: pip install fonttools")

SOURCE_URL = (
    "https://raw.githubusercontent.com/google/fonts/main/ofl/quicksand/"
    "Quicksand%5Bwght%5D.ttf"
)
LICENSE_URL = "https://raw.githubusercontent.com/google/fonts/main/ofl/quicksand/OFL.txt"

FAMILY = "Quicksand"
# (weight, style name, output filename)
INSTANCES = [
    (400, "Regular", "Quicksand-Regular.ttf"),
    (700, "Bold", "Quicksand-Bold.ttf"),
]

FONTS_DIR = Path(__file__).resolve().parent.parent / "fonts"

# Name table ids that have to agree for fontconfig to group the files into one
# family: 1 = family, 2 = subfamily, 3 = unique id, 4 = full name, 6 = PostScript.
# 16/17 are the typographic family/subfamily and are dropped so they cannot
# contradict 1/2.
NAME_FAMILY, NAME_SUBFAMILY, NAME_UNIQUE, NAME_FULL, NAME_PS = 1, 2, 3, 4, 6
NAME_TYPO_FAMILY, NAME_TYPO_SUBFAMILY = 16, 17

FSSELECTION_REGULAR = 1 << 6
FSSELECTION_BOLD = 1 << 5
MACSTYLE_BOLD = 1 << 0


def retitle(font: TTFont, style: str, weight: int) -> None:
    """Rewrite the name table and weight bits for a single static instance."""
    full = FAMILY if style == "Regular" else f"{FAMILY} {style}"
    values = {
        NAME_FAMILY: FAMILY,
        NAME_SUBFAMILY: style,
        NAME_UNIQUE: f"{FAMILY};{style}",
        NAME_FULL: full,
        NAME_PS: f"{FAMILY}-{style}",
    }

    name_table = font["name"]
    for name_id, value in values.items():
        name_table.setName(value, name_id, 3, 1, 0x409)  # Windows / Unicode BMP
        name_table.setName(value, name_id, 1, 0, 0)  # Macintosh / Roman

    for name_id in (NAME_TYPO_FAMILY, NAME_TYPO_SUBFAMILY):
        name_table.removeNames(nameID=name_id)

    os2 = font["OS/2"]
    os2.usWeightClass = weight
    if style == "Bold":
        os2.fsSelection = (os2.fsSelection & ~FSSELECTION_REGULAR) | FSSELECTION_BOLD
        font["head"].macStyle |= MACSTYLE_BOLD
    else:
        os2.fsSelection = (os2.fsSelection & ~FSSELECTION_BOLD) | FSSELECTION_REGULAR
        font["head"].macStyle &= ~MACSTYLE_BOLD


def main() -> None:
    FONTS_DIR.mkdir(exist_ok=True)

    print(f"Downloading {SOURCE_URL}")
    variable_font = urllib.request.urlopen(SOURCE_URL).read()
    source = FONTS_DIR / "Quicksand[wght].ttf"
    source.write_bytes(variable_font)

    for weight, style, filename in INSTANCES:
        font = instancer.instantiateVariableFont(TTFont(source), {"wght": weight})
        retitle(font, style, weight)
        target = FONTS_DIR / filename
        font.save(target)
        print(f"  + {target.name}  ({style}, wght={weight}, {target.stat().st_size:,} bytes)")

    source.unlink()

    print(f"Downloading {LICENSE_URL}")
    license_text = urllib.request.urlopen(LICENSE_URL).read()
    (FONTS_DIR / "OFL.txt").write_bytes(license_text)
    print("  + OFL.txt")


if __name__ == "__main__":
    main()
