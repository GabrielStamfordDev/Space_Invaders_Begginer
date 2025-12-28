import pygame
from settings import Settings

class Ship():
    def __init__(self, ai_game):
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.screen_rect.midbottom
        self.moving_right = False
        self.moving_left = False
        self.setting = Settings()
        self.x = float(self.rect.x)
    
    def blit_ship(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        if self.moving_right and (self.rect.right < self.screen_rect.right):
            self.x += self.setting.ship_speed # I tried a float number, but it didn't work
        if self.moving_left and (self.rect.left > 0):
            self.x -= self.setting.ship_speed
        self.rect.x = self.x