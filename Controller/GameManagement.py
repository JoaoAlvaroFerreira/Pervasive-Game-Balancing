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

class GameManagement:
    
    def create(self, conn):
        self.load(conn)
        self.generatePlayers()
        self.generateGameObjects()
        self.generateChallenges(40.9229, 41.4201, -8.8248, -7.7193)
        self.gameplay_moments = []
        

        
        for player in self.players:
            print("inserting player "+player.name)
            player.insert_player(conn)

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
            conn.commit()
 


    
    def load(self, conn):
        self.conn = conn
        self.players = []
        self.load_game_objects()
        self.load_challenges()
        self.gameplay_moments = []
        self.challenge_instances = []

        cur = conn.execute(''' SELECT id, name from Player''' )
        for row in cur:
            new_p = Player(row[1])
            new_p.load_player(conn,row[0])
            self.players.append(new_p)
            sql = ''' SELECT id, latitude, longitude, play_timestamp, gameSession FROM PlayMoment WHERE playerID == {} '''.format(row[0])
            cur2 = conn.execute(sql)
            for row2 in cur2:
                new_gm = PlayMoment(new_p, row2[1],row2[2],row2[3], row2[4])
                self.gameplay_moments.append(new_gm)
            
            sql = ''' SELECT id, challengeID, attempted, success, ch_timestamp FROM ChallengeInstance WHERE playerID == {} '''.format(row[0])
            cur3 = conn.execute(sql)
            for row3 in cur3:
                ch =  self.find_challenge(row3[1])
                new_chi = ChallengeInstance(ch, row3[2],row3[3], new_p, row3[4])
                self.challenge_instances.append(new_chi)
      

       
            

       



    def load_game_objects(self):
        self.gameObjectTypes = []
        self.gameObjects = []
        cur = self.conn.execute(''' SELECT id, name, importance from GameObjectType''' )

        for row in cur:
            new_got = GameObjectType(self,row[1], row[2])
            query = ''' SELECT id, name, keyItem from GameObject WHERE gameObjectTypeID =={}''' .format(row[0])
            cur2 = self.conn.execute(query)
            self.gameObjectTypes.append(new_got)
            for row2 in cur2:
                new_go = GameObject(new_got, row2[1], row2[2])
                self.gameObjects.append(new_go)
                

    def load_challenges(self):
        self.challengeTypes = []
        self.challenges = []
        cur = self.conn.execute(''' SELECT id,name, temporary, narrative, locationRelevant, uniqueChallenge from ChallengeType''' )

        for row in cur:
            new_cht = ChallengeType(self,row[1], row[2], row[3],row[4], row[5])
            query = ''' SELECT id, name, startDateAvailable, endDateAvailable, radiusLocationAvailable, radiusLocationVisible, latitude, longitude, itemReward, itemSpend, Multiplayer From Challenge WHERE ChallengeTypeID =={}''' .format(row[0])
            cur2 = self.conn.execute(query)
            
            self.challengeTypes.append(new_cht)
            for row2 in cur2:
                new_ch = Challenge(new_cht, row2[1], row2[2], row2[3],row2[4],row2[5],row2[6],row2[7], None, None, row2[10])
                new_ch.id = row2[0]
               
               
                query = ('''SELECT name FROM GameObject WHERE id == {}'''.format(row2[8]))
                go_name = self.conn.execute(query)
                new_ch.itemReward = self.find_object(go_name)
                self.challenges.append(new_ch)

                query = ('''SELECT name FROM GameObject WHERE id == {}'''.format(row2[9]))
                go_name = self.conn.execute(query)
                new_ch.itemSpend = self.find_object(go_name)
                self.challenges.append(new_ch)

    
    def find_object(self,name):
        
        for obj in self.gameObjects:
            if obj.name == name:
                return obj
        
        return None

    def find_challenge(self, id):
        for challenge in self.challenges:
            if challenge.id == id:
                return challenge
        
       
    def generatePlayers(self):
        self.players = []

        for _ in range(3):
            self.players.extend(playgen.generatePlayer())

        

    def generateGameObjects(self):
        self.gameObjectTypes = []
        self.gameObjects = []

        self.gameObjectTypes.append(GameObjectType(self, "Pokemon", 5))
        self.gameObjectTypes.append(GameObjectType(self, "Consumable", 2))
        self.gameObjectTypes.append(GameObjectType(self, "Cosmetic", 1))
        self.gameObjectTypes.append(GameObjectType(self, "PokeBall", 3))
        
        self.gameObjects.append(GameObject(self.gameObjectTypes[0], "Pikachu", False ))
        self.gameObjects.append(GameObject(self.gameObjectTypes[0], "Charizard", False ))
        self.gameObjects.append(GameObject(self.gameObjectTypes[0], "Mewtwo", False ))
        self.gameObjects.append(GameObject(self.gameObjectTypes[0], "Abra", False ))

    
        self.gameObjects.append(GameObject(self.gameObjectTypes[1], "Encounter Booster", False ))
        self.gameObjects.append(GameObject(self.gameObjectTypes[1], "EasyRaid", False ))

        
        self.gameObjects.append(GameObject(self.gameObjectTypes[2], "Jacket", False ))
        self.gameObjects.append(GameObject(self.gameObjectTypes[2], "Hat", False ))

        
        self.gameObjects.append(GameObject(self.gameObjectTypes[3], "PokeBall", False ))
        self.gameObjects.append(GameObject(self.gameObjectTypes[3], "SuperBall", False ))
        self.gameObjects.append(GameObject(self.gameObjectTypes[3], "UltraBall", False ))
        





    def generateChallenges(self, minlat, maxlat, minlon, maxlon):
        self.challengeTypes = []
        self.challenges = []

        self.challengeTypes.append(ChallengeType(self, "PokeStops", False, False, True, False))
        self.challengeTypes.append(ChallengeType(self,"PokemonCatch", True, False, False, False))
        self.challengeTypes.append(ChallengeType(self,"Missions", True, True, True, True))
        
        self.spawnPokemon(minlat, maxlat, minlon, maxlon)
        self.spawnPokeStops(minlat, maxlat, minlon, maxlon)
        
        self.spawnRaids(minlat, maxlat, minlon, maxlon)

        for player in self.players:
            self.spawnMissions(player)    
   
    def spawnPokemon(self, minlat, maxlat, minlon, maxlon):
        self.challenges = []
        load_file = 'D:\\School\\5oAno\\TESE\Repo\\Pervasive-Game-Balancing\\Resources\\CountryDistributionCSVs\PRT_population.csv'
              
        df_acc = pd.read_csv(load_file)
        df_acc = df_acc[df_acc['population']>5] # Reducing data size so it runs faster
        df_acc = df_acc[(df_acc['latitude'] > minlat) & (df_acc['latitude'] < maxlat)]
        df_acc = df_acc[(df_acc['longitude'] > minlon) & (df_acc['longitude'] < maxlon)]
        # Add marker for Boulder, CO
        for index, row in df_acc.iterrows():
            a = Challenge(self.challengeTypes[1], "Catch Pokemon", 0, 0, 0.01,0.1, row['latitude'], row['longitude'], self.gameObjects[0], self.gameObjects[8], False)
            self.challenges.append(a)
        
    
    
    def spawnPokeStops(self, minlat, maxlat, minlon, maxlon): #rework
        nodes = location_data_from_Overpass(minlat, maxlat, minlon, maxlon, "public_transport")
        
        for node in nodes:
            a = Challenge(self.challengeTypes[0], "PokeStop Metro", 0,0, 0.01,0.1, node.lat, node.lon, self.gameObjects[8],None, False)
            self.challenges.append(a)
        
        
        nodes = location_data_from_Overpass(minlat, maxlat, minlon, maxlon, "tourism")
        
        for node in nodes:
            a = Challenge(self.challengeTypes[0], "PokeStop Landmark", 0,0, 0.01,0.1, node.lat, node.lon, self.gameObjects[9], None, False)
            self.challenges.append(a)

    
    def spawnRaids(self, minlat, maxlat, minlon, maxlon):
        print("TO DO RAIDS")
    
    def spawnMissions(self,player): #rework
        for _ in range(0,5):
            rand_mod_a = random.uniform(-0.2,0.2)
            rand_mod_b  = random.uniform(-0.2,0.2)
            a = Challenge(self.challengeTypes[2], "Starter mission", 0, 0, 0,0, player.PlayerLocationInfo.latitude, player.PlayerLocationInfo.longitude,self.gameObjects[4], self.gameObjects[0], False)
            self.challenges.append(a)
        
        

    def create_moment(self,player, latitude, longitude, timestamp, i):
        gm = PlayMoment(player, latitude, longitude, timestamp,i)
        gm.insert_into_db(self.conn)
        self.gameplay_moments.append(gm)


        

        
        
    