# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import neopixel
import random
import MatrixHandler


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
    return (r, g, b) if ORDER in (neopixel.RGB, neopixel.GRB) else (r, g, b, 0)


def rainbow_cycle(wait):
    for j in range(255):
        for i in range(num_pixels):
            pixel_index = (i * 256 // num_pixels) + j
            pixels[i] = wheel(pixel_index & 255)
        pixels.show()
        time.sleep(wait)


def rand_color():
    return random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255)


if __name__ == '__main__':

    # On a Raspberry pi, use this instead, not all pins are supported
    pixel_pin = board.D18

    # The number of NeoPixels
    num_pixels = 300

    # The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
    ORDER = neopixel.GRB

    pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.25, auto_write=False, pixel_order=ORDER)

    random.seed(69)

    try:
        while True:

            MatrixHandler.display_volumes(pixels)

            # for i in range(num_pixels):
            #     pixels[i] = (rand_color())
            #     # pixels.show()
            #     pixels[(i-1 if i-1 > -1 else 0)] = (0, 0, 0)
            #     pixels.show()

            # for i in range(num_pixels-1, -1, -1):
            #     pixels[i] = (rand_color())
            #     # pixels.show()
            #     pixels[(i+1 if i+1 < num_pixels else 0)] = (0, 0, 0)
            #     pixels.show()

            # pixels.fill((255, 0, 0))
            # pixels.show()
            # time.sleep(1)

            # pixels.fill((0, 255, 0))
            # pixels.show()
            # time.sleep(1)

            # pixels.fill((0, 0, 255))
            # pixels.show()
            # time.sleep(1)

            # rainbow_cycle(0.001)  # rainbow cycle with 1ms delay per step
    
    except KeyboardInterrupt:
        print(" accepted")
        print("Turning off LED strip")
        pixels.fill((0, 0, 0))
        pixels.show()
        print("Exiting program")
