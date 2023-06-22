# -*- coding: utf-8 -*-
"""
Created on Fri Feb 10 09:34:15 2023

@author: Zizhao Zhou
"""

from area_model import Area, Water_area, Wetland_area, Grass_area, Forest_area, Urban_area
from bird_model import Gene, Heron
from species_model import Specie, Animal, Tree
import random


        
class Enviornment:
    
    ## ----- initialization -----
    
    def __init__(self, x_scale, y_scale, heron_init, start_time = [1,1,0]):
              
        self.map = dict()

        for x in range(0,x_scale):
            for y in range(0,y_scale):
                self.map[(x,y)] = Area((x,y))
                
        self.animal = dict()
        self.tree = dict()
        
        self.year = 0
        self.month = start_time[0]
        self.date = start_time[1]
        self.timetick = start_time[2]
        
        self.temperature_list = [55, 60, 65, 72, 80, 88, 95, 93, 88, 78, 62, 74]
        self.temperature = self.temperature_list[self.month-1]
        self.rainy_possibility = [0.4, 0.3, 0.1, 0.1, 0, 0, 0, 0, 0, 0.1, 0.3, 0.2]
        self.weather = "sunny"
        self.time = "night"
        self.season = "winter"

        self.heron = None
        self.heron_num = 0
        self.heron_total = 0
        self.heron_ages = None
        self.heron_history_amount = []
        
        self.gene_ave = dict()
                
    def area_define(self, location, area_type):
        if area_type == 0:
            self.map[location] = Water_area(location)
        elif area_type == 1:
            self.map[location] = Wetland_area(location)
        elif area_type == 2:
            self.map[location] = Grass_area(location)
        elif area_type == 3:
            self.map[location] = Forest_area(location)
        elif area_type == 4:
            self.map[location] = Urban_area(location)
                   
    def species_define(self, name, total, bio_status, max_capacity, max_increase, power = 0, nutrition = 0, p_sum = 0):
        if bio_status == "prey" or bio_status == "hunter":
            self.animal[name] = Animal(name, total, bio_status, max_capacity, max_increase, power, nutrition, p_sum)
            for a in self.map.values():
                a.fauna[name] = 0
                a.fauna_p[name] = 0
                a.resources_p_init()
                
            s = 0
            for a in self.map.values():
                s += a.fauna_p[name]
                
            for a in self.map.values():
                a.fauna_calculate(name, total, s)
                
        elif bio_status == "producer":
            self.tree[name] = Tree(name, total, bio_status, max_capacity, max_increase)
            for a in self.map.values():
                a.flora_CC[name] = 0
                a.flora_p[name] = 0
                a.flora_ages[name] = [[],0.9,0] ##[[Immature days], Mature number, Dead number]
                a.resources_p_init()
                
            s = 0
            for a in self.map.values():
                s += a.flora_p[name]
                
            for a in self.map.values():
                a.flora_calculate(name, total, s)

            

    def heron_count(self):
        count = [0,0,0,0]
        for b in self.heron.values():
            if b.life_status == "egg":
                count[0] += 1
            elif b.life_status == "youth":
                count[1] += 1
            elif b.life_status == "adult":
                count[2] += 1
            elif b.life_status == "old":
                count[3] += 1
        self.heron_total = count[1] + count[2] + count[3]
        self.heron_ages = count
        
    def birds_define(self, birds, record = True):
        self.heron = birds
        self.heron_count()
        self.heron_num = self.heron_total
        if record == True:
            self.heron_history_amount.append(self.heron_total)
            
    ## ----- fire -----
    
    def fire_set(self, location):
        self.map[location].burn = min(self.map[location].bio_mass_density, 1)*100
        for b in self.heron.values():
            if b.location == location:
                if b.life_status == "egg" or b.life_status == "youth":
                    b.dead = True
                else:
                    fire_danger = random.random()
                    if fire_danger < b.DEX/100:
                        b.dead == True
        
    def fire_spread(self):
        spread_list = []
        direction_list = [(0,1),(0,-1),(1,0),(-1,0)]
        for a in self.map.values():
            a.burn_update(self.weather)
            if a.burn > 10:
                for d in direction_list:
                    location = (a.location[0]+d[0], a.location[1]+d[1])
                    if location in self.map.keys() and location not in spread_list:
                        if self.map[location].burn == 0:
                            spread_list.append(self.map[location])
        for a in spread_list:
            fire_risk = 0
            if a.area_type == 0:
                fire_risk = 0
            elif a.area_type == 1:
                fire_risk = 0.1
            elif a.area_type == 2:
                fire_risk = 0.7 * a.bio_mass_density**2
            elif a.area_type == 3:
                fire_risk = 0.9 * a.bio_mass_density**2
            if self.weather == "rainy":
                fire_risk = 0
            fire = random.random()
            if fire < fire_risk*(self.temperature/100)*0.5:
                self.fire_set(a.location)
    
    ## -----calculatoin-----
    
    def resource_consume(self, fish_consume, mouse_consume, frog_consume):
        self.animal["fish"].total = self.animal["fish"].total - fish_consume
        self.animal["mouse"].total = self.animal["mouse"].total - mouse_consume
        self.animal["frog"].total = self.animal["frog"].total - frog_consume
        
    def sum_update(self, specie, bio_status):
        if bio_status == "prey" or bio_status == "hunter":
            self.animal[specie].p_sum = 0
            for a in self.map.values():
                self.animal[specie].p_sum += a.fauna_p[specie]*(1-a.burn_debuff/100)
        elif bio_status == "producer":
            self.tree[specie].p_sum = 0
            for a in self.map.values():
                self.tree[specie].p_sum += a.flora_p[specie]
        
    def resource_update(self):
        for s in self.animal.keys():
            self.animal[s].specie_increase()
            self.sum_update(s, self.animal[s].bio_status)
            for a in self.map.values():
                if a.burn > 20:
                    self.animal[s].total -= a.fauna[s]
                    a.fauna[s] = 0
                    print("burnt")
                else:
                    a.fauna_calculate(s, self.animal[s].total, self.animal[s].p_sum)
                
        for s in self.tree.keys():
            t = 0
            for a in self.map.values():
                self.tree[s].specie_increase(a)
                t += a.flora_CC[self.tree[s].name]*a.flora_ages[self.tree[s].name][1]
            self.tree[s].total = t
        
        for a in self.map.values():
            a.bio_mass_calculate()
            a.hunt_debuff = min(a.hunt_debuff+0.01, 1)
        
        
            
        ##self.competitor_total = self.competitor_total + self.competitor_total*((food/20-self.heron_total)-self.competitor_total)/(((food/20-self.heron_total)/2)**2)*5

    def gene_ave_update(self):
        for g in ["hungry_threshold", "tired_threshold", "mate_tendence", "child_tendence", "fish_preference", "risky_rest"]:
            s = 0
            n = 0
            for b in self.heron.values():
                if b.life_status != "egg":
                    s = s+b.gene.DNA[g]
                    n += 1
            self.gene_ave[g] = s/n

    def bird_behavior(self):
        
        fish_consume = 0
        mouse_consume = 0
        frog_consume = 0
        new_born = []
        
        for b in self.heron.values():
            if b.life_status == "adult" or b.life_status == "old":
            
                b.strategy = b.decide_strategy(timetick = self.timetick, season = self.season)
                
                if b.strategy == "hunt":
                    
                    b.destination = b.hunting_place(min(b.endurance_left/b.energy_per_dist, b.sense_radius))
                    b.move(b.destination)
                    
                    result = b.hunt(self.map[b.location], self.animal)
                    if result[0] == "fish":
                        fish_consume += result[1]
                    if result[0] == "mouse":
                        mouse_consume += result[1]
                    if result[0] == "frog":
                        frog_consume += result[1]
                        
                elif b.strategy == "rest":
                    
                    b.destination = b.rest_place(min(b.endurance_left/b.energy_per_dist, b.sense_radius))
                    b.move(b.destination)
                    b.rest()
                    
                elif b.strategy == "mate":
                    if b.gender == 1:
                        b.destination = b.nest_place(min(b.endurance_left/b.energy_per_dist, b.sense_radius))
                        b.move(b.destination)
                        b.endurance_left -= 5
                        
                elif b.strategy == "child":
                    
                    b.destination = b.nest
                    b.move(b.destination)
                    b.raise_child()
                    
            elif b.life_status == "youth":
                b.food_left -= 0.1
        
        for b in self.heron.values():
            
            if b.gender == 0 and b.strategy == "mate":
                partner = b.partner_seek(min(b.endurance_left/2, b.sense_radius))
                
                if partner is not None:
                    b.destination = partner.location
                    b.move(b.destination)
                    if random.random() < (b.APP/100)*(partner.APP/100):
                        b.mate_with(partner)
                        eggs, n = b.birth(self.heron_num)
                        b.endurance_left -= 5
                        new_born = new_born + eggs
                        self.heron_num += n
                            
            if b.strategy == "mate":
                b.endurance_left -= 5
                b.food_left -= 5
                
        ## -----Birth Process-----
        for b in new_born:
            self.heron[b.num] = b
        

        ## -----Dying Process-----
        death_note = []
        for b in self.heron.keys():
            self.heron[b].danger(self.heron_total/10, self.timetick)
            self.heron[b].heat_lose()
            self.heron[b].heat_generate()
            if self.heron[b].refresh() == False:
                death_note.append(b)
        for i in death_note:
            del self.heron[i]
        
        for b in self.heron.values():
            b.children_refresh()
            
        self.heron_count()

        self.resource_consume(fish_consume, mouse_consume, frog_consume)
    
    ## ----time pass----
    
    def time_update(self):
        date_swich = False
        month_swich = False
        year_swich = False
        
        if self.timetick + 3 >= 24:
            date_swich = True
            if self.date + 1 >= 31:
                month_swich = True
                if self.month + 1 > 12:
                    year_swich = True
                
        self.timetick = (self.timetick + 3) % 24
        
        if date_swich == True:
            
            self.date = self.date % 30 + 1
            
            ##self.resource_update()
            
            for b in self.heron.values():
                b.grow()
            
            self.heron_history_amount.append(self.heron_total)
            for s in self.animal.values():
                s.history_record()
            for s in self.tree.values():
                s.history_record()
                
            ##self.gene_ave_update()
            
            for a in self.map.values():
                if len(a.installation) > 0:
                    for inst in a.installation:
                        if inst.decomposed == False:
                            inst.update()
            
        if month_swich == True:
            
            self.month = self.month % 12 + 1
            
        if year_swich == True:
            print("new year")
            for b in self.heron.values():
                b.mate_reset()
            self.year += 1
            
        if self.timetick < 6:
            self.time = "night"
        elif self.timetick < 12:
            self.time = "morning"
        elif self.timetick < 18:
            self.time = "afternoon"
        else:
            self.time = "evening"
            
        if self.month in [12,1,2]:
            self.season = "winter"
        elif self.month in [3,4,5]:
            self.season = "spring"
        elif self.month in [6,7,8]:
            self.season = "summer"
        elif self.month in [9,10,11]:
            self.season = "autumn"
            
        if random.random() < self.rainy_possibility[self.month-1]:
            self.weather = "rainy"
        else:
            self.weather = "sunny"
            
        if self.time == "morning" or self.time == "afternoon":
            self.temperature = self.temperature_list[self.month-1] + 2
        else:
            self.temperature = self.temperature_list[self.month-1] - 2

        

