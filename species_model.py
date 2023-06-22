# -*- coding: utf-8 -*-
"""
Created on Mon Mar  6 13:12:51 2023

@author: Zizhao Zhou
"""

import random

class Specie:
    
    def __init__(self, name, total, bio_status, max_capacity, max_increase):
        self.name = name
        self.total = total
        self.bio_status = bio_status
        self.max_capacity = max_capacity
        self.max_increase = max_increase

        self.history_amount = []
        self.history_amount.append(self.total)
        
    

    def history_record(self):
        self.history_amount.append(self.total)

class Animal(Specie):
    def __init__(self, name, total, bio_status, max_capacity, max_increase, power, nutrition = 0, p_sum = 0):
        super(Animal, self).__init__(name, total, bio_status, max_capacity, max_increase)
        self.power = power
        self.nutrition = nutrition
        self.p_sum = p_sum
    
    def specie_increase(self):
        if self.bio_status == "prey":
            self.total = self.total + self.total*(self.max_capacity-self.total)/((self.max_capacity/2)**2)*self.max_increase
        
class Tree(Specie):
    def __init__(self, name, total, bio_status, max_capacity, max_increase, mature_age=3600, power=0, nutrition = 0, p_sum = 0):
        super(Tree, self).__init__(name, total, bio_status, max_capacity, max_increase)
        self.mature_age = mature_age
        
    def specie_increase(self, area):
        space_left = area.flora_CC[self.name] - (area.flora_ages[self.name][1]*area.flora_CC[self.name] + len(area.flora_ages[self.name][0]))
        if space_left < 0 :
            if -space_left > len(area.flora_ages[self.name][0]):
                area.flora_ages[self.name][1] = 1
                area.flora_ages[self.name][0].clear()
            else:
                while space_left < 0:
                    for j in range(0, len(area.flora_ages[self.name][0])):
                        if area.flora_ages[self.name][0][j] == min(area.flora_ages[self.name][0]):
                            area.flora_ages[self.name][0].pop(j)
                            break
                    space_left += 1
        elif space_left > 0:
            j = 0
            for i in range(0, len(area.flora_ages[self.name][0])):
                if area.flora_ages[self.name][0][j] > self.mature_age:
                    print("mature",area.flora_ages[self.name][0][j])
                    area.flora_ages[self.name][0].pop(j)
                    area.flora_ages[self.name][1] = area.flora_ages[self.name][1] + 1/area.flora_CC[self.name]
                else:
                    area.flora_ages[self.name][0][j] += 1/8
                    j += 1
                    
        if random.random() < self.max_increase*area.flora_ages[self.name][1]:
            area.flora_ages[self.name][0].append(0)
            
                
                             
    