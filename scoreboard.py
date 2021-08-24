import pygame.font
from pygame.sprite import Group ##to create a group of ships to display
from ship import Ship 
class Scoreboard:
	def __init__(self,ai_game):
		self.ai_game=ai_game
		self.screen=ai_game.screen
		self.screen_rect=self.screen.get_rect()
		self.settings=ai_game.settings
		self.stats=ai_game.stats

		self.text_color=(30,30,30)
		self.font=pygame.font.SysFont(None,48)
		self.prep_score()	
		self.prep_high_score()
		self.prep_level()
		self.prep_ships()

	def prep_score(self):
		rounded_score=round(self.stats.score,-1)  ##round function rounds a decimal number to a set number of decimal places given as second argument.
		##Negative number as second argument wii round value to nearest 10,100,1000 so on
		score_str="{:,}".format(rounded_score) ##rurning numerical value score into a string
		self.score_image=self.font.render(score_str,True,self.text_color,self.settings.bg_color)  ##render text to image
		self.score_rect=self.score_image.get_rect()
		self.score_rect.right=self.screen_rect.right-20  ## positioning the score at top right corner , setting it's right edge 20 pixels from right edge of the screen
		self.score_rect.top=20  ##top edge down 20 pixels from topof the screen

	def show_score(self):
		self.screen.blit(self.score_image,self.score_rect)
		self.screen.blit(self.high_score_image,self.high_score_rect)
		self.screen.blit(self.level_image,self.level_image_rect)
		self.ships.draw(self.screen)

	def prep_high_score(self):
		high_score=round(self.stats.high_score,-1)
		high_score_str="{:,}".format(high_score)
		self.high_score_image=self.font.render(high_score_str,True,self.text_color,self.settings.bg_color)
		self.high_score_rect=self.high_score_image.get_rect()
		self.high_score_rect.centerx=self.screen_rect.centerx
		self.high_score_rect.top=self.score_rect.top

	def check_high_score(self):
		if self.stats.score > self.stats.high_score:
			self.stats.high_score=self.stats.score 
			self.prep_high_score()

	def prep_level(self):
		level_str=str(self.stats.level)
		self.level_image=self.font.render(level_str,True,self.text_color,self.settings.bg_color)
		self.level_image_rect=self.level_image.get_rect()
		self.level_image_rect.right=self.score_rect.right
		self.level_image_rect.top=self.score_rect.bottom+10

	def prep_ships(self):
		self.ships=Group()
		for ship_number in range(self.stats.ships_left):  ##to display the number of ships left for player
			ship=Ship(self.ai_game)
			ship.rect.x=10 + ship_number * ship.rect.width
			ship.rect.y=10
			self.ships.add(ship)  ##adding ships to the group



