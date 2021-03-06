import pygame.font
import json

from pygame.sprite import Group
from ship import Ship

class Scoreboard:

	def __init__(self, ai_game):
		""" initialize scoreboard attributes"""
		self.ai_game = ai_game
		self.screen = ai_game.screen
		self.screen_rect = self.screen.get_rect()
		self.settings = ai_game.settings
		self.stats = ai_game.stats

		# Font settings for scoring info
		self.text_color = (30,30,30)
		self.font = pygame.font.SysFont(None, 48)

		# prep score image
		self.prep_score()
		self.prep_high_score()
		self.prep_level()
		self.prep_ships()

	def prep_high_score(self):
		high_score = round(self.stats.high_score, -1)
		high_score_str = "{:,}".format(high_score)
		self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.settings.bg_color)

		# Center the score at top
		self.high_score_rect = self.high_score_image.get_rect()
		self.high_score_rect.centerx = self.screen_rect.centerx
		self.high_score_rect.top = self.score_rect.top

	def prep_score(self):
		""" turn score into an image"""
		rounded_score = round(self.stats.score, -1)
		score_str = "{:,}".format(rounded_score)
		self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color)

		# Display the score at the top right of the screen
		self.score_rect = self.score_image.get_rect()
		self.score_rect.right = self.screen_rect.right - 20
		self.score_rect.top = 20

	def prep_level(self):
		""" Turn the level into a rendered image """
		level_str = str(self.stats.level)
		self.level_image = self.font.render("Level: " + level_str, True, self.text_color,self.settings.bg_color)

		# Position the level below the score
		self.level_rect = self.level_image.get_rect()
		self.level_rect.right = self.score_rect.right
		self.level_rect.top = self.score_rect.bottom + 10

	def prep_ships(self):
		""" Show how many ships are left """
		self.ships = Group()
		for ship_number in range(self.stats.ships_left):
			ship = Ship(self.ai_game)
			ship.rect.x = 10 + ship_number * ship.rect.width
			ship.rect.y = 10
			self.ships.add(ship)

	def show_score(self):
		""" Draw score to screen """
		self.screen.blit(self.score_image, self.score_rect)
		self.screen.blit(self.high_score_image, self.high_score_rect)
		self.screen.blit(self.level_image, self.level_rect)
		self.ships.draw(self.screen)

	def check_high_score(self):
		""" check to see if theres a new high score, set as high score"""
		if self.stats.score > self.stats.high_score:
			self.stats.high_score = self.stats.score
			self.write_high_score_to_file()
			self.prep_high_score()

	def write_high_score_to_file(self):
		new_highscore = self.stats.score 

		highscorefile = 'highscore.json'
		with open(highscorefile, 'w') as hsfile:
			json.dump(new_highscore, hsfile)