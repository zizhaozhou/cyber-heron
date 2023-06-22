# -*- coding: utf-8 -*-
"""
Created on Fri Feb 10 20:45:27 2023

@author: Zizhao Zhou
"""

import random
import pygame

def mouse_location(position, grid_x, grid_y, area_scale):
    x = position[0] // area_scale
    y = position[1] // area_scale
    if x < grid_x and y < grid_y:
        return(x,y)
    else:
        return None
    
def image_save(env, surface):
    
    img_name = str(env.month) + "-" + str(env.date) + "-" + str(env.timetick) + ".bmp"
    pygame.image.save(surface, img_name)

class Button:
    def __init__(self, name, button_type, surface, position, scale):
        self.name = name
        self.button_type = button_type
        self.position1 = position
        self.scale = scale
        self.position2 = (position[0] + scale[0], position[1] + scale[1])
        
        self.buttondown = False
        
    def click_detect(self, click_position):
        if click_position[0] > self.position1[0] and click_position[1] > self.position1[1] and click_position[0] < self.position2[0] and click_position[1] < self.position2[1] :
            self.buttondown = True
            return True
        else:
            return False
        
    def button_relese(self):
        self.buttondown = False
    
class Sub_display_button(Button):
    def __init__(self, mood, button_type, surface, position, scale):
        super(Sub_display_button, self).__init__(mood, button_type, surface, position, scale)
        self.mood = mood
        
    def mood_switch(self):
        return self.mood
    
class Robot_mood_button(Button):
    def __init__(self, mood, button_type, surface, position, scale):
        super(Robot_mood_button, self).__init__(mood, button_type, surface, position, scale)
        self.mood = mood
        
    def mood_switch(self):
        return self.mood
    
class Amount_display_button(Button):
    def __init__(self, mood, button_type, surface, position, scale):
        super(Amount_display_button, self).__init__(mood, button_type, surface, position, scale)
        self.mood = mood
        
    def mood_switch(self):
        return self.mood