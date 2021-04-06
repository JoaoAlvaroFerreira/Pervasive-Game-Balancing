import Controller.PlayerGeneration as playgen
from Model.player import *
from Model.game_object import *
from Model.challenge import *
from Model.game import *
import datetime
import random
import pandas as pd
import matplotlib.pyplot as plt

class Simulation:

    def __init__(self, game):
        self.game = game

    def sim(self):

        for player in self.game.players:
            self.total_play(player)

    
    def total_play(self,player):
        player.motivation = player.Personality.Competitiveness
        date =  datetime.datetime(2021, 1, 1,0,0)
        i = 0
        for _ in range(1, 365):
            
            date = date + datetime.timedelta(hours = 1)
            load_file = 'Resources/weather.csv'
            df = pd.read_csv(load_file)
            today = df.loc[df['Day'] == date.timetuple().tm_yday]
            print("The weather is:"+today['Weather'])

            if player.motivation > 1:
                i = i+1
                self.gameplay_session(player, date, i)

            print(date)
            print("Concentration: ")
            print(player.Personality.Concentration)

    def gameplay_session(self,player, datetime, i):
        
        curr_lat = player.PlayerLocationInfo.latitude
        curr_long = player.PlayerLocationInfo.longitude
        a = 0
     

        while a < 2:
            rand_mod_a = random.uniform(-0.05,0.05)
            rand_mod_b  = random.uniform(-0.05,0.05)
            curr_lat = curr_lat + rand_mod_a
            curr_long = curr_long + rand_mod_b

            self.game.create_moment(player, curr_lat, curr_long, datetime, i) 
            a = a+1

            doable_challenges = self.find_doable_challenge_location(curr_lat, curr_long)
            #visible_challenges = self.find_visible_challenge_location(curr_lat, curr_long)

            if len(doable_challenges) > 0:
                a = a - self.do_challenges(doable_challenges, player, datetime)
                


    
    def find_doable_challenge_location(self, curr_lat, curr_long):
        
        doable_challenges = []

        for challenge in self.game.challenges:
            min_lat = challenge.latitude - challenge.radiusLocationAvailable
            max_lat = challenge.latitude + challenge.radiusLocationAvailable
            min_long = challenge.longitude - challenge.radiusLocationAvailable
            max_long = challenge.longitude + challenge.radiusLocationAvailable

            if curr_lat > min_lat and curr_lat< max_lat and curr_long>min_long and curr_long < max_long:
                doable_challenges.append(challenge)
            

        return doable_challenges

    def do_challenges(self, doable_challenges, player, datetime):
              

        for ch in doable_challenges:
            if ch.ChallengeType.temporary:
                if self.verify_done(ch, player):
                    continue
            
            chi = ChallengeInstance(ch, True, True , player,datetime)
            chi.insert_into_db(self.conn)
            self.game.challenge_instances.append(chi)
            return 1
        
        return 0
        

    def verify_done(self, ch, player):
        
        for chi in self.challenge_instances:
            if chi.player == player and chi.Challenge == ch and chi.attempted == True:
                return True
        
        return False
        