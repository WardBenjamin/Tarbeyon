import pygame, random, os, math

import constant
from constant import loadMapFile

class velocity(object):
    def __init__(self):
        self.x = 0
        self.y = 0

class Entity(pygame.sprite.Sprite):
    # Constructor. Pass in the color of the block and it's dimensions
    def __init__(self, color, width, height, pos, maxHealth, name, isPlayer):
        # Basic Sprite stuff
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        self.add(constant.entities)

        # Create an image of the block, and fill it with a color.
        # Note: This could also be an image loaded from the disk.
        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x and rect.y
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

        self.origin = self.image.get_rect()
        self.origin.x = pos[0]
        self.origin.y = pos[1]

        self.velocity = velocity()
        self.onGround = True
        self.gravity = 1

        self.name = name
        self.maxHealth = maxHealth
        self.health = maxHealth
        self.damage = 1
        self.armor = 0

        self.directionPicked = False

        self.do_personal_init()

        if isPlayer:
            self.HUD = HUD()


        # Test
        print(self.name, "was created")

    def do_personal_init(self):
        print("This is just a method to overwrite!")


    def check_death(self):
        if self.health <= 0:
            pygame.sprite.Sprite.kill()

    def handle_movement(self):

        if not self.directionPicked:
            self.direction = random.randint(1, 100) #Randomly picking a direction
            self.moveNumber = 60 # Total Number of frames for one movement action
            self.moveInterval = random.randint(30, 55) # Number of frames to wait between moving

        if self.direction > 50 and self.moveNumber > self.moveInterval:
            self.velocity.x = -2
            self.directionPicked = True
            self.direction = 51
            self.moveNumber -= 1

        elif self.direction <= 50 and self.moveNumber > self.moveInterval:
            self.velocity.x = 2
            self.directionPicked = True
            self.direction = 49
            self.moveNumber -= 1

        elif self.moveNumber <= self.moveInterval and self.moveNumber > 0:
            self.moveNumber -= 1

        elif self.moveNumber <= 0:
            self.directionPicked = False


    def update(self):

        self.velocity.y += self.gravity
        self.rect.y += self.velocity.y

        for block in constant.blocks:
            if self.rect.colliderect(block.rect):
                if self.velocity.y > 0: # Moving down; Hit the top side of the block
                    self.rect.bottom = block.rect.top
                    self.velocity.y = 0
                    self.onGround = True
                elif self.velocity.y < 0: # Moving up; Hit the bottom side of the block
                    self.rect.top = block.rect.bottom
                    self.velocity.y = 0


        self.rect.x += self.velocity.x

        for block in constant.blocks:
            if self.rect.colliderect(block.rect):
                if self.velocity.x > 0: # Moving right; Hit the left side of the block
                    self.rect.right = block.rect.left
                    self.velocity.x = 0
                elif self.velocity.x < 0: # Moving left; Hit the right side of the block
                    self.rect.left = block.rect.right
                    self.velocity.x = 0

class Player(Entity):
    def do_personal_init(self):
        self.add(constant.player)
        self.xp = 0
        self.gravity = 0.5
        self.canJump = True
        self.ableToDJ = True
        self.doubleJump = True
        self.hitTimer = 8
        self.maxHitTimer = self.hitTimer
        self.effects = []
        self.validEffects = ["none", "regen", "fireTick"]

    #Currently not used/implemented
    def updateState(self):
        for state in self.effects:
            if state in self.validEffects:
                if state == "regen":
                    self.health += 1
                elif state == "fireTick":
                    self.health -= 1
                else:
                    print("Error in Player.updateState")

    def start_jump(self):
        self.velocity.y = -11
        self.onGround = False
        if self.ableToDJ:
            self.doubleJump = True
        else:
            self.doubleJump = False

    def double_jump(self):
        self.velocity.y = -11
        self.doubleJump = False

    def handle_movement(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            self.velocity.x = -3
        if key[pygame.K_RIGHT]:
            self.velocity.x = 3
        if key[pygame.K_UP] and not self.onGround and self.doubleJump and self.velocity.y >= -2:
            self.double_jump()
        if key[pygame.K_UP] and self.onGround:
            self.start_jump()


        if not key[pygame.K_LEFT] and not key[pygame.K_RIGHT]:
            self.velocity.x = 0

    def update(self):

        if self.velocity.y > 20:
            self.velocity.y = 20

        self.velocity.y += self.gravity
        self.rect.y += self.velocity.y

        for block in constant.blocks:
            if self.rect.colliderect(block.rect):
                if self.velocity.y > 0: # Moving down; Hit the top side of the block
                    self.rect.bottom = block.rect.top
                    self.velocity.y = 0
                    self.onGround = True
                elif self.velocity.y < 0: # Moving up; Hit the bottom side of the block
                    self.rect.top = block.rect.bottom
                    self.velocity.y = 0

        for monster in constant.monsters: # Hit a monster
            if self.rect.colliderect(monster.rect):
                if self.hitTimer <= 0:
                    self.health = self.health - monster.damage
                monster.health = monster.health - self.damage
                if self.velocity.y > 0: # Moving down; Hit the top side of the monster
                    self.rect.bottom = monster.rect.top
                    self.velocity.y = 0
                    self.onGround = True
                elif self.velocity.y < 0: # Moving up; Hit the bottom side of the monster
                    self.rect.top = monster.rect.bottom
                    self.velocity.y = 0

        self.rect.x += self.velocity.x

        for block in constant.blocks:
            if self.rect.colliderect(block.rect):
                if self.velocity.x > 0: # Moving right; Hit the left side of the block
                    self.rect.right = block.rect.left
                    self.velocity.x = 0
                elif self.velocity.x < 0: # Moving left; Hit the right side of the block
                    self.rect.left = block.rect.right
                    self.velocity.x = 0

        for monster in constant.monsters: # Hit a monster
            if self.rect.colliderect(monster.rect):
                if self.hitTimer <= 0:
                    self.health = self.health - monster.damage
                monster.health = monster.health - self.damage
                if self.velocity.x > 0: # Moving right; Hit the left side of the monster
                    self.rect.right = monster.rect.left
                    self.velocity.x = 0
                elif self.velocity.x < 0: # Moving left; Hit the right side of the monster
                    self.rect.left = monster.rect.right
                    self.velocity.x = 0

        if self.hitTimer > 0:
            self.hitTimer -= 1
        else:
            self.hitTimer = self.maxHitTimer

class Monster(Entity):
    def do_personal_init(self):
        self.add(constant.monsters)
        self.drops = ""
        self.damage = 1

    def check_death(self):
        if self.health <= 0:
            self.kill()
            for player in constant.player:
                player.xp += 1
            self.print_death_log()

    def print_death_log(self):
        print("This is just a method to overwrite!")


class Square(Monster):
    def print_death_log(self):
        print(self.name, "is dead")

#----------------------------------HUD--------------------------------------

class HUD(object):
    def __init__(self, healthMap="Player" + os.sep + "health.map"):
        self.components = pygame.sprite.Group()

        print("HUD Init")

        self.healthPath = "Player" + os.sep + "health.map"
        self.healthMap = loadMapFile(self.healthPath, False)
        self.health = Health(self.healthMap)

        for component in constant.HUDcomponents:
            component.remove(constant.HUDcomponents)
            component.add(self.components)

    def update_components(self):
        for component in self.components:
            component.update()

    def draw_components(self, screen):
        for component in self.components:
            component.draw(screen)

class Health(pygame.sprite.Sprite):
    def __init__(self, healthMap, screenX=928):
        pygame.sprite.Sprite.__init__(self)
        self.add(constant.HUDcomponents)

        self.healthMap = healthMap # Get the healthMap from the main HUD class 
        self.hearts = pygame.sprite.Group()
        self.heart = {}

        self.player = next(iter(constant.player))

        self.heartIterator = 1

        self.parse_health()

    def update(self):
        for heart in self.hearts:
            heart.update() # Update each heart

    def draw(self, screen):
        for heart in self.hearts:
            heart.draw(screen)

    def parse_health(self): # WIP, Find out how many hearts are needed
        x = 0
        y = 0
        lower_boundary = 0
        upper_boundary = 10
        for row in self.healthMap:
            for col in row:
                if col == "H":
                    self.heart[str(self.heartIterator)] = Heart((lower_boundary, upper_boundary), (x, y), self.hearts)
                    self.heartIterator += 1
                x += 32
                lower_boundry = upper_boundary + 1
                upper_boundary += 10
            y += 32

class Heart(pygame.sprite.Sprite):

    def __init__(self, boundary, pos, group):
        pygame.sprite.Sprite.__init__(self)
        self.add(group)
        self.upper_boundary = boundary[1]
        self.lower_boundary = boundary[0]

        self.images = {
            "10"   : pygame.image.load("Images" + os.sep + "health" + os.sep + "full.png"),
            "5"    : pygame.image.load("Images" + os.sep + "health" + os.sep + "half_left.png"),
            "0"    : pygame.image.load("Images" + os.sep + "health" + os.sep + "empty.png"),
        }

        self.image = self.images["10"]
        self.amount = 10
        self.healthAmount = 0
        self.rect = self.image.get_rect()
        self.rect.topright = (pos[0], pos[1])

    def check_image(self):
        if self.lower_boundary <= self.healthAmount < self.upper_boundary:
            tempAmount = self.healthAmount - self.lower_boundary
            if tempAmount > 5:
                self.amount = 5
            elif tempAmount < 5:
                self.amount = 0
            del tempAmount
        elif self.healthAmount < self.lower_boundary:
            self.amount = 0
        elif self.healthAmount > self.upper_boundary:
            self.amount = 10

        x = self.images[str(self.amount)]
        return x

    def update(self):
        for player in constant.player:
            self.healthAmount = player.health
        self.image = self.check_image()

    def draw(self, screen):
        screen.blit(self.image, self.rect)
