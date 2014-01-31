import pygame, random, os

import constant
from constant import itemid
from color import *
from entity import velocity


class Item(pygame.sprite.Sprite):
    # Constructor. Pass in the color of the block and it's dimensions
    def __init__(self, color, pos, width, height, name):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        self.add(constant.blocks)

        self.id = itemid["null"]
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