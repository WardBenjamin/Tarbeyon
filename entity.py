#Entity Script
import random
import pygame

from blocks import *

error = False

entities = []
monsters = []

class Entity(object):
    def __init__(self, pos, health, name):
        self.name = name
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.health = health

    def checkDeath(self):
        if self.health <= 0:
            self.rect = self.originalRect
            self.health = self.originalHealth


class Player(Entity):

    def __init__(self, pos, health, name, damage, armor):

        self.rect = pygame.Rect(pos[0], pos[1], 32, 32)
        self.originalRect = pygame.Rect(pos[0], pos[1], 32, 32) 
        entities.append(self)
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.originalHealth = health
        self.health = health
        self.armor = armor
        self.damage = damage
        self.xp = 0

        self.effects = []

        self.gravity = True
        self.canJump = True

        #Var Defintion
        self.xp = 0
        self.xpString = str(self.xp)
        self.attackDamage = 0
        self.attackDamageString = str(self.attackDamage)

        self.validEffects = ["none", "fireDamage", "regen"]

    
    #States
    #Currently not used/implemented
    def updateState(self):
        for state in self.effects:
            if state in self.validEffects:
                if state == "regen":
                    self.health += 1
                elif state == "fireDamage":
                    self.health -= 1
                else:
                    print("Error in Player.updateState")


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
        for block in blocks:
            if self.rect.colliderect(block.rect):
                if dx > 0: # Moving right; Hit the left side of the block
                    self.rect.right = block.rect.left

                elif dx < 0: # Moving left; Hit the right side of the block
                    self.rect.left = block.rect.right


        for monster in monsters:
            if self.rect.colliderect(monster.rect):
                self.health = self.health - monster.damage

        """for liquid in liquids:
            if self.rect.colliderect(liquid.rect):
                liquid.applyEffects()"""


    def move_y(self, dy):

        # Move the rect
        self.rect.y += dy


        # If you collide with a block, reset the position to the edge of the block
        for block in blocks:
            if self.rect.colliderect(block.rect):
                if dy > 0: # Moving down; Hit the top side of the block
                    self.rect.bottom = block.rect.top
                    self.canJump = True

                elif dy < 0: # Moving up; Hit the bottom side of the block
                    self.rect.top = block.rect.bottom

        for monster in monsters:
            if self.rect.colliderect(monster.rect):
                self.health = self.health - monster.damage

    def handleMovement(self):
        #Capturing and Responding to Keys
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            self.move(-2, 0)
        if key[pygame.K_RIGHT]:
            self.move(2, 0)
        if key[pygame.K_UP]:
            self.move(0, -2)
        if key[pygame.K_DOWN]:
            self.move(0, 2)

        if self.gravity:
            self.move(0, 2)
        if key[pygame.K_UP] and self.gravity:
            self.move(0, -2)




class Monster(Entity):

    def __init__(self, pos, health, xp, damage, armor, drops):
        entities.append(self)
        monsters.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], 32, 32)
        self.originalRect = pygame.Rect(pos[0], pos[1], 32, 32)
        self.health = health
        self.originalHealth = health
        self.xp = xp
        self.damage = damage
        self.armor = armor
        self.drops = drops

        self.gravity = True

    def isKilled(self):
        player.xp += self.xp
        monsters.remove(self)

    def handleMovement(self):
        #Randomly picking a dirction
        direction = random.randint(1, 2)
        if direction == 1:
            self.move(-2, 0)
        elif direction == 2:
            self.move(2, 0)

        if self.gravity:
            self.move(0, 2)

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
        for block in blocks:
            if self.rect.colliderect(block.rect):
                if dx > 0: # Moving right; Hit the left side of the block
                    self.rect.right = block.rect.left

                elif dx < 0: # Moving left; Hit the right side of the block
                    self.rect.left = block.rect.right


        for monster in monsters:
            if self.rect.colliderect(monster.rect):
                self.health = self.health - monster.damage

        """for liquid in liquids:
            if self.rect.colliderect(liquid.rect):
                liquid.applyEffects()"""


    def move_y(self, dy):

        # Move the rect
        self.rect.y += dy


        # If you collide with a block, reset the position to the edge of the block
        for block in blocks:
            if self.rect.colliderect(block.rect):
                if dy > 0: # Moving down; Hit the top side of the block
                    self.rect.bottom = block.rect.top
                    self.canJump = True

                elif dy < 0: # Moving up; Hit the bottom side of the block
                    self.rect.top = block.rect.bottom

        for monster in monsters:
            if self.rect.colliderect(monster.rect):
                self.health = self.health - monster.damage
        
        
class Square(Monster):

    def __init__(self, pos, health, xp, damage, armor, drops):
        monsters.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], 32, 32)
        self.health = health
        self.xp = xp
        self.damage = damage
        self.armor = armor
        self.drops = drops


    def isKilled(self):
        player.xp += self.xp
        monsters.remove(self)
        print("You have killed a Square.")