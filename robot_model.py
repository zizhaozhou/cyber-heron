# -*- coding: utf-8 -*-
"""
Created on Thu Mar  9 17:52:31 2023

@author: Zizhao Zhou
"""

import interaction as ITR
import random
from installation_model import Installation

class Harvest_robot:
    def __init__(self, env, location, company, build_installation = True):
        self.env = env
        self.location = location
        self.env.map[self.location].robot = True
        self.process = 0
        
        self.company = company
        self.cost = 0
        
        self.harvest_species = "pine"
        self.efficiency = 3
        self.speed = 0.2
        self.status = "awaiting"
        self.detect_radius = 4
        
        self.remain_threshold = 0.2
        self.harvest_threshold = 0.3
        
        self.destination = None
        
        self.harvest_plan = 0
        
        self.build_installation = True
        
    def change_status(self):
        
        self.destination = None

        
        search_list = []
        for x in range(-self.detect_radius,self.detect_radius+1):
            for y in range(-self.detect_radius,self.detect_radius+1):
                d = (self.location[0]+x, self.location[1]+y)
                if (x**2 + y**2 <= self.detect_radius**2) and (d in self.env.map.keys()) and d != self.location:
                    search_list.append(d)
        random.shuffle(search_list)
        
        bio_mass_list = []
        for loca in search_list:
            bio_mass_list.append(self.env.map[loca].bio_mass_density)
            
        max_biomass = self.harvest_threshold
        for i in range(0, len(search_list)):
            if bio_mass_list[i] > max_biomass and self.env.map[search_list[i]].robot == False:
                max_biomass = bio_mass_list[i]
                self.destination = search_list[i]
        
        if self.destination is not None:
            self.status = "re-deploying"
            self.process = 1
        else:
            self.status = "awaiting"
        
    def move(self):
        if self.env.map[self.destination].robot == False:
            total_dist = ((self.destination[0]-self.location[0])**2 + (self.destination[1]-self.location[1])**2)**0.5
            self.process -= self.speed/total_dist
            if self.process <= 0:
                self.status = "harvesting"
                self.env.map[self.location].robot = False
                self.env.map[self.destination].robot = True
                self.location = self.destination
                self.destination = None
                self.process = 1
        else:
            self.status = "awaiting"
            self.harvest_plan = 0
            self.process = 0
    
    def installation_set(self):
        if self.build_installation == True:
            self.env.map[self.location].installation.append(Installation(0, self.env.map[self.location]))
    
    def robot_update(self):
                
        if self.env.season == "spring":
            self.remain_threshold = 0.3
            self.harvest_threshold = 0.4
        else:
            self.remain_threshold = 0.2
            self.harvest_threshold = 0.3
            
        self.env.map[self.location].robot = True
    
    def robot_action(self):
        self.robot_update()
        if self.status == "awaiting":
            self.change_status()
        elif self.status == "re-deploying":
            self.move()
        elif self.status == "harvesting":
            self.harvest()
        
class Harvest_robot_CC(Harvest_robot):
    
    def __init__(self, env, location, company, proportion):
        super(Harvest_robot_CC, self).__init__(env, location, company)
        self.target = 0
        self.version = "CC"
        self.remain_threshold = 0.05
        self.harvest_threshold = 0.05
        self.efficiency = 30
        self.direction = proportion
        
        self.cost = 500
        self.company.robot_cost(self.cost)
        
    def change_status(self):
        
        self.destination = None

        search_list = []
        d = (self.location[0]+self.direction[0], self.location[1]+self.direction[1])
        if d in self.env.map.keys():
            search_list.append(d)
        random.shuffle(search_list)
        
        bio_mass_list = []
        for loca in search_list:
            bio_mass_list.append(self.env.map[loca].bio_mass_density)
            
        max_biomass = self.harvest_threshold
        for i in range(0, len(search_list)):
            if bio_mass_list[i] > max_biomass and self.env.map[search_list[i]].robot == False:
                max_biomass = bio_mass_list[i]
                self.destination = search_list[i]
        
        if self.destination is not None:
            self.status = "re-deploying"
            self.process = 1
        else:
            self.status = "awaiting"
    
    def harvest(self):
        a = self.env.map[self.location]
        if self.harvest_plan <= 0:
            self.harvest_plan = a.flora_CC[self.harvest_species]*(a.flora_ages[self.harvest_species][1]-self.target)
        else:
            self.process -= self.efficiency/self.harvest_plan
            self.company.mature_wood_profit(self.harvest_species, self.efficiency)
            b,d = ITR.Harvest(a, self.harvest_species, n=self.efficiency)
                
            if d < self.remain_threshold or self.process <= 0:
                self.status = "awaiting"
                self.installation_set()
                self.harvest_plan = 0
                self.process = 0

class Harvest_robot_MP(Harvest_robot):
    
    def __init__(self, env, location, company, proportion):
        super(Harvest_robot_MP, self).__init__(env, location, company)
        self.proportion = proportion
        self.version = "MP"
        self.efficiency = 15
        
    def harvest(self):
        a = self.env.map[self.location]
        if  self.harvest_plan <= 0:
            self.harvest_plan = a.flora_CC[self.harvest_species]*a.flora_ages[self.harvest_species][1]*self.proportion
        else:
            self.process -= self.efficiency/self.harvest_plan
            self.company.mature_wood_profit(self.harvest_species, self.efficiency)
            b,d = ITR.Harvest(a, self.harvest_species, n=self.efficiency)
            
            if d < self.remain_threshold or self.process <= 0:
                self.status = "awaiting"
                self.installation_set()
                self.harvest_plan = 0
                self.process = 0

'''                
class Harvest_robot_MT(Harvest_robot):
    
    def __init__(self, env, location, target):
        super(Harvest_robot_MT, self).__init__(env, location)
        self.target = target
        self.version = "MT"
        
    def harvest(self):
        a = self.env.map[self.location]
        if self.harvest_plan <= 0:
            self.harvest_plan = a.flora_CC[self.harvest_species]*(a.flora_ages[self.harvest_species][1]-self.target)
        else:
            self.process -= self.efficiency/self.harvest_plan
            b,d = ITR.Harvest(a, self.harvest_species, n=self.efficiency)
                
            if d < self.remain_threshold or self.process <= 0:
                self.status = "awaiting"
                self.harvest_plan = 0
                self.process = 0
'''            

class Harvest_robot_DC(Harvest_robot):
    
    def __init__(self, env, location, company, proportion):
        super(Harvest_robot_DC, self).__init__(env, location, company)
        self.proportion = proportion
        self.version = "DC"
        self.efficiency = 15
        self.remain_threshold = 0.2
        
    def change_status(self):
        
        self.destination = None
        
        search_list = []
        for x in range(-self.detect_radius,self.detect_radius+1):
            for y in range(-self.detect_radius,self.detect_radius+1):
                d = (self.location[0]+x, self.location[1]+y)
                if (x**2 + y**2 <= self.detect_radius**2) and (d in self.env.map.keys()) and d != self.location:
                    search_list.append(d)
        random.shuffle(search_list)
        
        deadtree_list = []
        for loca in search_list:
            r = self.harvest_species
            deadtree_list.append(self.env.map[loca].flora_CC[r]*self.env.map[loca].flora_ages[r][2])
            
        deadtree_amount = 0
        for i in range(0, len(search_list)):
            if deadtree_list[i] > deadtree_amount and self.env.map[search_list[i]].robot == False:
                deadtree_amount = deadtree_list[i]
                self.destination = search_list[i]
        
        if self.destination is not None:
            self.status = "re-deploying"
            self.process = 1
        else:
            self.status = "awaiting"
    
    def harvest(self):
        a = self.env.map[self.location]
        r = self.harvest_species
        if self.harvest_plan <= 0:
            self.harvest_plan = self.env.map[self.location].flora_CC[r]*self.env.map[self.location].flora_ages[r][2]
        else:
            self.process -= self.efficiency/self.harvest_plan
            self.company.dead_wood_profit(self.harvest_species, self.efficiency)
            b,d = ITR.Harvest(a, self.harvest_species, n=self.efficiency, target = "dead")
                
            if self.process <= 0 or a.flora_ages[r][2] <= self.remain_threshold:
                self.status = "awaiting"
                self.installation_set()
                self.harvest_plan = 0
                self.process = 0