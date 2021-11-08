import neopixel
import time
import random


class NeoHandler(neopixel.NeoPixel):
    '''NeoHandler is a child of the NeoPixel class'''

    def __init__(self, pixel_pin, num_pixels, brightness, auto_write, pixel_order):
        super().__init__(pixel_pin, num_pixels, brightness=brightness, auto_write=auto_write, pixel_order=pixel_order)
        self.num_pixels = num_pixels
        self.pixel_order = pixel_order


    def segment_array(linear_array, col_count):
        '''converts a one dimentional array into a 2D matrix based on the desired number of columns'''
        matrix_array = []
        pos = 0
        col_height = linear_array / col_count

        for i in range(col_count):
            matrix_array.append(linear_array[pos:pos+col_height])
            pos += col_height

        return matrix_array


    def display_volumes(self, freq_vols = [10, 5, 1, 5, 15, 0, 2, 4, 6, 8, 6, 4, 3, 2, 1, 0, 1, 5, 10, 15], wait = 0.01, keep = False):
        '''displays the volume level of each given frequency on a linear array'''

        # the number of LEDs in one column
        col_height = int(self.num_pixels/len(freq_vols))

        # for each whole column given by the number of frequencies
        for x in range(len(freq_vols)):
            # for the volume level from each frequency
            for y in range(freq_vols[x]):
                # add colored LEDs up to the set volume level
                self[(x*col_height + y)] = (255, 16, 225)
        
        # update LED strip
        self.show()
        time.sleep(wait)
        if not keep:
            self.fill((0, 0, 0))


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
        return (r, g, b) if self.pixel_order in (neopixel.RGB, neopixel.GRB) else (r, g, b, 0)


    def rainbow_cycle(self, wait):
        for j in range(255):
            for i in range(self.num_pixels):
                pixel_index = (i * 256 // self.num_pixels) + j
                self[i] = self.wheel(pixel_index & 255)
            self.show()
            time.sleep(wait)
    

    def bounce(self, color = (rand_color())):
        for i in range(self.num_pixels):
            self[i] = color
            # pixels.show()
            self[(i-1 if i-1 > -1 else 0)] = (0, 0, 0)
            self.show()

        for i in range(self.num_pixels-1, -1, -1):
            self[i] = color
            # pixels.show()
            self[(i+1 if i+1 < self.num_pixels else 0)] = (0, 0, 0)
            self.show()


    def rgb_cycle(self, wait):
        self.fill((255, 0, 0))
        self.show()
        time.sleep(wait)

        self.fill((0, 255, 0))
        self.show()
        time.sleep(wait)

        self.fill((0, 0, 255))
        self.show()
        time.sleep(wait)
