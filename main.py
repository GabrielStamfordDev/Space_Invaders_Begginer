import pygame
import sys
from settings import Settings
from ship import Ship

# BG_COLOR = (230, 230, 230)

class AlienInvasion():
    def __init__(self):
        pygame.init()
        self.setting = Settings()
        self.screen = pygame.display.set_mode((self.setting.screen_width,self.setting.screen_higth))
        #self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        #self.setting.screen_height = self.screen.get_rect().height
        #self.setting.screen_width = self.screen.get_rect().width
        self.clock  = pygame.time.Clock()
        pygame.display.set_caption("Alien Invasion")
        self.ship = Ship(self)
        # self.bg_color = (230,230,230)
    
    def _check_keydown_events(self,event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
                sys.exit()
                    
    def _check_keyup_events(self,event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _check_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
    
    def _update_screen(self):
        self.screen.fill(self.setting.bg_color)
        self.ship.blit_ship()
        pygame.display.flip()

    def run_game(self):
        while True:
            self._check_event()
            self._update_screen()
            self.ship.update()
            self.clock.tick(60)

if __name__ == "__main__":
    ai = AlienInvasion()
    ai.run_game()

