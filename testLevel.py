from color import *
from blocks import *
from entity import Player, Square
import constant

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
        self.player = {}
        self.block = {}
        self.tile = {}
        self.monster = {}

        self.blockIterator = 1
        self.tileIterator = 1
        self.fountainIterator = 1
        self.monsterIterator = 1
        self.squareIterator = 1
        self.playerIterator = 1

    def parse_level(self):
        x = 144
        y = 0
        for row in self.levelMap:
            for col in row:
                if col == "W":
                    self.block["Block" + str(self.blockIterator)] = Block(colors["black"], (x, y), 16, 16)
                    self.blockIterator += 1
                elif col == "X":
                    self.player["Player" + str(self.playerIterator)] = Player(colors["yellow"], 16, 32, (x, y), 100, "Player", True)
                elif col == "S":
                    self.monster["Monster" + str(self.monsterIterator)] = Square(colors["fuchsia"], 16, 16, (x, y), 50, ("Square" + str(self.squareIterator)), False)
                    self.monsterIterator += 1
                    self.squareIterator += 1
                elif col == "F":
                    name = "Fountain" + str(self.fountainIterator)
                    self.block[name] = Fountain((x, y), name)
                    self.fountainIterator += 1
                self.tile["Tile" + str(self.tileIterator)] = Tile(colors["white"], (x, y), 16, 16)
                self.tileIterator += 1
                x += 16
            y += 16
            x = 144


levelMap = loadMapFile("testLevel.map")


level = Level(levelMap)