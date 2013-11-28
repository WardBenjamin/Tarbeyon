import pygame
import sys
import time
import random

pygame.init()
pygame.font.init()

#Colors
black = (0, 0, 0)
white = (255, 255, 255)
aqua =(  0, 255, 255)
blue = (0, 0, 255)
fuchsia = (255, 0, 255)
gray = (128, 128, 128)
green = (0, 128, 0)
lime = (0, 255, 0)
maroon = (128, 0, 0)
navyBlue = (0, 0, 128)
olive = (128, 128, 0)
purple = (128, 0, 128)
red = (255, 0, 0)
silver = (192, 192, 192)
teal = (0, 128, 128)
deepBlue = (35, 68, 255)
yellow = (255, 255, 0)

#Screen Definition
screenX = 928
screenY = 480

screenX_center = screenX/2
screenY_center = screenY/2
screen_center = (screenX_center, screenY_center)


screenSize = screenX, screenY

screen = pygame.display.set_mode(screenSize)
pygame.display.set_caption("Unnamed Ship Game - Xeo Games")

#Font/Text Declaration

fpsFont = pygame.font.Font(None, 15)

moneyFont = pygame.font.Font(None, 15)
goodsFont = pygame.font.Font(None, 15)

#Images
bkg = pygame.image.load("f3TAE.png")
bkgRect = bkg.get_rect()
bkgRect.center = screen_center

splash = pygame.image.load("Splash.png")
splashRect = splash.get_rect()
splashRect.center = screen_center

Clock = pygame.time.Clock()

#Variable Declaration
goodsAvailable = 0
moveAvailable = False


#Definitions
def wipeScreenWhite():
	screen.fill(white)
#def displaySplashscreen():
	#screen.fill(teal)
	#time.sleep(2)
	#global Starting
	#Starting = False


#Object Declaration:
# Class for the orange dude
class Player(object):


	
	def __init__(self):
		self.rect = pygame.Rect(224, 96, 32, 32)

		self.atPort = False
		self.money = 0
		self.moneyString = ""
		self.goodsNumber = 0
		self.goodsNumberString = ""

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

class Block(object):
	
	def __init__(self, pos):
		blocks.append(self)
		self.rect = pygame.Rect(pos[0], pos[1], 32, 32)


class Port(Block):

	def __init__(self, pos):
		ports.append(self)
		self.rect = pygame.Rect(pos[0], pos[1], 32, 32)


blocks = [] # List to hold the blocks
ports = [] # List to hold the ports
player = Player() # Create the player

# Holds the level layout in a list of strings.
level = [
"WWWWWWWWWWWWWWWWWWWW",
"W                  W",
"W                  W",
"W             P    W",
"W                  W",
"W                  W",
"W                  W",
"W                  W",
"W                  W",
"W                  W",
"W                  W",
"W                  W",
"W   P              W",
"W                  W",
"WWWWWWWWWWWWWWWWWWWW",
]

# Parse the level string above. W = wall, E = exit
x = 144
y = 0
for row in level:
    for col in row:
        if col == "W":
            Block((x, y))
        if col == "P":
            Port((x, y,))
        x += 32
    y += 32
    x = 144

#Program Loops
timeVar = 0 # Amount of time that has passed
Starting = True # Whether or not to show the splashscreen
Running = True


while Running:
	while Starting == True:
		timeVar = timeVar + 1
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				Starting == False
				Running = False
		if timeVar == 150:
			timeVar = 0
			Starting = False
			
		#FPS LABEL
		fps = Clock.get_fps()
		fps = round(fps, 2)
		fpsString = str(fps)
		fpsLabel = fpsFont.render(fpsString, 20, black)		
		
		#Drawing to screen
		wipeScreenWhite()
		screen.blit(splash, splashRect)
		screen.blit(fpsLabel, (10, 10))
		pygame.display.flip()
		Clock.tick(50)

	#Main Loop, if Starting is False

	timeVar = timeVar + 1
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			Running = False
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				Running = False


	#Capturing Mouse Position
	mousePos = pygame.mouse.get_pos()
	mouseX = mousePos[0]
	mouseY = mousePos[1]

	#Capturing and Responding to Keys
	key = pygame.key.get_pressed()
	if key[pygame.K_LEFT]:
		player.move(-32, 0)
	if key[pygame.K_RIGHT]:
		player.move(32, 0)
	if key[pygame.K_UP]:
		player.move(0, -32)
	if key[pygame.K_DOWN]:
		player.move(0, 32)
	
	#FPS LABEL
	fps = Clock.get_fps()
	fps = round(fps, 2)
	fpsString = str(fps)
	fpsLabel = fpsFont.render(fpsString, 20, black)	

	if player.atPort == True:
		player.money = player.money + (10*player.goodsNumber)
		player.moneyString =  str(player.money)
		player.goodsNumber = 0

		goodsAvailable = random.randrange(1, 20)
		print("How many goods would you like to take? The max is: ", goodsAvailable)
		player.goodsNumber = int(input(">>>"))
		if player.goodsNumber > goodsAvailable:
			print("You can only take up to: ", goodsAvailable, ". Pick another number.")
			player.goodsNumber = int(input(">>>"))
			print("You have brought ", player.goodsNumber," goods on board.")
			player.goodsNumberString = str(player.goodsNumber)
			player.atPort = False
		else:
			print("You have brought ", player.goodsNumber," goods on board.")
			player.goodsNumberString = str(player.goodsNumber)
			player.atPort = False

	#Goods and Money Labels
	goodsLabel = goodsFont.render(player.goodsNumberString, 20, black)
	moneyLabel = moneyFont.render(player.moneyString, 20, black)


	#Drawing to Screen
	wipeScreenWhite()
	screen.blit(bkg, bkgRect)
	for block in blocks:
		pygame.draw.rect(screen, (0, 0, 0), block.rect)
	for port in ports:
		pygame.draw.rect(screen, deepBlue, port.rect)
	pygame.draw.rect(screen, (255, 200, 0), player.rect)
	screen.blit(goodsLabel, (10, 50))
	screen.blit(moneyLabel, (10, 30))
	screen.blit(fpsLabel, (10, 10))
	pygame.display.flip()
	Clock.tick(30)

pygame.font.quit()
pygame.quit()
sys.exit()