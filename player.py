import pygame
from block import *

class Player(object):
	
	def __init__(self):

		self.rect = pygame.Rect(224, 96, 32, 32)

		self.atPort = False
		self.atPortA = False
		self.atPortB = False
		self.money = 0
		self.moneyString = ""
		self.goodsNumber = 0
		self.goodsNumberString = ""

	VALID_STATES = ['atPort', 'state2', 'state3']

    #States
    #Currently not used/implemented
	def check_state(self, state):
		if state in Player.VALID_STATES:
			return self.__state == state

	def move(self, dx, dy):
		
		# Move each axis separately. Note that this checks for collisions both times.
		if dx != 0:
			self.move_single_axis(dx, 0)
		if dy != 0:
			self.move_single_axis(0, dy)
	
	def move_single_axis(self, dx, dy):

		# Move the rect
		self.rect.x += dx
		self.rect.y += dy

		# If you collide with a port, move out based on velocity
		for port in ports:
			if self.rect.colliderect(port.rect):
				if dx > 0: # Moving right; Hit the left side of a port
					self.rect.right = port.rect.left
					self.atPort = True
				if dx < 0: # Moving left; Hit the right side of a port
					self.rect.left = port.rect.right
					self.atPort = True
				if dy > 0: # Moving down; Hit the top side of a port
					self.rect.bottom = port.rect.top
					self.atPort = True
				if dy < 0: # Moving up; Hit the bottom side of a port
					self.rect.top = port.rect.bottom
					self.atPort = True

		# If you collide with a block, move out based on velocity
		for block in blocks:
			if self.rect.colliderect(block.rect):
				if dx > 0: # Moving right; Hit the left side of the block
					self.rect.right = block.rect.left
				if dx < 0: # Moving left; Hit the right side of the block
					self.rect.left = block.rect.right
				if dy > 0: # Moving down; Hit the top side of the block
					self.rect.bottom = block.rect.top
				if dy < 0: # Moving up; Hit the bottom side of the block
					self.rect.top = block.rect.bottom