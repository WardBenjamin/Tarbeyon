import pygame

from blocks import *
from player import *
from pirate import *

def roundTo32(x, base=32):
	return int(base * round(float(x)/base))

def wipeScreenWhite():
	screen.fill(white)