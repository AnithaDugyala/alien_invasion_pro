import pygame.font
class Button:
	def __init__(self,ai_game,msg):
		##initalizing button attributes
		self.screen=ai_game.screen
		self.screen_rect=self.screen.get_rect()

		##button dimensions and properties
		self.width,self.height=200,50
		self.button_color=(0,255,0)    ##green
		self.text_color=(255,255,255)  ##white
		self.font=pygame.font.SysFont('Corbel',48)  ##None indicates default font and 48 specifies text size

		self.rect=pygame.Rect(0,0,self.width,self.height)
		self.rect.center=self.screen_rect.center

		self.prep_msg(msg)  ##creating image from the text(msg) and blit this onto the screen

	def prep_msg(self,msg):
		self.msg_image=self.font.render(msg,True,self.text_color)    ##font.render funnction turns text into image and it is stored in msg_image
		##Boolean value to turn ON or OFF of antialiasing (making edges of text smoother)
		##set text background color to same color as  button color

		self.msg_image_rect=self.msg_image.get_rect()
		self.msg_image_rect.center=self.rect.center

	def draw_button(self):
		self.screen.fill(self.button_color,self.rect)   ##to draw rectangular portion of button
		self.screen.blit(self.msg_image,self.msg_image_rect)   ##to draw text image to the screen




