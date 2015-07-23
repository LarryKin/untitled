# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 14:31:50 2015

@author: larry
"""
import pygame

white = (255,255,255)
class floor(pygame.sprite.Sprite):
    def __init__(self):
        super(floor, self).__init__()
        self.image = pygame.Surface((200,3))
        self.image.fill(white)
        self.rect = self.image.get_bounding_rect()
        self.rect.topleft = (100,100)
        self.x = self.rect.topleft[0]
        self.y = self.rect.topleft[1]
          
        
        