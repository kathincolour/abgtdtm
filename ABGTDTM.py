from classes import *


def main_menu():
    print('wip')


def main():
    # game states
    done = False
    level_number = 1  # level 0 by default means menu screen
    save_file = 'save_game.txt'

    pygame.display.set_caption('A Beginniner\'s guide to destroying the Moon')
    clock = pygame.time.Clock()

    # create the 4 walls to stop player

    # create top wall
    #wall_top = Wall((INNERSCREENX + 5), 0, (INNERSCREENWIDTH - 5), 5)

    # bottom wall - May not be needed, the game will look more continous without borders
    #wall_bottom = Wall(INNERSCREENX, (SCREENHEIGHT - 5), INNERSCREENWIDTH, 5)

    # create left wall
    wall_left = Wall(INNERSCREENX, 0, 5, INNERSCREENHEIGHT)

    # create right wall
    wall_right = Wall(INNERSCREENWIDTH + INNERSCREENX, 0, 5, SCREENHEIGHT)

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.go_left()
                elif event.key == pygame.K_RIGHT:
                    player.go_right()
                elif event.key == pygame.K_UP:
                    player.jump()
                #elif event.key == pygame.K_DOWN:
                   #player.change_speed(0, 1)

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player.change_x < 0:
                    player.stop()
                if event.key == pygame.K_RIGHT and player.change_x > 0:
                    player.stop()

        # fill main screen with blue
        game_screen.fill(game_screen_fill)

        # update player and level
        player.update()

        current_level.update_level()

        current_level.move_level()

        # draw below here
        #pygame.draw.rect(game_screen, LBLUE, (INNERSCREENX, 0, INNERSCREENWIDTH, INNERSCREENHEIGHT)) # draw inner screen
        game_screen.blit(current_level.background,[INNERSCREENX, SCREENHEIGHT])
        current_level.draw(game_screen)
        all_sprites.draw(game_screen)

        pygame.display.flip()
        clock.tick(210)

    pygame.quit()


if __name__ == "__main__":
    main()
