import pygame
pygame.init()

BLUE = (10, 107, 250)
# screens and dimensions
SCREENWIDTH = 800
SCREENHEIGHT = 600
game_screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
game_screen_fill = BLUE
INNERSCREENX = SCREENWIDTH / 5.6
INNERSCREENWIDTH = SCREENWIDTH - (INNERSCREENX * 2)
INNERSCREENHEIGHT = SCREENHEIGHT