#!/usr/bin/python3

##
# Prerequisites:
# A Touchscreen properly installed on your system:
# - a device to output to it, e.g. /dev/fb1
# - a device to get input from it, e.g. /dev/input/touchscreen
##

import pygame, time, evdev, select, math

# Very important: the exact pixel size of the TFT screen must be known so we can build graphics at this exact format
surfaceSize = (320, 240)

# Note that we don't instantiate any display!
pygame.init()

# The pygame surface we are going to draw onto.
# /!\ It must be the exact same size of the target display /!\
lcd = pygame.Surface(surfaceSize)

# This is the important bit
def refresh():
    # We open the TFT screen's framebuffer as a binary file. Note that we will write bytes into it, hence the "wb" operator
    f = open("/dev/fb1","wb")
    # According to the TFT screen specs, it supports only 16bits pixels depth
    # Pygame surfaces use 24bits pixels depth by default, but the surface itself provides a very handy method to convert it.
    # once converted, we write the full byte buffer of the pygame surface into the TFT screen framebuffer like we would in a plain file:
    f.write(lcd.convert(16,0).get_buffer())
    # We can then close our access to the framebuffer
    f.close()
    time.sleep(0.1)

# Now we've got a function that can get the bytes from a pygame surface to the TFT framebuffer,
# we can use the usual pygame primitives to draw on our surface before calling the refresh function.

# Here we just blink the screen background in a few colors with the "Hello World!" text
pygame.font.init()
defaultFont = pygame.font.SysFont(None,30)

lcd.fill((255,0,0))
lcd.blit(defaultFont.render("Hello World!", False, (0, 0, 0)),(0, 0))
refresh()

lcd.fill((0, 255, 0))
lcd.blit(defaultFont.render("Hello World!", False, (0, 0, 0)),(0, 0))
refresh()

lcd.fill((0,0,255))
lcd.blit(defaultFont.render("Hello World!", False, (0, 0, 0)),(0, 0))
refresh()

lcd.fill((128, 128, 128))
lcd.blit(defaultFont.render("Hello World!", False, (0, 0, 0)),(0, 0))
refresh()

##
# Everything that follows is for handling the touchscreen touch events via evdev
##

# Used to map touch event from the screen hardware to the pygame surface pixels.
# (Those values have been found empirically, but I'm working on a simple interactive calibration tool
tftOrig = (3750, 180)
tftEnd = (150, 3750)
tftDelta = (tftEnd [0] - tftOrig [0], tftEnd [1] - tftOrig [1])
tftAbsDelta = (abs(tftEnd [0] - tftOrig [0]), abs(tftEnd [1] - tftOrig [1]))

# We use evdev to read events from our touchscreen
# (The device must exist and be properly installed for this to work)
touch = evdev.InputDevice('/dev/input/touchscreen')

# We make sure the events from the touchscreen will be handled only by this program
# (so the mouse pointer won't move on X when we touch the TFT screen)
touch.grab()
# Prints some info on how evdev sees our input device
print(touch)
# Even more info for curious people
#print(touch.capabilities())

# Here we convert the evdev "hardware" touch coordinates into pygame surface pixel coordinates
def getPixelsFromCoordinates(coords):
    # TODO check divide by 0!
    if tftDelta [0] < 0:
        x = float(tftAbsDelta [0] - coords [0] + tftEnd [0]) / float(tftAbsDelta [0]) * float(surfaceSize [0])
    else:
        x = float(coords [0] - tftOrig [0]) / float(tftAbsDelta [0]) * float(surfaceSize [0])
    if tftDelta [1] < 0:
        y = float(tftAbsDelta [1] - coords [1] + tftEnd [1]) / float(tftAbsDelta [1]) * float(surfaceSize [1])
    else:
        y = float(coords [1] - tftOrig [1]) / float(tftAbsDelta [1]) * float(surfaceSize [1])
    return (int(x), int(y))

# Was useful to see what pieces I would need from the evdev events
def printEvent(event):
    print(evdev.categorize(event))
    print("Value: {0}".format(event.value))
    print("Type: {0}".format(event.type))
    print("Code: {0}".format(event.code))

# This loop allows us to write red dots on the screen where we touch it
while True:
    # TODO get the right ecodes instead of int
    r,w,x = select.select([touch], [], [])
    for event in touch.read():
        if event.type == evdev.ecodes.EV_ABS:
            if event.code == 1:
                X = event.value
            elif event.code == 0:
                Y = event.value
        elif event.type == evdev.ecodes.EV_KEY:
            if event.code == 330 and event.value == 1:
                printEvent(event)
                p = getPixelsFromCoordinates((X, Y))
                print("TFT: {0}:{1} | Pixels: {2}:{3}".format(X, Y, p [0], p [1]))
                pygame.draw.circle(lcd, (255, 0, 0), p , 2, 2)
                refresh()

exit()