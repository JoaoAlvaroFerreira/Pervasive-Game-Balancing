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

class Analytics:
    def __init__(self, game):
        self.game = game
    
    def analyse_players(self):
        
        for player in self.game.players:
            a = self.get_player_challenges(player)
            b = self.get_player_moments(player)
            avg_distance = self.measure_distances(b)
            string = "Player {} engaged with {} challenges and has {} recorded play moments, in a total of X days".format(player.name,len(a),len(b))

            print(string )
        #print(len(self.game.gameplay_moments))
        
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

    def measure_distances(self, moment_list):
        value_distance = 0
        for x in range(len(moment_list)-1):
            if(moment_list[x].session == moment_list[x+1].session):
                value_distance = value_distance + self.calc_distance_two_moments(moment_list[x],moment_list[x+1])

        return value_distance
            
    def calc_distance_two_moments(self,moment1, moment2):
       latdelta = math.abs(moment1.latitude - moment2.latitude)
       longdelta = math.abs(moment1.longitude - moment2.longitude)
       hdist = longdelta * 110574
       vdist = latdelta * 111.320*math.cos(longdelta)
       dist = math.sqrt(math.pow(hdist,2)+math.pow(vdist,2))

       return dist


    


