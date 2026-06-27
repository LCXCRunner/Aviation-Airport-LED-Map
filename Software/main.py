try:
    import board
except Exception:
    board = None

try:
    import neopixel
except Exception:
    neopixel = None

import time
from metarFlightCatagory import getMetarFlightCategory

numberOfPixels : int = 11
pixelBuffer : list[tuple[int, int, int]] = [(0, 0, 0)] * numberOfPixels
airports : list[str] = ["KHCR", "KPVU", "KSVR", "KSLC", "KTYV", "KENV", "KHIF", "KOGD", "KBMC", "KLGU", "KEVW"]

class _MockNeoPixel:
    def __init__(self, pin, count):
        self._pixels = [(0, 0, 0)] * count

    def __setitem__(self, index, value):
        self._pixels[index] = value

    def __getitem__(self, index):
        return self._pixels[index]

    def fill(self, color):
        self._pixels = [color] * len(self._pixels)

    def show(self):
        pass


def create_pixels():
    if neopixel is None or board is None:
        return _MockNeoPixel(None, numberOfPixels)
    return neopixel.NeoPixel(board.D18, numberOfPixels)


pixels = create_pixels()
hardware_available = neopixel is not None and board is not None

def setPixelColor(pixelNumber : int, color : tuple):
    if pixelNumber < numberOfPixels:
        pixels[pixelNumber] = color

def rainbowCycle(pause : float = 0.1):
    red : tuple = (255, 0, 0)
    orange : tuple = (255, 127, 0)
    yellow : tuple = (255, 255, 0)
    green : tuple = (0, 255, 0)
    blue : tuple = (0, 0, 255)
    cyan : tuple = (0, 255, 255)
    magenta : tuple = (255, 0, 255)

    colorOrder : list[tuple] = [red, orange, yellow, green, cyan, blue, magenta]

    cycles : int = 0
    while True:
        for i in range(numberOfPixels):
            pixelBuffer[i] = colorOrder[(i + cycles) % len(colorOrder)]
            pixels[i] = pixelBuffer[i]
            # pixels.show()
        cycles += 1
        if cycles >= 25:
            # pixels.fill((0, 0, 0)) # Turn off all pixels
            # pixels.show()
            break
        time.sleep(pause)

if __name__ == "__main__":
    if not hardware_available:
        print("Running in software fallback mode because no Raspberry Pi LED hardware was detected.")
        rainbowCycle(0.1)
    else:
        # # red
        # pixels.fill((255, 0, 0))
        # pixels.show()
        # time.sleep(0.5)
        # # green
        # pixels.fill((0, 255, 0))
        # pixels.show()
        # time.sleep(0.5)
        # # cyan
        # pixels.fill((0, 255, 255))
        # pixels.show()
        # time.sleep(0.5)
        # # magenta
        # pixels.fill((255, 0, 255))
        # pixels.show()
        # time.sleep(0.5)

        rainbowCycle(0.1)  # rainbow cycle with 100ms delay per step
