"""Lichteffekte.

Jeder Effekt kapselt seinen eigenen Animationszustand (Phase, Position, Farbton …).
Dadurch muss die Hauptschleife nichts über die Interna der Effekte wissen.
"""
import math
from abc import ABC, abstractmethod

from colors import Color
from led_strip import LedStrip


class Effect(ABC):
    """Basisklasse für alle Effekte.

    - `start()` wird einmal aufgerufen, wenn der Effekt aktiv wird.
    - `render()` wird in jedem Frame aufgerufen und zeichnet den nächsten Schritt.
    """

    def start(self, strip: LedStrip) -> None:
        """Optionaler Hook beim Aktivieren. Standard: nichts tun."""

    @abstractmethod
    def render(self, strip: LedStrip) -> None:
        ...


class SolidColor(Effect):
    """Ganzer Strip in einer festen Farbe. Wird nur beim Aktivieren gezeichnet."""

    def __init__(self, color: Color):
        self.color = color

    def start(self, strip: LedStrip) -> None:
        strip.fill(self.color)
        strip.show()

    def render(self, strip: LedStrip) -> None:
        pass  # Bild ändert sich nicht – nichts neu zu zeichnen


class Breathe(Effect):
    """Pulsiert von der Mitte nach außen.

    Am dunkelsten Punkt jedes Atemzugs springt der Farbton weiter.
    """

    MIN_LEVEL = 0.05

    def __init__(self, speed: float = 0.04, hue_step: float = 0.12):
        self.speed = speed
        self.hue_step = hue_step
        self._phase = 0.0
        self._hue = 0.0
        self._last_level = 0.0

    def render(self, strip: LedStrip) -> None:
        level = (math.sin(self._phase) + 1) / 2
        base = Color.from_hue(self._hue)
        center = (strip.num_leds - 1) / 2

        for index in range(strip.num_leds):
            falloff = max(0.0, 1.0 - abs(index - center) / center)
            strip.set_pixel(index, base.scaled(level * falloff))
        strip.show()

        if level < self.MIN_LEVEL <= self._last_level:
            self._hue += self.hue_step
        self._last_level = level
        self._phase += self.speed


class Scanner(Effect):
    """Ein Lichtpunkt mit Schweif, der zwischen den Enden hin- und herläuft."""

    TAIL_LENGTH = 5
    HEAD_OFFSET = 3

    def __init__(self, speed: float = 0.35, hue_step: float = 0.002):
        self.speed = speed
        self.hue_step = hue_step
        self._position = 0.0
        self._direction = 1
        self._hue = 0.0

    def render(self, strip: LedStrip) -> None:
        color = Color.from_hue(self._hue)
        head = int(self._position) - self.HEAD_OFFSET

        strip.clear()
        strip.set_pixel(head, color)
        for distance in range(1, self.TAIL_LENGTH + 1):
            faded = color.scaled(1.0 - distance / (self.TAIL_LENGTH + 1))
            strip.set_pixel(head - distance, faded)
            strip.set_pixel(head + distance, faded)
        strip.show()

        self._advance(strip.num_leds)

    def _advance(self, num_leds: int) -> None:
        """Bewegt den Punkt weiter und kehrt an den Enden um."""
        if self._position >= num_leds - 1:
            self._direction = -1
        elif self._position <= 0:
            self._direction = 1
        self._position += self.speed * self._direction
        self._hue += self.hue_step


class RainbowStrobe(Effect):
    """Ganzer Strip springt jeden Frame ein Stück im Farbkreis weiter (sehr schnell!)."""

    def __init__(self, hue_step: float = 0.12):
        self.hue_step = hue_step
        self._hue = 0.0

    def render(self, strip: LedStrip) -> None:
        strip.fill(Color.from_hue(self._hue))
        strip.show()
        self._hue += self.hue_step
