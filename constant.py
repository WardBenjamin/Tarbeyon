import pygame

pygame.init()
# Creating sprite Groups
entities = pygame.sprite.Group()
player = pygame.sprite.Group()
monsters = pygame.sprite.Group()
blocks = pygame.sprite.Group()
fountains = pygame.sprite.Group()
tiles = pygame.sprite.Group()

HUDcomponents = pygame.sprite.Group()

def loadMapFile(filename, level):
    file = open(filename)
    map = file.read().split('\n')
    file.close()
    return map