import pygame, random, os, math

import constant
from constant import loadMapFile, blockid
from color import *

class velocity(object):
    def __init__(self):
        self.x = 0
        self.y = 0

class stats(object):
    def __init__(self, maxHealth, health, damage, xp):
        self.health = 100
        self.maxHealth = 100
        self.xp = 0
        self.damage = 5
        self.armor = 0
        self.deaths = 0
        self.speed = 4

class Entity(pygame.sprite.Sprite):
    # Constructor. Pass in the color of the block and it's dimensions
    def __init__(self, color, width, height, pos, maxHealth, name, ID):
        # Basic Sprite stuff
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        self.add(constant.entities)

        self.id = ID

        # Create an image of the block, and fill it with a color.
        # Note: This could also be an image loaded from the disk.
        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x and rect.y
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

        self.origin = self.image.get_rect()
        self.origin.x = pos[0]
        self.origin.y = pos[1]

        self.velocity = velocity()
        self.onGround = True
        self.gravity = 1

        self.name = name
        self.maxHealth = maxHealth
        self.health = maxHealth
        self.damage = 1
        self.armor = 0

        self.directionPicked = False

        self.do_personal_init()

        # Test
        print(self.name, "was created")

    def do_personal_init(self):
        print("This is just a method to overwrite!")


    def check_death(self):
        try:
            if self.health <= 0:
                pygame.sprite.Sprite.kill(self)
        except:
            if self.stats.health <= 0:
                self.stats.health = self.stats.maxHealth
                self.stats.deaths += 1
                self.rect.topleft = self.origin.topleft

    def handle_movement(self, time_passed):

        if not self.directionPicked:
            self.direction = random.randint(1, 100) #Randomly picking a direction
            self.moveNumber = 60 # Total Number of frames for one movement action
            self.moveInterval = random.randint(30, 55) # Number of frames to wait between moving

        if self.direction > 50 and self.moveNumber > self.moveInterval:
            self.velocity.x = -2
            self.directionPicked = True
            self.direction = 51
            self.moveNumber -= 1

        elif self.direction <= 50 and self.moveNumber > self.moveInterval:
            self.velocity.x = 2
            self.directionPicked = True
            self.direction = 49
            self.moveNumber -= 1

        elif self.moveNumber <= self.moveInterval and self.moveNumber > 0:
            self.moveNumber -= 1

        elif self.moveNumber <= 0:
            self.directionPicked = False


    def update(self):

        self.velocity.y += self.gravity
        self.rect.y += self.velocity.y

        for block in constant.blocks:
            if self.rect.colliderect(block.rect):
                if self.velocity.y > 0: # Moving down; Hit the top side of the block
                    self.rect.bottom = block.rect.top
                    self.velocity.y = 0
                    self.onGround = True
                elif self.velocity.y < 0: # Moving up; Hit the bottom side of the block
                    self.rect.top = block.rect.bottom
                    self.velocity.y = 0


        self.rect.x += self.velocity.x

        for block in constant.blocks:
            if self.rect.colliderect(block.rect):
                if self.velocity.x > 0: # Moving right; Hit the left side of the block
                    self.rect.right = block.rect.left
                    self.velocity.x = 0
                elif self.velocity.x < 0: # Moving left; Hit the right side of the block
                    self.rect.left = block.rect.right
                    self.velocity.x = 0

class Player(Entity):
    # Constructor. Pass in the color of the block and it's dimensions
    def __init__(self, color, width, height, pos, maxHealth, name, ID):
        # Basic Sprite stuff
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        self.add(constant.entities)
        self.add(constant.player)

        self.name = name
        self.id = ID

        # Create an image of the block, and fill it with a color.
        # Note: This could also be an image loaded from the disk.
        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x and rect.y
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

        self.origin = self.image.get_rect()
        self.origin.x = pos[0]
        self.origin.y = pos[1]

        self.stats = stats(maxHealth, maxHealth, 0, 0)
        self.velocity = velocity()
        self.onGround = True

        self.gravity = 1
        self.canJump = True
        self.ableToDJ = True
        self.doubleJump = True

        self.hitTimer = 0
        self.maxHitTimer = self.hitTimer

        self.effects = []
        self.validEffects = ["none", "regen", "fireTick"]

        self.HUD = HUD(self)

        # Test
        print(self.name, "was created")



    #Currently not used/implemented
    def check_status(self):
        for status in self.statuses:
            if status in self.validStatuses:
                if status == "regen":
                    self.health += 1
                elif status == "fireTick":
                    self.health -= 1
                else:
                    print("Error in Player.check_status")

    def start_jump(self):
        self.velocity.y = -1 * (4 * self.stats.speed)
        self.onGround = False
        if self.ableToDJ:
            self.doubleJump = True
        else:
            self.doubleJump = False

    def double_jump(self):
        self.velocity.y = -1 * (4 * self.stats.speed)
        self.doubleJump = False

    def handle_movement(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            self.velocity.x = -1 * self.stats.speed
        if key[pygame.K_RIGHT]:
            self.velocity.x = self.stats.speed
        if key[pygame.K_UP] and not self.onGround and self.doubleJump and self.velocity.y >= -2:
            self.double_jump()
        if key[pygame.K_UP] and self.onGround:
            self.start_jump()


        if not key[pygame.K_LEFT] and not key[pygame.K_RIGHT]:
            self.velocity.x = 0

    def update(self, time_passed):

        if self.velocity.y > 20:
            self.velocity.y = 20

        self.velocity.y += self.gravity
        self.rect.y += self.velocity.y

        for block in constant.blocks:
            if self.rect.colliderect(block.rect):
                if self.velocity.y > 0: # Moving down; Hit the top side of the block
                    self.rect.bottom = block.rect.top
                    self.velocity.y = 0
                    self.onGround = True
                elif self.velocity.y < 0: # Moving up; Hit the bottom side of the block
                    self.rect.top = block.rect.bottom
                    self.velocity.y = 0

                block.do_effects(self)

                if self.stats.health > self.stats.maxHealth:
                    self.stats.health = self.stats.maxHealth

        for monster in constant.monsters: # Hit a monster
            if self.rect.colliderect(monster.rect):
                if self.hitTimer <= 0:
                    self.stats.health -= monster.damage
                monster.health -= self.stats.damage
                if self.velocity.y > 0: # Moving down; Hit the top side of the monster
                    self.rect.bottom = monster.rect.top
                    self.velocity.y = 0
                    self.onGround = True
                elif self.velocity.y < 0: # Moving up; Hit the bottom side of the monster
                    self.rect.top = monster.rect.bottom
                    self.velocity.y = 0

        self.rect.x += self.velocity.x

        for block in constant.blocks:
            if self.rect.colliderect(block.rect):
                if self.velocity.x > 0: # Moving right; Hit the left side of the block
                    self.rect.right = block.rect.left
                    self.velocity.x = 0
                elif self.velocity.x < 0: # Moving left; Hit the right side of the block
                    self.rect.left = block.rect.right
                    self.velocity.x = 0

                block.do_effects(self)

                if self.stats.health > self.stats.maxHealth:
                    self.stats.health = self.stats.maxHealth

        for monster in constant.monsters: # Hit a monster
            if self.rect.colliderect(monster.rect):
                if self.hitTimer <= 0:
                    self.stats.health -= monster.damage
                monster.health -= self.stats.damage
                if self.velocity.x > 0: # Moving right; Hit the left side of the monster
                    self.rect.right = monster.rect.left
                    self.velocity.x = 0
                elif self.velocity.x < 0: # Moving left; Hit the right side of the monster
                    self.rect.left = monster.rect.right
                    self.velocity.x = 0

        if self.hitTimer > 0:
            self.hitTimer -= 1
        else:
            self.hitTimer = self.maxHitTimer

class Monster(Entity):
    def do_personal_init(self):
        self.add(constant.monsters)
        self.drops = ""
        self.damage = 1

    def check_death(self):
        if self.health <= 0:
            self.kill()
            for player in constant.player:
                player.stats.xp += 1
            self.print_death_log()

    def print_death_log(self):
        print("This is just a method to overwrite!")


class Square(Monster):
    def print_death_log(self):
        print(self.name, "is dead")

#----------------------------------HUD--------------------------------------

class HUD(object):
    def __init__(self, player, width=160, height=32):
        self.components = pygame.sprite.Group()

        self.backgroundImage = pygame.image.load("Images" + os.sep + "hud" + os.sep + "hud.png")
        self.image = pygame.Surface([width, height])
        self.image.fill(colors["white"])
        self.rect = self.image.get_rect()
        self.image.blit(self.backgroundImage, self.rect)

        self.health = Health(self, player)

        print("HUD Init")

    def update_components(self):
        for component in self.components:
            component.update()

    def draw_components(self):
        self.image.fill(colors["white"])
        self.image.blit(self.backgroundImage, self.rect)
        for component in self.components:
            component.draw(self.image)

    def draw(self, screen):
        self.draw_components()
        screen.blit(self.image, self.rect)



    def update(self):
        self.update_components()

class Health(pygame.sprite.Sprite):
    def __init__(self, HUD, player):
        pygame.sprite.Sprite.__init__(self)
        self.add(HUD.components)

        self.font = pygame.font.Font(None, 15)

        self.health = player.stats.health
        self.maxHealth = player.stats.maxHealth
        self.healthAmt = 0

        self.image = pygame.Surface([self.maxHealth, 12])
        self.image.fill(colors["health"])
        self.rect = self.image.get_rect(topleft=(45, 14))

        self.healthString = "Hit Points:" + str(self.health)
        self.healthLabel = self.font.render(self.healthString, 20, colors["health"]) # Render the surface

        self.hearts = pygame.sprite.Group()
        self.heart = {}

        self.player = next(iter(constant.player))

        self.heartIterator = 1

    def update(self):
        for player in constant.player:
            self.healthAmt = player.stats.health
            if self.health == self.healthAmt:
                pass
            else:
                self.health = self.healthAmt
                # Render the red bar and find its rect
                self.image = pygame.Surface([self.health, 12])
                self.image.fill(colors["health"])
                self.rect = self.image.get_rect()
                self.rect.topleft = (45, 14)

                print(self.rect.width, self.health)

                # Render the label
                self.healthString = "Hit Points:" + str(self.health)
                self.healthLabel = self.font.render(self.healthString, 20, colors["health"]) # Render the surface

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        screen.blit(self.healthLabel, (59, 2))