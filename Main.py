import pygame
import sys
import time

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
yellow = (255, 255, 0)

#Screen Definition
screenX = 950
screenY = 500

screenX_center = screenX/2
screenY_center = screenY/2
screen_center = (screenX_center, screenY_center)


screenSize = screenX, screenY

screen = pygame.display.set_mode(screenSize)
pygame.display.set_caption("Unnamed Ship Game - Xeo Productions")

#Font/Text Declaration

fpsFont = pygame.font.Font(None, 15)

#Images
bkg = pygame.image.load("f3TAE.png")
bkgRect = bkg.get_rect()
bkgRect.center = screen_center

splash = pygame.image.load("Splash.png")
splashRect = splash.get_rect()
splashRect.center = screen_center

Clock = pygame.time.Clock()


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
		self.rect = pygame.Rect(32, 32, 16, 16)

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
		self.rect = pygame.Rect(pos[0], pos[1], 16, 16)


#Program Loops
timeVar = 0 # Amount of time that has passed
Starting = True # Whether or not to show the splashscreen
Running = True

blocks = [] # List to hold the blocks
player = Player() # Create the player

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
		player.move(-2, 0)
	if key[pygame.K_RIGHT]:
		player.move(2, 0)
	if key[pygame.K_UP]:
		player.move(0, -2)
	if key[pygame.K_DOWN]:
		player.move(0, 2)
	
	#FPS LABEL
	fps = Clock.get_fps()
	fps = round(fps, 2)
	fpsString = str(fps)
	fpsLabel = fpsFont.render(fpsString, 20, black)		

	wipeScreenWhite()
	screen.blit(bkg, bkgRect)
	for block in blocks:
		pygame.draw.rect(screen, (255, 255, 255), block.rect)
	pygame.draw.rect(screen, (255, 200, 0), player.rect)
	screen.blit(fpsLabel, (10, 10))
	pygame.display.flip()
	Clock.tick(30)

pygame.font.quit()
pygame.quit()
sys.exit()