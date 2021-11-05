import neopixel
import board
import time
import random


def segment_array(linear_array, col_count):
    matrix_array = []
    pos = 0
    col_height = linear_array / col_count

    for i in range(col_count):
        matrix_array.append(linear_array[pos:pos+col_height])
        pos += col_height

    return matrix_array

test_vols = [1, 2, 3, 2, 1, 0, 2, 4, 6, 8, 6, 4, 3, 2, 1, 0, 1, 5, 10, 15]
def display_volumes(neo_array, freq_vols = test_vols):
    col_height = len(neo_array)/len(freq_vols)

    for x in range(len(freq_vols)):
        for y in range(freq_vols[x]):
            neo_array[int((x*col_height)+y)] = (255, 225, 55)
    neo_array.show()


def rand_color():
    return random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255)


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
            pixel_array[i] = wheel(pixel_index & 255)
        pixel_array.show()
        time.sleep(wait)
