import pygame, random, os, math

import constant

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
        self.gravity = 1
        self.canJump = True
        self.ableToDJ = True
        self.doubleJump = True

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
        self.velocity.y = -16
        self.onGround = False
        if self.ableToDJ:
            self.doubleJump = True
        else:
            self.doubleJump = False

    def double_jump(self):
        self.velocity.y = -16
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

        print(self.health, "1")

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
                self.health = self.health - monster.damage
                monster.health = monster.health - self.damage
                if self.velocity.x > 0: # Moving right; Hit the left side of the monster
                    self.rect.right = monster.rect.left
                    self.velocity.x = 0
                elif self.velocity.x < 0: # Moving left; Hit the right side of the monster
                    self.rect.left = monster.rect.right
                    self.velocity.x = 0

        self.HUD.update()

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
    def __init__(self):
        self.Health = Health()
        self.components = pygame.sprite.Group()
        for component in constant.HUDcomponents:
            component.remove(constant.HUDcomponents)
            component.add(self.components)

    def update(self):
        for component in self.components:
            component.update()


class Health(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.add(constant.HUDcomponents)
        print("HEALTH INIT")

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
        x = str(math.floor(self.amount / 10.0) * 10)
        y = self.images[x]
        print(x, "2")
        return y

    def update(self):
        for player in constant.player:
            self.amount = player.health
        self.check_image()