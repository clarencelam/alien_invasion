class GameStats:
	""" Tracks statistics for Alien Invasion """
	
	def __init__(self, ai_game):
		""" Initialize game statistics"""
		self.settings = ai_game.settings
		self.reset_stats()

		# Start Alien Invasion in an active state
		self.game_active = False


	def reset_stats(self):
		""" initialize statistics that can change during the game"""
		self.ships_left = self.settings.ship_limit
		self.score = 0

