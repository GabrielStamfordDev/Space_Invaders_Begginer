import pygame
import sys
import time
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
# BG_COLOR = (230, 230, 230)

class AlienInvasion():
    def __init__(self):
        pygame.init()
        self.setting = Settings()
        self.playing = False
        self.screen = pygame.display.set_mode((self.setting.screen_width,self.setting.screen_higth))
        #self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        #self.setting.screen_height = self.screen.get_rect().height
        #self.setting.screen_width = self.screen.get_rect().width
        self.clock  = pygame.time.Clock()
        pygame.display.set_caption("Alien Invasion")
        self.stats = GameStats(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens  = pygame.sprite.Group()
        self.play_button = Button(self, "Play")
        self.create_fleet()
        # self.bg_color = (230,230,230)
    
    def create_alien(self, x_pos, y_pos):
        new_alien = Alien(self)
        new_alien.x = x_pos
        new_alien.rect.x = x_pos
        new_alien.rect.y = y_pos
        self.aliens.add(new_alien)

    def check_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self.change_fleet_direction()
                break
    
    def change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.setting.fleet_y_speed
        self.setting.fleet_direction *= -1

    def create_fleet(self):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        current_x, current_y = alien.rect.width, alien.rect.height
        while current_y < (self.setting.screen_higth - 3 * alien_height):
            while current_x < (self.setting.screen_width - 2 * alien_width):
                self.create_alien(current_x, current_y)
                current_x += 2 * alien_width
            current_x = alien_width
            current_y += 2 * alien_height

    def update_aliens(self):
        self.check_edges()
        self.aliens.update()
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self.ship_hit()
        self.aliens_check_bottom()

    def aliens_check_bottom(self):
        for alien in self.aliens:
            if alien.rect.bottom >= self.setting.screen_higth:
                self.ship_hit()
                break

    def ship_hit(self):
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.bullets.empty()
            self.aliens.empty()
            self.create_fleet()
            self.ship.center_ship()

            time.sleep(1)
        else:
            self.playing = False

    def fire_bullet(self):
        if len(self.bullets) < self.setting.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _check_keydown_events(self,event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
                sys.exit()
        elif event.key == pygame.K_SPACE:
            self.fire_bullet()

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
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blit_ship()
        self.aliens.draw(self.screen)
        if not self.playing:
            self.play_button.draw_button()
        pygame.display.flip()

    def update_bullet(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, False, True) # True arguments say who is gonna disapear when colission happens
        if not self.aliens:
            self.bullets.empty()
            self.create_fleet()
    def run_game(self):
        while True:
            self._check_event()
            if self.playing:
                self.ship.update()
                self.update_bullet()
                self.update_aliens()
            self._update_screen()
            self.clock.tick(60)

if __name__ == "__main__":
    ai = AlienInvasion()
    ai.run_game()

