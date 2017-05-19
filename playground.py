#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat May  6 22:00:26 2017

@author: larry
"""

import pygame

white = (255,255,255)

class Playground(pygame.sprite.Sprite):
    def __init__(self):
        super(Playground, self).__init__()
        self.bot_bound = pygame.Surface((640,3))
        self.top_bound = pygame.Surface((640,3))
        self.left_bound = pygame.Surface((3,480))
        self.right_bound = pygame.Surface((3,480))
        self.bot_bound.fill(white)
        self.top_bound.fill(white)
        self.left_bound.fill(white)
        self.right_bound.fill(white)