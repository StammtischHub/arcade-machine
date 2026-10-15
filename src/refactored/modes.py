"""Modusverwaltung: Hauptmodi und ihre Effekte (Subtypen)."""
import threading
from dataclasses import dataclass

from effects import Effect


@dataclass(frozen=True)
class Mode:
    """Ein Hauptmodus mit seinen Effekten. Die Anzahl der Subtypen ergibt sich daraus."""

    name: str
    effects: tuple[Effect, ...]


class ModeController:
    """Hält fest, welcher Modus und welcher Effekt gerade aktiv sind.

    Wird vom Taster-Thread verändert und von der Render-Schleife gelesen,
    deshalb ist jeder Zugriff durch einen Lock geschützt.
    """

    def __init__(self, modes: list[Mode]):
        if not modes or any(not mode.effects for mode in modes):
            raise ValueError("Es wird mindestens ein Modus mit mindestens einem Effekt benötigt.")
        self._modes = modes
        self._mode_index = 0
        self._effect_index = 0
        self._lock = threading.Lock()

    def next_effect(self) -> None:
        """Nächster Effekt innerhalb des aktuellen Modus (kurzer Druck)."""
        with self._lock:
            count = len(self._modes[self._mode_index].effects)
            self._effect_index = (self._effect_index + 1) % count

    def next_mode(self) -> None:
        """Nächster Hauptmodus, beginnend bei dessen erstem Effekt (langer Druck)."""
        with self._lock:
            self._mode_index = (self._mode_index + 1) % len(self._modes)
            self._effect_index = 0

    @property
    def current_effect(self) -> Effect:
        with self._lock:
            return self._modes[self._mode_index].effects[self._effect_index]
