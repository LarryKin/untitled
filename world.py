import pygame
import sprite_anime
from settings import Settings
import floor

ups = Settings.ups
black = (0, 0, 0)

#just some place holder
coor = (100,0)

class World(object):
    
    def __init__(self, screen):       
        #create some basic sprite in the world and group them
        self.main_character = sprite_anime.main_character(coor, ups)
        self.floor1 = floor.floor()
        self.characters = pygame.sprite.Group(self.main_character)
        self.tiles = pygame.sprite.Group(self.floor1)
        self.screen = screen

    def update(self, dt):
        self.characters.update(self.tiles.sprites())   
       
    
    def draw(self, dt):
        #this draw is temporary. Later replaced by camera class
        self.screen.fill(black)
        self.characters.draw(self.screen)
        self.tiles.draw(self.screen)
        pygame.display.flip()