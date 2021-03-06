import pygame.font

class DiffButton:

	def __init__(self, ai_game, msg, x, y):
		""" pygame doesn't have a button method so we're creating one
		msg will be the button's text"""

		self.screen = ai_game.screen
		self.screen_rect = self.screen.get_rect()

		# Set dimensions and properties of the button
		self.width, self.height = 300,50
		self.text_color = (255,255,255)
		self.button_color = (0,255,0)
		self.font = pygame.font.SysFont(None, 48)

		# Build the button's rect object and center
		self.rect = pygame.Rect(x,y, self.width,self.height)
		#self.rect.center = self.screen_rect.center

		# The button message needs to be prepped once
		self._prep_msg(msg)

	def _prep_msg(self,msg):
		""" turn msg into a rendered image and center text on the button"""
		self.msg_image = self.font.render(msg,True,self.text_color,self.button_color)
		self.msg_image_rect = self.msg_image.get_rect()
		self.msg_image_rect.center = self.rect.center

	def draw_button(self):
		# Draw blank button and draw message onto it
		self.screen.fill(self.button_color, self.rect)
		self.screen.blit(self.msg_image, self.msg_image_rect)