import sys ##to exit from the game when the player quits
import pygame
from time import sleep  ##we can pause the game when ship is hit 
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien 
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

class AlienInvasion:
	def __init__(self):
		pygame.init()  ##Initializes background settings
		self.settings=Settings()    ##import Settings and make instance of Settings
		self.screen=pygame.display.set_mode((0,0),pygame.FULLSCREEN)##initially screen width and height are set to 0 and fullscreen mode
		self.settings.screen_width=self.screen.get_rect().width ## we get screen width and height from get_rect() method and assign them to settings objects
		self.settings.screen_height=self.screen.get_rect().height 
		##self.screen=pygame.display.set_mode((self.settings.s_width,self.settings.s_height))    ##Tuple to define game window dimensions and assigned to self.screen , so that it can be accessed in all methods in this class
		pygame.display.set_caption("Alien Invasion")  ##display the caption
		self.stats=GameStats(self)
		self.sb=Scoreboard(self)
		self.ship=Ship(self)  ##import Ship and make instance of the Ship after screen is set   and one argument i.e., instances of AlienInvasion class, so that ship can get access to game resources(screen)
		self.bullets=pygame.sprite.Group()     ##to draw bullets to the screen on each pass through main loop
		self.aliens=pygame.sprite.Group()
		self.play_button=Button(self,"Play")  ##we need only one play button, so we create in __init__ method

		self.create_fleet()
		
	
	def run_game(self):   ## to control the game
		while True: ##this loop runs continually
			self.check_events()  ##to check whether player has clicked exit button .To call a method from within a class ,use dot notation with variable "self" and name of the method
			
			if self.stats.game_active:
				self.ship.update()   ## ship's position is updated after we've checked for keyboard events and before we update screen 
			                            ####i.e.if any keyboard activity is pressed by player then ship's position need to be update and this position of ship is used to draw the ship on the screen
				self.update_bullets()
				self.update_aliens()
				self.update_screen()     ##for every loop it updates the screen ,ship position,bg_color
			
	def check_events(self):
		for event in pygame.event.get():   ##to access the events the pygame detects, we use pygame.event.get() function like keyboard or mouse event
			if event.type==pygame.QUIT:
				sys.exit()
			elif event.type==pygame.KEYDOWN: ##if pygame detects a KEYDOWN event 
				self.check_keydown_events(event)   
			elif event.type==pygame.KEYUP:   ##if it detects the KEYUP event i.e., player releases the KEY
				self.check_keyup_events(event)

			elif event.type==pygame.MOUSEBUTTONDOWN:  
				mouse_pos=pygame.mouse.get_pos()
				self.check_play_button(mouse_pos)

	def check_play_button(self,mouse_pos):
		##if self.play_button.rect.collidepoint(mouse_pos):   ## check whether the point of mouse click overlap with region defined by play button
		button_clicked=self.play_button.rect.collidepoint(mouse_pos)   ##flag button button_clicked stores True or False value  
		if button_clicked and not self.stats.game_active:      ##The game will restart only if play is clicked and game is currently inactive
			self.settings.initialize_dynamic_settings()
			pygame.mouse.set_visible(False)
			self.stats.reset_stats()
			self.stats.game_active=True
			self.sb.prep_score()
			self.sb.prep_level()
			self.sb.prep_ships()
			self.aliens.empty()
			self.bullets.empty()
			self.create_fleet()
			self.ship.center_ship()


	def check_keydown_events(self,event):   ## two arguments self and event
		if event.key==pygame.K_RIGHT:   ## checks whether key pressed(i.e.,event) is right arrow key(pygame.K_RIGHT)
			self.ship.moving_right=True ## set moving_right to True
		elif event.key==pygame.K_LEFT:
			self.ship.moving_left=True
		elif event.key==pygame.K_q:
			sys.exit()
		elif event.key==pygame.K_SPACE:   ##when space bar is pressed , fire the bullet
			self.fire_bullet()   ##calling fire_bullet method

	def check_keyup_events(self,event):
		if event.key==pygame.K_RIGHT:  ##checks whether the key released is right arrow key
			self.ship.moving_right=False  ##sets moving_right to False
		elif event.key==pygame.K_LEFT:
			self.ship.moving_left=False
		elif event.key==pygame.K_q:
			sys.exit()

	def fire_bullet(self):
		if len(self.bullets) < self.settings.bullets_allowed:
			new_bullet=Bullet(self)##make an instance of Bullet class and call it as new_bullet
			self.bullets.add(new_bullet)   ##add the new_bullet to bullets group

	def update_bullets(self):
		self.bullets.update()   ##update the position of the bullets on each pass of while loop for each bullet                       
		for bullet in self.bullets.copy():    ###list or group lenghth should remain constant using "for" loop . we can't remove items from the list using "for" loop . so we used cop() method to setup for loop
			if bullet.rect.bottom<=0:   ##to check whether the bullet has disappered after reaching top of the screen
				self.bullets.remove(bullet) ##if it is, then remove that bullet

		self.check_bullet_alien_collisions()

	def check_bullet_alien_collisions(self):
		collisions=pygame.sprite.groupcollide(self.bullets,self.aliens,False,True)   ##check for any bullet in bullets group and alien in aliens have collided
					##when they collide groupcollide fuction returns key(bullet),value(alien) pair that is been collided
					##two True arguments tell python to delete those bullet and aliens that have collided
					##to make the bullet move even after colliding the alien,then make the third argument to False 
		if collisions:
			for aliens in collisions.values():
				self.stats.score+=self.settings.alien_points*len(aliens)  ##score is that list of aliens hit by a single bullet
				self.sb.prep_score()
				self.sb.check_high_score()
		if not self.aliens:
			self.bullets.empty()               
			self.create_fleet()
			self.settings.increase_speed()

			self.stats.level+=1
			self.sb.prep_level()

	def update_aliens(self):
		self.check_fleet_edges()
		self.aliens.update()
		if pygame.sprite.spritecollideany(self.ship,self.aliens):   ##spritecollideany function looks for any member of group that has collided
		##if any collision occurs it returns that alien which is collided with ship, else it returns None and if block is not executed
			self.ship_hit()
		self.check_aliens_bottom()

	def ship_hit(self):
		if self.stats.ships_left > 0:
			self.stats.ships_left-=1  ## decrement ships_left
			self.sb.prep_ships()
			self.aliens.empty()  ##empty the aliens and bullets
			self.bullets.empty()

			self.create_fleet()   ## create a new fleet of aliens
			self.ship.center_ship()

			sleep(0.5) ##pause the game for player to understand that ship has collided with alien .After sleep time the screen is updated 
		else:
			self.stats.game_active=False
			pygame.mouse.set_visible(True)


	def create_fleet(self):
		alien=Alien(self)   ### creating an instance and adding it to the group 
		alien_width,alien_height=alien.rect.size
		available_space_x=self.settings.screen_width-(2*alien_width)
		number_aliens_x=available_space_x // (2*alien_width)   ##floor division to get results in integer
		ship_height=self.ship.rect.height 
		available_space_y=self.settings.screen_height-(4*alien_height)-ship_height
		number_rows=(available_space_y) // (2*alien_height) 
		for row_number in range(number_rows):
			for alien_number in range(number_aliens_x):
				self.create_alien(alien_number,row_number)
			

	def create_alien(self,alien_number,row_number):
		alien=Alien(self)   ##instance for the class
		alien_width,alien_height=alien.rect.size  ## width of alien
		alien.x=alien_width+2*alien_width*alien_number
		alien.rect.x =alien.x
		alien.rect.y=alien.rect.height+2*alien.rect.height*row_number
		self.aliens.add(alien)  ##add alien to alien group

	def update_screen(self):
		self.screen.fill(self.settings.bg_color)    ## access the background color from settings and then fill the screen
		self.ship.blitme()  ##After filling bg_color , we draw the ship on the screen using "blitme method"
		for bullet in self.bullets.sprites():    ## bullets.sprite() method returns list of all sprites in the group bullets
		 				##to draw all the fired bullets to the screen , we loop through the sprites in the bullets 
			bullet.draw_bullet()  ##Then call the draw_bullet() method on each one 
		self.aliens.draw(self.screen)  ##alien class doesn't need any method of drawing   and draw method requires one argument i.e., surface 
		self.sb.show_score()  ##just before play button draw
		if not self.stats.game_active:
			self.play_button.draw_button()  ##button appears only when the game is inactive
		pygame.display.flip() ## updates the display to show new position of game elements

	def check_fleet_edges(self):
		for alien in self.aliens.sprites():
			if alien.check_edges():
				self.change_fleet_direction()
				break

	def change_fleet_direction(self):
		for alien in self.aliens.sprites():
			alien.rect.y+=self.settings.fleet_drop_speed
		self.settings.fleet_direction*=-1

	def check_aliens_bottom(self):
		self.screen_rect=self.screen.get_rect()
		for alien in self.aliens.sprites():
			if alien.rect.bottom>=self.screen_rect.bottom:
				self.ship_hit()
				break   ##if one alien gets hit the bottom ,then no need to check for the rest of the loop



if __name__=='__main__':     ## __name__ variable is set to  string" __main__" if we use in the same module .If we import this module into other module  __name__ variable changes to module name
           #### Block the code when modules are imported
	ai=AlienInvasion()   ##creating instance of the class
	ai.run_game()  ##calling run_game method
    
    
