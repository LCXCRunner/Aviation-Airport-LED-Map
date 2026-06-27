import board
import neopixel
import time
from metarFlightCatagory import getMetarFlightCategory

numberOfPixels : int = 11
airports : list[str] = ["KHCR", "KPVU", "KSVR", "KSLC", "KTYV", "KENV", "KHIF", "KOGD", "KBMC", "KLGU", "KEVW"]

# does not work very well when not run on the pi
pixels : neopixel.NeoPixel = neopixel.NeoPixel(board.D18, numberOfPixels)

def setPixelColor(pixelNumber : int, color : tuple):
    if pixelNumber < numberOfPixels:
        pixels[pixelNumber] = color

if __name__ == "__main__":
    setPixelColor(0, (255, 0, 0)) # Red
    pixels.show()
    time.sleep(1)
    setPixelColor(5, (0, 0, 255)) # Green
    pixels.show()
    time.sleep(1)
    pixels.fill((0, 255, 0)) # Turn on all pixels
    time.sleep(1)
    pixels.fill((0, 0, 0)) # Turn off all pixels
    print("Pixels set to red.")
    # setPixelColor(0, (0, 255, 0)) # Green
    # time.sleep(1)
    # setPixelColor(0, (0, 0, 255)) # Blue
    # time.sleep(1)
    # setPixelColor(0, (255, 255, 0)) # Yellow
    # time.sleep(1)
    # setPixelColor(0, (255, 0, 255)) # Magenta
    # time.sleep(1)
    # setPixelColor(0, (0, 255, 255)) # Cyan
    # time.sleep(1)
    # setPixelColor(0, (255, 255, 255)) # White

    # for airport in airports:
    #     flightCategory : str = getMetarFlightCategory(airport)
    #     print()
    #     print(f"{airport}: {flightCategory}")