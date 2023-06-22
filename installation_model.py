# -*- coding: utf-8 -*-
"""
Created on Thu Apr 20 11:51:34 2023

@author: Zizhao Zhou
"""
class Installation:
    def __init__(self, num ,area, life = 360):
        self.num = num
        self.life = life
        self.area = area
        self.location = area.location
        self.decomposed = False
        
    def update(self):
        if self.decomposed == False:
            
            if self.area.burn == 0 and self.area.burn_debuff > 0:
                self.area.burn_debuff = max(self.area.burn_debuff*0.99, 0)
            
            self.life = max(0, self.life-1)
        
        if self.life <= 0:
            self.decomposed = True