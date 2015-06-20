# -*- coding: utf-8 -*-
"""
Created on Fri May 22 13:03:49 2015

@author: larry
"""
import sprite_handle
import pygame

white = (255, 255, 255)
gravity = (0,1)

class main_character(pygame.sprite.Sprite):  
    def __init__(self, initial_coor, frames):
        super(main_character, self).__init__()
        self.attack_key_down = False
        # 8 directions + last item (True if one of the directions is pressed)
        self.directions_down = [False] * 9
        self.frames = frames
        
        self.speed = (0,0)
        self.speed_mag = 1 #in pixels per frame
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
                                               -1, True, self.frames)
        self.walk_left = sprite_handle.sprite_strip_anim(
                                               'sprites/goblins.png', 
                                               (0,224, 32, 32), 10, 
                                               -1, True, True, self.frames)        
        self.walk_right = sprite_handle.sprite_strip_anim(
                                               'sprites/goblins.png', 
                                               (0,224, 32, 32), 10, 
                                               -1, True, False, self.frames)
        self.walk_up = sprite_handle.sprite_strip_anim(
                                               'sprites/jael.png', 
                                               (0, 144, 32, 48), 4, 
                                               -1, True, self.frames)
        self.idle_right = sprite_handle.sprite_strip_anim(
                                               'sprites/goblins.png', 
                                               (0, 160, 32, 32), 10, 
                                               -1, True, False, self.frames)
                                               
        self.idle_left = sprite_handle.sprite_strip_anim(
                                               'sprites/goblins.png', 
                                               (0, 160, 32, 32), 10,
                                               -1, True, True, self.frames)
        
        self.on_ground = False
        self.state = self.idle_right
        self.image = self.state.next()
        
        self.rect = self.image.get_bounding_rect()
        self.rect.centerx = initial_coor[0]
        self.rect.centery = initial_coor[1]
        self.x = initial_coor[0]
        self.y = initial_coor[1]
    
    def update(self, blocks):
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
        
        if self.directions_down[0:8] == [False] * 8:
            self.directions_down[8] = False
        else:
            self.directions_down[8] = True
                                       
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
            
                
        #update the speed and new coordinate
        for i in range(8):
            if self.directions_down[i] == True:
                self.speed = self.speed_list[i]
            elif self.directions_down[8] == False:
                self.speed = (0,0)
        
        #now include gravity
        self.speed = (self.speed[0] + gravity[0], 
                      self.speed[1] + gravity[1])
        
        #update y first
        self.y += self.speed[1]
        self.rect.centery = round(self.y)
        self.on_ground = False
        self._collide_info(0, self.speed[1], blocks)
        
        #then update x
        self.x += self.spped[0]
        self.rect.centerx = round(self.x)
        
        print self.rect.centery
        self._collide_info(self.speed[0], 0, blocks)
        
        
        self.image = self.state.next()
    def _collide_info(self, xvel, yvel, blocks):
        '''
        borrowed from 
        http://stackoverflow.com/questions/18966882/
        add-collision-detection-to-a-plattformer-in-pygame
        '''
        # all blocks that we collide with
        for block in [blocks[i] for i in self.rect.collidelistall(blocks)]:
            # if xvel is > 0, we know our right side bumped 
            # into the left side of a block etc.
            if xvel > 0: self.rect.right = block.rect.left
            if xvel < 0: self.rect.left = block.rect.right

            # if yvel > 0, we are falling, so if a collision happpens 
            # we know we hit the ground (remember, we seperated checking for
            # horizontal and vertical collision, so if yvel != 0, xvel is 0)
            if yvel > 0:
                self.rect.bottom = block.rect.top
                self.on_ground = True
                self.yvel = 0
            # if yvel < 0 and a collision occurs, we bumped our head
            # on a block above us
            if yvel < 0: self.rect.top = block.rect.bottom

    
    def _reset(self):
        #reset all animationss
        self.idle_right.iter()
        self.idle_left.iter()
        self.walk_right.iter()
        self.walk_left.iter()

    
