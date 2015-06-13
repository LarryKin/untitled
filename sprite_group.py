# -*- coding: utf-8 -*-
"""
Created on Thu Jun 11 20:20:18 2015

@author: larry
"""

import pygame

gravity = (0,1)
class Ground_Group(pygame.sprite.Group): 
    def __init__(self):
        super(Ground_Group, self).__init__()
    
    def sprites(self):
        #return a list of sprite contained inside this group
        return super(Ground_Group, self).sprites()
        
    def update(self, floor):
    #this will update the location as well as check for collisions
        super(Ground_Group, self).update()
        for ground_sprite in self.sprites():
            #first check to see if the sprite in on the ground
                        
            
            collision_sides = self._collision_info(ground_sprite.rect,
                                                   floor.rect)


            
    def _collision_info(sprite_rect, tile_rect):
        collision = [False] *4
        collision[0] = sprite_rect.rect.collidepoint(tile_rect.topleft)
        collision[1] = sprite_rect.rect.collidepoint(tile_rect.topright)
        collision[2] = sprite_rect.rect.collidepoint(tile_rect.bottomleft)
        collision[3] = sprite_rect.rect.collidepoint(tile_rect.bottomright)
        return collision
            
 
        
            