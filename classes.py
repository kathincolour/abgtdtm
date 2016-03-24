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


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.image_left = pygame.image.load("assets/protagonist_spr.png").convert_alpha()
        self.image_right = pygame.transform.flip(self.image_left, True, False)
        self.image = self.image_left # set the default sprite image to left

        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

        self.change_x = 0
        self.change_y = 0

        # variables related to gameplay
        lives = 4
        invincibility = False


    def change_speed(self, x, y):
        self.change_x += x
        self.change_y += y

    def update(self):

        # calculate gravity
        self.calc_gravity()

        # move left or right
        self.rect.x += self.change_x

        # check for  collision
        block_hit_list = pygame.sprite.spritecollide(self, all_static_sprites, False)
        for entity in block_hit_list:
            if self.change_x > 0:  # player is moving right because it is positive
                self.rect.right = entity.rect.left  # Change player right side to equal object left side
            else:  # player is moving left
                self.rect.left = entity.rect.right

        # move up or down
        self.rect.y += self.change_y

        block_hit_list = pygame.sprite.spritecollide(self, all_static_sprites, False)
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
        platform_hit_list = pygame.sprite.spritecollide(self, current_level.platforms, False)
        self.rect.y -= 2

        # If it is ok to jump, set our speed upwards
        if len(platform_hit_list) > 0 or self.rect.bottom >= SCREENHEIGHT:
            self.change_y = -6

    def go_left(self):
        # Called when the user hits the left arrow.
        self.image = self.image_left # flip the sprite image to the original if turning left
        self.change_x = -0.5

    def go_right(self):
        # Called when the user hits the right arrow.
        self.image = self.image_right # flip sprite image
        self.change_x = 1

    def stop(self):
        # Called when the user lets off the keyboard.
        self.change_x = 0


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


class Platform(pygame.sprite.Sprite):
    def __init__(self, width, height):
        self.image = pygame.Surface([width, height])
        self.image.fill(PURPLE) # maybe have a level specific colour/graphic here

        self.rect = self.image.get_rect()

        pygame.sprite.Sprite.__init__(self)


class Level:
    """ super class used to define each level """

    def __init__(self):
        self.platforms = pygame.sprite.Group()  # group containing the platform objects of the level
        self.enemies = pygame.sprite.Group()  # group containing the enemies of the level
        self.power_ups = pygame.sprite.Group()  # group containing the power ups of the level
        self.time_enabled = False  # is this level timed
        self.level_height = 3  # meaning 3 screen shifts therefore SCREENHEIGHT * 3 = maximum height = 1800
        self.current_height = 0 # keeps track of current height in level
        self.level_sprites = []


    def update_level(self):
        """ Update everything in this level."""
        self.platforms.update()

    def draw(self, screen):  # draw everything on the level

        # draw the sprites
        self.platforms.draw(screen)

    def move_level(self):  # Check if player has reached edge of top screen

        if player.rect.top <= 1:
            self.current_height += 1
            if self.current_height == self.level_height:
                self.new_level()
            else:
                for platform in self.platforms:
                    if platform.rect.top > 0:
                        platform.kill()
                    else:
                        if platform.rect.top <= -1200:
                            platform.rect.top += SCREENHEIGHT * 2
                        else:
                            platform.rect.top += SCREENHEIGHT
            player.rect.bottom = SCREENHEIGHT
                # insert enemy move and power up move

    def new_level(self):
        print('Level complete')
        # save game
        # level number + 1
        # generate new level


class Level_01(Level):
    def __init__(self):
        # Call the parent constructor
        Level.__init__(self)

        # array of platforms to be drawn- width, height, x, y
        # x must be greater than (or equal to) INNERSCREENX and less than 500
        # y must be less than 600 (SCREENHEIGHT) and less than max screen height of level i.e. -1800
        level = [[170, 40, 350, 430], [150, 40, INNERSCREENX, 300], [100, 40, INNERSCREENX + 230, 190],
                 [150, 40, INNERSCREENX + 120, -150],[150, 40, INNERSCREENX + 350, -200],
                 [150, 30, INNERSCREENX + 100, - 350], [150, 40, INNERSCREENX + 200, -500],
                 [150, 40, INNERSCREENX + 100, -1350], [150, 40, INNERSCREENX + 350, -1500],
                 [150, 40, INNERSCREENX + 200, -1650]]

        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            self.platforms.add(block)
            all_static_sprites.add(block)


# create all sprite groups and player instance
all_sprites = pygame.sprite.Group()
all_static_sprites = pygame.sprite.Group()  # Sprites that don't move (walls and platforms)
player = Player(500, (SCREENHEIGHT + 10))
all_sprites.add(player)
wall_list = pygame.sprite.Group()

# create all the levels and add to a list
level_list = [Level_01()]

current_level_no = 0 # denotes level number (Default for now is 0 for the first level- menu screen will be 0)
current_level = level_list[current_level_no]
