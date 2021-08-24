import pygame
from pygame.sprite import Sprite   ##importing Sprite class from pygame     ####sprite indicates a two dimensional image
class Bullet(Sprite):   ##Bullet class inherits from Sprite class    ###### Sprite class is used so that we can group all related elements and act on all elements at once
	def __init__(self,ai_game):  ## self argument and AI calss instance
		super().__init__()   ##to inherit Sprite class
		self.screen=ai_game.screen  ## create screen attribute 
		self.settings=ai_game.settings  ##create settings attribute
		self.color=self.settings.bullet_color  ## assign bullet_color to color attribute
		self.rect=pygame.Rect(0,0,self.settings.bullet_width,self.settings.bullet_height)   ##bullet is not an image so we have to use pygame.RECT()class and assign it to rect 
										###initially x and y coordinates of top left corner is set to 0,0 and width,height attributes from settings class
		self.rect.midtop=ai_game.ship.rect.midtop   ##bullet position depends on the ship position
											##bullet emerges from the top of the ship
		self.y=float(self.rect.y)   ##decimal value for y_coordinate

	def update(self):   ##update method manages bullet's position
		self.y-=self.settings.bullet_speed ##when a bullet is fired , it moves up the screen .So it's y-coordinate decreases
		self.rect.y=self.y  ##assign y value to bullet rect attribute y

		##even if the ship moves, the bullet x-coordinate doesn't change , it moves vertically

	def draw_bullet(self):  ##to draw the bullet
		pygame.draw.rect(self.screen,self.color,self.rect)   ##fills the part of the scrren defined by bullet's rect with color