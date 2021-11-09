import neopixel
import time
import random
import math
import numpy as np


class NeoHandler(neopixel.NeoPixel):
    '''NeoHandler is a child of the NeoPixel class'''

    def __init__(self, pixel_pin, num_pixels, pixels_per_column, brightness, auto_write, pixel_order):
        super().__init__(pixel_pin, num_pixels, brightness=brightness, auto_write=auto_write, pixel_order=pixel_order)
        
        self.num_pixels = num_pixels

        self.broken_matrix = np.zeros(1, dtype=int)
        if type(pixels_per_column) is not int:
            self.broken_matrix = pixels_per_column
        elif type(pixels_per_column) is int:
            self.broken_matrix = np.full((num_pixels // pixels_per_column), pixels_per_column, dtype=int)
        
        self.columns = math.ceil(num_pixels // max(pixels_per_column))
        self.px_per_col = max(pixels_per_column)
        
        self.pixel_order = pixel_order


    def display_volumes(self, col_vols, color1, color2=None, wait = 0.1, keep = False):
        '''displays the volume level of each given frequency on an alternating matrix'''
        if color2 == None:
            color2 = color1

        # for each whole column given by the number of frequencies
        for col in range(self.columns):
            # if given volume is greater than current column height
            if col_vols[col] > self.broken_matrix[col]:
                # clip volume to column height
                volume = self.broken_matrix[col]
            else:
                # otherwise continue with given volume
                volume = col_vols[col]
            
            offset = self.px_per_col - self.broken_matrix[col]

            if offset == 0:

                # for the volume level of each frequency range
                for vol_add in range(volume):
                    # add colored LEDs up to the set volume level
                    if col % 2 == 0:
                        self[col*self.px_per_col + vol_add] = color1
                    else:
                        self[(col+1)*self.px_per_col-1 - vol_add] = color2
                
                for vol_sub in range(self.px_per_col - volume):
                    # remove colored LEDs down to the set volume level
                    if col % 2 == 0:
                        self[(col+1)*self.px_per_col-1 - vol_sub] = (0, 0, 0)
                    else:
                        self[col*self.px_per_col + vol_sub] = (0, 0, 0)
            
            else:

                # for the volume level of each frequency range
                for vol_add in range(volume):
                    # add colored LEDs up to the set volume level
                    if col % 2 == 0:
                        self[col*self.px_per_col + vol_add] = color1
                    else:
                        self[(col+1)*self.px_per_col-1 - offset - vol_add] = color2
                
                for vol_sub in range(self.px_per_col - volume - offset):
                    # remove colored LEDs down to the set volume level
                    if col % 2 == 0:
                        self[(col+1)*self.px_per_col-1 - offset - vol_add] = (0, 0, 0)
                    else:
                        self[col*self.px_per_col + vol_add] = (0, 0, 0)


        # update LED strip
        self.show()
        time.sleep(wait)


    def rand_color(self):
        '''generates a random 3 tuple of RGB values'''
        return random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255)
    

    def solid(self, r, g, b):
        self.fill((r, g, b))
        self.show()


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


    def rainbow_cycle(self, wait=0.01):
        for j in range(255):
            for i in range(self.num_pixels):
                pixel_index = (i * 256 // self.num_pixels) + j
                self[i] = self.wheel(pixel_index & 255)
            self.show()
            time.sleep(wait)
    

    def bounce(self, color = None):
        if color == None:
            color = (self.rand_color())
        
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


    def rgb_cycle(self, wait=1):
        self.fill((255, 0, 0))
        self.show()
        time.sleep(wait)

        self.fill((0, 255, 0))
        self.show()
        time.sleep(wait)

        self.fill((0, 0, 255))
        self.show()
        time.sleep(wait)
