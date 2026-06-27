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
airportDict : dict[str, str] = {}

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
            pixels.show()
        cycles += 1
        if cycles >= 25:
            pixels.fill((0, 0, 0)) # Turn off all pixels
            pixels.show()
            break
        time.sleep(pause)

if __name__ == "__main__":
    # mainly for testing purposes
    if not hardware_available:
        print("Running in software fallback mode because no Raspberry Pi LED hardware was detected.")

        # get initial flight categories for all airports
        flightCategories : list[str] = []
        for airport in airports:
            flightCategory : str = getMetarFlightCategory(airport)
            flightCategories.append(flightCategory)
            print(f"Initial flight category for {airport}: {flightCategory}")
    else:
        while True:
            try:
                # red
                pixels.fill((255, 0, 0))
                pixels.show()
                time.sleep(0.5)
                # green
                pixels.fill((0, 255, 0))
                pixels.show()
                time.sleep(0.5)
                # cyan
                pixels.fill((0, 255, 255))
                pixels.show()
                time.sleep(0.5)
                # magenta
                pixels.fill((255, 0, 255))
                pixels.show()
                time.sleep(0.5)

                rainbowCycle(0.25)  # rainbow cycle with 100ms delay per step
                print("Boot sequence complete. Starting main loop.")

                # get initial flight categories for all airports
                # possible flight categories: VFR, MVFR, IFR, LIFR, Unknown
                # VFR: Visual Flight Rules - Green
                # MVFR: Marginal VFR - Blue
                # IFR: Instrument Flight Rules - Red
                # LIFR: Low IFR - Magenta
                # Unknown: Unknown - White

                # inital setup of the board, threads should handle it from there. 
                flightCategories : list[str] = []
                for i in range(len(airports)):

                    flightCategory : str = getMetarFlightCategory(airports[i])
                    flightCategories.append(flightCategory)
                    # print(f"Initial flight category for {airport}: {flightCategory}")
                    
                print(flightCategories)

                # i want some sort of dim out between this and the next loop, but for now, just a pause.
                time.sleep(1)

                # let the loop figure out the catagories and set the colors accordingly.
                for i in range(len(airports)):
                    if flightCategory == "VFR":
                        color : tuple = (0, 255, 0)  # Green
                    elif flightCategory == "MVFR":
                        color : tuple = (0, 0, 255)  # Blue
                    elif flightCategory == "IFR":
                        color : tuple = (255, 0, 0)  # Red
                    elif flightCategory == "LIFR":
                        color : tuple = (255, 0, 255)  # Magenta
                    else:
                        color : tuple = (255, 255, 255)  # White for Unknown

                    setPixelColor(i, color)

                
            except Exception as e:
                print("Error in main loop: " + str(e))
                pixels.fill((0, 0, 0)) # Turn off all pixels
                break
            finally:
                pixels.fill((0, 0, 0)) # Turn off all pixels
                pixels.show()