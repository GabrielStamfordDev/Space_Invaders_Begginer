import pygame
import sys
from settings import Settings

# BG_COLOR = (230, 230, 230)

class AlienInvasion():
    def __init__(self):
        pygame.init()
        self.setting = Settings()
        self.screen = pygame.display.set_mode((self.setting.screen_width,self.setting.screen_higth))
        self.clock  = pygame.time.Clock()
        pygame.display.set_caption("Alien Invasion")
        # self.bg_color = (230,230,230)
    def run_game(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            self.screen.fill(self.setting.bg_color)
            pygame.display.flip()
            self.clock.tick(60)

if __name__ == "__main__":
    ai = AlienInvasion()
    ai.run_game()

