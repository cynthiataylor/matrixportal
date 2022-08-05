# SPDX-FileCopyrightText: 2020 Jeff Epler for Adafruit Industries
#
# SPDX-License-Identifier: MIT

# This example implements a simple two line scroller using
# Adafruit_CircuitPython_Display_Text. Each line has its own color
# and it is possible to modify the example to use other fonts and non-standard
# characters.

WIDTH = 32
HEIGHT = 16

import random
import time


import adafruit_display_text.label
import board
import displayio
import framebufferio
import rgbmatrix
import terminalio

# If there was a display before (protomatter, LCD, or E-paper), release it so
# we can create ours


# This next call creates the RGB Matrix object itself. It has the given width
# and height. bit_depth can range from 1 to 6; higher numbers allow more color
# shades to be displayed, but increase memory usage and slow down your Python
# code. If you just want to show primary colors plus black and white, use 1.
# Otherwise, try 3, 4 and 5 to see which effect you like best.
#
# These lines are for the Feather M4 Express. If you're using a different board,
# check the guide to find the pins and wiring diagrams for your board.
# If you have a matrix with a different width or height, change that too.
# If you have a 16x32 display, try with just a single line of text.
displayio.release_displays()
matrix = rgbmatrix.RGBMatrix(
    width=32, bit_depth=4,
    rgb_pins=[
        board.MTX_R1,
        board.MTX_G1,
        board.MTX_B1,
        board.MTX_R2,
        board.MTX_G2,
        board.MTX_B2
    ],
    addr_pins=[
        board.MTX_ADDRA,
        board.MTX_ADDRB,
        board.MTX_ADDRC
    ],
    clock_pin=board.MTX_CLK,
    latch_pin=board.MTX_LAT,
    output_enable_pin=board.MTX_OE
)
display = framebufferio.FramebufferDisplay(matrix)
# Associate the RGB matrix with a Display so that we can use displayio features
#display = framebufferio.FramebufferDisplay(matrix, auto_refresh=False)

# Create a bitmap with two colors
bitmap = displayio.Bitmap(display.width, display.height, 2)

# Create a two color palette
palette = displayio.Palette(2)
palette[0] = 0x000000
palette[1] = 0xff00ff

# Create a TileGrid using the Bitmap and Palette
tile_grid = displayio.TileGrid(bitmap, pixel_shader=palette)

# Create a Group
group = displayio.Group()

# Add the TileGrid to the Group
group.append(tile_grid)

# Add the Group to the Display
display.show(group)

bitmap[WIDTH//2, 0] = 1

rule = 30

def draw(rule):
    # Draw even more pixels
    for y in range(1, HEIGHT):
        for x in range(1, WIDTH-1):
            if (bitmap[x-1,y-1] == 1 and bitmap[x,y-1] == 1 and bitmap[x+1,y-1]==1):
                bitmap[x,y]=((rule>>7) & 1)
            if (bitmap[x-1,y-1] == 1 and bitmap[x,y-1] == 1 and bitmap[x+1,y-1]==0):
                bitmap[x,y]=((rule>>6) & 1)
            if (bitmap[x-1,y-1] == 1 and bitmap[x,y-1] == 0 and bitmap[x+1,y-1]==1):
                bitmap[x,y]=((rule>>5) & 1)
            if (bitmap[x-1,y-1] == 1 and bitmap[x,y-1] == 0 and bitmap[x+1,y-1]==0):
                bitmap[x,y]=((rule>>4) & 1)
            if (bitmap[x-1,y-1] == 0 and bitmap[x,y-1] == 1 and bitmap[x+1,y-1]==1):
                bitmap[x,y]=((rule>>3) & 1)
            if (bitmap[x-1,y-1] == 0 and bitmap[x,y-1] == 1 and bitmap[x+1,y-1]==0):
                bitmap[x,y]=((rule>>2) & 1)
            if (bitmap[x-1,y-1] == 0 and bitmap[x,y-1] == 0 and bitmap[x+1,y-1]==1):
                bitmap[x,y]=((rule>>1) & 1)
            if (bitmap[x-1,y-1] == 0 and bitmap[x,y-1] == 0 and bitmap[x+1,y-1]==0):
                bitmap[x,y]=(rule & 1)

# Loop forever so you can enjoy your image

rule = 0

while True:
    draw(rule)
    rule = rule + 1
    if (rule > 256):
       rule = 0
    time.sleep(3)
