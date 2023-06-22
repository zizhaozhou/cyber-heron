# -*- coding: utf-8 -*-
"""
Created on Thu Feb  9 13:18:25 2023

@author: Zizhao Zhou
"""
import random
import math

class Gene:
    
    def __init__(self, init_value = [0,0,0,0,0,0]):
        
        self.DNA = dict()
        self.gene_list = ["hungry_threshold", "tired_threshold", "mate_tendence", "child_tendence", "risky_rest"]
        self.gene_range = [(0,100),(0,100),(0,100),(0,100),(0,1)]
        for i in range(0,len(self.gene_list)):
            gene_name = str(self.gene_list[i])
            self.DNA[gene_name] = init_value[i]

    def genovariation(self, p):
        if random.random() < p:
            i = random.randint(0, len(self.gene_list)-1)
            self.DNA[self.gene_list[i]] = random.uniform(self.gene_range[i][0], self.gene_range[i][1])
    
    def cross_fusion(self, gene1, gene2):
        for g in self.DNA.keys():
            self.DNA[g] = random.choice([gene1.DNA[g],gene2.DNA[g]])

class Heron:
    
    ## -----Initialize-----
    def __init__(self, num, AGE, CON, STR, DEX, APP, gender, gene, env, location=(0,0), life_status = "egg"):
        
        self.adult_age = 40
        self.old_age = 720
        self.die_age = 1080
        self.life_status = life_status
        self.dead = False
        
        self.num = num ##[Identifi number of each heron, include eggs and dead birds. Range from 0 to infinite]
        self.gene = gene
        
        self.AGE = AGE
        self.CON = CON ##[Define the maxium endurance of the bird. Range from 0-99]
        self.STR = STR ##[Define the possibility of hunting successfully. Range from 0-99]
        self.DEX = DEX ##[Define the possibility of escaping from danger. Range from 0-99]
        self.APP = APP ##[Define the possibility of mating with another bird. Range from 0-99]
        self.sense_radius = 10
        self.energy_per_dist = 1
        
        self.gender = gender ##[0 for female, 1 for male]
        self.mate = False
        self.couple = None ##[the identification number of its husband/wife]
        self.nest = None
        self.children = []
        
        self.food_left = 60
        self.hungry = False
        
        self.water_left = 100
        self.thirsty = False
        
        self.endurance_left = self.CON
        self.tired = False
        
        self.temperature = 100
        self.cold = False
        
        self.env = env
        self.location = location
        self.history_position = []
        
        self.hunt_will = 1
        self.rest_will = 1
        self.mate_will = 0
        self.child_will = 0
        self.strategy = "rest"
        self.destination = None
        
        self.food_preference = dict()
        self.food_preference["fish"] = 1.5
        self.food_preference["mouse"] = 0.8
        self.food_preference["frog"] = 1.2
        
    ## -----Status-----
    def refresh(self):
        if self.food_left < self.gene.DNA["hungry_threshold"]:
            self.hungry = True
        else:
            self.hungry = False
            
        if self.water_left < 40:
            self.thirsty = True
        else:
            self.thirsty = False
            
        if self.endurance_left < self.gene.DNA["tired_threshold"]:
            self.tired = True
        else:
            self.tired = False
            
        if self.temperature < 90:
            self.cold = True
        else:
            self.cold = False
            
        if self.food_left <= 0 or self.water_left <= 0 or self.endurance_left <= 0 or self.temperature <= 85:
            self.dead = True
            print(self.num, "starved")
            
        return not self.dead
    
    def mate_reset(self):
        self.mate = False
        self.couple = None
        self.nest = None
        self.children = []
        print(self.num, "mate reset")
        
    def children_refresh(self):
        dead_child = []
        if len(self.children) != 0:
            for c in self.children:
                if c.dead == True or c.life_status == "adult":
                    dead_child.append(c)
            for c in dead_child:
                self.children.remove(c)
            if len(self.children) == 0:
                self.mate_reset()
    
    def grow(self):
        self.AGE += 1
        
        if self.AGE >= self.old_age:
            self.life_status = "old"
        elif self.AGE >= self.adult_age:
            self.life_status = "adult"
        elif self.AGE >= 0:
            self.life_status = "youth"
        else:
            self.life_status = "egg"
            
        if self.AGE >= self.die_age:
            self.death = True
    
    def heat_lose(self):
        heat = max((self.temperature - self.env.temperature),0) * 0.1 * 0.125
        self.temperature -= heat
        return heat
        
    ## -----Decide-----
    
    def decide_strategy(self, timetick = 0, weather = "sunny", season = "summer"):
        if timetick < 6 or timetick >= 18:
            hunt_bonus = 10
            rest_bonus = 0.1
        else:
            hunt_bonus = 0.1
            rest_bonus = 10
            
        H = self.gene.DNA["hungry_threshold"]
        self.hunt_will = min(math.log(self.food_left/H,100/H)*(-1) + 1, 10000)*hunt_bonus
        
        T = self.gene.DNA["tired_threshold"]
        self.rest_will = min(math.log(self.endurance_left/T,self.CON/T)*(-1) + 1, 10000)*rest_bonus
        
        M = self.gene.DNA["mate_tendence"]
        if not self.mate and self.AGE > self.adult_age and season == "spring":
            self.mate_will += (0.02*M*0.125)
        else:
            if not self.mate:
                self.mate_will = max(0, self.mate_will - 0.02*0.125)
            else:
                self.mate_will = 0
            
        C = self.gene.DNA["child_tendence"]
        self.child_will = 0
        if self.children != []:
            for c in self.children:
                if c.cold == True:
                    self.child_will += C
                if c.hungry == True:
                    self.child_will += C
            
        
        choice = self.strategy
        choice_will = [self.hunt_will, self.rest_will, self.mate_will, self.child_will]
        choice_name = ["hunt", "rest", "mate", "child"]

        if self.hunt_will > 1 or self.rest_will > 1:
            if self.hunt_will > self.rest_will:
                choice = "hunt"
            else:
                choice = "rest"
        else:
            for i in range(0,len(choice_will)):
                if choice_will[i] == max(choice_will):
                    choice = choice_name[i]
                    break
        ##print(choice_will, choice)
        self.strategy = choice
        return choice
                
    ## -----Sensing-----
    
    def get_surrounding_area(self, r, randomize = True):
        area_list = []
        for area_location in self.env.map.keys():
            if (area_location[0] - self.location[0])**2 + (area_location[1] - self.location[1])**2 <= r**2:
                if self.env.map[area_location].burn == 0:
                    area_list.append(self.env.map[area_location])
        if randomize == True:
            random.shuffle(area_list)
                
        return area_list
    
    def get_surrounding_birds(self, r, randomize = True):
        area_location_list = []
        for area_location in self.env.map.keys():
            if (area_location[0] - self.location[0])**2 + (area_location[1] - self.location[1])**2 <= r**2:
                area_location_list.append(area_location)
                
        surrounding_birds = []
        for bird_num in self.env.heron.keys():
            if self.env.heron[bird_num].location in area_location_list and bird_num != self.num:
                surrounding_birds.append(self.env.heron[bird_num])
                
        if randomize == True:
            random.shuffle(surrounding_birds)
                
        return surrounding_birds

    ## -----Move-----
    
    def path_calculate(self, destination):
        
        if destination is not None:
            temp_location = self.location
            x_direction = (destination[0] - temp_location[0]) / abs(destination[0] - temp_location[0])
            y_direction = (destination[1] - temp_location[1]) / abs(destination[1] - temp_location[1])
            path = []
            ##path.append(temp_location)
            
            while destination[0] - temp_location[0] != 0 and destination[1] - temp_location[1] != 0:
                
                delta_x = abs(destination[0] - temp_location[0])
                delta_y = abs(destination[1] - temp_location[1])
                if random.random() < delta_x / (delta_x + delta_y):
                    temp_location = (temp_location[0] + x_direction, temp_location[1])
                else:
                    temp_location = (temp_location[0], temp_location[1] + y_direction)
                path.append(temp_location)
            
            path.append(temp_location)
        else:
            path = []
            
        return path
            
    def move(self, destination):
        
        ##print(self.location, destination)

        distant = ((destination[0]-self.location[0])**2 + (destination[1]-self.location[1])**2)**0.5
        energy = distant*self.energy_per_dist
        self.location = destination
        self.endurance_left -= energy

    ## -----Behavior-----
    
    ### Hunt
    
    def hunting_place(self, r):
        hunt_area_location = self.location
        animal = self.env.animal
        
        hunt_area_list = self.get_surrounding_area(r)
        random.shuffle(hunt_area_list)
        area_location_list = []
        prey_amount_list = []
        
        food_choice = dict()
        for k in animal.keys():
            if animal[k].bio_status == "prey":
                food_choice[k] = random.random()*self.food_preference[k]
        for k in food_choice.keys():
            if food_choice[k] == max(food_choice.values()):
                prey = k
        '''
        if random.random() < self.gene.DNA["fish_preference"]:
            prey = "fish"
        else:
            prey = "mouse"
        '''
        for area in hunt_area_list:
            area_location_list.append(area.location)
            prey_amount = area.fauna[prey]*(100-area.bio_mass_density)*area.hunt_debuff
            prey_amount_list.append(prey_amount)

        for i in range(0, len(area_location_list)):
            if prey_amount_list[i] == max(prey_amount_list):
                hunt_area_location = area_location_list[i]
                
        return hunt_area_location
    
    def hunt(self, area, animal):
        
        targets_amount = dict()
        for k in area.fauna.keys():
            targets_amount[k] = random.random()*area.fauna[k]*self.food_preference[k]
        for k in targets_amount.keys():
            if targets_amount[k] == max(targets_amount.values()):
                prey_type = k
        '''
        if area.fauna["fish"] > area.fauna["mouse"]:
            prey_type = "fish"
        else:
            prey_type = "mouse"
        '''
        success = (1-(1-self.STR/100)**(area.fauna[prey_type]*(1-animal[prey_type].power)))*area.hunt_debuff
        area.hunt_debuff = area.hunt_debuff*0.8
        if random.random() <= success:
            self.food_left = min(self.food_left + animal[prey_type].nutrition, 100)
            self.endurance_left = self.endurance_left - 5

            return [prey_type,1]
        else:
            return [prey_type,0]
        
    ### Rest
    
    def rest_place(self, r):
        rest_area_location = self.location
        
        if random.random() >= self.gene.DNA["risky_rest"]:
            rest_area_list = self.get_surrounding_area(r)
            area_risk_list = []
            for a in rest_area_list:
                if a.bio_mass_density >= 0.5:
                    risk = a.risk
                else:
                    risk = a.risk
                area_risk_list.append(risk)
            
            for i in range(0, len(area_risk_list)):
                if area_risk_list[i] == min(area_risk_list):
                    rest_area_location = rest_area_list[i].location
        
        return rest_area_location
    
    def rest(self):
        self.food_left = self.food_left-5
        self.endurance_left = min(self.endurance_left+25, self.CON)
        return ["rest", ""]
    
    ### Mate
    
    def nest_place(self, r):
        nest_area_location = self.location
        if self.nest is not None:
            nest_area_location = self.nest
        else:
            for area in self.get_surrounding_area(r):
                if area.area_type == 3 and area.burn == 0 and area.burn_debuff <20:
                    nest_area_location = area.location
                    break
                    
        return nest_area_location
    
    def partner_seek(self, r):
        partner = None
        surrounding_birds = self.get_surrounding_birds(r)
        
        suitable_birds = []
        suitable_birds_app = []
        for b in surrounding_birds:
            if b.gender is not self.gender and b.strategy == "mate" and self.env.map[b.location].area_type == 3:
                suitable_birds.append(b)
                suitable_birds_app.append(b.APP)
        for i in range(0,len(suitable_birds_app)):
            if suitable_birds_app[i] == max(suitable_birds_app):
                partner = suitable_birds[i]
        
        return partner
    
    def mate_with(self, partner):
        self.mate = True
        partner.mate = True
        self.couple = partner
        partner.couple = self
        self.nest = partner.location
        partner.nest = partner.location
        
    def birth(self, num):
        lay_egg_date = random.randint(15,40)
        egg_num = num
        eggs_list = []
        for i in range(0,random.randint(3, 5)):
            egg_gene = Gene()
            egg_gene.cross_fusion(self.gene, self.couple.gene)
            egg_gene.genovariation(0.01)
            new_egg = Heron(egg_num, -40-lay_egg_date+random.randint(0, 10), 60, 30, 80, 60, random.randint(0, 1), egg_gene, self.env, location = self.nest, life_status = "egg")
            eggs_list.append(new_egg)
            self.children.append(new_egg)
            self.couple.children.append(new_egg)
            egg_num += 1
        
        return eggs_list, len(eggs_list)
    
    ### Child
    
    def raise_child(self):
        feed_list = []
        for c in self.children:
            c.temperature = self.temperature
            if c.life_status == "youth":
                feed_list.append(c)
        if len(feed_list) > 0:
            food_supply = max((self.food_left - self.gene.DNA["hungry_threshold"]), 0)/len(feed_list)
            for c in feed_list:
                c.food_left = min((c.food_left + food_supply)*0.9, 100)
                self.food_left -= food_supply

        self.endurance_left += 15
            
    ## -----survive-----
    
    def heat_generate(self):
        if self.cold == True and self.life_status != "egg":
            h = (93-self.temperature)*0.8
            self.food_left -= h
            self.temperature += h
            
    ## -----risk-----
    
    def danger(self, enemy_total, timetick):
        if timetick < 6 or timetick >= 18:
            risk_buff = 0.5
        else:
            risk_buff = 1.5
        if random.random()<(1-(1-self.env.map[self.location].risk)**(enemy_total*risk_buff/(len(self.env.map.keys())))):
            if random.random()*100 > self.DEX:
                self.dead = True
                print(self.num, "hunted")