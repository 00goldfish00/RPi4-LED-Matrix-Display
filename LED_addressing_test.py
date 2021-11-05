import time
import board
import neopixel
import random
from neohandler import NeoHandler


def rand_color():
    return random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255)


if __name__ == '__main__':

    # the number of NeoPixels
    pixel_count = 300

    # order of the color signal
    ORDER = neopixel.GRB

    random.seed(69)

    # create pixel handler object for led strip
    ph = NeoHandler(pixel_pin=board.D18, num_pixels=pixel_count, brightness=0.25, auto_write=False, pixel_order=ORDER)

    try:
        while True:

            ph.rainbow_cycle(0.005)  # rainbow cycle with 1ms delay per step

            ph.display_volumes()
            # time.sleep(5)

            # for i in range(pixel_count):
            #     ph[i] = (rand_color())
            #     # pixels.show()
            #     ph[(i-1 if i-1 > -1 else 0)] = (0, 0, 0)
            #     ph.show()

            # for i in range(pixel_count-1, -1, -1):
            #     ph[i] = (rand_color())
            #     # pixels.show()
            #     ph[(i+1 if i+1 < pixel_count else 0)] = (0, 0, 0)
            #     ph.show()

            # ph.fill((255, 0, 0))
            # ph.show()
            # time.sleep(1)

            # ph.fill((0, 255, 0))
            # ph.show()
            # time.sleep(1)

            # ph.fill((0, 0, 255))
            # ph.show()
            # time.sleep(1)

    except KeyboardInterrupt:
        print(" accepted")
        print("Turning off LED strip")
        ph.fill((0, 0, 0))
        ph.show()
        print("Exiting program")
