class Settings:
	""" A class to store all settings for Alien Invasion """

	def __init__(self):
		"""initialize the game settings"""
		# Screen Settings
		self.screen_width = 1600
		self.screen_height = 1000
		self.bg_color = (100,100,100)

		# Ship settings
		self.ship_speed = 1.5
		
		# Bullet Settings 
		self.bullet_speed = 2.0
		self.bullet_width = 1
		self.bullet_height = 15
		self.bullet_color = (60, 60, 60)
		self.bullets_allowed = 50

		# Alien Settings
		self.alien_speed = 3.0
		self.fleet_drop_speed = 10
		# fleet direction of 1 = going right (forward)
		self.fleet_direction = 1                                                                                                                                                                                                                                                                   
		