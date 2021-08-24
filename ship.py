import pygame
from pygame.sprite import Sprite
class Ship(Sprite):
	def __init__(self,ai_game):  ##self argument and AlienInvasion class instance argument 
		super().__init__()
		self.screen=ai_game.screen   ##assigns screen(AlienInvasion class screen) to the attribute of the ship
		self.settings=ai_game.settings   ##create settings attribute
		self.screen_rect=ai_game.screen.get_rect()  ##screen rect attributes from get_rect() method is assigned to screen_rect.To place the ship in correct location on the scren
		self.image=pygame.image.load('ships.png')   ##to load image ,call image.load() and assign it to image
		self.rect=self.image.get_rect()   ####     when the image is loaded , we call get_rect() to access ships rect attributes and assign it to rect
		self.rect.midbottom=self.screen_rect.midbottom   ## rec(ship) position matches with screen_rect(screen) position at the mid bottom
		self.x=float(self.rect.x)   ##to hold decimal values
		self.moving_right=False
		self.moving_left=False
	def update(self):   ## one argument 
		if self.moving_right and self.rect.right<self.screen_rect.right:  ## checks the position before changing the value 
			self.x+=self.settings.ship_speed
		if self.moving_left and self.rect.left>0:
			self.x-=self.settings.ship_speed
		self.rect.x=self.x   ##assigns the value of x to ship rect attribute X position

	def blitme(self):    ##to draw ship at the specified location
		self.screen.blit(self.image,self.rect)  ##points the ship at the position specified by self.rect on the screen 

	def center_ship(self):
		self.rect.midbottom=self.screen_rect.midbottom
		self.x=float(self.rect.x)







