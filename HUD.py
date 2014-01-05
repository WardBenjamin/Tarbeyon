import pygame
import os
import math

import constant


class HUD(object):
    def __init__(self):
        self.Health = Health()

class Health(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.add(constant.HUDcomponents)

        self.images = {
            "100"    : pygame.image.load("Images" + os.sep + "health" + os.sep + "full_health_100.png"),
            "90"     : pygame.image.load("Images" + os.sep + "health" + os.sep + "90_health_100.png"),
            "80"     : pygame.image.load("Images" + os.sep + "health" + os.sep + "80_health_100.png"),
            "70"     : pygame.image.load("Images" + os.sep + "health" + os.sep + "70_health_100.png"),
            "60"     : pygame.image.load("Images" + os.sep + "health" + os.sep + "60_health_100.png"),
            "50"     : pygame.image.load("Images" + os.sep + "health" + os.sep + "half_health_100.png"),
            "40"     : pygame.image.load("Images" + os.sep + "health" + os.sep + "40_health_100.png"),
            "30"     : pygame.image.load("Images" + os.sep + "health" + os.sep + "30_health_100.png"),
            "20"     : pygame.image.load("Images" + os.sep + "health" + os.sep + "20_health_100.png"),
            "10"     : pygame.image.load("Images" + os.sep + "health" + os.sep + "10_health_100.png"),
            "0"      : pygame.image.load("Images" + os.sep + "health" + os.sep + "zero_health_100.png")
        }


        self.maxAmount = 100
        self.amount = 100

        self.image = self.images["100"]
        self.rect = self.image.get_rect()

        self.player = next(iter(constant.player))

    def check_image(self):
        return self.images[str(math.floor(self.amount / 10.0) * 10)]

    def update(self):
        self.player = next(iter(constant.player))
        self.amount = self.player.health
        self.check_image()