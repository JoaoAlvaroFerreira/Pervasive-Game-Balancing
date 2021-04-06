import Controller.PlayerGeneration as playgen
from Model.player import *
from Model.game_object import *
from Model.challenge import *
from Model.game import *
import datetime
import random
import pandas as pd
import matplotlib.pyplot as plt

class Analytics:
    def __init__(self, game):
        self.game = game
    
    def analyse_players(self):
        for player in self.game.players:
            a = self.get_player_challenges(player)
            b = self.get_player_moments(player)
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

    
    


