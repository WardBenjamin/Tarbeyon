import random

import pygame

import constant

class velocity(object):
    def __init__(self):
        self.x = 0
        self.y = 0


class Entity(pygame.sprite.Sprite):
    # Constructor. Pass in the color of the block and it's dimensions
    def __init__(self, color, width, height, pos, maxHealth, name):
        # Basic Sprite stuff
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        self.add(constant.entities)

        # Create an image of the block, and fill it with a color.
        # Note: This could also be an image loaded from the disk.
        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x and rect.y
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

        self.velocity = velocity()
        self.onGround = True
        self.gravity = 1

        self.name = name
        self.maxHealth = maxHealth
        self.health = maxHealth
        self.damage = 1
        self.armor = 0

        self.directionPicked = False

        self.doPersonalInit()


        # Test
        print(self.name, "was created")

    def doPersonalInit(self):
        print("This is just a method to overwrite!")


    def checkDeath(self):
        if self.health <= 0:
            pygame.sprite.Sprite.kill()

    def handleMovement(self):

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


    def Update(self):

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
    def doPersonalInit(self):
        self.add(constant.player)
        self.xp = 0
        self.gravity = 1
        self.canJump = True

        self.effects = []
        self.validEffects = ["none", "regen", "fireTick"]

    #Currently not used/implemented
    def updateState(self):
        for state in self.effects:
            if state in self.validEffects:
                if state == "regen":
                    self.health += 1
                elif state == "fireTick":
                    self.health -= 1
                else:
                    print("Error in Player.updateState")

    def StartJump(self):
        if self.onGround:
            self.velocity.y = -16
            self.onGround = False

    def EndJump(self):
        if self.velocity.y < -6:
            self.velocity.y = -6

    def handleMovement(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            self.velocity.x = -2
        if key[pygame.K_RIGHT]:
            self.velocity.x = 2
        if key[pygame.K_UP] and self.onGround:
            self.StartJump()

        if not key[pygame.K_LEFT] and not key[pygame.K_RIGHT]:
            self.velocity.x = 0

    def Update(self):

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

        for monster in constant.monsters: # Hit a monster
            if self.rect.colliderect(monster.rect):
                self.health = self.health - monster.damage
                monster.health = monster.health - self.damage
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

        for monster in constant.monsters: # Hit a monster
            if self.rect.colliderect(monster.rect):
                self.health = self.health - monster.damage
                monster.health = monster.health - self.damage
                if self.velocity.x > 0: # Moving right; Hit the left side of the monster
                    self.rect.right = monster.rect.left
                    self.velocity.x = 0
                elif self.velocity.x < 0: # Moving left; Hit the right side of the monster
                    self.rect.left = monster.rect.right
                    self.velocity.x = 0

class Monster(Entity):
    def doPersonalInit(self):
        self.add(constant.monsters)
        self.drops = ""

    def checkDeath(self):
        if self.health <= 0:
            self.kill()
            for player in constant.player:
                player.xp += 1
            self.deathLog()

    def deathLog(self):
        print("This is just a method to overwrite!")


class Square(Monster):
    def deathLog(self):
        print(self.name, "is dead")
