import itertools
import player

class GameObjectType:
    def __init__(self,game, name, importance):
        self.game = game
        self.name = name
        self.importance = importance

class GameObject:
    def __init__(self,GameObjectType, name, keyItem):
        self.GameObjectType = GameObjectType
        self.name = name
        self.keyItem

class GameObjectInstance:
    def __init__(self,GameObject, name, quality, spentIn, rewardFor):
        self.GameObject = GameObject
        self.name = name
        self.quality = quality
        self.spentIn
        self.rewardFor

class Inventory:
    def __init__(self,Player, GameObjectInstance):
        self.Player = Player
        self.GameObjectInstance = GameObjectInstance

class Wallet:
    def __init__(self,player, Currency):
        self.player = player
        self.Currency = Currency

class StoreItem:
    def __init__(self, prices, GameObject):
        self.prices = prices
        self.GameObject = GameObject

class Purchase:
    def __init__(self, StoreItem, Player, TimeStamp, CurrencyUsed, Cosmetic):
        self.StoreItem = StoreItem
        self.Player = Player
        self.TimeStamp = TimeStamp
        self.CurrencyUsed = CurrencyUsed
        self.Cosmetic = Cosmetic