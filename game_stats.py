class GameStats():
    def __init__(self, ai_game):
        self.setting = ai_game.setting
        self.max_score = 0
        self.reset()

    def reset(self):
        self.ships_left = self.setting.ship_limit
        self.score = 0
        self.level = 1
