import Controller.PlayerGeneration as playgen
from Model.player import *
from Model.game_object import *
from Model.challenge import *
from Model.game import *
import datetime
import random
import pandas as pd

class GameManagement:
    
    def create(self, conn):
        self.generatePlayers()
        self.generateGameObjects()
        self.generateChallenges()
        self.gameplay_moments = []
        

        #for player in self.players:
        #    print("inserting player "+player.name)
        #    player.insert_player(conn)

        for got in self.gameObjectTypes:
            print("inserting got "+got.name)
            got.insert_into_db(conn)

        cur = conn.execute("SELECT id, name from GameObjectType")
        for row in cur:
            print("ID ",row[0])
            print("Name: ",row[1])
        
        for go in self.gameObjects:
            print("inserting go "+go.name)
            go.insert_into_db(conn)
        
        for cht in self.challengeTypes:
            cht.insert_into_db(conn)
        
        for ch in self.challenges:
            ch.insert_into_db(conn)
        
      


    
    def load(self, conn):
        self.players = []
        
        #self.load_moments(conn)

        cur = conn.execute(''' SELECT id, name from Player''' )
        for row in cur:
            new_p = Player(row[1])
            new_p.load_player(conn,row[0])
            self.players.append(new_p)

        self.load_game_objects(conn)

        self.load_challenges(conn)
            
        for player in self.players:
            print("Age:"+player.Demographic.Age)
            print("Country:"+player.PlayerLocationInfo.country)
            print("Personality:"+player.Personality.PersonalityType)


    def load_game_objects(self, conn):
        self.gameObjectTypes = []
        self.gameObjects = []
        cur = conn.execute(''' SELECT id, name, importance from GameObjectType''' )

        for row in cur:
            new_got = GameObjectType(self,row[1], row[2])
            query = ''' SELECT id, name, keyItem from GameObject WHERE gameObjectTypeID =={}''' .format(row[0])
            cur2 = conn.execute(query)
            gameObjectTypes.append(new_got)
            for row2 in cur2:
                new_go = GameObject(new_got, row2[1], row2[2])
                self.gameObjects.append(new_go)
                

    def load_challenges(self, conn):
        self.challengeTypes = []
        self.challenges = []
        cur = conn.execute(''' SELECT id,name, temporary, narrative, locationRelevant, uniqueChallenge from ChallengeType''' )

        for row in cur:
            new_cht = ChallengeType(self,row[1], row[2], row[3],row[4], row[5])
            query = ''' SELECT id, name, startDateAvailable, endDateAvailable, radiusLocationAvailable, radiusLocationVisible, latitude, longitude, itemReward, Multiplayer WHERE ChallengeTypeID =={}''' .format(row[0])
            cur2 = conn.execute(query)
            challengeTypes.append(new_cht)
            for row2 in cur2:
                new_ch = Challenge(new_cht, row2[1], row2[2], row2[3],row2[4],row2[5],row2[6],row2[7], None, row2[9])
                query = ('''SELECT name FROM GameObject WHERE id == {}'''.format(row2[8])  )
                go_name = conn.execute(query)
                new.ch.itemReward = self.find_object(go_name)

    
    def find_object(self,name):
        
        for obj in self.gameObjects:
            if obj.name == "name":
                return obj
        
        return None
        
       
    def generatePlayers(self):
        self.players = []

        for _ in range(1):
            self.players.extend(playgen.generatePlayer())

        

    def generateGameObjects(self):
        self.gameObjectTypes = []
        self.gameObjects = []

        self.gameObjectTypes.append(GameObjectType(self, "Pokemon", 5))
        self.gameObjects.append(GameObject(self.gameObjectTypes[0], "Charizard", False ))

    def generateChallenges(self):
        self.challengeTypes = []
        self.challenges = []

        self.challengeTypes.append(ChallengeType(self, "PokeStops", False, False, True, False))
        self.challengeTypes.append(ChallengeType(self,"PokemonCatch", True, False, True, False))
        self.challengeTypes.append(ChallengeType("Missions", True, True, True, True, True))
        
        for player in self.players:
            self.spawnPokemon(player)

      

    
    def spawnPokeStops(self,player): #rework
        for _ in range(0,5):
            rand_mod_a = random.uniform(-0.2,0.2)
            rand_mod_b  = random.uniform(-0.2,0.2)
            a = Challenge(self.challengeTypes[0], "PokeStop Metro", 0, 0, 0,0, player.PlayerLocationInfo.latitude, player.PlayerLocationInfo.longitude, "No Reward", False)
            self.challenges.append(a)
        
    def spawnPokemon(self, player):
        
        
        for _ in range(0,5):

            rand_mod_a = random.uniform(-0.2,0.2)
            rand_mod_b  = random.uniform(-0.2,0.2)
            a = Challenge(self.challengeTypes[1], "Catch Charizard", 0, 0, 0.001,0.01, player.PlayerLocationInfo.latitude, player.PlayerLocationInfo.longitude, self.gameObjects[0], False)
            self.challenges.append(a)
    
    def spawnMissions(self,player): #rework
        for _ in range(0,5):
            rand_mod_a = random.uniform(-0.2,0.2)
            rand_mod_b  = random.uniform(-0.2,0.2)
            a = Challenge(self.challengeTypes[1], "Starter mission", 0, 0, 0,0, player.PlayerLocationInfo.latitude, player.PlayerLocationInfo.longitude, "No Reward", False)
            self.challenges.append(a)
        
        

    def total_play(self,player):
        player.motivation = 5
        date =  datetime.datetime(2021, 1, 1,0,0)
        for _ in range(1, 365):
            
            date = date + datetime.timedelta(hours = 1)
            load_file = 'Resources/weather.csv'
            df = pd.read_csv(load_file)
            today = df.loc[df['Day'] == date.timetuple().tm_yday]
            print("The weather is:"+today['Weather'])

            if player.motivation > 1:
                self.gameplay_session(player, date)

            print(date)
            print("Concentration: ")
            print(player.Personality.Concentration)

    def gameplay_session(self,player, datetime):
        
        curr_lat = player.PlayerLocationInfo.latitude
        curr_long = player.PlayerLocationInfo.longitude
        a = 0

        while a < 2:
            rand_mod_a = random.uniform(-0.05,0.05)
            rand_mod_b  = random.uniform(-0.05,0.05)
            curr_lat = curr_lat + rand_mod_a
            curr_long = curr_long + rand_mod_b

            self.create_moment(player, curr_lat, curr_long, datetime) 
            a = a+1


        
    def create_moment(self,player, latitude, longitude, timestamp):
        self.gameplay_moments.append(PlayMoment(player, latitude, longitude, timestamp))


        

        
        
    