"""Farb-Datentyp und Farbumrechnungen."""
from __future__ import annotations

import colorsys
from typing import NamedTuple


class Color(NamedTuple):
    """RGB-Farbe mit Kanälen von 0 bis 255. Lässt sich wie ein Tupel entpacken."""

    r: int
    g: int
    b: int

    @classmethod
    def from_hue(cls, hue: float, saturation: float = 1.0, value: float = 1.0) -> Color:
        """Erzeugt eine Farbe aus dem HSV-Farbraum. `hue` wird auf [0, 1) normiert."""
        r, g, b = colorsys.hsv_to_rgb(hue % 1.0, saturation, value)
        return cls(int(r * 255), int(g * 255), int(b * 255))

    def scaled(self, factor: float) -> Color:
        """Gibt dieselbe Farbe mit skalierter Helligkeit zurück (factor 0.0–1.0)."""
        return Color(int(self.r * factor), int(self.g * factor), int(self.b * factor))


STATIC_COLORS: dict[str, Color] = {
    "red": Color(255, 0, 0),
    "yellow": Color(255, 255, 0),
    "green": Color(0, 255, 0),
    "cyan": Color(0, 255, 255),
    "blue": Color(0, 0, 255),
    "magenta": Color(255, 0, 255),
}

OFF = Color(0, 0, 0)
