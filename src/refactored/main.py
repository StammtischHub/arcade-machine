"""Einstiegspunkt: baut alle Komponenten zusammen und startet den Controller."""
import signal

import config
from app import LedApp
from button import Button
from colors import OFF, STATIC_COLORS
from effects import Breathe, RainbowStrobe, Scanner, SolidColor
from led_strip import LedStrip
from modes import Mode, ModeController


def build_modes() -> ModeController:
    """Definiert die Hauptmodi. Neue Effekte/Modi werden nur hier eingetragen."""
    return ModeController([
        Mode("Colorful", (Breathe(), Scanner(), RainbowStrobe())),
        Mode("Static", tuple(SolidColor(color) for color in STATIC_COLORS.values())),
        Mode("Off", (SolidColor(OFF),)),
    ])


def main() -> None:
    strip = LedStrip(config.NUM_LEDS)
    modes = build_modes()
    button = Button(
        device_path=config.INPUT_DEVICE,
        key_code=config.LED_BUTTON,
        on_short_press=modes.next_effect,
        on_long_press=modes.next_mode,
        hold_threshold=config.HOLD_THRESHOLD,
        debounce_time=config.DEBOUNCE_TIME,
    )
    app = LedApp(strip, modes, button, config.FRAME_DELAY)

    def handle_signal(signum, frame):
        app.stop()

    signal.signal(signal.SIGTERM, handle_signal)
    signal.signal(signal.SIGINT, handle_signal)

    app.run()


if __name__ == "__main__":
    main()
