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

entityid = {
	"player"   : 0,
	"square"   : 1
}

blockid = {
	"null"     : 0,
	"wall"     : 1,
	"health"   : 2,
	"sewage"   : 3,
	"fountain" : 4
}

itemid = {
	"null"    : 0,
	"health"  : 1
}