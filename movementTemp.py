    def handleMovement(self):
        #Capturing and Responding to Keys
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            self.move(-2, 0)
        if key[pygame.K_RIGHT]:
            self.move(2, 0)
        if key[pygame.K_UP]:
            self.move(0, -6)
        if key[pygame.K_DOWN]:
            self.move(0, 2)

        if self.gravity:
            self.move(0, 6)
        if key[pygame.K_UP] and self.gravity:
            self.move(0, -6)

    def move_y(self, dy):

        # Move the rect
        self.rect.y += dy

        # If you collide with a block, reset the position to the edge of the block
        for block in constant.blocks:
            if self.rect.colliderect(block.rect):
                if dy > 0: # Moving down; Hit the left side of the block
                    self.rect.bottom = block.rect.top
                elif dy < 0: # Moving up; Hit the right side of the block
                    self.rect.top = block.rect.bottom

        for monster in constant.monsters: # Hit a monster
            if self.rect.colliderect(monster.rect):
                self.health = self.health - monster.damage
                monster.health = monster.health - self.damage
                if dy > 0: # Moving down; Hit the left side of the monster
                    self.rect.bottom = monster.rect.top
                elif dy < 0: # Moving up; Hit the right side of the monster
                    self.rect.top = monster.rect.bottom

    def move_x(self, dx):

        # Move the rect
        self.rect.x += dx

        # If you collide with a block, reset the position to the edge of the block
        for block in constant.blocks:
            if self.rect.colliderect(block.rect):
                if dx > 0: # Moving right; Hit the left side of the block
                    self.rect.right = block.rect.left
                elif dx < 0: # Moving left; Hit the right side of the block
                    self.rect.left = block.rect.right

        for monster in constant.monsters: # Hit a monster
            if self.rect.colliderect(monster.rect):
                self.health = self.health - monster.damage
                monster.health = monster.health - self.damage
                if dx > 0: # Moving right; Hit the left side of the monster
                    self.rect.right = monster.rect.left
                elif dx < 0: # Moving left; Hit the right side of the monster
                    self.rect.left = monster.rect.right





    def handleMovement(self):

        if not self.directionPicked:
            self.direction = random.randint(1, 100) #Randomly picking a direction
            self.moveNumber = 60 # Total Number of frames for one movement action
            self.moveInterval = random.randint(30, 55) # Number of frames to wait between moving

        if self.direction > 50 and self.moveNumber > self.moveInterval:
            self.velocity.x = -2
            self.velocity.y = 0
            self.move()
            self.directionPicked = True
            self.direction = 51
            self.moveNumber -= 1

        elif self.direction <= 50 and self.moveNumber > self.moveInterval:
            self.velocity.x = 2
            self.velocity.y = 0
            self.move()
            self.directionPicked = True
            self.direction = 49
            self.moveNumber -= 1

        elif self.moveNumber <= self.moveInterval and self.moveNumber > 0:
            self.moveNumber -= 1

        elif self.moveNumber <= 0:
            self.directionPicked = False






    def move(self):
        # Move each axis separately. Note that this checks for collisions both times.
        self.move_x()
        self.move_y()

    def move_x(self):

        # Move the rect
        self.rect.x += self.velocity.x

        # If you collide with a block, reset the position to the edge of the block
        for block in constant.blocks:
            if self.rect.colliderect(block.rect):
                if self.velocity.x > 0: # Moving right; Hit the left side of the block
                    self.rect.right = block.rect.left
                    self.velocity.x = 0
                elif self.velocity.x < 0: # Moving left; Hit the right side of the block
                    self.rect.left = block.rect.right
                    self.velocity.x = 0


    def move_y(self):

        # Move the rect
        self.rect.y += self.gravity
        self.rect.y += self.velocity.y

        # If you collide with a block, reset the position to the edge of the block
        for block in constant.blocks:
            if self.rect.colliderect(block.rect):
                if self.velocity.y > 0: # Moving down; Hit the top side of the block
                    self.rect.bottom = block.rect.top
                    self.velocity.y = 0
                elif self.velocity.y < 0: # Moving up; Hit the bottom side of the block
                    self.rect.top = block.rect.bottom
                    self.velocity.y = 0