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

clock = pygame.time.Clock()


class Game_control:
    def __init__(self):
        self.done = False
        self.current_level_no = 0
        self.level_list = []
        self.current_level = None

    def change_level(self):
        self.current_level = self.level_list[self.current_level_no]


game_control = Game_control()


class Screen_element(pygame.sprite.Sprite):  # sprite class for visible objects on the side of the screen e.g. lives
    def __init__(self, name, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("assets/" + name + "_spr.png").convert_alpha()

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.bottom = y


class Help_Text(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([130, 50])
        self.image.fill(LLBLUE)  # maybe have a level specific colour/graphic here

        self.rect = self.image.get_rect()
        self.rect.x = 3
        self.rect.y = 270
        self.texts = ['Remember to collect power-ups', 'The moon is watching', 'Each level brings you closer']
        self.text = random.choice(self.texts)

        self.font2 = pygame.font.Font(None, 20)
        if len(self.text) > 16:
            self.text1 = self.text[0:17]
            self.text2 = self.text[17:]

        else:
            self.text1 = self.text
            self.text2 = 'null'

    def draw_text(self, screen):
        if self.text2 != 'null':
            help_1 = self.font2.render(self.text1, 0, BLACK)
            help_2 = self.font2.render(self.text2, 0, BLACK)

            screen.blit(help_1, (3, self.rect.y + 5))
            screen.blit(help_2, (3, self.rect.y + 15))
        else:
            help_1 = self.font2.render(self.text1, 0, BLACK)
            screen.blit(help_1, (3, 455))


heart1 = Screen_element('test', 660, 50)
heart2 = Screen_element('test', (heart1.rect.x + heart1.rect.width + 10), 50)
heart3 = Screen_element('test', (heart2.rect.x + heart2.rect.width + 10), 50)
heart4 = Screen_element('test', (heart3.rect.x + heart3.rect.width + 10), 50)
hearts = pygame.sprite.Group()
hearts.add(heart1)
hearts.add(heart2)
hearts.add(heart3)
hearts.add(heart4)

goddess = Screen_element('goddess', 3, 500)
goddess_group = pygame.sprite.GroupSingle()
goddess_group.add(goddess)


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.load_text = True
        self.time_of_init = pygame.time.get_ticks()

        self.image_left = pygame.image.load("assets/protagonist_spr.png").convert_alpha()
        self.image_right = pygame.transform.flip(self.image_left, True, False)
        # image of player when hurt by enemy
        self.hurt_left = pygame.image.load("assets/protagonist_hurt1_spr.png").convert_alpha()
        self.hurt_right = pygame.transform.flip(self.hurt_left, True, False)
        # image of player when invincibility = true
        self.invincible = pygame.image.load("assets/protagonist_powerup_spr.png").convert_alpha()
        self.invincible_right = pygame.transform.flip(self.invincible, True, False)
        self.image = self.image_left  # set the default sprite image to left

        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

        self.change_x = 0
        self.change_y = 0

        # variables related to gameplay
        self.lives = 4
        self.invincibility = False
        self.tock = 0
        self.time = 0

    def update(self):

        if pygame.time.get_ticks() > game_control.level_list[0].time_load + 17000: # pause player movement for an amount of time after starting game to stop platform rendering bug
            if pygame.time.get_ticks() > game_control.current_level.load_time + 5000 and game_control.current_level_no == 1:
                if 140 > self.rect.x > 615:
                    self.rect.x = 150
                # calculate gravity
                self.calc_gravity()

                # move left or right
                self.rect.x += self.change_x

                if self.invincibility and self.tock < 1200:
                    self.tock += 1
                    # print('tock')
                else:
                    self.invincibility = False

                # check for collision with walls
                wall_hit_list = pygame.sprite.spritecollide(self, wall_list, False)
                for wall in wall_hit_list:
                    if self.change_x > 0:  # player is moving right because it is positive
                        self.rect.right = wall.rect.left  # Change player right side to equal object left side
                    else:  # player is moving left
                        self.rect.left = wall.rect.right

                # check for collision with platform
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
                        # print('invincible')
                        self.image = self.invincible
                    elif pu.number == '2':
                        self.lives += 1
                        self.add_hearts()
                    pu.sound.play()
                    pu.kill()

                # check for collision with enemy
                enemy_hit_list = pygame.sprite.spritecollide(self, game_control.current_level.enemies, False)
                for enemy in enemy_hit_list:
                    if not self.invincibility and (pygame.time.get_ticks() - self.time) > 700:
                        # make sure player doesn't die straight away b checking how much time has passed.
                        self.lives -= 1

                        # play sound
                        enemy.sound.play()

                        if self.change_x > 0:  # player is moving right because it is positive
                            self.image = self.hurt_right  # change player image to 'hurt' sprite
                            self.rect.right = enemy.rect.left  # Change player right side to equal object left side
                            self.rect.x -= 5
                        elif self.change_x < 0:  # player is moving left
                            self.image = self.hurt_left
                            self.rect.left = enemy.rect.right  # change player left side to equal object right side
                            self.rect.x += 5
                        elif self.change_y > 0:  # player is moving downwards
                            self.image = self.hurt_left
                            self.rect.bottom = enemy.rect.top
                        self.remove_hearts()
                        self.check_health()
                        self.time = pygame.time.get_ticks()


                    else:  # invincibility is on and player doesn't lose health
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
            self.image = self.invincible  # change to the invincible sprite look
        else:
            self.image = self.image_left  # flip the sprite image to the original if turning left
        self.change_x = -0.5

    def go_right(self):
        # Called when the user hits the right arrow.
        if self.invincibility:
            self.image = self.invincible_right  # change to the invincible sprite look
        else:
            self.image = self.image_right  # flip sprite image
        self.change_x = 1

    def stop(self):
        # Called when the user lets off the keyboard.
        self.change_x = 0

    def add_hearts(self):
        if self.lives == 4:
            hearts.add(heart4)
        elif self.lives == 3:
            hearts.add(heart3)
        elif self.lives == 2:
            hearts.add(heart2)

    def remove_hearts(self):
        if self.lives == 3:
            hearts.remove(heart4)
        elif self.lives == 2:
            hearts.remove(heart3)
        elif self.lives == 1:
            hearts.remove(heart2)
        elif self.lives == 0:
            hearts.remove(heart1)

    def check_health(self):
        if self.lives <= 0:
            # restart level
            self.death()

    def death(self):
        # when player lives = 0
        self.lives = 4
        pygame.time.delay(1000)  # wait a second to let user adjust
        # add back lives
        hearts.add(heart1)
        hearts.add(heart2)
        hearts.add(heart3)
        hearts.add(heart4)
        game_control.current_level.restart_level()  # create new fresh instance of the level
        # position player back at start
        self.rect.x = 500
        self.rect.y = SCREENHEIGHT + 10


class Enemy(pygame.sprite.Sprite):
    def __init__(self, enem, x, y, speed):
        """
        :param enem: name of sprite file without _spr
        :param speed: how much the enemy moves each frame
        """
        pygame.sprite.Sprite.__init__(self)

        self.time_since_last_flip = pygame.time.get_ticks()
        self.image_left = pygame.image.load("assets/enemy1_spr.png").convert_alpha()
        self.image_right = pygame.transform.flip(self.image_left, True, False)
        self.image = self.image_left  # set the default sprite image to left

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.bottom = y

        self.sound = pygame.mixer.Sound('assets/music/hurt.wav')
        self.volume = self.sound.get_volume()
        self.sound.set_volume((self.volume - 0.5))

        self.direction = -1  # 1 denotes a rightward motion, whilst -1 denotes left
        self.speed = speed

    def update(self):

        self.gravity()

        '''platform_hit_list = pygame.sprite.spritecollide(self, game_control.current_level.platforms, False)
        for platform in platform_hit_list:
            self.rect.x += self.speed * self.direction
            print(str(self.rect.x))
            print(str(self.direction))
            #print(str(self.rect.x))
            #if platform.rect.left <= self.rect.left <= (platform.rect.left + 5):
            index_rect = self.rect.collidelist(game_control.current_level.platform_rects)
            if not game_control.current_level.platform_rects[index_rect].contains(self.rect):
                    print('yes')
                    self.flip()
                    self.time_since_last_flip = pygame.time.get_ticks()
            elif platform.rect.right <= self.rect.right <= (platform.rect.right + 5):
                if pygame.time.get_ticks() >= self.time_since_last_flip + 1000:
                    self.flip()
                    self.time_since_last_flip = pygame.time.get_ticks() '''

    def gravity(self):
        if self.rect.y > 0:
            platform_hit_list = pygame.sprite.spritecollide(self, game_control.current_level.platforms, False)
            while len(platform_hit_list) == 0 and not self.rect.bottom == 599:
                self.rect.y += 1
                platform_hit_list = pygame.sprite.spritecollide(self, game_control.current_level.platforms, False)

    def flip(self):
        if self.direction == 1:  # going right
            self.image = self.image_left
            self.direction = -1  # change to going left
        elif self.direction == -1:
            self.image = self.image_right
            self.direction = 1


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

        self.sound = pygame.mixer.Sound('assets/music/powerup.wav')
        self.volume = self.sound.get_volume()
        self.sound.set_volume((self.volume - 0.1))

        self.number = no[7]  # denotes the type of power up- to be used by the player class when interacting


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

        if file != 'main':
            self.rect.x = INNERSCREENX
            self.rect.bottom = SCREENHEIGHT


class Selector(pygame.sprite.Sprite):  # class for button selector- shows which button is currently selected
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('assets/powerup2_spr.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = center

    def move_down(self):
        self.rect.y += 70

    def move_up(self):
        self.rect.y -= 70


class Button(pygame.sprite.Sprite):
    def __init__(self, txt, x, y, w, h, func):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([w, h])
        self.image.fill(LBLUE)
        self.highlight = LLBLUE

        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.y = y

        self.func = func

        self.button_font = pygame.font.Font(None, 30)
        self.button_text = self.button_font.render(txt, 0, WHITE)
        self.txtpos = self.button_text.get_rect()
        self.txtpos.center = self.rect.center


class Main_menu:
    """ main menu class """

    def __init__(self):

        self.time_load = None
        self.buttons = []  # group for buttons to be added
        self.selectors = pygame.sprite.Group()
        self.buttons_sprite = pygame.sprite.Group()  # sprite group for buttons so they can be drawn
        self.backgrounds = pygame.sprite.Group()
        self.background_1 = Background('1')
        self.background_2 = Background('main')
        self.background = random.choice(
                [self.background_1, self.background_2])  # chooses between 2 different backgrounds to draw
        self.backgrounds.add(self.background_2)
        self.soundtrack = 'assets/music/god.ogg'

        self.target = 0

        self.main_font = pygame.font.Font('assets/font1.ttf', 45)
        self.title_text = self.main_font.render('A Beginner\'s guide to', 0, WHITE)
        self.title_text1 = self.main_font.render('Destroying the Moon', 0, WHITE)

        # create buttons and add to both arrays
        self.n_game_button = Button('New Game', 400, 220, 300, 60, 'new')
        self.buttons.append(self.n_game_button)
        self.buttons_sprite.add(self.n_game_button)
        self.c_game_button = Button('Continue Game', 400, 290, 300, 60, 'cont')
        self.buttons.append(self.c_game_button)
        self.buttons_sprite.add(self.c_game_button)
        self.help_button = Button('Help', 400, 360, 300, 60, 'help')
        self.buttons.append(self.help_button)
        self.buttons_sprite.add(self.help_button)
        self.options_button = Button('Options', 400, 430, 300, 60, 'opt')
        self.buttons.append(self.options_button)
        self.buttons_sprite.add(self.options_button)
        self.quit_button = Button('Quit', 400, 500, 300, 60, 'quit')
        self.buttons.append(self.quit_button)
        self.buttons_sprite.add(self.quit_button)

        self.plain_font = pygame.font.Font(None, 30)
        self.howto_text = self.plain_font.render('Use the up/down arrow keys, and the enter key to select', 0, WHITE)

        self.selector = Selector((520, 250))
        self.selectors.add(self.selector)

        # help screen code
        self.to_help = False
        self.help_screen = pygame.Surface((700, 500))
        self.help_screen.fill(BLUE)

        self.help_rect = self.help_screen.get_rect()

        self.close_button = Button('Press space to Close',self.help_rect.centerx, self.help_rect.centery + 200, 250, 40, 'close')
        self.closeButton = pygame.sprite.GroupSingle() # single sprite group for button above
        self.closeButton.add(self.close_button)

        self.text1 = self.plain_font.render('Use the arrow keys to move around the level.', 0, WHITE)
        self.text2 = self.plain_font.render('Press the up arrow key to jump. Avoid Enemies.', 0, WHITE)
        self.text3 = self.plain_font.render('Your aim is to climb and collect power ups', 0, WHITE)
        self.text4 = self.plain_font.render('Power ups give you special abilities or extra lives', 0, WHITE)
        self.text5 = self.plain_font.render('Your lives are shown through the amount of hearts on the right', 0, WHITE)
        self.text5_2 = self.plain_font.render('of the screen', 0, WHITE)
        self.text6 = self.plain_font.render('Once you run out of lives you have to start the level again', 0, WHITE)
        self.text7 = self.plain_font.render('The Moon goddess will follow you and give you tips throughout', 0, WHITE)

    def draw(self, screen):
        self.backgrounds.draw(screen)
        self.buttons_sprite.draw(screen)
        screen.blit(self.title_text, (170, 100))
        screen.blit(self.title_text1, (200, 150))
        for button in self.buttons:
            screen.blit(button.button_text, button.txtpos)
        self.selectors.draw(screen)
        screen.blit(self.howto_text, (120 , 570))

        if self.to_help:
            screen.blit(self.help_screen, (50, 50))
            self.closeButton.draw(screen)
            screen.blit(self.closeButton.sprite.button_text, self.closeButton.sprite.txtpos)
            screen.blit(self.text1, (100, 80))
            screen.blit(self.text2, (100, 115))
            screen.blit(self.text3, (100, 160))
            screen.blit(self.text4, (100, 210))
            screen.blit(self.text5, (100, 250))
            screen.blit(self.text5_2, (100, 270))
            screen.blit(self.text6, (100, 300))
            screen.blit(self.text7, (100, 340))

    def target_button(self):
        if self.target <= 4 or self.target >= 0:
            current_button = self.buttons[self.target]
            # current_button.image.fill(LBLUE)

    def target_up(self):  # called when user pressed up key
        # print('up key')
        if self.target > 0:
            # print('move up')
            self.target -= 1
            # print(str(self.target))
            self.selector.move_up()

    def target_down(self):
        # print('down key')
        if self.target < 4:
            # print('move down')
            self.target += 1
            # print(str(self.target))
            self.selector.move_down()

    def select(self):
        current_button = self.buttons[self.target]

        if current_button.func == 'new':
            self.new_game()
        elif current_button.func == 'cont':
            self.continue_game()
        elif current_button.func == 'help':
            self.g_help()
        elif current_button.func == 'opt':
            self.options()
        elif current_button.func == 'quit':
            game_control.done = True
            game_control.current_level_no = -1

    def new_game(self):
        print('warning message')
        open('save_file.txt', 'w').close()  # empty save file

        self.time_load = pygame.time.get_ticks()

        game_control.current_level_no = 1
        game_control.done = True

    def continue_game(self):
        if os.path.getsize('save_file.txt') > 0:  # if save file is not empty (could throw exception otherwise)
            with open('save_file.txt', 'r') as file:
                game_control.current_level_no = int(file.read())
        else:
            # print('yes')
            game_control.current_level_no = 1
        game_control.done = True

    def g_help(self):
        # new screen
        self.to_help = True
        print('wip')

    def options(self):
        # maybe not needed?
        print('wip_op')


class Level:
    """ super class used to define each level """

    def __init__(self):

        print(self)
        self.platforms = pygame.sprite.Group()  # group containing the platform objects of the level
        self.platform_rects = []  # array to store the second collision rects of the platforms
        self.enemies = pygame.sprite.Group()  # group containing the enemies of the level
        self.power_ups = pygame.sprite.Group()  # group containing the power ups of the level
        self.backgrounds = pygame.sprite.Group()  # create a sprite group for the background image so it is easier
        self.time_enabled = False  # is this level timed
        self.level_height = 3  # meaning 3 screen shifts therefore SCREENHEIGHT * 3 = maximum height = 1800
        self.current_height = 0  # keeps track of current height in level
        self.level_sprites = pygame.sprite.Group()  # sprite group containing all sprites in level
        self.texts = pygame.sprite.Group()  # to hold the help text etc
        self.help_text = Help_Text()

        self.level_font = pygame.font.Font('assets/font1.ttf', 30)
        self.level_text = None
        self.loading_text = basic_font.render('Loading', 10, WHITE)

        self.soundtrack = None  # pygame.mixer.music.load
        self.background = None

        self.load_time = 0

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
        self.texts.draw(screen)
        self.help_text.draw_text(screen)
        screen.blit(self.level_text, (5, 10))
        # draw loading text if needed
        if pygame.time.get_ticks() < game_control.level_list[0].time_load + 17000 and game_control.current_level_no == 1:
            screen.blit(self.loading_text, (450, 300))

    def restart_level(self):
        # called when player dies
        game_control.current_level = game_control.current_level.__class__()

    def move_level(self):  # Check if player has reached edge of top screen

        if player.rect.top <= 1:  # if player is near top of screen
            self.current_height += 1  # increment place in level
            if self.current_height == self.level_height:
                self.new_level()
            else:
                for platform in self.platforms:  # move platforms 'down' or kill if on screen
                    if platform.rect.top > 0:
                        platform.kill()
                        # print(str(platform.alive()))
                    else:
                        if platform.rect.top <= -1200:
                            platform.rect.top += SCREENHEIGHT * 2
                            print(str(platform.rect.x))
                        else:
                            platform.rect.top += SCREENHEIGHT
                            print(str(platform.rect.x))
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
                        if pu.rect.top <= -1200:
                            platform.rect.top += SCREENHEIGHT * 2
                        else:
                            platform.rect.top += SCREENHEIGHT

            self.load_time = pygame.time.get_ticks()

            player.rect.bottom = SCREENHEIGHT

    def new_level(self):
        # print('Level complete')
        # save game
        with open('save_file.txt', 'w') as savefile:  # access save file
            savefile.write(
                str(game_control.current_level_no + 1))  # save next level number (so player can start from new level)

        for sprite in self.level_sprites:
            sprite.kill()

        # display text saying level complete
        end_text = basic_font.render('Level ' + str(game_control.current_level_no + 1) + ' complete!', True, WHITE)
        game_screen.blit(end_text, [400, 300])
        game_control.current_level_no += 1  # level number + 1

        pygame.mixer.music.fadeout(750)
        game_control.change_level()
        pygame.mixer.music.load(game_control.current_level.soundtrack)
        pygame.mixer.music.play(-1)

    def platform_rect(self):
        for platform in self.platforms:
            second_rect = platform.image.get_rect()
            second_rect.bottom = platform.rect.top
            second_rect.height += 20
            self.platform_rects.append(second_rect)


class Level_01(Level):
    def __init__(self):
        # Call the parent constructor
        Level.__init__(self)

        self.background = pygame.image.load("assets/background_1.png")
        self.soundtrack = 'assets/music/mono.ogg'

        self.help_text = Help_Text()
        self.texts.add(self.help_text)

        self.level_text = self.level_font.render('Level 1', 0, WHITE)

        # array of platforms to be drawn- width, height, x, y
        # x must be greater than (or equal to) INNERSCREENX and less than 500
        # y must be less than 600 (SCREENHEIGHT) and less than max screen height of level i.e. -1800
        level_platforms = [[170, 40, 350, 430], [150, 40, INNERSCREENX, 300], [160, 40, INNERSCREENX + 230, 190],
                           [150, 40, INNERSCREENX + 120, -150], [150, 40, INNERSCREENX + 200, -200],
                           [150, 30, INNERSCREENX + 100, - 350], [150, 40, INNERSCREENX + 200, -500],
                           [150, 40, INNERSCREENX + 100, -1350], [150, 40, INNERSCREENX + 350, -1500],
                           [150, 40, INNERSCREENX + 200, -1650]]

        # array of enemies to be drawn- type of enemy (file name), x, y, speed
        # x & y should be on a platform or the ground - follow the level_platforms array
        level_enemies = [['test', 400, 430, 0.0001], ['test', 450, 190, 0.0001], ['test', 600, -10, 0.0001]]

        # array of power ups to be drawn- 'no' type should be string for file, x, y
        # can be drawn anywhere on screen (but not on top of platforms)
        level_power_ups = [['powerup1', INNERSCREENX + 100, 250], ['powerup1', 300, -400]]

        for platform in level_platforms:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            self.platforms.add(block)
            self.level_sprites.add(block)

        for enemy in level_enemies:
            entity = Enemy(enemy[0], enemy[1], enemy[2], enemy[3])
            # print(str(entity.rect.y))
            self.enemies.add(entity)
            self.level_sprites.add(entity)

        for power_up in level_power_ups:
            pu = Power_up(power_up[0], power_up[1], power_up[2])
            self.power_ups.add(pu)
            self.level_sprites.add(pu)

        self.platform_rect()
        level_background = Background('1')
        self.backgrounds.add(level_background)


class Level_02(Level):
    def __init__(self):
        # Call the parent constructor
        Level.__init__(self)

        self.background = None
        self.soundtrack = 'assets/music/god.ogg'
        self.help_text = Help_Text()
        self.texts.add(self.help_text)

        self.level_text = self.level_font.render('Level 2', 0, WHITE)

        # array of platforms to be drawn- width, height, x, y
        # x should be greater than (or equal to) INNERSCREENX and less than 500
        # y should be less than 600 (SCREENHEIGHT) and less than max screen height of level i.e. -1800
        level_platforms = [[155, 50, 170, 490], [190, 50, 420, 370], [100, 45, 215, 270], [160, 40, 420, 135],
                           [100, 50, 550, -150], [100, 50, 145, -125], [150, 50, 290, - 280], [100, 50, 400, -320], [200, 50, 150, - 480],
                           [100, 50, 360, -750], [90, 50, 180, - 900], [90, 50, 350, - 950], [90, 50, 500, -1050]]

        # array of enemies to be drawn- type of enemy (file name), x, y, speed
        # x & y should be on a platform or the ground - follow the level_platforms array
        level_enemies = []

        # array of power ups to be drawn- 'no' type should be string for file, x, y
        # can be drawn anywhere on screen (but not on top of platforms)
        level_power_ups = []

        for platform in level_platforms:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.image.fill(WHITE)
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

class Level_03(Level):
    def __init__(self):
        # Call the parent constructor
        Level.__init__(self)

        level_background = Background('2')
        self.backgrounds.add(level_background)
        self.soundtrack = 'assets/music/star.wav'
        self.help_text = Help_Text()
        self.texts.add(self.help_text)

        self.level_text = self.level_font.render('Level 3', 0, WHITE)

        # array of platforms to be drawn- width, height, x, y
        # x should be greater than (or equal to) INNERSCREENX and less than 500
        # y should be less than 600 (SCREENHEIGHT) and less than max screen height of level i.e. -1800
        level_platforms = [[155, 50, 170, 490], [190, 50, 420, 370], [100, 45, 215, 270], [160, 40, 420, 135],
                           [100, 50, 550, -150], [100, 50, 145, -125], [150, 50, 290, - 280], [100, 50, 400, -320], [200, 50, 150, - 480],
                           [100, 50, 360, -750], [90, 50, 180, - 900], [90, 50, 350, - 950], [90, 50, 500, -1050]]

        # array of enemies to be drawn- type of enemy (file name), x, y, speed
        # x & y should be on a platform or the ground - follow the level_platforms array
        level_enemies = []

        # array of power ups to be drawn- 'no' type should be string for file, x, y
        # can be drawn anywhere on screen (but not on top of platforms)
        level_power_ups = []

        for platform in level_platforms:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.image.fill(LLBLUE)
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



# create all sprite groups and the player instance
all_sprites = pygame.sprite.Group()
all_static_sprites = pygame.sprite.Group()  # Sprites that don't move (walls and platforms)
active_sprites = pygame.sprite.Group()  # group for the player
player = Player(500, (SCREENHEIGHT + 10))
all_sprites.add(player)
active_sprites.add(player)
wall_list = pygame.sprite.Group()

game_control.level_list = [Main_menu(), Level_01(), Level_02(), Level_03()]
game_control.change_level()
