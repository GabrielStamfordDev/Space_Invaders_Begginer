class GameStats():
    def __init__(self, ai_game):
        self.setting = ai_game.setting
        self.reset()

    def reset(self):
        self.ships_left = self.setting.ship_limit