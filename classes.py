from constants import *

# Classes for ABGTDTM

''' classes or items needed:
player
enemies
levels
- tutorial(?) with guided text
- mountain 
- sky
- enter space
- space
- finals
- boss
objects
- walls
- platforms
- moving platforms
- power ups
'''
from ABGTDTM import *
import random, os

class Game_control:
    def __init__(self):
        self.done = False
        self.current_level_no = 0
        self.level_list = []
        self.current_level = None

    def change_level(self):
        self.current_level = self.level_list[self.current_level_no]

game_control = Game_control()


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.image_left = pygame.image.load("assets/protagonist_spr.png").convert_alpha()
        self.image_right = pygame.transform.flip(self.image_left, True, False)
        self.hurt_left = pygame.image.load("assets/protagonist_hurt1_spr.png").convert_alpha() # image of player when hurt by enemy
        self.hurt_right = pygame.transform.flip(self.hurt_left, True, False)
        self.invincible = pygame.image.load("assets/protagonist_powerup_spr.png").convert_alpha()
        self.invincible_right = pygame.transform.flip(self.invincible, True, False)
        self.image = self.image_left # set the default sprite image to left

        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

        self.change_x = 0
        self.change_y = 0

        # variables related to gameplay
        self.lives = 4
        self.invincibility = False
        self.tock = 0


    #def change_speed(self, x, y):
        #self.change_x += x
        #self.change_y += y

    def update(self):

        # calculate gravity
        self.calc_gravity()

        # move left or right
        self.rect.x += self.change_x

        if self.invincibility and self.tock < 1200:
            self.tock += 1
            print('tock')
        else:
            self.invincibility = False



        # check for collision with platform or wall
        block_hit_list = pygame.sprite.spritecollide(self, game_control.current_level.platforms, False)
        for entity in block_hit_list:
            if self.change_x > 0:  # player is moving right because it is positive
                self.rect.right = entity.rect.left  # Change player right side to equal object left side
            else:  # player is moving left
                self.rect.left = entity.rect.right

        # check for collision with power_up
        pu_hit_list = pygame.sprite.spritecollide(self, game_control.current_level.power_ups, False)
        for pu in pu_hit_list:
            if pu.number == '1':
                self.invincibility = True
                print('invincible')
                self.image = self.invincible
            elif pu.number == '2':
                self.lives += 1
            pu.kill()

        # check for collision with enemy
        enemy_hit_list = pygame.sprite.spritecollide(self, game_control.current_level.enemies, False)
        for enemy in enemy_hit_list:
            if not self.invincibility:
                self.lives -= 1
                self.check_health()
                # play sound or change player sprite here

                if self.change_x > 0:  # player is moving right because it is positive
                    self.rect.right = enemy.rect.left  # Change player right side to equal object left side
                    self.rect.x -= 5
                elif self.change_x < 0:  # player is moving left
                    self.rect.left = enemy.rect.right
                    self.rect.x += 5
                elif self.change_y > 0: # player is moving downwards
                    self.rect.bottom = enemy.rect.top

            else: # invincibility is on and player doesn't lose health
                if self.change_x > 0:  # player is moving right because it is positive
                    self.rect.right = enemy.rect.left  # Change player right side to equal object left side
                else:  # player is moving left
                    self.rect.left = enemy.rect.right


        # move up or down
        self.rect.y += self.change_y

        block_hit_list = pygame.sprite.spritecollide(self, game_control.current_level.platforms, False)
        for entity in block_hit_list:
            if self.change_y > 0:  # player is moving down because it is positive
                self.rect.bottom = entity.rect.top  # Change player bottom side to equal object top side
            else:  # player is moving up
                self.rect.top = entity.rect.bottom

            # Stop our vertical movement
            self.change_y = 0

    def calc_gravity(self):
        # calculate effect of  Gravity
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += 0.12

        # see if the player is on the ground/bottom
        if self.rect.y >= SCREENHEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = SCREENHEIGHT - self.rect.height

    def jump(self):
        # called when user presses jump button
        # move down a bit and see if there is a platform below us.
        # Move down 2 pixels because it doesn't work well if we only move down
        # 1 when working with a platform moving down.
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, game_control.current_level.platforms, False)
        self.rect.y -= 2

        # If it is ok to jump, set our speed upwards
        if len(platform_hit_list) > 0 or self.rect.bottom >= SCREENHEIGHT:
            self.change_y = -6  # change to lower

    def go_left(self):
        # Called when the user hits the left arrow.
        if self.invincibility:
            self.image = self.invincible   # change to the invincible sprite look
        else:
            self.image = self.image_left # flip the sprite image to the original if turning left
        self.change_x = -0.5

    def go_right(self):
        # Called when the user hits the right arrow.
        if self.invincibility:
            self.image = self.invincible_right   # change to the invincible sprite look
        else:
            self.image = self.image_right # flip sprite image
        self.change_x = 1

    def stop(self):
        # Called when the user lets off the keyboard.
        self.change_x = 0

    def check_health(self):
        if self.lives <= 0:
            # restart level
            print('death')

    def death(self):
        # show death sprite?
        inner_screen.fill(BLUE)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, enem, x, y, speed):
        """
        :param enem: name of sprite file without _spr
        :param x:
        :param y:
        :param speed:
        :return:
        """
        pygame.sprite.Sprite.__init__(self)

        self.image_left = pygame.image.load("assets/enemy1_spr.png").convert_alpha()
        self.image_right = pygame.transform.flip(self.image_left, True, False)
        self.image = self.image_left # set the default sprite image to left

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.bottom = y

        self.direction = 'right'

    def update(self):
        # test to see where the enemy is

        platform_hit = pygame.sprite.spritecollide(self, game_control.current_level.platforms, False)
        if len(platform_hit) > 0:
            for platform in platform_hit:
                if self.rect.bottom == platform.rect.topleft and self.change_x <= 0:
                    self.go_right()

                elif self.rect.bottom == platform.rect.topright and self.change_x > 0:
                    self.go_left()

        elif self.rect.bottom == SCREENHEIGHT: # enemy is on the bottom of the screen
            wall_hit_list = pygame.sprite.spritecollide(self, wall_list, False)
            for entity in wall_hit_list:
                if self.image == self.image_right:  # enemy is moving right because it is positive
                    self.rect.right = entity.rect.left  # Change enemy right side to equal object left side
                else:  # enemy is moving left
                    self.rect.left = entity.rect.right

    def go_left(self):
        self.image = self.image_left  # flip the sprite image to the original if turning left
        self.rect.x -= 2

    def go_right(self):
        self.image = self.image_right # flip sprite image
        self.rect.x += 2


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)

        # make a black wall with width and height passed
        self.image = pygame.Surface((width, height))
        self.image.fill((0, 0, 0))

        # Pass in the x & y for location
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        wall_list.add(self)
        all_sprites.add(self)
        all_static_sprites.add(self)


class Power_up(pygame.sprite.Sprite):
    def __init__(self, no, x, y):
        pygame.sprite.Sprite.__init__(self)

        # create power up sprite from image file
        self.image = pygame.image.load("assets/" + no + "_spr" + ".png").convert_alpha()

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.bottom = y

        self.number = no[7]   # denotes the type of power up- to be used by the player class when interacting


class Platform(pygame.sprite.Sprite):
    def __init__(self, width, height):
        self.image = pygame.Surface([width, height])
        self.image.fill(PURPLE)  # maybe have a level specific colour/graphic here

        self.rect = self.image.get_rect()

        pygame.sprite.Sprite.__init__(self)


class Background(pygame.sprite.Sprite):
    def __init__(self, file):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('assets/background_' + file + '.png').convert()
        self.image.set_alpha(200)
        self.rect = self.image.get_rect()
        self.rect.x = INNERSCREENX
        self.rect.bottom = SCREENHEIGHT


class Button(pygame.sprite.Sprite):
    def __init__(self, txt, x, y, w, h, func):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([w, h])
        self.image.fill(LBLUE)
        self.highlight = LLBLUE

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.func = func

        self.button_font = pygame.font.Font(None, 15)


class Main_menu:
    """ main menu class """
    def __init__(self):

        self.buttons = []  # group for buttons to be added
        self.buttons_sprite = pygame.sprite.Group()  # sprite group for buttons so they can be drawn
        self.backgrounds = pygame.sprite.Group()
        self.background_1 = Background('1')
        self.background_2 = Background('1')
        self.background = random.choice([self.background_1, self.background_2])  # chooses between 2 different backgrounds to draw
        self.backgrounds.add(self.background)
        '''self.background.rect.x = 0
        self.background.rect.y = SCREENHEIGHT '''

        self.target = 0

        self.main_font = pygame.font.Font('assets/font1.ttf', 100)
        self.title_text = self.main_font.render('A Beginner\'s guide to', 0, WHITE)
        self.title_text1 = self.main_font.render('Destroying the Moon', 0, WHITE)

        # create buttons
        self.n_game_button = Button('New Game', 200, 280, 300, 100, 'new')
        self.buttons.append(self.n_game_button)
        self.buttons_sprite.add(self.n_game_button)
        self.c_game_button = Button('Continue Game', 200, 330, 300, 100, 'cont')
        self.buttons.append(self.c_game_button)
        self.buttons_sprite.add(self.c_game_button)
        self.help_button = Button('Help', 200, 380, 300, 100, 'help')
        self.buttons.append(self.help_button)
        self.buttons_sprite.add(self.help_button)
        self.options_button = Button('Options',200, 430, 300, 100, 'opt')
        self.buttons.append(self.options_button)
        self.buttons_sprite.add(self.options_button)
        self.quit_button = Button('Quit', 200, 480, 300, 100, 'quit')
        self.buttons.append(self.quit_button)
        self.buttons_sprite.add(self.quit_button)

    def draw(self, screen):
        self.backgrounds.draw(screen)
        self.buttons_sprite.draw(screen)
        self.title_text.blit(screen, (200, 200))
        self.title_text1.blit(screen, (250, 250))

    def target_button(self):
        if self.target <= 4 or self.target >= 0:
            current_button = self.buttons[self.target]
            current_button.image.fill(LBLUE)

    def target_up(self):  # called when user pressed up key
        print('up key')
        if self.target > 0:
            print('move up')
            self.target -= 1
            print(str(self.target))

    def target_down(self):
        print('down key')
        if self.target < 4:
            print('move down')
            self.target += 1
            print(str(self.target))

    def select(self):
        print('select key')
        current_button = self.buttons[self.target]

        if current_button.func == 'new':
            print('new')
            self.new_game()
        elif current_button.func == 'cont':
            self.continue_game()
        elif current_button.func == 'help':
            self.g_help()
        elif current_button.func == 'opt':
            self.options()
        elif current_button.func == 'quit':
            print('quit')

    def new_game(self):
        print('warning message')
        open('save_file.txt', 'w').close()   # empty save file

        game_control.current_level_no = 1
        print(str(game_control.current_level_no))
        game_control.done = True
        print(str(game_control.current_level))

    def continue_game(self):
        print('cont')
        if os.path.getsize('save_file.txt') > 0:  # if save file is not empty (could throw exception otherwise)
            with open('save_file.txt', 'r') as file:
                game_control.current_level_no = int(file.read())
        else:
            print('yes')
            game_control.current_level_no = 1
        game_control.done = True

    def g_help(self):
        # new screen
        print('wip')

    def options(self):
        # maybe not needed?
        print('wip_op')


class Level:
    """ super class used to define each level """

    def __init__(self):
        self.platforms = pygame.sprite.Group()  # group containing the platform objects of the level
        self.enemies = pygame.sprite.Group()  # group containing the enemies of the level
        self.power_ups = pygame.sprite.Group()  # group containing the power ups of the level
        self.backgrounds = pygame.sprite.Group()  # create a sprite group for the background image so it is easier
        self.time_enabled = False  # is this level timed
        self.level_height = 3  # meaning 3 screen shifts therefore SCREENHEIGHT * 3 = maximum height = 1800
        self.current_height = 0 # keeps track of current height in level
        self.level_sprites = pygame.sprite.Group()  # sprite group containing all sprites in level

        self.soundtrack = None  # pygame.mixer.music.load
        self.background = None

    def update_level(self):
        """ Update everything in this level."""
        self.platforms.update()
        self.enemies.update()
        self.power_ups.update()

    def draw(self, screen):  # draw everything on the level
        # draw the sprites
        self.backgrounds.draw(screen)
        self.platforms.draw(screen)
        self.enemies.draw(screen)
        self.power_ups.draw(screen)

    def move_level(self):  # Check if player has reached edge of top screen

        if player.rect.top <= 1:   # if player is near top of screen
            self.current_height += 1  # increment place in level
            if self.current_height == self.level_height:
                print('woo new level')
                self.new_level()
            else:
                for platform in self.platforms: # move platforms 'down' or kill if on screen
                    if platform.rect.top > 0:
                        platform.kill()
                        print(str(platform.alive()))
                    else:
                        if platform.rect.top <= -1200:
                            platform.rect.top += SCREENHEIGHT * 2
                        else:
                            platform.rect.top += SCREENHEIGHT
                for enem in self.enemies:  # move enemies 'down' or kill if on screen
                    if enem.rect.top > 0:
                        enem.kill()
                    else:
                        if enem.rect.top <= -1200:
                            enem.rect.top += SCREENHEIGHT * 2
                        else:
                            enem.rect.top += SCREENHEIGHT

                for pu in self.power_ups:
                    if pu.rect.top > 0:
                        pu.kill()
                    else:
                        if pu.rec.top <= -1200:
                            platform.rect.top += SCREENHEIGHT * 2
                        else:
                            platform.rect.top += SCREENHEIGHT

            player.rect.bottom = SCREENHEIGHT

    def new_level(self):
        print('Level complete')
        # save game
        with open('save_file.txt', 'w') as savefile:   # access save file
            savefile.write(str(game_control.current_level_no + 1))   # save next level number (so player can start from new level)

        for sprite in self.level_sprites:
            sprite.kill()
            print('good die')

        # display text saying level complete
        end_text = basic_font.render('Level ' + str(game_control.current_level_no + 1) + ' complete!', True, WHITE)
        game_screen.blit(end_text, [400, 300])
        print(str(game_control.current_level_no))
        game_control.current_level_no += 1  # level number + 1
        print(str(game_control.current_level_no))

        game_control.change_level()


class Level_01(Level):
    def __init__(self):
        # Call the parent constructor
        Level.__init__(self)

        self.background = pygame.image.load("assets/background_1.png")

        # array of platforms to be drawn- width, height, x, y
        # x must be greater than (or equal to) INNERSCREENX and less than 500
        # y must be less than 600 (SCREENHEIGHT) and less than max screen height of level i.e. -1800
        level_platforms = [[170, 40, 350, 430], [150, 40, INNERSCREENX, 300], [100, 40, INNERSCREENX + 230, 190],
                 [150, 40, INNERSCREENX + 120, -150],[150, 40, INNERSCREENX + 350, -200],
                 [150, 30, INNERSCREENX + 100, - 350], [150, 40, INNERSCREENX + 200, -500],
                 [150, 40, INNERSCREENX + 100, -1350], [150, 40, INNERSCREENX + 350, -1500],
                 [150, 40, INNERSCREENX + 200, -1650]]

        # array of enemies to be drawn- type of enemy (file name), x, y, speed
        # x & y should be on a platform or the ground - follow the level_platforms array
        level_enemies = [['test', 360, 500, 1]]

        # array of power ups to be drawn- 'no' type should be string for file, x, y
        # can be drawn anywhere on screen (but not on top of platforms)
        level_power_ups = [['powerup1', INNERSCREENX + 100, 600]]

        for platform in level_platforms:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            self.platforms.add(block)
            self.level_sprites.add(block)

        for enemy in level_enemies:
            entity = Enemy(enemy[0], enemy[1], enemy[2], enemy[3])
            self.enemies.add(entity)
            self.level_sprites.add(entity)

        for power_up in level_power_ups:
            pu = Power_up(power_up[0], power_up[1], power_up[2])
            self.power_ups.add(pu)
            self.level_sprites.add(pu)

        level_background = Background('1')
        self.backgrounds.add(level_background)

class Level_02(Level):
    def __init__(self):
        # Call the parent constructor
        Level.__init__(self)

        self.background = None

        # array of platforms to be drawn- width, height, x, y
        # x should be greater than (or equal to) INNERSCREENX and less than 500
        # y should be less than 600 (SCREENHEIGHT) and less than max screen height of level i.e. -1800
        level_platforms = [[100, 50, INNERSCREENX + 200, 450]]

        # array of enemies to be drawn- type of enemy (file name), x, y, speed
        # x & y should be on a platform or the ground - follow the level_platforms array
        level_enemies = []

        for platform in level_platforms:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            self.platforms.add(block)
            self.level_sprites.add(block)

        for enemy in level_enemies:
            entity = Enemy(enemy[0], enemy[1], enemy[2], enemy[3])
            self.enemies.add(entity)
            self.level_sprites.add(entity)




# create all sprite groups and player instance
all_sprites = pygame.sprite.Group()
all_static_sprites = pygame.sprite.Group()  # Sprites that don't move (walls and platforms)
active_sprites = pygame.sprite.Group() # group for the player
player = Player(500, (SCREENHEIGHT + 10))
all_sprites.add(player)
active_sprites.add(player)
wall_list = pygame.sprite.Group()

game_control.level_list = [Main_menu(), Level_01(), Level_02()]
game_control.change_level()

