import pygame

class Ship:
	""" A class to manage the ship object"""

	def __init__(self, ai_game):
		"""initalize a ship and its starting position"""
		self.screen = ai_game.screen
		self.settings = ai_game.settings
		self.screen_rect = ai_game.screen.get_rect()

		# Load the ship image and get its rect
		shipimg = pygame.image.load('images/ship.bmp')
		self.image = pygame.transform.scale(shipimg, (100, 100))

		self.rect = self.image.get_rect()

		# Start each new ship at the bottom center of the screen
		self.rect.midbottom = self.screen_rect.midbottom

		# Store a decimal value for the ship's horizontal position.
		self.x = float(self.rect.x)

		# Movement Flag
		self.moving_right = False
		self.moving_left = False

	def update(self):
		"""update the ship's position based on the movement flag"""
		# Update the ship's X value, not the rect
		if self.moving_right and self.rect.right < self.screen_rect.right:
			self.x += self.settings.ship_speed
		if self.moving_left and self.rect.left > 0:
			self.x -= self.settings.ship_speed

		# Update rect object from self.x===
		self.rect.x = self.x

	def blitme(self):
		"""Draw the ship at its current position"""
		self.screen.blit(self.image, self.rect)