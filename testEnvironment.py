import pygame, os, sys

from color import *
import constant, testLevel
from entity import Player

pygame.init()

class Screen(object):
    def __init__(self):
        self.x = 928
        self.y = 510

        self.x_center = self.x / 2
        self.y_center = self.y / 2
        self.center = (self.x_center, self.y_center)

        self.size = self.x, self.y


class Environment(object):
    def __init__(self):
        # Center the screen
        os.environ["SDL_VIDEO_CENTERED"] = "1"

        # Initialize the screen:
        self.screen = Screen()
        self.display = pygame.display.set_mode(self.screen.size)
        pygame.display.set_caption("Test Environment")

        self.clock = pygame.time.Clock()

        self.level = testLevel.level
        self.level.parse_level()

        self.state = "test1"
        self.running = True

        self.load_content()

    def load_content(self):
        #Loading Images
        self.bkg = pygame.image.load("Images" + os.sep + "TempBkg.png").convert()
        self.bkgRect = self.bkg.get_rect()
        self.bkgRect.center = self.screen.center

        #Loading Text Surfaces
        self.fpsFont = pygame.font.Font(None, 15)

    def loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
        
        for player in constant.player:
            player.handle_movement()
            player.update()

        # Computing FPS
        self.fps = self.clock.get_fps()
        self.fps = round(self.fps)
        self.fpsString = "FPS:" + str(self.fps)
        self.fpsLabel = self.fpsFont.render(self.fpsString, 20, colors["black"])

        self.draw()

    def draw(self):
        #Clear the screen
        #self.wipe_display()

        #Draw the background
        #self.display.blit(self.bkg, self.bkgRect)

        constant.blocks.draw(self.display)
        constant.player.draw(self.display)

        #Draw the text
        self.display.blit(self.fpsLabel, (10, 10))

        #Update the screen
        pygame.display.update()

    def wipe_display(self):
        self.display.fill(colors["white"])

testEnvironment = Environment()

while testEnvironment.running:
    testEnvironment.loop()
    testEnvironment.clock.tick(40)

pygame.quit()
sys.exit()
