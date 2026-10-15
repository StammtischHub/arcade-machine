"""Zentrale Konfiguration für den LED-Controller.

Alle Werte, die man typischerweise anpassen möchte, stehen hier –
der restliche Code muss dafür nicht angefasst werden.
"""
from evdev import ecodes

from colors import Color

# ----------------------------
# Hardware
# ----------------------------
NUM_LEDS = 65
INPUT_DEVICE = "/dev/input/event0"
LED_BUTTON = ecodes.BTN_TOP2

# ----------------------------
# Taster-Timing (Sekunden)
# ----------------------------
HOLD_THRESHOLD = 2.0   # So lange halten → Hauptmodus wechseln
DEBOUNCE_TIME = 0.25   # Erneutes Drücken innerhalb dieser Zeit gilt als Prellen

# ----------------------------
# Rendering
# ----------------------------
FRAME_DELAY = 0.02     # Pause zwischen zwei Frames (≈ 50 FPS)

# ----------------------------
# Statische Farben
# Reihenfolge = Reihenfolge beim Durchschalten per kurzem Druck
# ----------------------------
STATIC_COLORS: dict[str, Color] = {
    "red": Color(255, 0, 0),
    "yellow": Color(255, 255, 0),
    "green": Color(0, 255, 0),
    "cyan": Color(0, 255, 255),
    "blue": Color(0, 0, 255),
    "magenta": Color(255, 0, 255),
}
