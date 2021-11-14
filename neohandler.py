import neopixel
import time
import random
import math
import numpy as np


class NeoHandler(neopixel.NeoPixel):
    '''NeoHandler is a child of the NeoPixel class which adds display matrix settings and mode options.
    The pixels_per_column parameter is assumed to be either an int or a numpy array.'''

    def __init__(self, pixel_pin, num_pixels, pixels_per_column, brightness, auto_write, pixel_order):
        # initialize parent class by passing the required settings to it
        super().__init__(pixel_pin, num_pixels, brightness=brightness, auto_write=auto_write, pixel_order=pixel_order)
        
        # store settings that were difficult to retrieve from parent
        self.num_pixels = num_pixels
        self.pixel_order = pixel_order

        # calculate the number of columns that fit on the LED strip
        self.columns = math.ceil(num_pixels // max(pixels_per_column))

        # find the column that sets the displays perfect rectangle height
        self.px_per_col = max(pixels_per_column)

        # initialize broken matrix to a single item zero array
        self.broken_matrix = np.zeros(1, dtype=int)

        # if the given column height is an array use that
        if type(pixels_per_column) is not int:
            self.broken_matrix = pixels_per_column
        # if pixels_per_column is an int
        elif type(pixels_per_column) is int:
            # extend the array to the number of columns and fill the broken_matrix with the provided value
            self.broken_matrix = np.full(self.columns, pixels_per_column, dtype=int)


    def display_volumes(self, col_vols, color1, color2=None, wait = 0.1, keep = False):
        '''Displays the max volume of each given frequency on the created display matrix.'''

        # if no sencondary color is provided use the primary color
        if color2 == None:
            color2 = color1

        # loop through each whole column set by the constructor
        for col in range(self.columns):
            
            # if the volume is greater than current columns height
            if col_vols[col] > self.broken_matrix[col]:
                # clip the volume to the column height
                volume = self.broken_matrix[col]
            else:
                # otherwise continue with given volume
                volume = col_vols[col]
            
            # calculate the curent columns offset to compensate for missing pixels
            offset = self.px_per_col - self.broken_matrix[col]
            
            # fill whole column with respective color
            if col % 2 == 0:
                self.fill(color1)
            else:
                self.fill(color2)
            
            # remove colored LEDs down to the set volume level
            for vol_sub in range(self.px_per_col - volume - offset):
                if col % 2 == 0:
                    # jump ahead to the bottom of the next column and step back to reach the top of the current
                    # then iterate backwards to remove filled color
                    self[(col+1)*self.px_per_col-1 - offset - vol_sub] = (0, 0, 0)
                else:
                    # jump to the bottom of the column and iterate upwards to remove filled color
                    self[col*self.px_per_col + vol_sub] = (0, 0, 0)

        # update LED strip and hold
        self.show()
        time.sleep(wait)


    def rand_color(self):
        '''Generates a random RGB value. Returns a 3 tuple'''
        return random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255)


    # pattern methods

    def solid(self, r, g, b, wait=0):
        '''Simply fills and display with the given color and updates the display.
        If the wait parameter is set the color will hold for the wait time and then the display will clear.'''
        self.fill((r, g, b))
        self.show()

        if wait > 0:
            time.sleep(wait)
            self.fill((0, 0, 0))
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
        '''Displays a single pixel racing up and then back down the LED strip.'''

        # if a color is not provided a random one is genrated
        if color == None:
            color = (self.rand_color())
        
        # iterate up the display array
        for i in range(self.num_pixels):
            # set the current pixels color
            self[i] = color
            # if the previous pixel is not at the -1 index then clear it
            # otherwise clear the next pixel which should already be cleared
            self[(i-1 if i-1 > -1 else 1)] = (0, 0, 0)
            # update the display
            self.show()

        # iterate down the display array
        for i in range(self.num_pixels-1, -1, -1):
            # set the current pixels color
            self[i] = color
            # if the previous pixel is not past the last index then clear it
            # otherwise clear the next pixel which should already be cleared
            self[(i+1 if i+1 < self.num_pixels else 0)] = (0, 0, 0)
            # update the display
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


    # the following patterns are planned to be adapted from C++


    # void rainbow() //Rainbow
    # {
    # // FastLED's built-in rainbow generator
    # fill_rainbow( leds, NUM_LEDS, partyHue, 7);
    # }

    # void rainbowWithGlitter() //Not used
    # {
    # // built-in FastLED rainbow, plus some random sparkly glitter
    # rainbow();
    # addGlitter(80);
    # }

    # void addGlitter( fract8 chanceOfGlitter) 
    # {
    # if( random8() < chanceOfGlitter) {
    #     leds[ random16(NUM_LEDS) ] += CRGB::White;
    # }
    # }

    # void confetti()     //Party
    # {
    # // random colored speckles that blink in and fade smoothly
    # fadeToBlackBy( leds, NUM_LEDS, 2);    //2 represents how long it takes for the color to fade away (makes it seem like there are more leds lighting up)
    # int pos = random16(NUM_LEDS);
    # leds[pos] += CHSV( partyHue + random8(8), random8(180,255), 255);       //  leds[pos] += CHSV( partyHue + random8(64), 200, 255);   this was the original
    # }

    # void sinelon()   //Snake
    # {
    # // a colored dot sweeping back and forth, with fading trails
    # fadeToBlackBy( leds, NUM_LEDS, 20);
    # int pos = beatsin16( 13, 0, NUM_LEDS-1 );
    # leds[pos] += CHSV( partyHue, 255, 192);
    # }

    # void bpm()    //Not Used
    # {
    # // colored stripes pulsing at a defined Beats-Per-Minute (BPM)
    # uint8_t BeatsPerMinute = 62;
    # CRGBPalette16 palette = PartyColors_p;
    # uint8_t beat = beatsin8( BeatsPerMinute, 64, 255);
    # for( int i = 0; i < NUM_LEDS; i++) { //9948
    #     leds[i] = ColorFromPalette(palette, partyHue+(i*2), beat-partyHue+(i*10));
    # }
    # }

    # void juggle() {   //Not Used
    # // eight colored dots, weaving in and out of sync with each other
    # fadeToBlackBy( leds, NUM_LEDS, 20);
    # byte dothue = 0;
    # for( int i = 0; i < 8; i++) {
    #     leds[beatsin16( i+7, 0, NUM_LEDS-1 )] |= CHSV(dothue, 200, 255);
    #     dothue += 32;
    # }
    # }
