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

    def decision(self,probability):
        return random.random() < probability
    
    def total_play(self,player):
        player.base_motivation = random.uniform(0,5)
        player.session = 0
        date =  datetime.datetime(2021, 1, 1,0,0)
        i = 0
        for _ in range(1, 14):
            
            date = date + datetime.timedelta(days = 1)
            load_file = 'D:\\School\\5oAno\\TESE\Repo\\Pervasive-Game-Balancing\\Resources\\weather.csv'
            df = pd.read_csv(load_file)
            today = df.loc[df['Day'] == date.timetuple().tm_yday]
            print("The weather is:"+today['Weather'])

            player.base_motivation = player.base_motivation + self.decision(0.2)

            if date.weekday() is 5 or date.weekday() is 6:
                weekend = True
            played_today = True

            for hour in range(0,24):
                
                now = date + datetime.timedelta(hours=hour)
                hour = hour + 1

                if played_today:
                    if self.decision(player.base_motivation/50):
                        print("play again")
                        played_today = False

               

                if hour > 8 or hour < 22:
                    if player.base_motivation > 3:
                        if weekend:
                            if self.decision(player.Personality.Competitiveness/10):
                                print("Play!")
                                self.gameplay_session(player,date)
                        
                

          
           # if player.base_motivation > 1:
            #    i = i+1
             #   self.gameplay_session(player, date, i)

           
            
            

    def gameplay_session(self,player, datetime):
        
        curr_lat = player.PlayerLocationInfo.latitude
        curr_long = player.PlayerLocationInfo.longitude
        
        player.session = player.session + 1
     
        local_motivation = player.base_motivation

        while(local_motivation > 0):
            rand_mod_a = random.uniform(-0.03,0.02)
            rand_mod_b  = random.uniform(-0.03,0.02)
            curr_lat = curr_lat + rand_mod_a
            curr_long = curr_long + rand_mod_b

            self.game.create_moment(player, curr_lat, curr_long, datetime, player.session) 
        

            doable_challenges = self.find_doable_challenge_location(curr_lat, curr_long)
            #visible_challenges = self.find_visible_challenge_location(curr_lat, curr_long)

            if len(doable_challenges) > 0:
                player.base_motivation = player.base_motivation + self.do_challenges(doable_challenges, player, datetime)
            
            local_motivation = local_motivation - 3
            
   
                


    
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
              
        purchase = Purchase(player, self.game.gameObjects[8], datetime)
        print("Price: ")
        print(self.game.gameObjects[8].price)
        self.game.purchases.append(purchase)
        purchase.insert_into_db(self.game.conn)
        for ch in doable_challenges:
            if ch.ChallengeType.temporary:
                if self.verify_done(ch, player):
                    continue
            
            if self.doChallenge(ch, player):
                chi = ChallengeInstance(ch, True, True , player,datetime)
                print("DID CHALLENGE")
                inv = Inventory(player,ch.itemReward)
                inv.insert_into_db(self.game.conn)
                self.game.inventories.append(inv)
            else:
                chi = ChallengeInstance(ch, True, False , player,datetime)

            chi.insert_into_db(self.game.conn)
            self.game.challenge_instances.append(chi)
            return 1
        
        return -1
        
    def doChallenge(self,ch, player):
        if ch.itemSpend is None:
            return True

        else:
            return self.game.find_object_in_inventory(player, ch.itemSpend)
        

    def verify_done(self, ch, player):
        
        for chi in self.game.challenge_instances:
            if chi.player == player and chi.Challenge == ch and chi.attempted == True:
                return True
        
        return False
        