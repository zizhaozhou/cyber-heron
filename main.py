# -*- coding: utf-8 -*-
"""
Created on Fri Feb 10 15:45:16 2023

@author: Zizhao Zhou
"""

from map_model import Enviornment
from bird_model import Gene, Heron
import business_model as BS
import robot_model as RB
import pygame, sys
import random
import cv2
import render as RD
import UI
import interaction as ITR

## -----Master plan read-----
def color_recognition(rgb):
    R = int(rgb[2] >= 128)
    G = int(rgb[1] >= 128)
    B = int(rgb[0] >= 128)
    RGB = [R, G, B]
    if RGB == [1,1,1]:
        color = "white"
    elif RGB == [1,1,0]:
        color = "yellow"
    elif RGB == [1,0,1]:
        color = "purple"
    elif RGB == [0,1,1]:
        color = "cyan"
    elif RGB == [1,0,0]:
        color = "red"
    elif RGB == [0,1,0]:
        color = "green"
    elif RGB == [0,0,1]:
        color = "blue"
    elif RGB == [0,0,0]:
        color = "black"
        
    return color


master_plan_cv = cv2.imread("D://Project//Studio One//2nd semester//week 3//testmap3.jpg")
print(master_plan_cv.shape)
img_x = master_plan_cv.shape[0]
img_y = master_plan_cv.shape[1]
grid_x = 40
grid_y = 40
pix_per_grid_x = img_x / grid_x
pix_per_grid_y = img_y / grid_y

MP = dict()
for x in range(0,grid_x):
    for y in range(0,grid_y):
        color = color_recognition(master_plan_cv[int((y+0.5)*pix_per_grid_y)][int((x+0.5)*pix_per_grid_x)])
        MP[(x,y)] = color


## -----Initialize Enviornment-----


TestPlan = Enviornment(grid_x, grid_y, 70, start_time = [6, 1, 0])
for k in MP.keys():
    if MP[k] == "red":
        TestPlan.area_define(k, 0)
    elif MP[k] == "green":
        TestPlan.area_define(k, 1)
    elif MP[k] == "purple":
        TestPlan.area_define(k, 2)
    elif MP[k] == "blue":
        TestPlan.area_define(k, 3)
    elif MP[k] == "yellow":
        TestPlan.area_define(k, 4)

TestPlan.species_define("fish", 10000, "prey", 10000, 20, power = 0.4, nutrition = 15)
TestPlan.species_define("mouse", 10000, "prey", 10000, 7, power = 0.6, nutrition = 30)
TestPlan.species_define("frog", 12000, "prey", 12000, 15, power = 0.5, nutrition = 20)

TestPlan.species_define("pine", 600000, "producer", 600000,  0.1)

TestPlan.sum_update("fish", "prey")
TestPlan.sum_update("mouse","prey")
TestPlan.sum_update("pine","producer")
     
##TestPlan.fire_set((10,10))

## -----Initialize Birds-----
Bird = dict()
Bird_num = 0

while Bird_num < 70:
    
    AGE = random.randint(50,100)
    CON, STR, DEX, APP = 60, 40, 80, 40
    gender = random.randint(0, 1)
    hungry_threshold = 40
    tired_threshold = 40
    mate_tendence = 0.5
    child_tendence = 0.5
    fish_preference = 0.5
    risky_rest = 0.2
    gene_value = [hungry_threshold, tired_threshold, mate_tendence, child_tendence, fish_preference, risky_rest]
    
    Bird[Bird_num] = Heron(Bird_num, AGE, CON, STR, DEX, APP, gender, Gene(init_value = gene_value), TestPlan, location = (random.randint(0, grid_x), random.randint(0,grid_y)), life_status = "adult")
    Bird_num += 1

TestPlan.birds_define(Bird)

## -----Initialize Company-----

company = BS.Company()


## -----Initialize Robots-----

Robot = dict()
Robot_num = 0
Robot_mood = "MP"

def New_robot (click_location):
    if Robot_mood == "MP":
        Robot[Robot_num] = RB.Harvest_robot_MP(TestPlan, click_location, company, 0.6)
    elif Robot_mood == "DC":
           Robot[Robot_num] = RB.Harvest_robot_DC(TestPlan, click_location, company, 0.05)
    elif Robot_mood == "CC":
        Robot[Robot_num] = RB.Harvest_robot_CC(TestPlan, click_location, company, (0,1))
    
## -----Initialize Display Mode-----
screen_size = (1400,800)
area_scale = 15
info_position = (620,20)
resources_position = (620, 400)
Nchart_position = (20,620)
Sub_monitor_position = (800,0)
company_position = (800,620)

pygame.init()
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Bird Behavior")
fps = 60
fclock = pygame.time.Clock()

## ----- UI Initialization -----

Buttons = []

Buttons.append(UI.Sub_display_button("bio_mass", "Sub_display", screen, (800,620), (140,50)))
Buttons.append(UI.Sub_display_button("burn", "Sub_display", screen, (950,620), (140,50)))
Buttons.append(UI.Sub_display_button("bird_history", "Sub_display", screen, (1100,620), (140,50)))

Buttons.append(UI.Robot_mood_button("MP", "Robot_mood", screen, (620,220), (100,45)))
Buttons.append(UI.Robot_mood_button("DC", "Robot_mood", screen, (620,270), (100,45)))
Buttons.append(UI.Robot_mood_button("CC", "Robot_mood", screen, (620,320), (100,45)))

Buttons.append(UI.Amount_display_button("flora", "Amount_display", screen, (620,620), (100,45)))
Buttons.append(UI.Amount_display_button("fauna", "Amount_display", screen, (620,670), (100,45)))

mouse_location = None

subscreen_mood = "burn"
amount_chart_mood = "flora"

pause = False
simulation_switch = dict()
simulation_switch["bird"] = True
simulation_switch["robot"] = True

## -----image save -----

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            click_location = UI.mouse_location(event.pos, grid_x, grid_y, area_scale)
            if click_location is not None:
                if event.button == 1:
                    TestPlan.fire_set(click_location)
                elif event.button == 3:
                    New_robot(click_location)
                    Robot_num += 1
            else:
                for bt in Buttons:
                    flag = bt.click_detect(event.pos)
                    if flag == True:
                        for other in Buttons:
                            if other is not bt and other.button_type == bt.button_type:
                                other.button_relese()
                        if bt.button_type == "Sub_display":
                            subscreen_mood = bt.mood_switch()
                        elif bt.button_type == "Robot_mood":
                            Robot_mood = bt.mood_switch()
                        elif bt.button_type == "Amount_display":
                            amount_chart_mood = bt.mood_switch()
                            
        elif event.type == pygame.MOUSEMOTION:
            mouse_location = UI.mouse_location(event.pos, grid_x, grid_y, area_scale)
            
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pause = not pause
            elif event.key == pygame.K_b:
                simulation_switch["bird"] = not simulation_switch["bird"]
            elif event.key == pygame.K_r:
                simulation_switch["robot"] = not simulation_switch["robot"]
            elif event.key == pygame.K_p:
                UI.image_save(TestPlan, screen)
            
    ## -----Behavior-----
    if pause == False:
        
        if simulation_switch["bird"] == True:
            TestPlan.bird_behavior()
        
        if simulation_switch["robot"] == True:
            for r in Robot.values():
                r.robot_action()

        TestPlan.fire_spread()
        
        TestPlan.resource_update()
        

    ## -----Display-----
    
    screen.fill((0,0,0))
    RD.map_display(screen, TestPlan, area_scale, mouse = mouse_location)
    RD.installation_display(screen, TestPlan, area_scale)
    if simulation_switch["robot"] == True:
        RD.robot_display(screen, Robot, area_scale)
    if simulation_switch["bird"] == True:
        RD.bird_display(screen, Bird, area_scale, bird_simulation = not pause)
    
    RD.button_display(screen, Buttons)
    ##UI.bird_trace_display(screen, Bird)
    RD.envinfo_display(screen, TestPlan, info_position)
    RD.resources_display(screen, TestPlan, mouse_location, resources_position)
    
    if amount_chart_mood == "fauna":
        RD.fauna_amount_display(screen, TestPlan, Nchart_position, 560, 160, 360)
    elif amount_chart_mood == "flora":
        RD.flora_amount_display(screen, TestPlan, Nchart_position, 560, 160, 360)
    ##print(TestPlan.date, TestPlan.gene_ave)
    
    if subscreen_mood == "bio_mass":
        RD.bio_mass_display(screen, TestPlan, area_scale, Sub_monitor_position, mouse = mouse_location)
    elif subscreen_mood == "burn":
        RD.burn_display(screen, TestPlan, area_scale, Sub_monitor_position, mouse = mouse_location)
    elif subscreen_mood == "bird_history":
        RD.bird_history_display(screen, TestPlan, area_scale, Bird, Sub_monitor_position, n = 30, mouse = mouse_location)

    RD.profit_display(screen, company, company_position, 560, 160, 360)
    
    if pause == False:
        TestPlan.time_update()
        if TestPlan.timetick == 0:
            company.update()
    
    pygame.display.update()
    fclock.tick(fps)

