import neopixel
import time
import random


class NeoHandler(neopixel.NeoPixel):
    '''NeoHandler is a child of the NeoPixel class'''

    def __init__(self, pixel_pin, num_pixels, brightness, auto_write, pixel_order):
        super().__init__(pixel_pin, num_pixels, brightness=brightness, auto_write=auto_write, pixel_order=pixel_order)
        self.num_pixels = num_pixels


    def segment_array(linear_array, col_count):
        '''converts a one dimentional array into a 2D matrix based on the desired number of columns'''
        matrix_array = []
        pos = 0
        col_height = linear_array / col_count

        for i in range(col_count):
            matrix_array.append(linear_array[pos:pos+col_height])
            pos += col_height

        return matrix_array


    def display_volumes(self, freq_vols = [1, 2, 3, 2, 1, 0, 2, 4, 6, 8, 6, 4, 3, 2, 1, 0, 1, 5, 10, 15]):
        '''displays the volume level of each given frequency on a linear array'''

        # the number of LEDs in one column
        col_height = int(self.num_pixels/len(freq_vols))

        # for each whole column given by the number of frequencies
        for x in range(len(freq_vols)):
            # for the volume level from each frequency
            for y in range(freq_vols[x]):
                # add colored LEDs up to the set volume level
                self[(x*col_height + y)] = (255, 55, 200)
        
        # update LED strip
        self.show()


    def rand_color():
        '''generates a random 3 tuple of RGB values'''
        return random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255)


    def wheel(self, pos):
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
        return (r, g, b) if self.ORDER in (neopixel.RGB, neopixel.GRB) else (r, g, b, 0)


    def rainbow_cycle(self, wait):
        for j in range(255):
            for i in range(self.num_pixels):
                pixel_index = (i * 256 // self.num_pixels) + j
                self[i] = self.wheel(pixel_index & 255)
            self.show()
            time.sleep(wait)
