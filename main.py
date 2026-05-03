import board
import neopixel

numberOfPixels : int = 30

pixels = neopixel.NeoPixel(board.D18, numberOfPixels)

def setPixelColor(pixelNumber : int, color : tuple):
    if pixelNumber < numberOfPixels:
        pixels[pixelNumber] = color

