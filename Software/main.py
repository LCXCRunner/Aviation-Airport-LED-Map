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

def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos * 3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos * 3)
        g = 0
        b = int(pos * 3)
    else:
        pos -= 170
        r = 0
        g = int(pos * 3)
        b = int(255 - pos * 3)
    return (r, g, b) if ORDER in {neopixel.RGB, neopixel.GRB} else (r, g, b, 0)


def rainbow_cycle(wait):
    for j in range(255):
        for i in range(num_pixels):
            pixel_index = (i * 256 // num_pixels) + j
            pixels[i] = wheel(pixel_index & 255)
        pixels.show()
        time.sleep(wait)


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
            pixelBuffer[i] = colorOrder[i % len(colorOrder)]
            pixels[i] = pixelBuffer[i]
            pixels.show()
        cycles += 1
        if cycles >= 10:
            pixels.fill((0, 0, 0)) # Turn off all pixels
            pixels.show()
            break
        time.sleep(pause)

if __name__ == "__main__":
    while True:
        cycle : int = 0

        # Comment this line out if you have RGBW/GRBW NeoPixels
        pixels.fill((255, 0, 0))
        # Uncomment this line if you have RGBW/GRBW NeoPixels
        # pixels.fill((255, 0, 0, 0))
        pixels.show()
        time.sleep(1)

        # Comment this line out if you have RGBW/GRBW NeoPixels
        pixels.fill((0, 255, 0))
        # Uncomment this line if you have RGBW/GRBW NeoPixels
        # pixels.fill((0, 255, 0, 0))
        pixels.show()
        time.sleep(1)

        # Comment this line out if you have RGBW/GRBW NeoPixels
        pixels.fill((0, 0, 255))
        # Uncomment this line if you have RGBW/GRBW NeoPixels
        # pixels.fill((0, 0, 255, 0))
        pixels.show()
        time.sleep(1)

        rainbow_cycle(0.001)  # rainbow cycle with 1ms delay per step

        cycle += 1
        if cycle >= 100:
            pixels.fill((0, 0, 0)) # Turn off all pixels
            pixels.show()
            break
