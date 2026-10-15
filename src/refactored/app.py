"""Hauptklasse: verbindet Taster, Modusverwaltung und LED-Strip."""
from __future__ import annotations

import threading

from button import Button
from effects import Effect
from led_strip import LedStrip
from modes import ModeController


class LedApp:
    def __init__(self, strip: LedStrip, modes: ModeController, button: Button, frame_delay: float):
        self._strip = strip
        self._modes = modes
        self._button = button
        self._frame_delay = frame_delay
        self._stop_event = threading.Event()

    def run(self) -> None:
        """Startet den Taster-Thread und die Render-Schleife. Blockiert bis stop()."""
        threading.Thread(target=self._button.listen, daemon=True).start()
        active_effect: Effect | None = None

        try:
            while not self._stop_event.is_set():
                effect = self._modes.current_effect
                if effect is not active_effect:
                    effect.start(self._strip)
                    active_effect = effect

                effect.render(self._strip)
                self._stop_event.wait(self._frame_delay)
        finally:
            print("Service stopping, turning off LEDs...")
            self._strip.shutdown()

    def stop(self) -> None:
        """Beendet die Render-Schleife nach dem aktuellen Frame (thread- und signal-sicher)."""
        self._stop_event.set()
