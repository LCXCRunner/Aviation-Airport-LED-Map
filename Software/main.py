try:
    import board
except Exception:
    board = None

try:
    import neopixel
except Exception:
    neopixel = None

import threading
import time
from metarFlightCatagory import getMetarFlightCategory

numberOfPixels : int = 11
pixelBuffer : list[tuple[int, int, int]] = [(0, 0, 0)] * numberOfPixels
airports : list[str] = ["KHCR", "KPVU", "KSVR", "KSLC", "KTYV", "KENV", "KHIF", "KOGD", "KBMC", "KLGU", "KEVW"]
airportDict : dict[str, str] = {airport: "Unknown" for airport in airports}
flight_update_lock = threading.Lock()
flight_update_event = threading.Event()
stop_event = threading.Event()
polling_interval_seconds = 15 * 60

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

def setPixelColor(pixelNumber : int, color : tuple[int, int, int]):
    if pixelNumber < numberOfPixels:
        pixels[pixelNumber] = color


def update_all_flight_categories():
    global airportDict
    new_categories : dict[str, str] = {}

    for airport in airports:
        category : str = getMetarFlightCategory(airport)
        new_categories[airport] = category

    with flight_update_lock:
        airportDict = new_categories
        flight_update_event.set()


def polling_thread():
    while not stop_event.is_set():
        print("Polling METAR API for flight categories...")
        update_all_flight_categories()
        for _ in range(polling_interval_seconds):
            if stop_event.is_set():
                break
            time.sleep(1)


def apply_flight_categories_to_pixels():
    with flight_update_lock:
        categories = [airportDict[airport] for airport in airports]

    for i, flightCategory in enumerate(categories):
        if flightCategory == "VFR":
            color : tuple[int, int, int] = (0, 255, 0)
        elif flightCategory == "MVFR":
            color : tuple[int, int, int] = (0, 0, 255)
        elif flightCategory == "IFR":
            color : tuple[int, int, int] = (255, 0, 0)
        elif flightCategory == "LIFR":
            color : tuple[int, int, int] = (255, 0, 255)
        else:
            color : tuple[int, int, int] = (255, 255, 255)

        setPixelColor(i, color)
    pixels.show()


def rainbowCycle(pause : float = 0.1):
    red : tuple[int, int, int] = (255, 0, 0)
    orange : tuple[int, int, int] = (255, 127, 0)
    yellow : tuple[int, int, int] = (255, 255, 0)
    green : tuple[int, int, int] = (0, 255, 0)
    blue : tuple[int, int, int] = (0, 0, 255)
    cyan : tuple[int, int, int] = (0, 255, 255)
    magenta : tuple[int, int, int] = (255, 0, 255)

    colorOrder : list[tuple[int, int, int]] = [red, orange, yellow, green, cyan, blue, magenta]

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

def initialize_board_sequence():
    pixels.fill((255, 0, 0))
    pixels.show()
    time.sleep(0.5)
    pixels.fill((0, 255, 0))
    pixels.show()
    time.sleep(0.5)
    pixels.fill((0, 255, 255))
    pixels.show()
    time.sleep(0.5)
    pixels.fill((255, 0, 255))
    pixels.show()
    time.sleep(0.5)
    rainbowCycle(0.25)


def run_main_loop():
    polling = threading.Thread(target=polling_thread, daemon=True)
    polling.start()

    try:
        update_all_flight_categories()

        while not stop_event.is_set():
            if flight_update_event.wait(timeout=10):
                flight_update_event.clear()
                print("Applying updated flight categories to pixels...")
                apply_flight_categories_to_pixels()

            time.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down due to KeyboardInterrupt.")
    except Exception as e:
        print("Error in main loop: " + str(e))
    finally:
        stop_event.set()
        polling.join(timeout=5)
        pixels.fill((0, 0, 0))
        pixels.show()


if __name__ == "__main__":
    if not hardware_available:
        print("Running in software fallback mode because no Raspberry Pi LED hardware was detected.")
    else:
        print("Hardware detected. Booting LED board sequence.")
        initialize_board_sequence()
        print("Boot sequence complete. Starting main loop.")

    run_main_loop()