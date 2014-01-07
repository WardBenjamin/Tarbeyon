#Jerks with Swords?
import os
import sys

from color import *
import level
from entity import *


#Game Class
class Game(object):
    def __init__(self):

        #Debugging stuff
        self.debug = True
        self.debugShown = True
        self.debugMonsters = True
        self.showFPS = True

        self.captureMouse = True

        pygame.init()
        pygame.font.init()
        pygame.mixer.init()

        self.icon = pygame.image.load("Images" + os.sep + "icon.png")

        self.constructScreen() # Init the screen
        self.loadContent() # Load the images and sounds

        self.buildMap() # Build the map

        self.clock = pygame.time.Clock()
        self.tickNumber = 0

        self.icon = pygame.image.load("Images" + os.sep + "Icon.png")

        self.Running = True
        if self.debug:
            self.state = "player_turn"
            print("Debug is enabled! Beware, strangers")
        else:
            self.intromusicplay = True
            self.state = "splashscreen"

    def constructScreen(self):

        # Make the screen centered
        os.environ["SDL_VIDEO_CENTERED"] = "1"

        # Initialize the screen:
        self.screenX = 928
        self.screenY = 510

        self.screenX_center = self.screenX / 2
        self.screenY_center = self.screenY / 2
        self.screen_center = (self.screenX_center, self.screenY_center)

        self.screenSize = self.screenX, self.screenY
        self.screen = pygame.display.set_mode(self.screenSize)
        pygame.display.set_icon(self.icon)

        pygame.display.set_caption("Tarbeyon - Xeo Games")


    def buildMap(self):
        self.level = level.Level(level.levelMap)
        self.level.parseLevel() # Building the level

        self.player = Player(colors["yellow"], 16, 32, self.level.player1pos, 100, "player", True)
        self.square1 = Square(colors["fuchsia"], 16, 16, self.level.square1pos, 50, "square1", False)

    def loadContent(self):
        #Loading Images
        self.bkg = pygame.image.load("Images" + os.sep + "TempBkg.png").convert()
        self.bkgRect = self.bkg.get_rect()
        self.bkgRect.center = self.screen_center

        self.splash = pygame.image.load("Images" + os.sep + "Splash.png").convert()
        self.splashRect = self.splash.get_rect()
        self.splashRect.center = self.screen_center

        #Loading Sounds/Music
        self.intro_music_ogg_file = "Music" + os.sep + "IntroMusic.ogg"
        self.intro_music_ogg = pygame.mixer.Sound(self.intro_music_ogg_file)

        #Loading Text Surfaces
        self.fpsFont = pygame.font.Font(None, 15)

    def Tick(self):

        if self.tickNumber >= 0:
            if self.state == "splashscreen":
                if self.tickNumber <= 1 and self.intromusicplay == True:
                    channel = self.intro_music_ogg.play()
                    self.intromusicplay = False
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.Running = False

                if self.tickNumber == 450:
                    pygame.mixer.quit()
                    self.state = "player_turn"
                    captureMouse = True
                    self.tickNumber = 0

                if not self.debug:
                    pygame.mouse.set_pos(self.screen_center)
                    pygame.mouse.set_visible(False)
                if self.debug and self.debugShown:
                    print("Debug is enabled! Beware, strangers")

                #FPS LABEL
                self.fps = self.clock.get_fps()
                self.fps = round(self.fps, 2)
                self.fpsString = str(self.fps)
                self.fpsLabel = self.fpsFont.render(self.fpsString, 20, self.black)
                
            elif self.state == "player_turn":
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.Running = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.Running = False
                            pygame.mixer.quit()


                #Capturing Mouse Position
                if self.captureMouse == True:
                    pygame.mouse.set_visible(True)
                    self.mousePos = pygame.mouse.get_pos()
                    self.mouseX = self.mousePos[0]
                    self.mouseY = self.mousePos[1]
                else:
                    pygame.mouse.set_visible(False)
                    pygame.mouse.set_pos(self.screen_center)

                for entity in constant.entities:
                    entity.handle_movement()
                    entity.update()
                    entity.check_death()

                #FPS LABEL
                self.fps = self.clock.get_fps()
                self.fps = round(self.fps, 2)
                self.fpsString = str(self.fps)
                self.fpsLabel = self.fpsFont.render(self.fpsString, 20, colors["black"])

            else:
                print("No valid game state set")

            self.Draw()
        self.tickNumber += 1

    def Draw(self):
        if self.state == "splashscreen":
            wipeScreenWhite()
            self.screen.blit(self.splash, self.splashRect)
            if self.showFPS:
                self.screen.blit(self.fpsLabel, (10, 10))
            pygame.display.update()

        elif self.state == "menu":
            #Unused
            wipeScreenWhite()


        elif self.state == "player_turn":
            #Clear the screen
            wipeScreenWhite()
            #Draw the background
            self.screen.blit(self.bkg, self.bkgRect)
            #Draw the tiles
            constant.tiles.draw(self.screen)
            #Draw the blocks on top of the tiles
            constant.blocks.draw(self.screen)

            # Draw the monsters
            constant.monsters.draw(self.screen)
            # Draw the player
            constant.player.draw(self.screen)

            # Draw the components of the HUD
            for player in constant.player:
                player.HUD.components.draw(self.screen)

            #Draw the text

            if self.showFPS:
                self.screen.blit(self.fpsLabel, (10, 10))

            #Update the screen
            pygame.display.update()

        else:
            print("Error in the Draw method")


#Misc Defs
def roundTo32(x, base=32):
    return int(base * round(float(x) / base))


def roundUpTo32(x, base=32):
    y = int(base * round(float(x) / base))
    return y


def roundTo16(x, base=16):
    return int(base * round(float(x) / base))


def wipeScreenWhite():
    Game.screen.fill(colors["white"])


Game = Game()

while Game.Running:
    Game.Tick()
    Game.clock.tick(30)

pygame.quit()
sys.exit()
