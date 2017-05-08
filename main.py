# -*- coding: utf-8 -*-
"""
Created on Sun May 17 12:41:58 2015

@author: larry
"""

import sys, pygame
import pygame.locals
import sprite_anime
import floor
import gameclock
from settings import Settings
import world

#some setting

size = width, height = Settings.screen_size
black = (0, 0, 0)
white = (255,255,255)


#constant FPS with lower rate of update per second
FPS = Settings.fps
ups = Settings.ups

#initial coor
coor = (100,0)


class Camera(object):
    pass


class Game(object):
    def __init__(self):       
        #initialize screen
        pygame.init()
        self.screen = pygame.display.set_mode(size)
        self.screen.fill(black)
        
        #initialize the world and camera
        self.my_world = world.World(self.screen)
        self.camera = world.Camera(self.screen)        
        
        #initialize gameclock
        self.clock = gameclock.GameClock(max_ups = Settings.ups,
                                         max_fps = Settings.fps,
                                         update_callback = self.my_world.update,
                                         frame_callback = self.camera.shoot,
                                         frame_callback_arg = self.my_world)
     
    def run(self):
        #main game loop
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    sys.exit()
            self.clock.tick()

        
if __name__ == '__main__':   
    Game().run()
        
pygame.quit()            
            