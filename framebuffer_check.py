import os
import pygame

drivers = ['fbcon', 'directfb', 'svgalib', 'xvfb', 'x11']
found = False
for driver in drivers:
    # Make sure that SDL_VIDEODRIVER is set
    if not os.getenv('SDL_VIDEODRIVER'):
        os.putenv('SDL_VIDEODRIVER', driver)
    try:
        pygame.display.init()
    except pygame.error:
        print('Driver: {0} failed.'.format(driver))
        continue
    found = True
    break

if not found:
    raise Exception('No suitable video driver found!')

size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
print("Framebuffer size: %d x %d" % (size[0], size[1]))
pygame.display.set_mode(size, pygame.FULLSCREEN)