import time
import board
import neopixel
from neohandler import NeoHandler
import random


if __name__ == '__main__':

    # create pixel handler object for led strip
    ph = NeoHandler(pixel_pin=board.D18, num_pixels=300, brightness=0.1, auto_write=False, pixel_order="GRB")

    try:
        while True:

            # ph.rainbow_cycle(0.01) # rainbow cycle with 1ms delay per step

            volumes = []

            for i in range(20):
                volumes.append(random.randint(0, 15))
            
            ph.display_volumes(volumes, wait=0.5)  # dispaly test frequency volume set

    except KeyboardInterrupt:
        print(" accepted")
        print("Turning off LED strip")
        # turn all LEDs off
        ph.fill((0, 0, 0))
        ph.show()
        print("Exiting program")
