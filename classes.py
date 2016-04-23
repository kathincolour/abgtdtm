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
        self.hurt_left = pygame.image.load("assets/protagonist_hurt1_spr.png").convert_alpha() # image of player when hurt by enemy
        self.hurt_right = pygame.transform.flip(self.hurt_left, True, False)
        self.image = self.image_left # set the default sprite image to left

        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

        self.change_x = 0
        self.change_y = 0

        # variables related to gameplay
        self.lives = 4
        self.invincibility = True


    #def change_speed(self, x, y):
        #self.change_x += x
        #self.change_y += y

    def update(self):

        # calculate gravity
        self.calc_gravity()

        # move left or right
        self.rect.x += self.change_x


        # check for collision with platform or wall
        block_hit_list = pygame.sprite.spritecollide(self, all_static_sprites, False)
        for entity in block_hit_list:
            if self.change_x > 0:  # player is moving right because it is positive
                self.rect.right = entity.rect.left  # Change player right side to equal object left side
            else:  # player is moving left
                self.rect.left = entity.rect.right

        # check for collision with enemy
        enemy_hit_list = pygame.sprite.spritecollide(self, current_level.enemies, False)
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

    def check_health(self):
        if self.lives <= 0:
            # restart level
            print('death')


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

        platform_hit = pygame.sprite.spritecollide(self, current_level.platforms, False)
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


class Platform(pygame.sprite.Sprite):
    def __init__(self, width, height):
        self.image = pygame.Surface([width, height])
        self.image.fill(PURPLE) # maybe have a level specific colour/graphic here

        self.rect = self.image.get_rect()

        pygame.sprite.Sprite.__init__(self)

current_level_no = 0 # denotes level number (Default for now is 0 for the first level- menu screen will be 0)

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

        self.soundtrack = None  # pygame.mixer.music.load
        self.background = None
        #self.background.rect = self.background.get_rect()

    def update_level(self):
        """ Update everything in this level."""
        self.platforms.update()
        self.enemies.update()

    def draw(self, screen):  # draw everything on the level


        # draw the sprites
        self.platforms.draw(screen)
        self.enemies.draw(screen)

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
        with open('save_file', 'w') as savefile: # access save file
            global current_level_no
            savefile.write(str(current_level_no)) # save level number

        current_level_no += 1  # level number + 1
        # display text saying level complete
        end_text = font.render('Level ' + str(current_level_no + 1) + ' complete!', True, WHITE)
        game_screen.blit(end_text, [400, 300])


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

        for platform in level_platforms:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            self.platforms.add(block)
            all_static_sprites.add(block)

        for enemy in level_enemies:
            entity = Enemy(enemy[0], enemy[1], enemy[2], enemy[3])
            self.enemies.add(entity)



# create all sprite groups and player instance
all_sprites = pygame.sprite.Group()
all_static_sprites = pygame.sprite.Group()  # Sprites that don't move (walls and platforms)
active_sprites = pygame.sprite.Group() # group for the player
player = Player(500, (SCREENHEIGHT + 10))
all_sprites.add(player)
active_sprites.add(player)
wall_list = pygame.sprite.Group()

# create all the levels and add to a list
level_list = [Level_01()]

current_level = level_list[current_level_no]
