# -*- coding: utf-8 -*-
"""
Created on Thu Mar  9 15:55:48 2023

@author: Zizhao Zhou
"""

##from species_model import Specie, Animal, Tree
##from area_model import Area, Water_area, Wetland_area, Grass_area, Forest_area, Urban_area

def P_harvest (area, species = [], proportion = 1):
    harvest_species = []
    harvest_wood = dict()
    if species == []:
        for s in area.flora_CC.keys():
            harvest_species.append(s)
    else:
        harvest_species = species
        
    for s in harvest_species:
        n = area.flora_ages[s][1]*area.flora_CC[s]*proportion
        area.flora_ages[s][1] = area.flora_ages[s][1]*(1-proportion)
        harvest_wood[s] = n
        
    return harvest_wood

def T_harvest (area, species = [], target_density = 0.2):
    harvest_species = []
    harvest_wood = dict()
    if species == []:
        for s in area.flora_CC.keys():
            harvest_species.append(s)
    else:
        harvest_species = species
        
    for s in harvest_species:
        if area.flora_ages[s][1] > target_density:
            n = (area.flora_ages[s][1] - target_density)*area.flora_CC[s]
            area.flora_ages[s][1] = target_density
        else:
            n = 0
        harvest_wood[s] = n
    
    return harvest_wood

def Harvest (area, specie, n = 1, target = "mature"):
    if target == "mature":
        area.flora_ages[specie][1] = max((area.flora_ages[specie][1] - n/area.flora_CC[specie]), 0)
    elif target == "dead":
        area.flora_ages[specie][2] = max((area.flora_ages[specie][2] - n/area.flora_CC[specie]), 0)
        print(area.flora_ages[specie][2])
        
    b,d = area.bio_mass_calculate()
    return b,d