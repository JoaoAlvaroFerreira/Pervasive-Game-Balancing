import Controller.PlayerGeneration as playgen
from Model.player import *
from Model.game_object import *
from Model.challenge import *
from Model.game import *
import datetime
import random
import pandas as pd
import matplotlib.pyplot as plt

class GameManagement:
    
    def create(self, conn):
        self.generatePlayers()
        self.generateGameObjects()
        self.generateChallenges()
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

        
    def plot(self, conn):
        self.load(conn)
        longs = [-6,-4,-2]
        lats = [38,40,43]
        for player in self.players:
            lats.append(player.PlayerLocationInfo.latitude)
            longs.append(player.PlayerLocationInfo.longitude)

        df = pd.DataFrame([lats, longs]).T
        df.columns=['Latitude', 'Longitude']
        ruh_m = plt.imread('Resources/map.png')
        BBox = (-10.371, 3.735, 35.443, 44.402)
        fig, ax = plt.subplots(figsize = (8,7))
        
        ax.scatter(df.Longitude, df.Latitude, zorder=1, alpha= 1, c='b', s=10)
        ax.set_title('Iberian Peninsula Players')
        ax.set_xlim(BBox[0],BBox[1])
        ax.set_ylim(BBox[2],BBox[3])
        ax.imshow(ruh_m, zorder=0, extent = BBox, aspect= 'equal')
        plt.show()



    
    def load(self, conn):
        self.conn = conn
        self.players = []
        self.load_game_objects(conn)
        self.load_challenges(conn)
        self.gameplay_moments = []
        self.challenge_instances = []

        cur = conn.execute(''' SELECT id, name from Player''' )
        for row in cur:
            new_p = Player(row[1])
            new_p.load_player(conn,row[0])
            self.players.append(new_p)
            sql = ''' SELECT id, latitude, longitude, play_timestamp FROM PlayMoment WHERE playerID == {} '''.format(row[0])
            cur2 = conn.execute(sql)
            for row2 in cur2:
                new_gm = PlayMoment(new_p, row2[1],row2[2],row2[3])
                self.gameplay_moments.append(new_gm)
            
            sql = ''' SELECT id, challengeID, attempted, success, ch_timestamp FROM ChallengeInstance WHERE playerID == {} '''.format(row[0])
            cur3 = conn.execute(sql)
            for row3 in cur3:
                ch =  self.find_challenge(row3[1])
                new_chi = ChallengeInstance(ch, row3[2],row3[3], new_p, row3[4])
                self.challenge_instances.append(new_chi)
      

       
            

       
    def sim(self, conn):
        self.load(conn)

        for player in self.players:
            self.total_play(player)
        
        #for gm in self.gameplay_moments:
        #    gm.insert_into_db(self.conn)
        
        #for chi in self.challenge_instances:
        #    chi.insert_into_db(self.conn)


    def load_game_objects(self, conn):
        self.gameObjectTypes = []
        self.gameObjects = []
        cur = conn.execute(''' SELECT id, name, importance from GameObjectType''' )

        for row in cur:
            new_got = GameObjectType(self,row[1], row[2])
            query = ''' SELECT id, name, keyItem from GameObject WHERE gameObjectTypeID =={}''' .format(row[0])
            cur2 = conn.execute(query)
            self.gameObjectTypes.append(new_got)
            for row2 in cur2:
                new_go = GameObject(new_got, row2[1], row2[2])
                self.gameObjects.append(new_go)
                

    def load_challenges(self, conn):
        self.challengeTypes = []
        self.challenges = []
        cur = conn.execute(''' SELECT id,name, temporary, narrative, locationRelevant, uniqueChallenge from ChallengeType''' )

        for row in cur:
            new_cht = ChallengeType(self,row[1], row[2], row[3],row[4], row[5])
            query = ''' SELECT id, name, startDateAvailable, endDateAvailable, radiusLocationAvailable, radiusLocationVisible, latitude, longitude, itemReward, Multiplayer From Challenge WHERE ChallengeTypeID =={}''' .format(row[0])
            cur2 = conn.execute(query)
            
            self.challengeTypes.append(new_cht)
            for row2 in cur2:
                new_ch = Challenge(new_cht, row2[1], row2[2], row2[3],row2[4],row2[5],row2[6],row2[7], None, row2[9])
                new_ch.id = row2[0]
               
                print(row2[8])
                query = ('''SELECT name FROM GameObject WHERE id == {}'''.format(row2[8]))
                go_name = conn.execute(query)
                new_ch.itemReward = self.find_object(go_name)
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
        
        

    def create_moment(self,player, latitude, longitude, timestamp):
        gm = PlayMoment(player, latitude, longitude, timestamp)
        gm.insert_into_db(self.conn)
        self.gameplay_moments.append(gm)


        

        
        
    