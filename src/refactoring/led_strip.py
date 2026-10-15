"""Dünne Hülle um den APA102-Treiber.

Die Effekte sprechen nur mit dieser Klasse, nicht direkt mit dem Treiber.
So bleibt die Hardware an einer einzigen Stelle gekapselt.
"""
from apa102_pi.driver import apa102

from colors import BLACK, Color


class LedStrip:
    def __init__(self, num_leds: int):
        self.num_leds = num_leds
        self._driver = apa102.APA102(num_led=num_leds)

    def set_pixel(self, index: int, color: Color) -> None:
        """Setzt ein einzelnes Pixel. Indizes außerhalb des Strips werden ignoriert."""
        if 0 <= index < self.num_leds:
            self._driver.set_pixel(index, *color)

    def fill(self, color: Color) -> None:
        """Setzt alle Pixel auf dieselbe Farbe (ohne anzuzeigen)."""
        for index in range(self.num_leds):
            self._driver.set_pixel(index, *color)

    def clear(self) -> None:
        """Setzt alle Pixel auf Schwarz (ohne anzuzeigen)."""
        self.fill(BLACK)

    def show(self) -> None:
        """Überträgt den aktuellen Puffer auf die LEDs."""
        self._driver.show()

    def shutdown(self) -> None:
        """Schaltet alle LEDs aus und gibt die SPI-Schnittstelle frei."""
        self.clear()
        self.show()
        self._driver.cleanup()
