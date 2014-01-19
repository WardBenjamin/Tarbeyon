#----------------------------------HUD--------------------------------------

class HUD(object):
    def __init__(self, healthMap="Player" + os.sep + "health.map"):
        self.components = pygame.sprite.Group()
        for component in constant.HUDcomponents:
            component.remove(constant.HUDcomponents)
            component.add(self.components)

        self.healthPath = "Player" + os.sep + "health.map"
        self.healthMap = loadMapFile(self.healthPath, False)
        self.health = Health(self.healthMap)

    def update(self):
        for component in self.components:
            component.update()

    def draw(self, screen):
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
                    self.heart[str(self.heartIterator)] = Heart((lower_boundary, upper_boundary), (x, y))
                    self.heartIterator += 1
                x += 32
                lower boundry = upper_boundary + 1
                upper_boundary += 10
            y += 32

class Heart(pygame.sprite.Sprite):

    def __init__(self, boundary, pos):
        pygame.sprite.Sprite.__init__(self)

        self.upper_boundary = boundary[1]
        self.lower_boundary = boundary[0]

        self.images = {
            "10"   : pygame.image.load("Images" + os.sep + "health" + os.sep + "full.png"),
            "5"    : pygame.image.load("Images" + os.sep + "health" + os.sep + "half_left.png"),
            "0"    : pygame.image.load("Images" + os.sep + "health" + os.sep + "empty.png"),
        }

        self.image = self.images["10"]
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
        elif amount < self.lower_boundary:
            self.amount = 0
        elif amount > self.upper_boundary:
            self.amount = 10

        x = self.images[str(self.amount)]
        return x

    def update(self):
        for health in constant.player:
            self.healthAmount = player.health
        self.image = self.check_image()

    def draw(self, screen):
        screen.blit(self.image, self.rect)