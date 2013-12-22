import pygame

blocks = [] # List to hold the blocks
tiles = [] # List to hold the tiles
liquids = [] # List to hold the liquid tiles

class Block(object):
	
	def __init__(self, pos):
		blocks.append(self)
		self.rect = pygame.Rect(pos[0], pos[1], 32, 32)

class Tile(Block):

	def __init__(self, pos):
		tiles.append(self)
		self.rect = pygame.Rect(pos[0], pos[1], 32, 32)

class Liquid(Block):

	def __init__(self, pos, liquidType):
		self.rect = pygame.Rect(pos[0], pos[1], 32, 32)
		self.type = liquidType
		self.effects = "none"
		if self.type == "water":
			self.effects = "none"
		elif self.type == "spring":
			self.effects = "regen"
		elif self.type == "lava":
			self.effects = "fireDamage"
		else:
			self.effects = "none"
	def applyEffects(self, player):
		player.effects.append(self.effects)