"""Zentrale Konfiguration für den LED-Controller.

Alle Werte, die man typischerweise anpassen möchte, stehen hier –
der restliche Code muss dafür nicht angefasst werden.
"""
from evdev import ecodes

# Hardware
NUM_LEDS = 65
INPUT_DEVICE = "/dev/input/event0"
LED_BUTTON = ecodes.BTN_TOP2

# Taster-Timing (Sekunden)
HOLD_THRESHOLD = 2.0   # So lange halten → Hauptmodus wechseln
DEBOUNCE_TIME = 0.25   # Erneutes Drücken innerhalb dieser Zeit gilt als Prellen

# Rendering
FRAME_DELAY = 0.02     # Pause zwischen zwei Frames
