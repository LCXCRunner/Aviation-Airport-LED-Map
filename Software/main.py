import board
import neopixel
import time
from metarFlightCatagory import getMetarFlightCategory

numberOfPixels : int = 11
airports : list[str] = ["KHCR", "KPVU", "KSVR", "KSLC", "KTYV", "KENV", "KHIF", "KOGD", "KBMC", "KLGU", "KEVW"]

# does not work very well when not run on the pi
pixels : neopixel.NeoPixel = neopixel.NeoPixel(board.D18, numberOfPixels)

def setPixelColorAll(pixelNumber : int, color : tuple):
    if pixelNumber < numberOfPixels:
        pixels[pixelNumber] = color

if __name__ == "__main__":
    setPixelColorAll(0, (255, 0, 0)) # Red
    pixels.show()
    time.sleep(1)
    print("Pixels set to red.")
    # setPixelColorAll(0, (0, 255, 0)) # Green
    # time.sleep(1)
    # setPixelColorAll(0, (0, 0, 255)) # Blue
    # time.sleep(1)
    # setPixelColorAll(0, (255, 255, 0)) # Yellow
    # time.sleep(1)
    # setPixelColorAll(0, (255, 0, 255)) # Magenta
    # time.sleep(1)
    # setPixelColorAll(0, (0, 255, 255)) # Cyan
    # time.sleep(1)
    # setPixelColorAll(0, (255, 255, 255)) # White

    # for airport in airports:
    #     flightCategory : str = getMetarFlightCategory(airport)
    #     print()
    #     print(f"{airport}: {flightCategory}")