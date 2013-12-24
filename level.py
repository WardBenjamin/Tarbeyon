import pygame

from entity import Player
from blocks import Block, blocks

# Holds the level layout in a list of strings.
levelMap = [
"WWWWWWWWWWWWWWWWWWWW",
"WX                 W",
"WW                 W",
"W                  W",
"W                  W",
"W                  W",
"W                  W",
"W          S       W",
"W                  W",
"W                  W",
"W                  W",
"W                  W",
"W                  W",
"W                  W",
"WWWWWWWWWWWWWWWWWWWW",
]

class Level(object):

	def __init__(self, levelMap):
		self.levelMap = levelMap
		self.squareNum = 1

	def parseLevel(self):
		x = 144
		y = 0
		for row in self.levelMap:
			for col in row:
				if col == "W":
					Block((x, y))
				if col == "X":
					self.player1pos = (x, y)
				if col == "S" and self.squareNum == 1:
					self.square1pos = (x, y)
					self.squareNum = 2
				if col == "S" and self.squareNum == 2:
					self.square2pos = (x, y)
					self.squareNum = 3
				x += 32
			y += 32
			x = 144

level = Level(levelMap)
level.parseLevel()