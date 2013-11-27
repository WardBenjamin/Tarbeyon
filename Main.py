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


#Image/Rect Declaration
#Template
#IMAGE = pygame.image.load("IMAGE.PNG")
#IMAGERect = IMAGE.get_rect()

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

#Variable Definition
timeVar = 0
Starting = True


Running = True

while Running:
	while Starting == True:
		timeVar = timeVar + 1
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				Starting == False
				Running = False
		if timeVar == 500:
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

	mousePos = pygame.mouse.get_pos()
	mouseX = mousePos[0]
	mouseY = mousePos[1]
	
	#FPS LABEL
	fps = Clock.get_fps()
	fps = round(fps, 2)
	fpsString = str(fps)
	fpsLabel = fpsFont.render(fpsString, 20, black)		

	wipeScreenWhite()
	screen.blit(bkg, bkgRect)
	screen.blit(fpsLabel, (10, 10))
	pygame.display.flip()
	Clock.tick(30)

pygame.font.quit()
pygame.quit()
sys.exit()