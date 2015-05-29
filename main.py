# -*- coding: utf-8 -*-
"""
Created on Sun May 17 12:41:58 2015

@author: larry
"""

import sys, pygame
import pygame.locals
import sprite_anime
import ai



pygame.init()

size = width, height = 200, 200
speed = [2, 2]
black = (0, 0, 0)
white = (255,255,255)

FPS = 120
frames = FPS / 24
screen = pygame.display.set_mode(size)


clock = pygame.time.Clock()
   

def event_fetch(events_list, keys_list):
    """
    handle the events
    """
    attack_key_down = keys_list[0]
    directions_down = keys_list[1]
    
    
    for event in events_list:
        if event.type == pygame.QUIT: 
            sys.exit()
            
        if event.type == pygame.KEYDOWN:
            
            if event.key == pygame.K_z:  
                attack_key_down = True

            if event.key == pygame.K_RIGHT:
                directions_down[0] = True
            if event.key == pygame.K_LEFT:
                directions_down[1] = True
            if event.key == pygame.K_UP:
                directions_down[2] = True
            if event.key == pygame.K_DOWN:
                directions_down[3] = True
            
              
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_z:
                attack_key_down = False               
            if event.key == pygame.K_RIGHT:
                directions_down[0] = False
            if event.key == pygame.K_LEFT:
                directions_down[1] = False
            if event.key == pygame.K_UP:
                directions_down[2] = False
            if event.key == pygame.K_DOWN:
                directions_down[3] = False
        
        #the 8th item in the list determine if the character is walking or not
        if directions_down[0:8] == [False]*8:
            directions_down[8] = False
        else:
            directions_down[8] = True
            
        
        #update the list
    keys_list[0] = attack_key_down
    keys_list[1] = directions_down
    return keys_list
    
    
            


#main game loop
test = 0
#ranger_image = ranger_idle 
speed = (0,0)
coor = (30,30)


#the first eight determines which key is pressed, while the 9th item in the 
#list is only False if rest of eight are all False
directions_down = [False]*9    
attack_key_down = False

keys_list = [attack_key_down, directions_down]

player_anime = sprite_anime.main_anime((30,30), frames)
pirate_one = ai.normal_pirate((100,100), frames)

while True:
 
    screen.fill(black)
    
    #initialize default state of sprites   

    keys_list = event_fetch(pygame.event.get(), keys_list)
    player_anime.update(keys_list)   
    player_coor = player_anime.draw(screen)
            
            
    pirate_one.draw(screen, player_coor)
    pygame.display.flip()
    clock.tick(FPS)
    
        
pygame.quit()            
            