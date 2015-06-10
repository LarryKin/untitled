# -*- coding: utf-8 -*-
"""
Created on Fri May 22 13:03:49 2015

@author: larry
"""
import sprite_handle
import pygame

white = (255, 255, 255)

class main_character(pygame.sprite.Sprite):  
    def __init__(self, initial_coor, frames):
        super(main_character, self).__init__()
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
        
        self.walk_down = sprite_handle.sprite_strip_anim(
                                               'sprites/jael.png', 
                                               (0, 0, 32, 48), 4,
                                               None, True, self.frames)
        self.walk_left = sprite_handle.sprite_strip_anim(
                                               'sprites/goblins.png', 
                                               (0,224, 32, 32), 10,
                                               None, True, True, self.frames)        
        self.walk_right = sprite_handle.sprite_strip_anim(
                                               'sprites/goblins.png', 
                                               (0,224, 32, 32), 10,
                                               None, True, False, self.frames)
        self.walk_up = sprite_handle.sprite_strip_anim(
                                               'sprites/jael.png', 
                                               (0, 144, 32, 48), 4,
                                               None, True, self.frames)
        self.idle_right = sprite_handle.sprite_strip_anim(
                                               'sprites/goblins.png', 
                                               (0, 160, 32, 32), 10,
                                               None, True, False, self.frames)
                                               
        self.idle_left = sprite_handle.sprite_strip_anim(
                                               'sprites/goblins.png', 
                                               (0, 160, 32, 32), 10,
                                               None, True, True, self.frames)
        
        self.state = self.idle_right
        self.image = self.state.next();
        self.rect = (self.coor[0], self.coor[1], 32, 32)
    
    def update(self):
        '''
        use keys_list found by events_fetch to update the keys_list
        '''
        #first record the state of last frame to determine if reset animation
        last_frame_state = self.state 
        #again if self.state is not changed, it is defaulted to None which will
        #be handled at the end of updated
        self.state = None
        
        self.attack_key_down = pygame.key.get_pressed()[pygame.K_z]
        # 8 directions + last item (True if one of the directions is pressed)        
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            self.directions_down[0] = True
            self.state = self.walk_right
        else:
            self.directions_down[0] = False
        
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            self.directions_down[1] = True
            self.state = self.walk_left
        else:
            self.directions_down[1] = False
        
        if pygame.key.get_pressed()[pygame.K_UP]:
            self.directions_down[2] = True
            self.state = self.walk_up
        else:
            self.directions_down[2] = False
        
        if pygame.key.get_pressed()[pygame.K_DOWN]:
            self.directions_down[3] = True
            self.state = self.walk_down
        else:
            self.directions_down[3] = False
                                                                   
            #right-up movement
        if self.directions_down[0] and self.directions_down[2]:
            self.directions_down[4] = True
            self.state = self.walk_up
        else:
            self.directions_down[4] = False
            #up-left movement
        if self.directions_down[2] and self.directions_down[1]:
            self.directions_down[5] = True
            self.state = self.walk_up
        else:
            self.directions_down[5] = False
            #left-down movement
        if self.directions_down[1] and self.directions_down[3]:
            self.directions_down[6] = True  
            self.state = self.walk_down
        else:
            self.directions_down[6] = False
            #down-right movement
        if self.directions_down[3] and self.directions_down[0]:
            self.directions_down[7] = True  
            self.state = self.walk_down
        else:
            self.directions_down[7] = False
        
        if self.directions_down[0:8] == [False] * 8:
            self.directions_down[8] = False
        else:
            self.directions_down[8] = True
        
        #update the speed
        for i in range(8):
            if self.directions_down[i] == True:
                self.speed = self.speed_list[i]
        
                      
        if self.directions_down[8]:
            new_x = self.coor[0] + self.speed[0]
            new_y = self.coor[1] + self.speed[1]
            self.coor = (new_x, new_y)
         
        #this if condition reset all animation if the state from the last frame
        #is NOT in the default idle_right or idle_left states
        if (self.state != last_frame_state) and last_frame_state != \
        self.idle_right and last_frame_state != self.idle_left:
            self._reset()
            if (self.state == None) and (last_frame_state == self.walk_right):
                self.state = self.idle_right
            if (self.state == None) and (last_frame_state == self.walk_left):
                self.state = self.idle_left
        #this allows the animation of default state to play
        if self.state == None:
            self.state = last_frame_state

        self.image = self.state.next()
        self.rect = (self.coor[0], self.coor[1], 32, 32)
        return None
    
    def _reset(self):
        #reset all animationss
        self.idle_right.iter()
        self.idle_left.iter()
        self.walk_right.iter()
        self.walk_left.iter()
        return None
    
