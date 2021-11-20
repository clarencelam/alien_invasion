class Settings:
	""" A class to store all settings for Alien Invasion """

	def __init__(self):
		"""initialize the game settings"""
		# Screen Settings
		self.screen_width = 1600
		self.screen_height = 1000
		self.bg_color = (100,100,100)

		# Ship settings
		self.ship_speed = 3
		self.ship_limit = 3
		
		# Bullet Settings 
		self.bullet_speed = 12.0
		self.bullet_width = 10
		self.bullet_height = 50
		self.bullet_color = (10, 200, 10)
		self.bullets_allowed = 5

		# Alien Settings
		self.alien_speed = 1
		self.fleet_drop_speed = 1
		# fleet direction of 1 = going right (forward)
		self.fleet_direction = 1      

		# Game difficulty adding
		self.speedup_scale = 1.1

		# Alien score addding
		self.score_scale = 1.5

		self.initialize_dynamic_settings()

	def initialize_dynamic_settings(self):
		"""initialize settings that will change throughout the game"""
		self.bullet_speed = 2.0
		self.alien_speed = 1.0
		self.alien_points = 50

	def increase_speed(self):
		""" increase speed settings """
		#self.ship_speed *= self.speedup_scale
		self.bullet_speed *= self.speedup_scale
		self.alien_speed *= self.speedup_scale

		self.alien_points = int(self.alien_points * self.score_scale)
