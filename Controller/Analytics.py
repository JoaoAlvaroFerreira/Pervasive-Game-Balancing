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
from Controller.Quadrant import Quadrant


class Analytics:
    def __init__(self, game):
        self.game = game
    
    def analyse_players(self):
        string_reply = ""
        #plotplot(self.game.players)
        self.calc_average_KPIs()

        averages = " Average Challenges Engaged With = {} \n Average Gameplay Moments = {} \n Average Distance Walked = {} \n Average Challenge Success Rate = {} \n Average Inventory Size = {} \n Average Purchases Made = {} \n Average Lifetime Value = {} \n Average Last Log In = {} \n Average Sessions Per Player = {} \n Average Conversion Rate (Install to Purchase) = {} \n".format( 
        self.KPIs.challenges 
        ,self.KPIs.moments 
        ,self.KPIs.distance_walked
        ,self.KPIs.challenge_success_rate 
        ,self.KPIs.inventory 
        ,self.KPIs.purchases
        ,self.KPIs.lifetime_value 
        ,self.KPIs.lastLogIn 
        ,self.KPIs.sessions 
        ,self.KPIs.conversion_rate)

        

        for player in self.game.players:
            
   
            string = "Player {} engaged with {} challenges, has {} recorded play moments, a {} challenge success rate in a total of {} play sessions. ".format(player.name, len(player.KPIs.challenges),len(player.KPIs.moments),player.KPIs.challenge_success_rate, player.KPIs.sessions)
            string2 = "They have purchased {} items, having spent a total of {}€ and having an inventory with {} items. They last logged in {} ago.".format(player.name, len(player.KPIs.purchases), player.KPIs.lifetime_value, len(player.KPIs.inventory), player.KPIs.lastLogIn)

            string_reply = string_reply + "\n" + string + string2
        #print(len(self.game.gameplay_moments))

        return averages + string_reply

    def calc_kpi(self,player):
        player.KPIs = lambda: None
        player.KPIs.challenges =  self.get_player_challenges(player)
        player.KPIs.moments = self.get_player_moments(player)
        player.KPIs.distance_walked = self.measure_distances(player.KPIs.moments)
        player.KPIs.challenge_success_rate = self.challenge_success_rate(player)
        player.KPIs.inventory = self.get_player_items(player)
        

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
            date =  datetime.datetime(2021, 1, 21,0,0)
            player.KPIs.lastLogIn = (date - datetime.datetime.strptime(player.KPIs.moments[-1].time, '%Y-%m-%d %H:%M:%S')).total_seconds()/3600
        
        

        #conversion rate (install to purchase)
        player.KPIs.conversion_rate = 0
        if(len(player.KPIs.purchases) > 0):
            player.KPIs.conversion_rate = 1

        #hours-played~
        player.KPIs.playtime = self.measure_playtime(player.KPIs.moments)

    def calc_average_KPIs(self):
        self.KPIs = lambda: None
        self.KPIs.challenges =  len(self.game.challenge_instances)/len(self.game.players)
        self.KPIs.moments = len(self.game.gameplay_moments)/len(self.game.players)
        self.KPIs.distance_walked = 0
        self.KPIs.challenge_success_rate = 0
        self.KPIs.inventory = len(self.game.inventories)/len(self.game.players)
        self.KPIs.purchases = len(self.game.purchases)/len(self.game.players)
        self.KPIs.lifetime_value = 0
        self.KPIs.lastLogIn = 0
        self.KPIs.sessions = 0
        self.KPIs.conversion_rate = 0

        for player in self.game.players:
            self.calc_kpi(player)

       
        
            self.KPIs.distance_walked = self.KPIs.distance_walked + player.KPIs.distance_walked
            self.KPIs.challenge_success_rate =  self.KPIs.challenge_success_rate + player.KPIs.challenge_success_rate
            self.KPIs.lifetime_value =  self.KPIs.lifetime_value + player.KPIs.lifetime_value
            self.KPIs.lastLogIn =  self.KPIs.lastLogIn + player.KPIs.lastLogIn
            self.KPIs.sessions =  self.KPIs.sessions + player.KPIs.sessions
            self.KPIs.conversion_rate =  self.KPIs.conversion_rate + player.KPIs.conversion_rate
        
        self.KPIs.distance_walked = self.KPIs.distance_walked/len(self.game.players)
        self.KPIs.challenge_success_rate = self.KPIs.challenge_success_rate/len(self.game.players)
        self.KPIs.lifetime_value = self.KPIs.lifetime_value/len(self.game.players)
        self.KPIs.lastLogIn = self.KPIs.lastLogIn/len(self.game.players)
        self.KPIs.sessions = self.KPIs.sessions/len(self.game.players)
        self.KPIs.conversion_rate = self.KPIs.conversion_rate/len(self.game.players)



        



        
       
    
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
                item_list.append(item)
        
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


    def data_preprocessing(self):
        data = []
        gender = 0
        age = 0
        for player in self.game.players:
            if player.Demographic.Gender == 'Male':
                gender = 1
            elif player.Demographic.Gender == 'Female':
                gender = 0
            
            if player.Demographic.Age == "Youth":
                age = 1
            elif player.Demographic.Age == "Adult":
                age = 2
            elif player.Demographic.Age == "Elderly":
                age = 3


            row = [player.Demographic.Age, gender, player.Demographic.SocioEconomicStatus, player.PlayerLocationInfo.latitude, player.PlayerLocationInfo.longitude, len(player.KPIs.challenges), player.KPIs.lifetime_value, player.KPIs.sessions]
            data.append(row)


        return pd.DataFrame.from_records(data, columns=['Age', 'Gender', "Economic Status", "Latitude", "Longitude", "Challenges Done", "Lifetime Value", "Sessions"])
    
    def early_triggers(self, dataset):
        returnable = ""

        kd = dataset[dataset["Age"] == 'Kid']
        kid_dataset = kd.copy()
        avg_lv = dataset['Economic Status'].mean()
        kid_count = 0
        print(kid_dataset)
        for kid in kid_dataset.itertuples():
            print("KID: ")
            print(kid)
            if kid._7 > avg_lv:
                kid_count = kid_count + 1

        kid_ratio = kid_count/len(kid_dataset)
        
        if kid_count>1:
            string = "Warning: {} of children seem to have a lifetime spending over the average. \n".format(kid_ratio)
            returnable = returnable + string


        #load_file = 'D:\\School\\5oAno\\TESE\Repo\\Pervasive-Game-Balancing\\Resources\\weather.csv'
        #df = pd.read_csv(load_file)
        #today = df.loc[df['Day'] == date.timetuple().tm_yday]
        #weather = print(today['Weather'])

        #for ch in self.game.challenge_instances:
        #    ch.timestamp.timetuple().tm_yday

        return returnable
    
    def demo_analysis(self, demos):
        stringTrigger = ""
        ageAdult = 0
        ageElderly = 0
        ageChild = 0
        men = 0
        women = 0
        total_economicstatus = 0
        for row in demos:
            total_economicstatus = total_economicstatus + row[4]
            if row[3] == 1:
                men = men + 1
            else: 
                women = women + 1

            if (row[0] > row[1]) and (row[0] > row[2]):
                ageAdult = ageAdult + 1
            elif (row[1] > row[0]) and (row[1] > row[2]):
                ageElderly = ageElderly + 1
            else:
                ageChild = ageChild + 1
        
        avg_economicstatus = total_economicstatus/(men+women)
        real_tes = 0

        for player in self.game.players:
            real_tes = real_tes + player.Demographic.SocioEconomicStatus
        
        avg_tes = real_tes/len(self.game.players)

        print("AVG_TES", avg_tes)
        print("AVG_SIM_TES", avg_economicstatus)

        
        tes_ratio = avg_economicstatus/avg_tes
        stringTrigger = stringTrigger + "The average economic status among this group is {} higher than the average \n".format(tes_ratio)

                   

        print("Men:", men)
        print("Women:", women)
        if men>women:
            count = 0
            for player in self.game.players:
                   if player.Demographic.Gender == 'Male':
                       count = count+1

            genderRatio = men/(men+women)
            trueGenderRatio = count/len(self.game.players)
            genderDelta = abs(genderRatio-trueGenderRatio)
            stringTrigger = stringTrigger + "Men are over-represented by a rate of {}. TruePercent = {}, Sim Percent = {} \n".format(genderDelta, trueGenderRatio, genderRatio)
            if genderDelta > 0.2:
                stringTrigger = stringTrigger + "WARNING WARNING \n"

        elif men < women:
            count = 0
            for player in self.game.players:
                   if player.Demographic.Gender == 'Female':
                       count = count+1

            genderRatio = women/(men+women)
            trueGenderRatio = count/len(self.game.players)
            genderDelta = abs(genderRatio-trueGenderRatio)
            stringTrigger = stringTrigger + "Women are over-represented by a rate of {}. TruePercent = {}, Sim Percent = {} \n".format(genderDelta, trueGenderRatio, genderRatio)
            if genderDelta > 0.2:
                stringTrigger = stringTrigger + "WARNING WARNING \n"

        if (ageAdult > ageElderly) and (ageAdult > ageChild):
            count = 0
            for player in self.game.players:
                   if player.Demographic.Age == 'Adult':
                       count = count+1
            
            truePercent = count/len(self.game.players)
            simPercent = ageAdult/(ageAdult+ageElderly+ageChild)
            deltaPercent = abs(simPercent-truePercent)
            stringTrigger = stringTrigger + "Adults are over-represented by a rate of {}. TruePercent = {}, Sim Percent = {} \n".format(deltaPercent, truePercent, simPercent)
            if deltaPercent > 0.2:
                stringTrigger = stringTrigger + "WARNING WARNING \n"





        elif (ageElderly > ageAdult) and (ageElderly > ageChild):
            count = 0
            for player in self.game.players:
                   if player.Demographic.Age == 'Elderly':
                       count = count+1
            
            truePercent = count/len(self.game.players)
            simPercent = ageAdult/(ageAdult+ageElderly+ageChild)
            deltaPercent = abs(simPercent-truePercent)
            stringTrigger = "The Elderly are over-represented by a rate of {}. TruePercent = {}, Sim Percent = {} \n".format(deltaPercent, truePercent, simPercent)
            if deltaPercent > 0.2:
                stringTrigger = stringTrigger + "WARNING WARNING \n"

        else:
            count = 0
            for player in self.game.players:
                   if player.Demographic.Age == 'Children':
                       count = count+1
            
            truePercent = count/len(self.game.players)
            simPercent = ageAdult/(ageAdult+ageElderly+ageChild)
            deltaPercent = abs(simPercent-truePercent)
            stringTrigger = "Children are over-represented by a rate of {}\n".format(deltaPercent)
            if deltaPercent > 0.2:
                stringTrigger = stringTrigger + "WARNING WARNING\n"

        stringTrigger = stringTrigger + self.geoAnalysis(demos)

        return stringTrigger

    def geoAnalysis(self, demos):
        print(demos)
        maxLat = 41.2788
        minLat = 41.1042
        maxLong = -8.4361
        minLong = -8.6627
        stepLat = (maxLat - minLat)/5
        stepLong = (maxLong - minLong)/5
        quadrants = []


        for x in range(1,6):
            for y in range(1,6):
                quadrants.append(Quadrant(
                    minLat + stepLat*(x-1),
                    minLat + stepLat*x,
                    minLong + stepLong*(x-1),
                    minLong + stepLong*x
                ))

        print("There are {} quadrants".format(len(quadrants)))

        for row in demos:
            print("ROW5: {}, ROW6: {}".format(row[6], row[7]))
            for quadrant in quadrants:
               
                if quadrant.add_player(row[6], row[7]):
                    print("eeeeeee????")
                    break

        quadrants.sort(key=lambda x: x.population, reverse=True)
        pop_avg = sum([quadrant.population for quadrant in quadrants]) / len(quadrants)

        stringTrigger = "The average player count per quadrant is {}".format(pop_avg)

        stringTrigger = stringTrigger + "\n The following quadrants have an above average concentration of players: "

        for q in quadrants:
            if(q.population > pop_avg):
                ratio = q.population/pop_avg
                string = "\n The quadrant from [{},{}] to [{},{}] has a population {} above the average.".format(q.minLat,q.minLong,q.maxLat, q.maxLong, ratio)
                stringTrigger = stringTrigger + string


        return stringTrigger