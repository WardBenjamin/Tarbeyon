#Jerks with Swords?
import pygame
import sys
import random

from entity import *
from blocks import *
from level import *

#Game Class
class Game(object):

	def __init__(self):

		self.debug = True
		if self.debug:
			self.showFPS = True
		else:
			self.showFPS = False

		self.captureMouse = True

		pygame.init()
		pygame.font.init()
		pygame.mixer.init()

		#Initialize the screen:
		self.screenX = 928
		self.screenY = 480

		self.screenX_center = self.screenX/2
		self.screenY_center = self.screenY/2
		self.screen_center = (self.screenX_center, self.screenY_center)

		self.screenSize = self.screenX, self.screenY

		self.screen = pygame.display.set_mode(self.screenSize)
		pygame.display.set_caption("Tarbeyon - Xeo Games")

		#Load the images and sounds
		self.loadContent()
		#Load the colors
		self.loadColors()

		#Load the clock and track the tick number
		self.clock = pygame.time.Clock()
		self.tickNumber = 0

		#Initialize the level:
		level = Level(levelMap)
		level.parseLevel()
		self.player1 = Player(level.player1pos, 100, "Player1", 1, 0)
		self.square1 = Square(level.square1pos, 1, 1, 1, 0, "")

		self.Running = True

		#Setting the state to "splashscreen" - DO THIS LAST!
		self.intromusicplay = True
		self.state = "player_turn"

	def loadContent(self):
		#Loading Images
		self.bkg = pygame.image.load("Images\TempBkg.png").convert()
		self.bkgRect = self.bkg.get_rect()
		self.bkgRect.center = self.screen_center

		self.splash = pygame.image.load("Images\Splash.png").convert()
		self.splashRect = self.splash.get_rect()
		self.splashRect.center = self.screen_center

		#Loading Sounds/Music
		self.intro_music_ogg_file = "Music\IntroMusic.ogg"
		self.intro_music_ogg = pygame.mixer.Sound(self.intro_music_ogg_file)

		#Loading Text Surfaces
		self.fpsFont = pygame.font.Font(None, 15)

	def loadColors(self):
		self.black = (0, 0, 0)
		self.white = (255, 255, 255)
		self.aqua =(  0, 255, 255)
		self.blue = (0, 0, 255)
		self.fuchsia = (255, 0, 255)
		self.gray = (128, 128, 128)
		self.green = (0, 128, 0)
		self.lime = (0, 255, 0)
		self.maroon = (128, 0, 0)
		self.navyBlue = (0, 0, 128)
		self.olive = (128, 128, 0)
		self.purple = (128, 0, 128)
		self.red = (255, 0, 0)
		self.silver = (192, 192, 192)
		self.teal = (0, 128, 128)
		self.deepBlue = (35, 68, 255)
		self.yellow = (255, 255, 0)

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

				if self.debug != True:
					pygame.mouse.set_pos(self.screen_center)
					pygame.mouse.set_visible(False)
			
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


				for entity in entities:
					entity.handleMovement()
				
				#FPS LABEL
				self.fps = self.clock.get_fps()
				self.fps = round(self.fps, 2)
				self.fpsString = str(self.fps)
				self.fpsLabel = self.fpsFont.render(self.fpsString, 20, self.black)

				print("X:", self.player1.rect.x, " ", "Y:", self.player1.rect.y, " ", "Health:", self.player1.health, "/", self.player1.originalHealth)

				if self.player1.health <= 0:
					self.player1.rect = self.player1.originalRect 
					self.player1.health = self.player1.originalHealth

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
			#Draw the blocks
			for block in blocks:
				pygame.draw.rect(self.screen, (0, 0, 0), block.rect)
			#Draw the tiles
			for tile in tiles:
				pygame.draw.rect(self.screen, self.deepBlue, tile.rect)
			for monster in monsters:
				pygame.draw.rect(self.screen, self.silver, monster.rect)
			#Draw the player
			pygame.draw.rect(self.screen, (255, 200, 0), self.player1.rect)

			#Draw the text

			if self.showFPS:
				self.screen.blit(self.fpsLabel, (10, 10))

			#Update the screen
			pygame.display.update()
		else:
			print("Error in the Draw method")

#Misc Defs
def roundTo32(x, base=32):
	return int(base * round(float(x)/base))

def roundUpTo32(x, base=32):
	y = int(base * round(float(x)/base))
	return y

def roundTo16(x, base=16):
	return int(base * round(float(x)/base))


def wipeScreenWhite():
	Game.screen.fill(Game.white)

Game = Game()

while Game.Running:
	Game.Tick()
	Game.clock.tick(30)

pygame.quit()
sys.exit()