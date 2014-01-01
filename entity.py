import random

import pygame

import constant


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

        self.gravity = True

        self.name = name
        self.maxHealth = maxHealth
        self.health = maxHealth
        self.damage = 1
        self.armor = 0

        self.doPersonalInit()


        # Test
        print(self.name, "was created")

    def doPersonalInit(self):
        print("This is just a method to overwrite!")


    def checkDeath(self):
        if self.health <= 0:
            pygame.sprite.Sprite.kill()

    def handleMovement(self):
        #Randomly picking a dirction
        direction = random.randint(1, 10000)
        if direction <= 5000:
            self.move(-2, 0)
        elif direction >= 6:
            self.move(2, 0)
        if self.gravity:
            self.move(0, 6)

    def move(self, dx, dy):
        # Move each axis separately. Note that this checks for collisions both times.
        if dx != 0:
            self.move_x(dx)
        if dy != 0:
            self.move_y(dy)

    def move_x(self, dx):

        # Move the rect
        self.rect.x += dx

        # If you collide with a block, reset the position to the edge of the block
        for block in constant.blocks:
            if self.rect.colliderect(block.rect):
                if dx > 0: # Moving right; Hit the left side of the block
                    self.rect.right = block.rect.left
                elif dx < 0: # Moving left; Hit the right side of the block
                    self.rect.left = block.rect.right


    def move_y(self, dy):

        # Move the rect
        self.rect.y += dy

        # If you collide with a block, reset the position to the edge of the block
        for block in constant.blocks:
            if self.rect.colliderect(block.rect):
                if dy > 0: # Moving down; Hit the left side of the block
                    self.rect.bottom = block.rect.top
                elif dy < 0: # Moving up; Hit the right side of the block
                    self.rect.top = block.rect.bottom


class Player(Entity):
    def doPersonalInit(self):
        self.add(constant.player)
        self.xp = 0
        self.gravity = True
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


    def handleMovement(self):
        #Capturing and Responding to Keys
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            self.move(-2, 0)
        if key[pygame.K_RIGHT]:
            self.move(2, 0)
        if key[pygame.K_UP]:
            self.move(0, -6)
        if key[pygame.K_DOWN]:
            self.move(0, 2)

        if self.gravity:
            self.move(0, 6)
        if key[pygame.K_UP] and self.gravity:
            self.move(0, -6)

    def move_y(self, dy):

        # Move the rect
        self.rect.y += dy

        # If you collide with a block, reset the position to the edge of the block
        for block in constant.blocks:
            if self.rect.colliderect(block.rect):
                if dy > 0: # Moving down; Hit the left side of the block
                    self.rect.bottom = block.rect.top
                elif dy < 0: # Moving up; Hit the right side of the block
                    self.rect.top = block.rect.bottom

        for monster in constant.monsters: # Hit a monster
            if self.rect.colliderect(monster.rect):
                self.health = self.health - monster.damage
                monster.health = monster.health - self.damage
                if dy > 0: # Moving down; Hit the left side of the monster
                    self.rect.bottom = monster.rect.top
                elif dy < 0: # Moving up; Hit the right side of the monster
                    self.rect.top = monster.rect.bottom

    def move_x(self, dx):

        # Move the rect
        self.rect.x += dx

        # If you collide with a block, reset the position to the edge of the block
        for block in constant.blocks:
            if self.rect.colliderect(block.rect):
                if dx > 0: # Moving right; Hit the left side of the block
                    self.rect.right = block.rect.left
                elif dx < 0: # Moving left; Hit the right side of the block
                    self.rect.left = block.rect.right

        for monster in constant.monsters: # Hit a monster
            if self.rect.colliderect(monster.rect):
                self.health = self.health - monster.damage
                monster.health = monster.health - self.damage
                if dx > 0: # Moving right; Hit the left side of the monster
                    self.rect.right = monster.rect.left
                elif dx < 0: # Moving left; Hit the right side of the monster
                    self.rect.left = monster.rect.right

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
