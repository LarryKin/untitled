import pygame
import sprite_anime
from settings import Settings
import floor

ups = Settings.ups
black = (0, 0, 0)

#just some place holder
coor = (150,50)

screen_centerx = 100
screen_centery = 100

class World(object):
    
    def __init__(self, screen):       
        #create some basic sprite in the world and group them
        self.main_character = sprite_anime.main_character(coor, 2)
        self.floor1 = floor.Wall((200,3), (100,100))
        self.characters = pygame.sprite.Group(self.main_character)
        self.tiles = pygame.sprite.Group(self.floor1)
        #add boundries walls to self.tiles member list
        floor.playground(self.tiles)
        self.screen = screen

    def update(self, dt):
        self.characters.update(self.tiles.sprites())   
       
    
    def draw(self, dt):
        #this draw is temporary. Later replaced by camera class
        self.screen.fill(black)
        self.characters.draw(self.screen)
        self.tiles.draw(self.screen)
        pygame.display.flip()
        
        
        
class Camera(object):
    def __init__(self, screen):
        self.screen = screen
        
    def shoot(self, dt, world):
        '''
        take a snapshot of the world and draw on the screen
        '''
        offsetx = world.main_character.x - screen_centerx
        offsety = world.main_character.y - screen_centery
        for sprite in world.characters.sprites():
            sprite.rect.topleft = (sprite.x - offsetx,
                                   sprite.y - offsety)
                                   
        for tile in world.tiles.sprites():
            tile.rect.topleft = (tile.x - offsetx,
                                 tile.y - offsety)

        
        #now update the screen
        self.screen.fill(black)
        world.characters.draw(self.screen)
        world.tiles.draw(self.screen)
        pygame.display.flip()
        
        
        #since draw command use rect as arg, we temporary change it above
        #after finishing drawing, we restore rect back to original position
        #so the camera will have no effects on our sprite instances
        #aka. it just take a snapshoot without affecting the properties
        for sprite in world.characters.sprites():
            sprite.rect.topleft = (round(sprite.x), round(sprite.y))                                   
        for tile in world.tiles.sprites():
            tile.rect.topleft = (round(tile.x), round(tile.y))
        