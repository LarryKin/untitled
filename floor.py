# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 14:31:50 2015

@author: larry
"""
import pygame

white = (255,255,255)
class Wall(pygame.sprite.Sprite):
    def __init__(self, dim, top_left):
        super(Wall, self).__init__()
        self.image = pygame.Surface(dim)
        self.image.fill(white)
        self.rect = self.image.get_bounding_rect()
        self.rect.topleft = top_left
        self.x = self.rect.topleft[0]
        self.y = self.rect.topleft[1]
          
        
def playground(group_class):
    #create a bounded playground with some floors for testing
    #at this moment, the wall has to be thick enough to prevent failling out
    ver_dim = (640, 20)
    hor_dim = (20, 480)
    top_wall = Wall(ver_dim, (0, 0))
    bot_wall = Wall(ver_dim, (0, 480))
    left_wall = Wall(hor_dim, (0, 0))
    right_wall = Wall((20,500), (640, 0))
    
    #add walls to group member list
    group_class.add(top_wall)
    group_class.add(bot_wall)
    group_class.add(left_wall)
    group_class.add(right_wall)
    