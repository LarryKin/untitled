# -*- coding: utf-8 -*-
"""
Created on Fri May 22 13:03:49 2015

@author: larry
"""
import sprite_handle
import pygame

white = (255, 255, 255)

class main_anime(object):  
    def __init__(self, initial_coor, frames):
        self.attack_key_down = False
        # 8 directions + last item (True if one of the directions is pressed)
        self.directions_down = [False] * 9
        self.coor = initial_coor
        self.frames = frames
        
        self.speed = (0,0)
        self.speed_mag = 2 #in pixels per frame
        self.speed_comp = 0.707 * self.speed_mag #normalize to 1/sqrt(2)
        self.speed_list = [(self.speed_mag, 0), (-self.speed_mag, 0), 
                           (0, -self.speed_mag), (0, self.speed_mag), 
                           (self.speed_comp, -self.speed_comp),
                           (-self.speed_comp, -self.speed_comp), 
                           (-self.speed_comp, self.speed_comp),
                           (self.speed_comp, self.speed_comp), (0,0)]
        
        #initialize sprite sheet handler
        self.sprite_attack = sprite_handle.sprite_strip_anim(
                                               'sprites/ranger.png', 
                                               (0, 96, 32, 32), 10,
                                               white, False, self.frames)
        self.sprite_idle = sprite_handle.sprite_strip_anim(
                                               'sprites/jael.png', 
                                               (0, 48, 32, 48), 1,
                                               None, True, self.frames)
        self.sprite_walk = sprite_handle.sprite_strip_anim(
                                               'sprites/jael.png', 
                                               (0, 48, 32, 48), 4,
                                               None, True, self.frames)
        self.sprite_image = self.sprite_idle #default to idle mode
    
    def update(self, keys_list):
        '''
        use keys_list found by events_fetch to update the keys_list
        '''
        self.attack_key_down = pygame.key.get_pressed()[pygame.K_z]
        # 8 directions + last item (True if one of the directions is pressed)        
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            self.directions_down[0] = True
        else:
            self.directions_down[0] = False
        
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            self.directions_down[1] = True
        else:
            self.directions_down[1] = False
        
        if pygame.key.get_pressed()[pygame.K_UP]:
            self.directions_down[2] = True
        else:
            self.directions_down[2] = False
        
        if pygame.key.get_pressed()[pygame.K_DOWN]:
            self.directions_down[3] = True
        else:
            self.directions_down[3] = False
                                                            
        
        #right-up movement
        if self.directions_down[0] and self.directions_down[2]:
            self.directions_down[4] = True
        else:
            self.directions_down[4] = False
            #up-left movement
        if self.directions_down[2] and self.directions_down[1]:
            self.directions_down[5] = True
        else:
            self.directions_down[5] = False
            #left-down movement
        if self.directions_down[1] and self.directions_down[3]:
            self.directions_down[6] = True  
        else:
            self.directions_down[6] = False
            #down-right movement
        if self.directions_down[3] and self.directions_down[0]:
            self.directions_down[7] = True  
        else:
            self.directions_down[7] = False
        
        if self.directions_down[0:8] == [False] * 8:
            self.directions_down[8] = False
        else:
            self.directions_down[8] = True

        for i in range(8):
            if self.directions_down[i] == True:
                self.speed = self.speed_list[i]
        

    def current_coor(self):
        #return coordinate and sprite surface object to be blit by pygame 
        if self.sprite_image == self.sprite_attack:
            if self.sprite_image.complete() == False:
                self.sprite_image = self.sprite_attack
                return self.sprite_image.next(), self.coor
            else:
                self.sprite_image.iter() #reset the image but dont return yet
        
        if self.attack_key_down:
            self.sprite_image = self.sprite_attack
            if self.sprite_image.complete() == False:
                self.sprite_image = self.sprite_attack
                return self.sprite_image.next(), self.coor
            else:
                self.sprite_image.iter()
                self.sprite_image = self.sprite_attack
                return self.sprite_image.next(), self.coor
                
        if self.directions_down[8]:
            new_x = self.coor[0] + self.speed[0]
            new_y = self.coor[1] + self.speed[1]
            self.coor = (new_x, new_y)
                       
            if self.sprite_image != self.sprite_walk:
                self.sprite_walk.iter()     
            
            self.sprite_image = self.sprite_walk
            return self.sprite_image.next(), self.coor
            
        if self.sprite_image != self.sprite_idle:
            self.sprite_idle.iter()
            self.sprite_image = self.sprite_idle
        return self.sprite_image.next(), self.coor
        
    def draw(self, surface):
        sprite_image_blit, self.coor = self.current_coor()              
        surface.blit(sprite_image_blit, self.coor)
        return self.coor
                
