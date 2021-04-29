import Controller.PlayerGeneration as playgen
from Model.player import *
from Model.game_object import *
from Model.challenge import *
from Model.game import *
import datetime
import random
import pandas as pd
import matplotlib.pyplot as plt
import math
from View.plots import *


class Analytics:
    def __init__(self, game):
        self.game = game
    
    def analyse_players(self):
        string_reply = ""
        #plotplot(self.game.players)
        
        for player in self.game.players:
            self.calc_kpi(player)
   
            string = "Player {} engaged with {} challenges, has {} recorded play moments, a {} challenge success rate in a total of {} play sessions. ".format(player.name, len(player.KPIs.challenges),len(player.KPIs.moments),player.KPIs.challenge_success_rate, player.KPIs.sessions)

            string_reply = string_reply + "\n" + string
        #print(len(self.game.gameplay_moments))

        return string_reply

    def calc_kpi(self,player):
        player.KPIs = lambda: None
        player.KPIs.challenges =  self.get_player_challenges(player)
        player.KPIs.moments = self.get_player_moments(player)
        player.KPIs.distance_walked = self.measure_distances(player.KPIs.moments)
        player.KPIs.challenge_success_rate = self.challenge_success_rate(player)
        

        #lifetime value
        player.KPIs.purchases = self.get_player_purchases(player)
        player.KPIs.lifetime_value = 0
        for purchase in player.KPIs.purchases:
            player.KPIs.lifetime_value = player.KPIs.lifetime_value + purchase.GameObject.price

        #last moment and sessions
        player.KPIs.lastLogIn = 365
        player.KPIs.sessions = 0
        if(len(player.KPIs.moments)>0):
            player.KPIs.sessions = player.KPIs.moments[-1].session
            date =  datetime.datetime(2021, 12, 31,0,0)
            player.KPIs.lastLogIn = datetime.datetime.strptime(player.KPIs.moments[-1].time, '%Y-%m-%d %H:%M:%S') - date
        
        player.KPIs.value_per_session = 0

        #conversion rate (install to purchase)
        player.KPIs.conversion_rate = 0
        if(len(player.KPIs.purchases) > 0):
            player.KPIs.conversion_rate = 1

        #hours-played~
        player.KPIs.playtime = self.measure_playtime(player.KPIs.moments)

     
        
       
    
    def challenge_success_rate(self, player):
        challenge_list = []
        failure = 0
        
        for chi in self.game.challenge_instances:
            if(chi.player.id == player.id):
                challenge_list.append(chi)

        if(len(challenge_list)>0):
            

            for ch in challenge_list:
                if not ch.success:
                    failure = failure +1
                
            return (len(challenge_list)-failure)/len(challenge_list)
        else: 
            return 0

        

    def get_player_purchases(self, player):
        purchase_list = []
        for purchase in self.game.purchases:
            if purchase.Player.id == player.id:
                purchase_list.append(purchase)
        
        return purchase_list
    
    def get_player_items(self, player):
        item_list = []
        for item in self.game.inventories:
            if item.Player.id == player.id:
                item_list.append(moment)
        
        return item_list
        
    def get_player_moments(self, player):
        moment_list = []
        for moment in self.game.gameplay_moments:
            if moment.player.id == player.id:
                moment_list.append(moment)
        
        return moment_list

        
    def get_player_challenges(self,player):
        challenge_instances = []
        for chi in self.game.challenge_instances:
            if chi.player.id == player.id:
                challenge_instances.append(chi)
        
        return challenge_instances

    def measure_playtime(self,moment_list):
        
        playtime = 0
        for x in range(len(moment_list)-1):
            
            if(moment_list[x].session == moment_list[x+1].session):
                playtime = playtime + datetime.datetime.strptime(moment_list[x].time, '%Y-%m-%d %H:%M:%S').timestamp()

        return playtime

    def measure_distances(self, moment_list):
        value_distance = 0
        for x in range(len(moment_list)-1):
            
            if(moment_list[x].session == moment_list[x+1].session):
                value_distance = value_distance + self.calc_distance_two_moments(moment_list[x],moment_list[x+1])

        return value_distance
            
    def calc_distance_two_moments(self,moment1, moment2):

    
        p = math.pi/180
        a = 0.5 - math.cos((moment2.latitude-moment1.latitude)*p)/2 + math.cos(moment1.latitude*p) * math.cos(moment2.latitude*p) * (1-math.cos((moment2.longitude-moment1.longitude)*p))/2
        return 12742 * math.asin(math.sqrt(a)) #2*R*asin...


    def show_challenges(self):
        print("There are {} challenges".format(len(self.game.challenges)))

        plot_challenges(self.game.challenges)


