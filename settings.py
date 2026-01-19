class Settings():
    def __init__(self):
        self.bg_color = (230,230,230)
        self.screen_width = 1200
        self.screen_higth = 700
        #self.screen_width = 0
        #self.screen_height = 0
        self.ship_limit = 1
        self.bullet_height = 13
        self.bullet_width  = 200
        self.bullet_color  = (60,60,60)  
        self.bullets_allowed = 5
        self.fleet_y_speed = 10
        self.scale_difficult = 1.1
        self.scale_score = 1.5
        self.inicialize('medium')

    def inicialize(self, difficult):
        self.fleet_direction = 1 
        if difficult == 'easy':   
            self.ship_speed = 1.5
            self.bullet_speed = 2.5
            self.alien_speed = 1
            self.score_alien = 50
        elif difficult == 'medium':
            self.ship_speed = 2.0
            self.bullet_speed = 3.0
            self.alien_speed = 1.5
            self.score_alien = 75
        elif difficult == 'hard':
            self.ship_speed = 3.0
            self.bullet_speed = 4.0
            self.alien_speed = 2.5
            self.score_alien = 100
 
    def increase_difficult(self):
        self.ship_speed *= self.scale_difficult
        self.bullet_speed *= self.scale_difficult
        self.alien_speed *= self.scale_difficult
        self.score_alien = int(self.score_alien * self.scale_score)
        # print(self.score_alien, self.alien_speed)
