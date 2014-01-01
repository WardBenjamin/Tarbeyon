import color
from blocks import *

# Holds the level layout in a list of strings.

def loadMapFile(filename):
    lvlfile = open(filename)
    lvlmap = lvlfile.read().split('\n')
    lvlfile.close()
    return lvlmap


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
                    Block(color.black, (x, y), 16, 16)
                elif col == "X":
                    self.player1pos = (x, y)
                elif col == "S" and self.squareNum == 1:
                    self.square1pos = (x, y)
                    self.squareNum = 2
                elif col == "S" and self.squareNum == 2:
                    self.square2pos = (x, y)
                    self.squareNum = 3
                Tile(color.white, (x, y), 16, 16)
                x += 16
            y += 16
            x = 144


levelMap = loadMapFile("level.map")