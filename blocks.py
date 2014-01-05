import pygame

import constant


class Block(pygame.sprite.Sprite):
    # Constructor. Pass in the color of the block and it's dimensions
    def __init__(self, color, pos, width, height):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        self.add(constant.blocks)

        # Create an image of the block, and fill it with a color.
        # Note: This could also be an image loaded from the disk.
        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x and rect.y
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

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