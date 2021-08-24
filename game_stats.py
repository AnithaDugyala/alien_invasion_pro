class GameStats:
	def __init__(self,ai_game):
		self.settings=ai_game.settings
		self.ships_left=self.settings.ship_limit
		self.game_active=False   ##start the game in inactive state initially
		self.score=0
		self.level=1
		self.high_score=0  ##high score should be never reset so we are placing in __init__method

	def reset_stats(self):
		self.ships_left=self.settings.ship_limit
		self.score=0  ##initializes to 0 after each game starts
		self.level=1  ##to reset the level for every new start of game