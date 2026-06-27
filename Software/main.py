import board
import neopixel
import time
from metarFlightCatagory import getMetarFlightCategory

numberOfPixels : int = 11
pixelBuffer : list[tuple] = [(0, 0, 0)] * numberOfPixels
airports : list[str] = ["KHCR", "KPVU", "KSVR", "KSLC", "KTYV", "KENV", "KHIF", "KOGD", "KBMC", "KLGU", "KEVW"]

# does not work very well when not run on the pi
pixels : neopixel.NeoPixel = neopixel.NeoPixel(board.D18, numberOfPixels)

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

    while True:
        cycles : int = 0
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
    while True:
        cycle : int = 0

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

        rainbowCycle(0.1)  # rainbow cycle with 100ms delay per step
