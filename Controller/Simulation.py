import Controller.PlayerGeneration as playgen
from Model.player import *
from Model.game_object import *
from Model.challenge import *
from Model.game import *
from Resources.API import *
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
        a = random.random()
        
        return a < probability
    
    def total_play(self,player):
        player.base_motivation = player.Personality.ClearGoals + player.Personality.SocialInteraction
        player.session = 0
        date =  datetime.datetime(2021, 1, 1,0,0)
        i = 0
        for _ in range(1, 21):
            
            if(player.base_motivation > 10):
                player.base_motivation = 5
                self.make_purchase(player, date)

            date = date + datetime.timedelta(days = 1)
            load_file = 'D:\\School\\5oAno\\TESE\Repo\\Pervasive-Game-Balancing\\Resources\\weather.csv'
            df = pd.read_csv(load_file)
            today = df.loc[df['Day'] == date.timetuple().tm_yday]
            weather = print(today['Weather'])


            player.base_motivation = player.base_motivation + self.decision(0.2)

            if date.weekday() == 5 or date.weekday() == 6:
                weekend = True

           

            played_today = False
            playval = player.base_motivation + player.Personality.Competitiveness + player.Personality.Immersion
                #Rain, Cloudy, Sunny, Storm, Very Sunny
            if weather == "Sunny":
                playval = playval + 1
            
            elif weather == "Cloudy":
                playval = playval - 1
            
            elif weather == "Rain":
                playval = playval - 4
            
            elif weather == "Storm":
                playval = 0

            elif weather == "Very Sunny":
                playval = playval + 3

            if is_holiday(date):
                weekend = True
                playval = playval + 1
                
            
            for hour in range(0,24):
                
                now = date + datetime.timedelta(hours=hour)
                hour = hour + 1
                

                if played_today:
                   
                    if self.decision(player.base_motivation/1000):
                        
                        played_today = False
                    
                    

               
                if not played_today:
                    
                    
                    if player.Demographic.Age == "Kid" and hour > 8 and hour < 20:
                        if weekend:
                            if player.base_motivation > 3:
                                if self.decision(playval/10):
                                    print("Play!")
                                    self.gameplay_session(player,date)
                                    played_today = True
                        else: 
                            if player.base_motivation > 4:
                                if self.decision(playval/10):
                                    print("Play!")
                                    self.gameplay_session(player,date)
                                    played_today = True

                    if player.Demographic.Age == "Young" and hour > 10:
                        if weekend:
                            if player.base_motivation > 4:
                                if self.decision(playval/10):
                                    print("Play!")
                                    self.gameplay_session(player,date)
                                    played_today = True
                        else: 
                            if player.base_motivation > 4:
                                if self.decision(playval/10):
                                    print("Play!")
                                    self.gameplay_session(player,date)
                                    played_today = True


                    if player.Demographic.Age == "Adult" and hour > 8 and hour < 22:
                        if weekend:
                            if player.base_motivation > 3:
                                if self.decision(playval/10):
                                    print("Play!")
                                    self.gameplay_session(player,date)
                                    played_today = True
                        else: 
                            if player.base_motivation > 5:
                                if self.decision(playval/10):
                                    print("Play!")
                                    self.gameplay_session(player,date)
                                    played_today = True
                    
                    if player.Demographic.Age == "Elderly" and hour > 5 and hour < 18:
                        if weekend:
                            if player.base_motivation > 3:
                                if self.decision(playval/10):
                                    print("Play!")
                                    self.gameplay_session(player,date)
                                    played_today = True
                        else: 
                            if player.base_motivation > 4:
                                if self.decision(playval/10):
                                    print("Play!")
                                    self.gameplay_session(player,date)
                                    played_today = True
                                    
           # if player.base_motivation > 1:
            #    i = i+1
             #   self.gameplay_session(player, date, i)

           
            
            

    def gameplay_session(self,player, datetime):
        
        curr_lat = player.PlayerLocationInfo.latitude
        curr_long = player.PlayerLocationInfo.longitude
        
        player.session = player.session + 1
     
        local_motivation = player.base_motivation

        while(local_motivation > 0):
            print("LOCAL MOTIVATION: {}".format(local_motivation))
            rand_mod_a = random.uniform(-0.03,0.02)
            rand_mod_b  = random.uniform(-0.03,0.02)
            curr_lat = curr_lat + rand_mod_a
            curr_long = curr_long + rand_mod_b

            self.game.create_moment(player, curr_lat, curr_long, datetime, player.session) 
        

            doable_challenges = self.find_doable_challenge_location(curr_lat, curr_long)
            #visible_challenges = self.find_visible_challenge_location(curr_lat, curr_long)

            if len(doable_challenges) > 0:
                player.base_motivation = player.base_motivation + self.do_challenges(doable_challenges, player, datetime)
                local_motivation = local_motivation + 1
            
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

    def make_purchase(self, player, datetime):
        if player.Demographic.SocioEconomicStatus > .5 and player.Demographic.SocioEconomicStatus < .7:
            purchasing_power = 1
        
        elif player.Demographic.SocioEconomicStatus > .7 and player.Demographic.SocioEconomicStatus < .9:
            purchasing_power = 2
        
        elif player.Demographic.SocioEconomicStatus > .9 and player.Demographic.SocioEconomicStatus < 1.1:
            purchasing_power = 3
        
        elif player.Demographic.SocioEconomicStatus > 1.1 and player.Demographic.SocioEconomicStatus < 1.3:
            purchasing_power = 4
        
        elif player.Demographic.SocioEconomicStatus > 1.3:
            purchasing_power = 5
        
        else:
            purchasing_power = 0
        
        purchase_obj = "a"
        for item in self.game.gameObjects:
            if item.price == purchasing_power:
                purchase_obj = item

        
        if purchase_obj != "a":
            purchase = Purchase(player, purchase_obj, datetime)
            self.game.purchases.append(purchase)
            purchase.insert_into_db(self.game.conn)

    def do_challenges(self, doable_challenges, player, datetime):
              
        #purchase = Purchase(player, self.game.gameObjects[8], datetime)
        #print("Price: ")
        #print(self.game.gameObjects[8].price)
        #self.game.purchases.append(purchase)
        #purchase.insert_into_db(self.game.conn)
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
                print("FAIL CHALLENGE")
                chi = ChallengeInstance(ch, True, False , player,datetime)

            chi.insert_into_db(self.game.conn)
            self.game.challenge_instances.append(chi)
            return 1
        
        return -1
        
    def doChallenge(self,ch, player):
        if ch.itemSpend is None:
            return True

        else:
            return self.game.spend_item(player, ch.itemSpend)


        

    def verify_done(self, ch, player):
        
        for chi in self.game.challenge_instances:
            if chi.player == player and chi.Challenge == ch and chi.attempted == True:
                return True
        
        return False
        