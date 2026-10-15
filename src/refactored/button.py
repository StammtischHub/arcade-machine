"""Taster-Auswertung: kurzer Druck vs. gedrückt halten."""
from __future__ import annotations

import select
import time
from typing import Callable

from evdev import InputDevice, KeyEvent, ecodes


class Button:
    """Wertet einen einzelnen Taster eines evdev-Geräts aus.

    - Loslassen vor `hold_threshold`  → `on_short_press`
    - Halten bis `hold_threshold`     → `on_long_press`, sofort beim Erreichen der
      Schwelle. Das anschließende Loslassen löst nichts mehr aus.

    Statt eines Timer-Threads wartet `select()` mit Timeout auf das nächste
    Ereignis: Kommt bis zur Schwelle kein Loslassen, ist es ein langer Druck.
    """

    def __init__(
            self,
            device_path: str,
            key_code: int,
            on_short_press: Callable[[], None],
            on_long_press: Callable[[], None],
            hold_threshold: float,
            debounce_time: float,
    ):
        self._device = InputDevice(device_path)
        self._key_code = key_code
        self._on_short_press = on_short_press
        self._on_long_press = on_long_press
        self._hold_threshold = hold_threshold
        self._debounce_time = debounce_time

        self._pressed_since: float | None = None
        self._long_press_fired = False
        self._last_edge = 0.0

    def listen(self) -> None:
        """Blockierende Ereignisschleife – in einem eigenen Thread starten."""
        try:
            while True:
                readable, _, _ = select.select([self._device], [], [], self._time_until_hold())
                if not readable:
                    self._long_press_fired = True
                    self._on_long_press()
                    continue

                for event in self._device.read():
                    if event.type == ecodes.EV_KEY and event.code == self._key_code:
                        self._handle_key(event.value)
        except OSError as error:
            print(f"Fehler im Input Listener: {error}")

    def _time_until_hold(self) -> float | None:
        """Wie lange select() warten darf: bis zur Halte-Schwelle oder unbegrenzt."""
        if self._pressed_since is None or self._long_press_fired:
            return None
        elapsed = time.monotonic() - self._pressed_since
        return max(0.0, self._hold_threshold - elapsed)

    def _handle_key(self, state: int) -> None:
        now = time.monotonic()

        if state == KeyEvent.key_down:
            if self._pressed_since is not None or now - self._last_edge < self._debounce_time:
                return
            self._pressed_since = now
            self._long_press_fired = False
            self._last_edge = now

        elif state == KeyEvent.key_up:
            if self._pressed_since is None:
                return
            if not self._long_press_fired:
                self._on_short_press()
            self._pressed_since = None
            self._last_edge = now
