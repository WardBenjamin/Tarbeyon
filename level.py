from color import *
from blocks import *
from entity import Player, Square
import constant
from constant import loadMapFile, blockid, itemid, entityid

class Level(object):
    def __init__(self, levelMap):
        self.levelMap = levelMap
        self.squareNum = 1
        self.block = {}
        self.tile = {}
        self.player = {}
        self.monster = {}

        self.blockIterator = 1
        self.healthBlockIterator = 1
        self.sewageBlockIterator = 1
        self.fountainIterator = 1
        self.tileIterator = 1
        self.playerIterator = 1
        self.monsterIterator = 1
        self.squareIterator = 1

    def parse_level(self):
        x = 144
        y = 0
        for row in self.levelMap:
            for col in row:
                if col == "W":
                    name = "Wall " + str(self.blockIterator)
                    self.block[name] = Wall(colors["black"], (x, y), 16, 16, name, blockid["wall"])
                    self.blockIterator += 1
                elif col == "X":
                    name = "Player " + str(self.playerIterator)
                    self.player[name] = Player(colors["yellow"], 16, 32, (x, y), 100, name, entityid["player"])
                elif col == "S":
                    name = "Square " + str(self.squareIterator)
                    self.monster["Monster " + str(self.monsterIterator)] = Square(colors["fuchsia"], 16, 16, (x, y), 50, name, entityid["square"])
                    self.monsterIterator += 1
                    self.squareIterator += 1
                elif col == "F":
                    name = "Fountain " + str(self.fountainIterator)
                    self.block[name] = Fountain((x, y), name, blockid["fountain"])
                    self.fountainIterator += 1
                elif col == "H":
                    name = "Health Block " + str(self.healthBlockIterator)
                    self.block[name] = HealthBlock((x, y), name, blockid["health"])
                elif col == "P":
                    name = "Sewage Block " + str(self.sewageBlockIterator)
                    self.block[name] = SewageBlock((x, y), name, blockid["sewage"])
                self.tile["Tile" + str(self.tileIterator)] = Tile(colors["white"], (x, y), 16, 16)
                self.tileIterator += 1
                x += 16
            y += 16
            x = 144


levelMap = loadMapFile("level.map", True)


level = Level(levelMap)