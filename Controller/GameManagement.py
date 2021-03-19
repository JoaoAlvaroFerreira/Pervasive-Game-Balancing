import Controller.PlayerGeneration as playgen
import Model.player
from Model.challenge import *

class GameManagement:
    def __init__(self):
        self.generatePlayers()
        self.challenges = generateChallenges()
       
    def generatePlayers(self):
        self.players = []

        for _ in range(0, 5):
            self.players.append(playgen.generatePlayer())

        


    def generateChallenges():
        self.PokeStops = ChallengeType(self, "PokeStops", False, False, True, False)
        self.PokemonCatch = ChallengeType("PokemonCatch", True, False, True, False)
        self.Pokemon = GameObjectType(self, "Pokemon", 5)
        self.Charizard = GameObject(self.Pokemon, "Charizard", False )
        self.PokemonSpawned = []
        
        for player in self.players:
            spawnPokemon(player)

        Missions = ChallengeType("Missions", True, True, True, True)

        
        
    def spawnPokemon(self, player):
        
        
        for _ in range(0,5):
            a = Challenge(self.PokemonCatch, "Catch Charizard", 0, 0, 0.001,0.01, player.PlayerLocationData.latitude, player.PlayerLocationData.longitude, False)
            self.PokemonSpawn.append(a)
    
    def spawnMissions(self,player):
        for _ in range(0,5):
            a = Challenge(self.Missions, "Starter mission", 0, 0, 0,0, player.PlayerLocationData.latitude, player.PlayerLocationData.longitude, False)
            self.PokemonSpawn.append(a)
        
        
        
        
    