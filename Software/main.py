import board
import neopixel
from metarFlightCatagory import getMetarFlightCategory

numberOfPixels : int = 11
airports : list[str] = ["KHCR", "KPVU", "KSVR", "KSLC", "KTYV", "KENV", "KHIF", "KOGD", "KBMC", "KLGU", "KEVW"]

# does not work very well when not run on the pi
# pixels = neopixel.NeoPixel(board.D18, numberOfPixels)

# def setPixelColor(pixelNumber : int, color : tuple):
#     if pixelNumber < numberOfPixels:
#         pixels[pixelNumber] = color

for airport in airports:
    flightCategory : str = getMetarFlightCategory(airport)
    print()
    print(f"{airport}: {flightCategory}")