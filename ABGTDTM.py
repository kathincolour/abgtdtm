import sys

from classes import *


def main():

    save_file = 'save_game.txt'

    pygame.display.set_caption('A Beginner\'s guide to destroying the Moon')
    clock = pygame.time.Clock()

    if game_control.current_level_no > 0:
        # create left wall to stop player
        wall_left = Wall(INNERSCREENX, 0, 5, INNERSCREENHEIGHT)

        # create right wall
        wall_right = Wall(INNERSCREENWIDTH + INNERSCREENX, 0, 5, SCREENHEIGHT)

    while game_control.current_level_no == 0 and not game_control.done:   # while main menu is functioning
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:  # when user presses up key
                    game_control.target_up()
                elif event.key == pygame.K_DOWN:  # when user presses down key
                    game_control.current_level.target_down()
                elif event.key == pygame.K_RETURN:  # when user presses enter key
                    game_control.current_level.select()

        game_control.current_level.draw(game_screen)
        game_control.current_level.target_button()
        pygame.display.flip()
        clock.tick(220)
    game_control.done = False
    game_control.change_level()

    while game_control.current_level_no > 0 and not game_control.done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_control.done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.go_left()
                elif event.key == pygame.K_RIGHT:
                    player.go_right()
                elif event.key == pygame.K_UP:
                    player.jump()

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player.change_x < 0:
                    player.stop()
                if event.key == pygame.K_RIGHT and player.change_x > 0:
                    player.stop()

        # fill main screen with blue
        game_screen.fill(game_screen_fill)

        # update player and level
        player.update()

        game_control.current_level.update_level()

        game_control.current_level.move_level()

        # draw below here
        # pygame.draw.rect(game_screen, LBLUE, (INNERSCREENX, 0, INNERSCREENWIDTH, INNERSCREENHEIGHT)) # draw inner screen
        # game_screen.blit(current_level.background,(INNERSCREENX, SCREENHEIGHT))
        game_control.current_level.draw(game_screen)
        all_sprites.draw(game_screen)

        pygame.display.flip()
        clock.tick(220)

    pygame.quit()


if __name__ == "__main__":
    main()
