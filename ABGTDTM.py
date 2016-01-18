import sys
from classes import *

'''
Save game feature needed

'''


def save_game():
    print('wip')


def main_menu():
    print('wip')

    platforms = []  # array containing the platforms of the level
    enemies = []  # array containing the enemies of the level
    power_ups = []  # array containing the power ups of the level
    time_enabled = False  # is this level timed


def main():
    # game states
    done = False
    level_number = 0  # level 0 by default means menu screen
    SAVE_FILE = 'save_game.txt'

    # Colours


    pygame.display.set_caption('A Beginniner\'s guide to destroying the Moon')

    # create the 4 walls to stop player

    # create top wall
    wall_top = Wall((INNERSCREENX + 5), 0, (INNERSCREENWIDTH - 5), 5)

    # bottom wall
    wall_bottom = Wall(INNERSCREENX, (SCREENHEIGHT - 5), INNERSCREENWIDTH, 5)

    # create left wall
    wall_left = Wall(INNERSCREENX, 0, 5, INNERSCREENHEIGHT)

    # create right wall
    wall_right = Wall(INNERSCREENWIDTH + INNERSCREENX - 6, 5, 5, INNERSCREENHEIGHT)

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.change_speed(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    player.change_speed(1, 0)
                elif event.key == pygame.K_UP:
                    player.change_speed(0, -1)
                elif event.key == pygame.K_DOWN:
                    player.change_speed(0, 1)
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    player.change_speed(1, 0)
                elif event.key == pygame.K_RIGHT:
                    player.change_speed(-1, 0)
                elif event.key == pygame.K_UP:
                    player.change_speed(0, 1)
                elif event.key == pygame.K_DOWN:
                    player.change_speed(0, -1)

        # fill main screen with blue
        game_screen.fill(game_screen_fill)

        # draw inner screen
        pygame.draw.rect(game_screen, (0, 191, 255), pygame.Rect(INNERSCREENX, 0, INNERSCREENWIDTH, INNERSCREENHEIGHT))

        # update player and draw all sprites to screen
        player.update()
        all_sprites.draw(game_screen)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
