import pygame, random, os

import constant
from constant import blockid
from color import *
from entity import velocity


class Block(pygame.sprite.Sprite):
    # Constructor. Pass in the color of the block and it's dimensions
    def __init__(self, color, pos, width, height, name, ID):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        self.add(constant.blocks)

        self.id = ID
        self.name = name

        # Create an image of the block, and fill it with a color.
        # Note: This could also be an image loaded from the disk.
        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x and rect.y
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def do_effects(self, player): pass


class Wall(Block): pass

class HealthBlock(Block):
    # Constructor. Pass in the color of the block and it's dimensions
    def __init__(self, pos, name, ID, healAmount=1):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        self.add(constant.blocks)

        self.id = ID
        self.name = name

        # Create an image of the block, and fill it with a color.
        # Note: This could also be an image loaded from the disk.
        self.image = pygame.image.load("Images" + os.sep + "blocks" + os.sep + "misc" + os.sep + "health.png")

        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x and rect.y
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

        self.healAmount = healAmount

    def do_effects(self, player):
        player.stats.health += self.healAmount


class SewageBlock(Block):
    # Constructor. Pass in the color of the block and it's dimensions
    def __init__(self, pos, name, ID):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        self.add(constant.blocks)

        self.id = ID
        self.name = name

        # Create an image of the block, and fill it with a color.
        # Note: This could also be an image loaded from the disk.
        self.image = pygame.image.load("Images" + os.sep + "blocks" + os.sep + "misc" + os.sep + "sewage1.png")

        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x and rect.y
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def do_effects(self, player):
        armor = player.stats.armor
        if armor == 0:
            damage = 2
        else:
            damage = 10 - (armor * 2)
            if damage <= 0:
                damage = 1
        player.stats.health -= damage

class LavaBlock(Block):
    # Constructor. Pass in the color of the block and it's dimensions
    def __init__(self, pos, name, ID):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        self.add(constant.blocks)

        self.id = ID
        self.name = name

        # Create an image of the block, and fill it with a color.
        # Note: This could also be an image loaded from the disk.
        self.image = pygame.image.load("Images" + os.sep + "blocks" + os.sep + "misc" + os.sep + "sewage1.png")

        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x and rect.y
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def do_effects(self, player):
        armor = player.stats.armor
        damage = 100 - (armor * 5)
        player.stats.health -= damage

class Tile(pygame.sprite.Sprite):
    # Constructor. Pass in the color of the block and it's dimensions
    def __init__(self, color, pos, width, height):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        self.add(constant.tiles)

        # Create an image of the block, and fill it with a color.
        # Note: This could also be an image loaded from the disk.
        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x and rect.y
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

class Fountain(Block):
    def __init__(self, pos, name, ID):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        self.add(constant.blocks)
        self.add(constant.fountains)

        self.id = ID
        self.name = name

        self.particles = pygame.sprite.Group()
        self.image = pygame.image.load("Images" + os.sep + "blocks" + os.sep + "misc" + os.sep + "fountain1.png")
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.wImage = pygame.image.load("Images" + os.sep + "blocks" + os.sep + "misc" + os.sep + "fountain2.png")
        self.wBoundingBox = self.wImage.get_rect()
        self.wBoundingBox.x = pos[0] + 25
        self.wBoundingBox.y = pos[1]

        self.waterOrigin = self.wBoundingBox.midbottom

        self.particles = {}
        self.particleGroup = pygame.sprite.Group()
        """self.create_particles()

    def create_particles(self):
        for i in range(10):
            self.particles[i] = WaterParticle(self.name, self.wBoundingBox, self.waterOrigin, 2, 2)

    def draw_particles(self, screen):
        for particle in self.particleGroup:
            particle.draw(screen)

    def update(self):
        self.draw_particles()"""

class WaterParticle(pygame.sprite.Sprite):
    def __init__(self, fountainName, boundingBox, originPos, width, height):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        # Iterate through the fountians to find which one it is part of
        for fountain in constant.fountains:
            if fountain.name == fountainName:
                self.add(fountain.particleGroup)
        self.image = pygame.Surface([width, height])
        self.color = self.pick_color()
        self.image.fill(self.color)

        self.rect = self.image.get_rect()
        self.origin = self.image.get_rect()

        self.rect.x = originPos[0]
        self.rect.y = originPos[1]
        self.origin.x = originPos[0]
        self.origin.y = originPos[1]

        self.gravity = 0.5

        self.originalVelocity = velocity()
        self.originalVelocity.y = -1
        self.velocity = velocity()
        self.choose_direction()

        self.boundingBox = boundingBox

    def pick_color(self):
        colorVar = random.randint(1, 4)
        if colorVar == 1:
            return colors["blue1"]
        elif colorVar == 2:
            return colors["blue2"]
        elif colorVar == 3:
            return colors["blue3"]
        elif colorVar == 4:
            return colors["blue4"]
        del colorVar

    def choose_direction(self):
        dir = random.randint(1, 2)
        if dir == 1:
            self.originalVelocity.x = -1
        elif dir == 2:
            self.originalVelocity.x = 1
        self.velocity = self.originalVelocity

    def check_collision(self):
        if not self.rect.colliderect(self.boundingBox):
            if self.rect.y > self.boundingBox.y:
                self.rect.x = self.origin.x
                self.rect.y = self.origin.y
                self.choose_direction()

    def update(self): # Move the particle based on velocity, checking for collision each time
        # Apply gravity to the y velocity
        self.velocity.y += self.gravity
        # Move on the y axis
        self.rect.y += self.velocity.y
        self.check_collision()      
        # Move on the x axis  
        self.rect.x += self.velocity.x
        self.check_collision()

    def draw(self, screen):
        screen.blit(self.image, self.rect)