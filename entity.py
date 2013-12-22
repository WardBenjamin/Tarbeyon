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

class Player(Entity):

    def __init__(self, pos, health, name, damage, armor):

        self.rect = pygame.Rect(pos[0], pos[1], 32, 32)
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.health = health
        self.armor = armor
        self.damage = damage
        self.xp = 0

        self.effects = []

        self.speed = (0, 0)

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


    def move(self):
        
        # Move each axis separately. Note that this checks for collisions both times.
        if self.speed[0] != 0:
            self.move_single_axis()
        if self.speed[1] != 0:
            self.move_single_axis()
    
    def move_single_axis(self):
        global error

        # Move the rect
        self.rect.x += self.speed[0]
        self.rect.y += self.speed[1]


        # If you collide with a block, reset the position to the edge of the block
        for block in blocks:
            if self.rect.colliderect(block.rect):
                if self.speed[0] > 0: # Moving right; Hit the left side of the block
                    self.rect.right = block.rect.left
                elif self.speed[0] < 0: # Moving left; Hit the right side of the block
                    self.rect.left = block.rect.right
                elif self.speed[1] > 0: # Moving down; Hit the top side of the block
                    self.rect.bottom = block.rect.top
                elif self.speed[1] < 0: # Moving up; Hit the bottom side of the block
                    self.rect.top = block.rect.bottom
                else:
                    error = True

        for monster in monsters:
            if self.rect.colliderect(monster.rect):
                if self.speed[0] > 0: # Moving right; Hit the left side of the monster
                    self.rect.right = monster.rect.left
                elif self.speed[0] < 0: # Moving left; Hit the right side of the monster
                    self.rect.left = monster.rect.right
                elif self.speed[1] > 0: # Moving down; Hit the top side of the monster
                    self.rect.bottom = monster.rect.top
                elif self.speed[1] < 0: # Moving up; Hit the bottom side of the monster
                    self.rect.top = monster.rect.bottom
                else:
                    error = True

        for liquid in liquids:
            if self.rect.colliderect(liquid.rect):
                liquid.applyEffects()



class Monster(Entity):

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
        
        
class Square(Monster):

    def isKilled(self):
        player.xp += self.xp
        monsters.remove(self)
        print("You have killed a Square.")