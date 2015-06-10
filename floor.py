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
        self.rect = (0,100,200,3)
          
        
        