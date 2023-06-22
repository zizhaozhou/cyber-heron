# -*- coding: utf-8 -*-
"""
Created on Thu Apr 20 12:50:34 2023

@author: Zizhao Zhou
"""

class Company:
    def __init__(self):
        self.money = 0
        self.earn_record = [0]
        self.cost_record = [0]
        
        self.daily_profit = 0
        self.profit_record = [0]
        
        self.product_price = dict()
        self.product_price["pine"] = 10
    
    def update(self):
        self.profit_record.append(self.daily_profit)
        self.daily_profit = 0
        
        self.earn_record.append(0)
        self.cost_record.append(0)
    
    def mature_wood_profit(self, specie, amount):
        income = amount * 0.8 * self.product_price[specie]
        self.money += income
        self.daily_profit += income
        self.earn_record[-1] += income 
        
    def dead_wood_profit(self, specie, amount):
        income = amount * 0.4 * self.product_price[specie]
        self.money += income
        self.daily_profit += income
        self.earn_record[-1] += income
        
    def robot_cost(self, cost):
        self.money -= cost
        self.daily_profit -= cost
        self.cost_record[-1] -= cost
        
        