# Thanks to Jovito Borges, jovitosanb@gmail.com, http://jovito.icydev.net/
# This is used with his permission from his game, Suicide Runner.

import pygame

class SpriteSheet(object):
    
    def __init__(self, sprite_size, file_path):
        self.image, self.rect = helper.load_image(file_path, -1)
        self.sprite_width, self.sprite_height = sprite_size[0], sprite_size[1]
        self.sprites = self.__set_sprites()
        print(len(self.sprites))
                
    def __set_sprites(self):
        sprites = []
        xpos, ypos = 0, 0
        
        for i in range(0, (self.rect.height - self.sprite_height) + 1, self.sprite_height):
            for j in range(0, (self.rect.width - self.sprite_width) + 1, self.sprite_width):
                self.image.set_clip(pygame.Rect(xpos, ypos, self.sprite_width, self.sprite_height))
                sprite = self.image.subsurface(self.image.get_clip())
                sprites.append(sprite)
                xpos += self.sprite_width
            
            ypos += self.sprite_height
            xpos = 0
        
        return sprites

class Animation(pygame.sprite.Sprite):
    
    def __init__(self, sprites, pos, fps, loop=False):
        pygame.sprite.Sprite.__init__(self)
        
        self.sprites = sprites
        self.sprite_index = 0
        self.image = self.sprites[self.sprite_index]
        
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        
        self.__sprite_lifetime = 1 / fps
        self.__time_passed = 0
        self.loop = loop
        
    def update(self, dt):
        self.__time_passed += dt
        if self.__time_passed > self.__sprite_lifetime:
            if self.sprite_index < len(self.sprites) - 1:
                self.sprite_index += 1
                self.image = self.sprites[self.sprite_index]
            else:
                if self.loop:
                    self.sprite_index = 0
                    self.image = self.sprites[self.sprite_index]
                else:
                    self.kill()
                
            self.__time_passed = 0