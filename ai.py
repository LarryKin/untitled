# -*- coding: utf-8 -*-
"""
Created on Mon May 25 11:15:52 2015

@author: larry
"""

import pygame
import sprite_anime


class normal_pirate(sprite_anime.main_anime):
    
    def __init__(self, initial_coor, frames):
        super(normal_pirate, self).__init__(initial_coor, frames)
        
        
        self.name = 'normal_pirate'
        self.level = 1
        self.strength = 1
        self.speed_mag = 1       

        self.safe_distance = 50
        self.coor = initial_coor
        
        #over ride the default speed in super class
        self.speed_mag = 1 #in pixels per frame
        self.speed_comp = 0.707 * self.speed_mag #normalize to 1/sqrt(2)
        self.speed_list = [(self.speed_mag, 0), (-self.speed_mag, 0), 
                           (0, -self.speed_mag), (0, self.speed_mag), 
                           (self.speed_comp, -self.speed_comp),
                           (-self.speed_comp, -self.speed_comp), 
                           (-self.speed_comp, self.speed_comp),
                           (self.speed_comp, self.speed_comp), (0,0)]
        
    def update(self, player_coor):
        '''
        this function determines the bot's behaviour. For a normal pirate,
        it chases the player until it reaches some safe distance where it can
        attack
        '''
        #first reset the direction
        self.directions_down = [False] * 9
        x_offset = player_coor[0] - self.coor[0]
        y_offset = player_coor[1] - self.coor[1]
        dist_offset = ((player_coor[0] - self.coor[0])**2.0 + 
                      (player_coor[1] - self.coor[1])**2.0)**(0.5)
                      
                      
        #determine the best way to stay away from the player if too closed
        if dist_offset < self.safe_distance:
            current_max = dist_offset
            max_ind = 0
            for i in range(8):
                temp_offset = ((player_coor[0] - self.coor[0] - 
                              self.speed_list[i][0])**2.0 + 
                              (player_coor[1] - self.coor[1] - 
                              self.speed_list[i][1])**2.0)**(0.5)
                if temp_offset > current_max:
                    current_max = temp_offset
                    max_ind = i
            self.directions_down[max_ind] = True
                     
            keys_list = [False, self.directions_down]
            super(normal_pirate, self).update(keys_list)
            return None
        
        #if too far from the player, try to gap close
        if x_offset >= 0:
            #turn right to chase the player
            self.directions_down[0] = True
        else:
            self.directions_down[1] = True
        if y_offset >= 0:
            self.directions_down[3] = True
        else:
            self.directions_down[2] = True
                 
        keys_list = [False, self.directions_down]
        super(normal_pirate, self).update(keys_list)
        return None
            
        
    def draw(self, surface, player_coor):
        #first update the coor 
        self.update(player_coor)
        sprite_image_blit, self.coor = super(normal_pirate, 
                                             self).current_coor()
            
        surface.blit(sprite_image_blit, self.coor)
        
        
        