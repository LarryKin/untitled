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
        self.directions_down = [False] * 5
        self.frames = frames  #number seconds between
        
        self.speed = (0,0)   #current speed of sprite
        self.walk_speed = 5 #in pixels per seconds
        self.jump_vel = 10
        self.jump_vel_comp = 10
        self.speed_list = [(self.walk_speed, 0), (-self.walk_speed, 0), 
                           (0, -self.jump_vel), 
                           (self.jump_vel_comp, -self.jump_vel_comp),
                           (-self.jump_vel_comp, -self.jump_vel_comp)]

        
        #initialize sprite sheet handler
        
        self.walk_down = sprite_handle.sprite_strip_anim(
                                               'sprites/goblins.png', 
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
                                               'sprites/goblins.png', 
                                               (0, 160, 32, 32), 1, 
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

        self.x = initial_coor[0]
        self.y = initial_coor[1]
        self.rect.topleft = (round(self.x), round(self.y))
    
    def update(self, blocks):
        '''
        use keys_list found by events_fetch to update the keys_list
        '''
        
        #first record the state of last update to determine if reset animation
        last_frame_state = self.state      
        #record last update vertical speed to enable jump
        last_y_vel = self.speed[1]
        
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
        
        #jump
        if pygame.key.get_pressed()[pygame.K_UP] and self.on_ground:
            self.directions_down[2] = True
            self.state = self.walk_up
        else:
            self.directions_down[2] = False
        
                                                                   
        #right-up diagonal jump
        if self.directions_down[0] and self.directions_down[2] and\
           self.on_ground:
            self.directions_down[3] = True
            self.state = self.walk_up
        else:
            self.directions_down[3] = False
        #left-up diagonal jump
        if self.directions_down[2] and self.directions_down[1] and\
           self.on_ground:
            self.directions_down[4] = True
            self.state = self.walk_up
        else:
            self.directions_down[4] = False
                                       
        #this if condition reset all animation if the state from the last frame
        #is NOT in the default idle_right or idle_left states
        if (self.state != last_frame_state) and last_frame_state != \
        self.idle_right and last_frame_state != self.idle_left:
            self._reset()
            if (self.state == None) and (last_frame_state == self.walk_right):
                self.state = self.idle_right
            if (self.state == None) and (last_frame_state == self.walk_left):
                self.state = self.idle_left
        #this allows the animation of default idle state to play
        if self.state == None:
            self.state = last_frame_state
            self.speed = (0,0)
                   
                
        #update the speed and new coordinate
        for i in range(5):
            if self.directions_down[i] == True:
                self.speed = self.speed_list[i]
        if not self.on_ground:
            self.speed = (self.speed[0], last_y_vel)
        
        #now include gravity
        self.speed = (self.speed[0] + gravity[0], 
                      self.speed[1] + gravity[1])
        
        #update y first
        self.y += self.speed[1]
        self.rect.topleft = (self.rect.topleft[0], round(self.y))
        self.on_ground = False
        self._collide_info(0, self.speed[1], blocks)
        
        #then update x
        self.x += self.speed[0]
        self.rect.topleft = (round(self.x), self.rect.topleft[1])
        
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
            if xvel > 0: 
                self.rect.right = block.rect.left
                self.x = self.rect.topleft[0]
            if xvel < 0: 
                self.rect.left = block.rect.right
                self.x = self.rect.topleft[0]

            # if yvel > 0, we are falling, so if a collision happpens 
            # we know we hit the ground (remember, we seperated checking for
            # horizontal and vertical collision, so if yvel != 0, xvel is 0)
            if yvel > 0:
                self.rect.bottom = block.rect.top
                self.on_ground = True
                self.y = self.rect.topleft[1]
                self.yvel = 0
            # if yvel < 0 and a collision occurs, we bumped our head
            # on a block above us
            if yvel < 0: 
                self.rect.top = block.rect.bottom
                self.y = self.rect.topleft[1]

    
    def _reset(self):
        #reset all animationss
        self.idle_right.iter()
        self.idle_left.iter()
        self.walk_right.iter()
        self.walk_left.iter()

    
