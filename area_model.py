# -*- coding: utf-8 -*-
"""
Created on Thu Feb  9 23:19:05 2023

@author: Zizhao Zhou
"""
import math
import statistics
import random

class Area:
    
    def __init__(self, location, risk = 1, area_type = -1):
        ##self.env = env
        self.location = location
        self.risk = risk
        self.area_type = area_type
        
        self.fauna = dict()
        self.fauna_p = dict()
        
        self.flora_CC = dict() 
        self.flora_p = dict()
        self.flora_ages = dict()
        
        self.bio_mass = 1000
        self.bio_mass_max = 1000
        self.bio_mass_density = 1
        
        self.robot = False
        
        self.installation = []

        self.burn = 0
        self.burn_debuff = 0
        
        self.hunt_debuff = 1
        
    def fauna_update(self, specie, amount):
        self.fauna[specie] = amount
    
    def fauna_calculate(self, specie, total, p_sum):
        self.fauna[specie] = total * (self.fauna_p[specie]*(1-self.burn_debuff/100)/p_sum)
        if specie == "frog":
            self.fauna[specie] = total * (self.fauna_p[specie]*(1-self.burn_debuff/100)/p_sum)*self.bio_mass_density
        
    def flora_calculate(self, specie, total, p_sum):
        self.flora_CC[specie] = total * (self.flora_p[specie]/p_sum)
    
    def bio_mass_calculate(self):
        self.bio_mass = 0
        for s in self.flora_CC.keys():
            self.bio_mass = self.bio_mass + self.flora_CC[s] * self.flora_ages[s][1] + sum(self.flora_ages[s][0])/3600
            
        if self.area_type == 4:
            self.bio_mass += 50*(1-self.burn_debuff/100)
        elif self.area_type == 3:
            self.bio_mass += 300*(1-self.burn_debuff/100)
        elif self.area_type == 2:
            self.bio_mass += 600*(1-self.burn_debuff/100)
        elif self.area_type == 1:
            self.bio_mass += 100*(1-self.burn_debuff/100)
            
        self.bio_mass_density = min(self.bio_mass/self.bio_mass_max, 1)
            
        return self.bio_mass, self.bio_mass_density
    
    def burn_update(self, weather):
        
        if self.burn > 0:
            for s in self.flora_CC.keys():
                if self.flora_CC[s] > 0:
                    burnt_tree = self.flora_CC[s]*self.flora_ages[s][1]*self.burn/100
                    self.flora_ages[s][1] -= burnt_tree/self.flora_CC[s]
                    self.flora_ages[s][2] += burnt_tree/self.flora_CC[s]
                    i = 0
                    while i < len(self.flora_ages[s][0]):
                        if random.random()<self.burn/100:
                            self.flora_ages[s][0].pop(i)
                        else:
                            i += 1
                
        if self.burn > 0:
            if weather == "rainy":
                self.burn = max(self.burn - 40, 0)
            else:
                self.burn = max(self.burn - 2, 0)
            self.burn_debuff = min(self.burn_debuff + 30, 100)
            
        if self.burn == 0 and self.burn_debuff > 0:
            self.burn_debuff = max(self.burn_debuff - 0.01, 0)
        
class Water_area(Area):
    
    def __init__(self, location, risk = 0.25, area_type = 0):
        super(Water_area, self).__init__(location, risk, area_type)
    
    def resources_p_init(self):
        self.fauna_p["fish"] = 25
        
class Wetland_area(Area):
    
    def __init__(self, location, risk = 0.1, area_type = 1):
        super(Wetland_area, self).__init__(location, risk, area_type)
        
    def resources_p_init(self):
        self.fauna_p["fish"] = 15
        self.fauna_p["mouse"] = 10
        self.fauna_p["frog"] = 5
        self.flora_p["fungus"] = 15
        
class Grass_area(Area):
    
    def __init__(self, location, risk = 0.2, area_type = 2):
        super(Grass_area, self).__init__(location, risk, area_type)
        
    def resources_p_init(self):
        self.flora_p["pine"] = 1
        self.fauna_p["mouse"] = 20
        self.fauna_p["fungus"] = 10
        
class Forest_area(Area):
    
    def __init__(self, location, risk = 0.05, area_type = 3):
        super(Forest_area, self).__init__(location, risk, area_type)
        
    def resources_p_init(self):
        self.flora_p["pine"] = 20
        self.fauna_p["mouse"] = 10
        self.fauna_p["frog"] = 40
        self.flora_p["fungus"] = 20
    
class Urban_area(Area):
    
    def __init__(self, location, risk = 0.1, area_type = 4):
        super(Urban_area, self).__init__(location, risk, area_type)
        
    def resources_p_init(self):
        self.flora_p["pine"] = 1
        self.fauna_p["mouse"] = 10
        self.flora_p["fungus"] = 5