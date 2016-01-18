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

        self.image = pygame.image.load("test_sprite.png").convert()

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
        # move left or right
        self.rect.x += self.change_x

        # check for wall collision
        object_hit_list = pygame.sprite.spritecollide(self, wall_list, False)
        for object in object_hit_list:
            if self.change_x > 0:  # player is moving right because it is positive
                self.rect.right = object.rect.left  # Change player right side to equal object left side
            else:  # player is moving left
                self.rect.left = object.rect.right

        # move up or down
        self.rect.y += self.change_y

        object_hit_list = pygame.sprite.spritecollide(self, wall_list, False)
        for object in object_hit_list:
            if self.change_y > 0:  # player is moving down because it is positive
                self.rect.bottom = object.rect.top  # Change player bottom side to equal object top side
            else:  # player is moving up
                self.rect.top = object.rect.bottom


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


class Level():
    """ super class used to define each level """

    def __init__(self):
        self.platforms = []  # array containing the platforms of the level
        self.enemies = []  # array containing the enemies of the level
        self.power_ups = []  # array containing the power ups of the level
        self.time_enabled = False  # is this level timed
        self.level_height = SCREENHEIGHT * 3  # temporary multiplier

    def move_level(self):  # Check if player has reached edge of top screen
        if player.rect.top <= SCREENHEIGHT - 2:
            # all_sprites.rect.top -=
            print('WIP')

    def new_level(self):
        if player.rect.top <= self.level_height - 3:
            print('Level complete')
            # save game
            # level number + 1
            # generate new level

wall_list = pygame.sprite.Group()
# create all sprite group and player instance
all_sprites = pygame.sprite.Group()
player = Player(500, 400)
all_sprites.add(player)