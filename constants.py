import pygame
pygame.init()
pygame.font.init()

BLUE = (10, 107, 250)
LLBLUE = (138, 242, 255)
LBLUE = (39, 219, 242)
PURPLE = (128, 0, 128)
WHITE = (255, 255, 255)
BLACK = (0,0,0)

# screens and dimensions
SCREENWIDTH = 800
SCREENHEIGHT = 600
game_screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
game_screen_fill = BLUE

INNERSCREENX = SCREENWIDTH / 5.6338  # = 142.857     142 = 800 / x
INNERSCREENWIDTH = SCREENWIDTH - (INNERSCREENX * 2)
INNERSCREENHEIGHT = SCREENHEIGHT
inner_screen = pygame.Rect(INNERSCREENX, 0, INNERSCREENWIDTH, INNERSCREENHEIGHT)


basic_font = pygame.font.Font(None, 20)