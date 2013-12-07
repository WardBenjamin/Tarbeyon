import pygame

blocks = [] # List to hold the blocks
ports = [] # List to hold the ports

class Block(object):
	
	def __init__(self, pos):
		blocks.append(self)
		self.rect = pygame.Rect(pos[0], pos[1], 32, 32)

class Port(Block):

	def __init__(self, pos):
		ports.append(self)
		self.rect = pygame.Rect(pos[0], pos[1], 32, 32)