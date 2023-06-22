# -*- coding: utf-8 -*-
"""
Created on Sun Mar 12 15:58:38 2023

@author: Zizhao Zhou
"""

## ----- render -----

import pygame, sys
import pygame.freetype
import random

## -----Color Define-----
WHITE = 255,255,255
BLACK = 0,0,0
RED = 255,0,0

WATER = 0,0,100
WETLAND = 20,100,255
GRASS = 10,255,0
FOREST = 0,100,0
URBAN = 128,128,128

BIRD = 255,0,0
BIRD_MATE = 255,150,0
BIRD_EGG =  0,0,0
BIRD_PATH = 150,0,0

ROBOT = 150,0,255
INSTALLATION = 200,200,0
FISH = 0,150,255
MOUSE = 200,100,0
FROG = 0,150,0
PINE = 0,100,0

FONT_PATH = "C://Windows//Fonts//times.ttf"

## ----- render function -----
def darker_color(color, dark):
    dark = max(0,min(dark,1))
    darker = (color[0]*dark, color[1]*dark, color[2]*dark)
    return darker

def alpha_color(color_a, alpha, color_b):
    alpha = max(0,min(alpha,1))
    new_color = (color_a[0]*alpha+color_b[0]*(1-alpha), color_a[1]*alpha+color_b[1]*(1-alpha), color_a[2]*alpha+color_b[2]*(1-alpha))
    return new_color

## ----- monitor -----

def map_display(surface, env, square_scale, color_list = [WATER, WETLAND, GRASS, FOREST, WHITE], mouse = None):
    
    for a in env.map.values():
        x_index = a.location[0]
        y_index = a.location[1]
        area_type = a.area_type
        pygame.draw.rect(surface, darker_color(color_list[area_type],(1-a.burn/100)), (x_index*square_scale, y_index*square_scale, square_scale, square_scale),0)
        pygame.draw.rect(surface, darker_color(color_list[area_type],(1-a.burn_debuff/100)), (x_index*square_scale, y_index*square_scale, square_scale, square_scale),1)
        if mouse is not None:
            if mouse == a.location:
                pygame.draw.rect(surface, WHITE, (x_index*square_scale, y_index*square_scale, square_scale, square_scale),2)

    
def bird_display(surface, bird, area_scale, original_point = (0,0), point_scale = 2, bird_simulation = True):
    for b in bird.values():
        if b.life_status == "egg":
            color = BIRD_EGG
        elif b.mate == True:
            color = BIRD_MATE
        else:
            color = BIRD
        if bird_simulation == True:
            location = b.location
            position = (location[0]+random.random())*area_scale+original_point[0] , (location[1]+random.random())*area_scale+original_point[1]
            if b.life_status in ["adult", "old"]:
                b.history_position.append(position)
            pygame.draw.circle(surface, color, position, point_scale)
        else:
            if len(b.history_position) > 0 and b.life_status in ["adult", "old"]:
                position = b.history_position[-1]
                pygame.draw.circle(surface, color, position, point_scale)
            

def bird_trace_display(surface, bird, n=2):
    for b in bird.values():
        if len(b.history_position) > 2:
            pygame.draw.lines(surface, BIRD_PATH, False, [b.history_position[-2], b.history_position[-1]], 1)

def robot_display(surface, robot, area_scale, original_point = (0,0), point_scale = 4):
    for r in robot.values():
        if r.status == "re-deploying":
            p = r.process
            position = (r.location[0]*p+r.destination[0]*(1-p)+0.5)*area_scale+original_point[0] , (r.location[1]*p+r.destination[1]*(1-p)+0.5)*area_scale+original_point[1]
        else:
            position = (r.location[0]+0.5)*area_scale+original_point[0] , (r.location[1]+0.5)*area_scale+original_point[1]
        pygame.draw.circle(surface, ROBOT, position, point_scale)
        robot_info = r.status + ": " + str(1-r.process)[:4]
        FONT = pygame.freetype.Font(FONT_PATH, point_scale)
        FONT.render_to(surface, (position[0],position[1]+point_scale*2), robot_info, fgcolor=ROBOT, size=10)

def installation_display(surface, env, area_scale):
    color_list = [WATER, WETLAND, GRASS, FOREST, WHITE]
    for a in env.map.values():
        if len(a.installation) > 0:
            x_index = a.location[0]
            y_index = a.location[1]
            area_type = a.area_type
            
            alpha = 0
            for inst in a.installation:
                if inst.life/360 > alpha:
                    alpha = inst.life/360
            pygame.draw.rect(surface, alpha_color(INSTALLATION, alpha, darker_color(color_list[area_type],(1-a.burn/100))), ((x_index+0.4)*area_scale, (y_index+0.4)*area_scale, area_scale*0.2, area_scale*0.2),0)
            
    
## ----- data display -----

def envinfo_display(surface, env, position, text_size = 15, distance = 3, color = WHITE):
    envinfo = []
    envinfo.append("season: " + env.season)
    envinfo.append("month: " + str(env.month))
    envinfo.append("date: " + str(env.date))
    envinfo.append("timetick: " + str(env.timetick)+":00")
    envinfo.append("time: " + env.time)
    envinfo.append("weather: " + env.weather)
    envinfo.append("----resoueces----")
    envinfo.append("heron_total: " + str(env.heron_total))
    envinfo.append("heron_ages: " + str(env.heron_ages))
    envinfo.append("fish_total: " + str(env.animal["fish"].total)[:8])
    envinfo.append("frog_total: " + str(env.animal["frog"].total)[:8])
    envinfo.append("mouse_total: " + str(env.animal["mouse"].total)[:8])
    envinfo.append("pine_total: " + str(env.tree["pine"].total)[:8])
    ##envinfo.append("competitor_total: " + str(env.competitor_total))

    FONT = pygame.freetype.Font(FONT_PATH, text_size)
    for i in range(0,len(envinfo)):
        FONT.render_to(surface, (position[0],position[1]+i*text_size), envinfo[i], fgcolor=color, size=15)

def resources_display(surface, env, target, position, text_size = 15, distance = 3, color = WHITE):
    
    if target is not None:
        
        resources_info = []
        
        for r in env.map[target].flora_CC.keys():
            resources_info.append(r + "_immature: " + str(len(env.map[target].flora_ages[r][0]))[:8])
            resources_info.append(r + "_mature: " + str(env.map[target].flora_CC[r]*env.map[target].flora_ages[r][1])[:8])
            resources_info.append(r + "_dead: " + str(env.map[target].flora_CC[r]*env.map[target].flora_ages[r][2])[:8])
        resources_info.append("bio_mass: " + str(env.map[target].bio_mass)[:8])
        resources_info.append("bio_density: " + str(env.map[target].bio_mass_density)[:8])
        resources_info.append(" ")
        for r in env.map[target].fauna.keys():
            resources_info.append(r + ": " + str(env.map[target].fauna[r])[:8])
        resources_info.append(" ")
        resources_info.append("burn: " + str(env.map[target].burn)[:8])
        resources_info.append("burn_debuff: " + str(env.map[target].burn_debuff)[:8])
        resources_info.append(" ")
        resources_info.append("hunt_debuff: " + str(env.map[target].hunt_debuff)[:8])
        FONT = pygame.freetype.Font(FONT_PATH, text_size)
        for i in range(0,len(resources_info)):
            FONT.render_to(surface, (position[0],position[1]+i*text_size), resources_info[i], fgcolor=color, size=15)

## ----- UI display -----
def button_display(surface, buttons, ON_color = WHITE, OFF_color = BLACK, text = None, text_size = 15):
    for bt in buttons:
        FONT = pygame.freetype.Font(FONT_PATH, text_size)
        if text is None:
            display_text = bt.name
        else:
            display_text = bt.name
            
        if bt.buttondown == True:
            pygame.draw.rect(surface, ON_color, (bt.position1[0], bt.position1[1], bt.scale[0], bt.scale[1]),0)
            FONT.render_to(surface, (bt.position1[0] + text_size/2, bt.position1[1]+ bt.scale[1]/2), display_text, fgcolor = OFF_color, size = text_size)
        else:
            pygame.draw.rect(surface, OFF_color, (bt.position1[0], bt.position1[1], bt.scale[0], bt.scale[1]),0)
            FONT.render_to(surface, (bt.position1[0] + text_size/2, bt.position1[1]+ bt.scale[1]/2), display_text, fgcolor = ON_color, size = text_size)
        pygame.draw.rect(surface, ON_color, (bt.position1[0], bt.position1[1], bt.scale[0], bt.scale[1]),2)
        

## ----- analysis diagram -----

def fauna_amount_display(surface, env, position, x_scale, y_scale, x_max):
    display_lists = [env.animal["fish"].history_amount, env.animal["mouse"].history_amount, env.animal["frog"].history_amount, env.heron_history_amount]
    color_list = [FISH, MOUSE, FROG, BIRD]
    d = 0
    
    pygame.draw.lines(surface, WHITE, False, [position,(position[0],position[1]+y_scale),(position[0]+x_scale,position[1]+y_scale)],2)
    for datalist in display_lists:
        
        data_max = max(datalist)
        if len(datalist) > x_max:
            datalist = datalist[-x_max:-1]
        point_list = []
        for i in range(0,len(datalist)):
            point_list.append((i/x_max*x_scale+position[0], y_scale-y_scale*(datalist[i]/data_max)+position[1]))
            if len(datalist) == 1:
                point_list.append(((i+1)/x_max*x_scale+position[0], y_scale-y_scale*(datalist[i]/data_max)+position[1]))
        pygame.draw.lines(surface, color_list[d], False, point_list)
        
        d += 1

def flora_amount_display(surface, env, position, x_scale, y_scale, x_max):
    species_list = ["pine"]
    color_list = [PINE]
    d = 0
        
    pygame.draw.lines(surface, WHITE, False, [position,(position[0],position[1]+y_scale),(position[0]+x_scale,position[1]+y_scale)],2)
    for specie in species_list:
        datalist = env.tree[specie].history_amount
        data_max = max(datalist)
        if len(datalist) > x_max:
            datalist = datalist[-x_max:-1]
        point_list = []
        for i in range(0,len(datalist)):
            point_list.append((i/x_max*x_scale+position[0], y_scale-y_scale*(datalist[i]/data_max)+position[1]))
            if len(datalist) == 1:
                point_list.append(((i+1)/x_max*x_scale+position[0], y_scale-y_scale*(datalist[i]/data_max)+position[1]))
        pygame.draw.lines(surface, color_list[d], False, point_list)
        
        d += 1
            
## ----- analysis map -----

def bio_mass_display(surface, env, square_scale, original_point, color = (255,255,255), max_biomass = 1000, min_biomass = 0, mouse = None):
    
    for a in env.map.values():
        x_index = a.location[0]
        y_index = a.location[1]
        b = max(min(a.bio_mass/max_biomass, 1),min_biomass)
        pygame.draw.rect(surface, darker_color(color,b), (x_index*square_scale+original_point[0], y_index*square_scale+original_point[1], square_scale, square_scale),0)
        ##pygame.draw.rect(surface, darker_color(color,b), (x_index*square_scale, y_index*square_scale, square_scale, square_scale),1)
        if mouse is not None:
            if mouse == a.location:
                pygame.draw.rect(surface, RED, (x_index*square_scale+original_point[0], y_index*square_scale+original_point[1], square_scale, square_scale),2)

def burn_display(surface, env, square_scale, original_point, color = (255,0,0), max_biomass = 1000, min_biomass = 0, mouse = None):
    
    for a in env.map.values():
        x_index = a.location[0]
        y_index = a.location[1]
        burn = a.burn/100
        burn_debuff = a.burn_debuff/100
        pygame.draw.rect(surface, darker_color(color,burn), (x_index*square_scale+original_point[0], y_index*square_scale+original_point[1], square_scale, square_scale),0)
        ##pygame.draw.rect(surface, darker_color(color,burn_debuff), (x_index*square_scale+original_point[0], y_index*square_scale+original_point[1], square_scale, square_scale),1)
        pygame.draw.lines(surface, darker_color(color,max(burn,burn_debuff)), False, [(x_index*square_scale+original_point[0],y_index*square_scale+original_point[1]), (x_index*square_scale+original_point[0]+square_scale,y_index*square_scale+original_point[1]+square_scale)], 2)
        pygame.draw.lines(surface, darker_color(color,max(burn,burn_debuff)), False, [(x_index*square_scale+original_point[0]+square_scale,y_index*square_scale+original_point[1]), (x_index*square_scale+original_point[0],y_index*square_scale+original_point[1]+square_scale)], 2)
        if mouse is not None:
            if mouse == a.location:
                pygame.draw.rect(surface, WHITE, (x_index*square_scale+original_point[0], y_index*square_scale+original_point[1], square_scale, square_scale),2)

def bird_history_display(surface, env, square_scale, bird, original_point, n=10, color=(255,100,0), point_scale = 1, mouse = None):
    for b in bird.values():
        if len(b.history_position) > 0:
            for p in b.history_position[-n:]:
                pygame.draw.circle(surface, color, (p[0]+original_point[0], p[1]+original_point[1]), point_scale)
    
    if mouse is not None:
        for a in env.map.values():
            if mouse == a.location:
                x_index = a.location[0]
                y_index = a.location[1]
                pygame.draw.rect(surface, WHITE, (x_index*square_scale+original_point[0], y_index*square_scale+original_point[1], square_scale, square_scale),2)
## def ages_display(surface, env, position, ages_list, text_size = 15, distance = 3, color = WHITE):
    
## -----business model-----
def profit_display(surface, company, position, x_scale, y_scale, x_max, y_max = 5000):
    pygame.draw.lines(surface, WHITE, False, [position,(position[0],position[1]+y_scale),(position[0]+x_scale,position[1]+y_scale)],2)
    month_profit = []
    for i in range(0,len(company.profit_record)):
        if i < 30:
            profit_ave = sum(company.profit_record[0:i])/(i+1)
        else:
            profit_ave = sum(company.profit_record[i-29:i])/30
        month_profit.append(profit_ave)
    display_lists = [company.earn_record, company.cost_record, month_profit]
    color_list = [(0,255,0), (255,0,0), (255,255,255)]
    d = 0
    
    pygame.draw.lines(surface, WHITE, False, [position,(position[0],position[1]+y_scale),(position[0]+x_scale,position[1]+y_scale)],2)
    
    data_max = y_max
    for datalist in display_lists:
        if max(datalist)>data_max:
            data_max = max(datalist)
            
    for datalist in display_lists:
        
        if len(datalist) > x_max:
            datalist = datalist[-x_max:-1]
        point_list = []
        for i in range(0,len(datalist)):
            point_list.append((i/x_max*x_scale+position[0], y_scale-y_scale*(datalist[i]/data_max)+position[1]))
            if len(datalist) == 1:
                point_list.append(((i+1)/x_max*x_scale+position[0], y_scale-y_scale*(datalist[i]/data_max)+position[1]))
        pygame.draw.lines(surface, color_list[d], False, point_list, 1)
        
        d += 1