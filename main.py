# -*- coding: utf-8 -*-
"""
Created on Sun May 17 12:41:58 2015

@author: larry
"""

import sys, pygame
import pygame.locals
import sprite_anime
import floor



pygame.init()

size = width, height = 200, 200
speed = [2, 2]
black = (0, 0, 0)
white = (255,255,255)

FPS = 120
frames = FPS / 24
screen = pygame.display.set_mode(size)


clock = pygame.time.Clock()
   

#main game loop
test = 0
#ranger_image = ranger_idle 
speed = (0,0)
coor = (100,0)


#the first eight determines which key is pressed, while the 9th item in the 
#list is only False if rest of eight are all False
directions_down = [False]*9    
attack_key_down = False

keys_list = [attack_key_down, directions_down]

main_character = sprite_anime.main_character(coor, frames)
floor1 = floor.floor()

characters = pygame.sprite.Group(main_character)
tiles = pygame.sprite.Group(floor1)

while True:
 
    screen.fill(black)
    
    #initialize default state of sprites   
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            sys.exit()
            
    characters.update(tiles.sprites())   
    characters.draw(screen)
    tiles.draw(screen)
            
    #pirate_one.draw(screen, player_coor)
    pygame.display.flip()
    clock.tick(FPS)
    
        
pygame.quit()            
            