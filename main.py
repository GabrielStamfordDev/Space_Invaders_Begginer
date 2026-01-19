import pygame
import sys
import time
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
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
        self.sb = Scoreboard(self)
        self.difficulty = 'medium'
        self.button_color_inactive = (0,0,0)
        self.button_color_active   = (0,255,0) 
        self.play_button = Button(self, "Play (P)")
        self.easy_button = Button(self, "Easy (1)")
        self.medium_button = Button(self, "Medium (2)")
        self.hard_button = Button(self, "Hard (3)")
        # Posiciona os botões de dificuldade abaixo do botão Play
        base_y = self.play_button.rect.bottom + 20 # 20px abaixo do Play
        
        # Easy (Esquerda)
        self.easy_button.rect.y = base_y
        self.easy_button.rect.right = self.play_button.rect.left - 10
        self.easy_button.save_msg("Easy (1)") # Atualiza posição do texto

        # Medium (Centro, abaixo do play)
        self.medium_button.rect.y = base_y
        self.medium_button.rect.centerx = self.screen.get_rect().centerx
        self.medium_button.save_msg("Medium (2)")

        # Hard (Direita)
        self.hard_button.rect.y = base_y
        self.hard_button.rect.left = self.play_button.rect.right + 10
        self.hard_button.save_msg("Hard (3)")

        # Atualiza as cores iniciais
        self._update_difficulty_visuals()
        self.create_fleet()
        # self.bg_color = (230,230,230)
    
    def _update_difficulty_visuals(self):
        """Atualiza a cor dos botões com base na seleção atual."""
        
        # Reseta todos para a cor inativa
        self.easy_button.update_color(self.button_color_inactive, "Easy (1)")
        self.medium_button.update_color(self.button_color_inactive, "Medium (2)")
        self.hard_button.update_color(self.button_color_inactive, "Hard (3)")

        # Ilumina apenas o selecionado
        if self.difficulty == 'easy':
            self.easy_button.update_color(self.button_color_active, "Easy (1)")
        elif self.difficulty == 'medium':
            self.medium_button.update_color(self.button_color_active, "Medium (2)")
        elif self.difficulty == 'hard':
            self.hard_button.update_color(self.button_color_active, "Hard (3)")

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
        self.stats.ships_left -= 1
        if self.stats.ships_left > 0:
            self.bullets.empty()
            self.aliens.empty()
            self.create_fleet()
            self.ship.center_ship()
            self.sb.prep_ships()
            time.sleep(1)
        else:
            self.sb.prep_ships()
            self.playing = False
            pygame.mouse.set_visible(True)

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
        elif event.key == pygame.K_p:
            self.start_game()
        if event.key == pygame.K_1:
            self.difficulty = 'easy'
            self._update_difficulty_visuals()
        elif event.key == pygame.K_2:
            self.difficulty = 'medium'
            self._update_difficulty_visuals()
        elif event.key == pygame.K_3:
            self.difficulty = 'hard'
            self._update_difficulty_visuals()
        elif event.key == pygame.K_SPACE:
            self.fire_bullet()

    def _check_keyup_events(self, event):
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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
                if self.easy_button.rect.collidepoint(mouse_pos):
                    self.difficulty = 'easy'
                    self._update_difficulty_visuals()
                elif self.medium_button.rect.collidepoint(mouse_pos):
                    self.difficulty = 'medium'
                    self._update_difficulty_visuals()
                elif self.hard_button.rect.collidepoint(mouse_pos):
                    self.difficulty = 'hard'
                    self._update_difficulty_visuals()

    def _check_play_button(self, mouse_pos):
        if self.play_button.rect.collidepoint(mouse_pos) and not self.playing:
            self.setting.inicialize(self.difficulty)
            self.stats.reset()
            self.playing = True
            self.bullets.empty()
            self.aliens.empty()
            self.create_fleet()
            self.ship.center_ship()
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
            pygame.mouse.set_visible(False)

    def start_game(self):
        if not self.playing:
            self.setting.inicialize(self.difficulty)
            self.stats.reset()
            self.playing = True
            self.bullets.empty()
            self.aliens.empty()
            self.create_fleet()
            self.ship.center_ship()
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
            pygame.mouse.set_visible(False)
    
    def _update_screen(self):
        self.screen.fill(self.setting.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blit_ship()
        self.aliens.draw(self.screen)
        self.sb.show_score()
        if not self.playing:
            self.play_button.draw_button()
            self.easy_button.draw_button()
            self.medium_button.draw_button()
            self.hard_button.draw_button()
        pygame.display.flip()

    def update_bullet(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, False, True) # True arguments say who is gonna disapear when colission happens
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.setting.score_alien * len(aliens)
            self.sb.prep_score()
            self.sb.check_max_score()
        if not self.aliens:
            self.bullets.empty()
            self.create_fleet()
            self.setting.increase_difficult()
            self.stats.level += 1
            self.sb.prep_level()

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

