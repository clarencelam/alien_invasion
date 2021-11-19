import sys, pygame

from time import sleep

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from diff_buttons import DiffButton
from scoreboard import Scoreboard

class AlienInvasion:
	"""overall class to manage game assets & behavior."""

	def __init__(self):
		"""initialize a game, create game resoures"""
		pygame.init()

		self.settings = Settings()

		self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
		self.screen_rect = self.screen.get_rect()

		self.settings.screen_width = self.screen.get_rect().width
		self.settings.screen_height = self.screen.get_rect().height #this code exists so we can use the screen's rect width/height to know what the screen width/height ends up being
			#(self.settings.screen_width, self.settings.screen_height))
		pygame.display.set_caption("Alien Invasion")

		# Create an instance to store game statistics
		self.stats = GameStats(self)
		self.scoreboard = Scoreboard(self)

		self.ship = Ship(self)
		self.bullets = pygame.sprite.Group()
		self.aliens = pygame.sprite.Group()

		self._create_fleet()

		# Make the Play button
		self.play_button = Button(self,"Play")

		# Make difficulty buttons
		self.hard_difficulty = DiffButton(self,"HARD MODE", 300, (self.screen_rect.height /2) - 100)
		self.med_difficulty = DiffButton(self,"REGULAR MODE", 300, (self.screen_rect.height /2))
		self.easy_difficulty = DiffButton(self,"EASY MODE", 300, (self.screen_rect.height /2) + 100)


	def run_game(self):
		""" start the main loop for the game"""
		while True:
			self._check_events()

			if self.stats.game_active:
				self.ship.update()
				self._update_bullets()
				self._update_aliens()
			
			self._update_screen()

	def _check_events(self):
		"""respond to keypresses and mouse events"""
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.ext()
			elif event.type == pygame.KEYDOWN:
				self._check_keydown_events(event)
			elif event.type == pygame.KEYUP:
				self._check_keyup_events(event)
			elif event.type == pygame.MOUSEBUTTONDOWN:
				mouse_pos = pygame.mouse.get_pos() # get and store mouse position
				self._check_play_button(mouse_pos)
				self._check_difficulty_buttons(mouse_pos)

	def _check_play_button(self, mouse_pos):
		""" Start a new game when the player clicks Play"""
		button_clicked = self.play_button.rect.collidepoint(mouse_pos)
		if button_clicked and not self.stats.game_active:
			self._start_game()

	def _check_difficulty_buttons(self, mouse_pos):
		""" change difficulty settings when buttons are clicked"""
		hard_button_clicked = self.hard_difficulty.rect.collidepoint(mouse_pos)
		med_button_clicked = self.med_difficulty.rect.collidepoint(mouse_pos)
		ez_button_clicked = self.easy_difficulty.rect.collidepoint(mouse_pos)

		if hard_button_clicked and not self.stats.game_active:
			self.settings.speedup_scale = 3
			print("hard clicked")
		if med_button_clicked and not self.stats.game_active:
			self.settings.speedup_scale = 1.4
		if ez_button_clicked and not self.stats.game_active:
			self.settings.speedup_scale = 1.1

	def _start_game(self):
		# Reset the game stats
		self.settings.initialize_dynamic_settings()
		self.stats.reset_stats()
		self.stats.game_active = True
		self.scoreboard.prep_score()
		self.scoreboard.prep_level()

		# Get rid of any remaining aliens / bullets
		self.aliens.empty()
		self.bullets.empty()

		# Create a new fleet and center the ship
		self._create_fleet
		self.ship.center_ship()

		# Hide mouse cursor
		pygame.mouse.set_visible(False)

	def _check_keydown_events(self, event):
		"""respond to key press-down events"""
		if event.key == pygame.K_RIGHT:
			self.ship.moving_right = True
		elif event.key == pygame.K_LEFT:
			self.ship.moving_left = True
		elif event.key == pygame.K_SPACE:
			self._fire_bullet()
		elif event.key == pygame.K_p:
			self._start_game()
		elif event.key == pygame.K_q:
			sys.exit()

	def _check_keyup_events(self, event):
		"""responds to key-up / key release events"""
		if event.key == pygame.K_RIGHT:
			self.ship.moving_right = False
		elif event.key == pygame.K_LEFT:
			self.ship.moving_left = False

	def _create_fleet(self):
		""" Create the fleet of aliens """
		# Make an Alien and find the number of aliens in a row
		# Spacing between each alien is equal to one alien width
		alien = Alien(self)
		alien_height = alien.rect.height
		alien_width = alien.rect.width
		available_space_x = self.settings.screen_width - (2 * alien_width)
		number_aliens_x = available_space_x // (2 * alien_width)

		# Determine the number of rows of aliens that fit on the screen
		ship_height = self.ship.rect.height 
		available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)

		number_rows = available_space_y // (2 * alien_height)

		# Create the fleet of aliens.
		for row_number in range(number_rows):
			for alien_number in range(number_aliens_x):
				# Create an alien and place it in the row
				self._create_alien(alien_number, row_number)

	def _create_alien(self, alien_number, row_number):
		# Create an alien and place it in the row
		alien = Alien(self)
		alein_height = alien.rect.height
		alien_width = alien.rect.width
		alien.x = alien_width + 2 * alien_width * alien_number
		alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number 
		alien.rect.x = alien.x 
		self.aliens.add(alien) 

	def _check_fleet_edges(self):
		""" Respond appropriately if any aliens touched the edge"""
		for alien in self.aliens.sprites():
			if alien.check_edges():
				self._change_fleet_direction()
				break

	def _change_fleet_direction(self):
		""" Drop the alien fleet and change directions""" 
		for alien in self.aliens.sprites():
			alien.rect.y += self.settings.fleet_drop_speed
		self.settings.fleet_direction = self.settings.fleet_direction * -1 #when the alien hits the edge, the fleet direction is shifted

	def _fire_bullet(self):
		""" function to fire bullet from ship """
		if len(self.bullets) < self.settings.bullets_allowed:
			new_bullet = Bullet(self) #making a bullet instance
			self.bullets.add(new_bullet)

	def _check_bullet_alien_collisions(self):
		""" Respond to bullet-alien collisions"""
		collisions = pygame.sprite.groupcollide(self.bullets,self.aliens,False,True)

		if collisions:
			for aliens in collisions.values(): #collisions store bullets as keys in collisions dictionaries
				self.stats.score += self.settings.alien_points * len(aliens)
			self.scoreboard.prep_score()
			self.scoreboard.check_high_score()

		if not self.aliens:
			# destroy existing bullets and create new fleet
			# not -> True if the statement is False, Flase if statement is True
			self.bullets.empty()
			self._create_fleet()
			self.settings.increase_speed()

			self.stats.level += 1
			self.scoreboard.prep_level()

	def _ship_hit(self):
		""" Respond to the ship being hit by an alien"""
		if self.stats.ships_left > 0:
			# Decreemnt ships_left
			self.stats.ships_left -= 1

			# Get rid of any remaining bullets & aliens
			self.aliens.empty()
			self.bullets.empty()

			# Create a new fleet and center the ship
			self._create_fleet()
			self.ship.center_ship()

			# Pause
			sleep(0.5)
		else:
			self.stats.game_active = False
			# Bring the mouse cursor back to navigate menu
			pygame.mouse.set_visible(True)


	def _update_bullets(self):
		""" Update the position of bullets and get rid of old bullets"""
		# Update bullet positions
		self.bullets.update()

		# Get rid of bullets that have hit the top of the screen
		for bullet in self.bullets.copy(): # we can't use the real bullets list because python expects a list to stay the same when a loop is running
			if bullet.rect.bottom <= 0:
				self.bullets.remove(bullet)

		self._check_bullet_alien_collisions()

	def _check_aliens_bottom(self):
		""" check if any aliens hae reached the bottom of the ship."""
		screen_rect = self.screen.get_rect()
		for alien in self.aliens.sprites():
			if alien.rect.bottom >= screen_rect.bottom:
				# Treat this like the ship got hit
				self._ship_hit()
				break

	def _update_aliens(self):
		""" check if the Fleet is at an edge. Then update positions of all aliens in the fleet"""
		self._check_fleet_edges()
		self.aliens.update()

		# Look for alien-ship collisions
		if pygame.sprite.spritecollideany(self.ship, self.aliens):
			self._ship_hit()
		self._check_aliens_bottom()

	def _update_screen(self):
		"""update images on the screen, and flip to the new screen"""
		self.screen.fill(self.settings.bg_color)
		self.ship.blitme()
		for bullet in self.bullets.sprites():
			bullet.draw_bullet()
		self.aliens.draw(self.screen)

		# Draw the scoreboard
		self.scoreboard.show_score()

		# Draw the play button if the game is inactive
		if not self.stats.game_active:
			self.play_button.draw_button()
			self.easy_difficulty.draw_button()
			self.med_difficulty.draw_button()
			self.hard_difficulty.draw_button()

		# make the most recently drawn screen visible
		pygame.display.flip() 


			
if __name__ == '__main__':
	# Make a game instance, and run the game
	ai = AlienInvasion()
	ai.run_game()

