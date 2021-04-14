import itertools
import Model.player

class GameObjectType:
    def __init__(self,game, name, importance):
        self.game = game
        self.name = name
        self.importance = importance

    def insert_into_db(self,conn):
        sql = ''' INSERT INTO GameObjectType(name, importance)
                VALUES("{}","{}") '''.format(self.name, self.importance)
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()        
        return cur.lastrowid


class GameObject:
    def __init__(self,GameObjectType, name, keyItem, price):
        self.GameObjectType = GameObjectType
        self.name = name
        self.keyItem = keyItem
        self.price = price

    def insert_into_db(self,conn):
        query = '''SELECT id FROM GameObjectType WHERE name == "{}"'''.format(self.GameObjectType.name)
        cur = conn.execute(query)
        for row in cur:
            got_id = row[0]

        sql = ''' INSERT INTO GameObject(gameObjectTypeID, name, keyItem, price)
                VALUES("{}","{}","{}","{}") '''.format(got_id,self.name, self.keyItem, self.price)
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()        
        return cur.lastrowid

class GameObjectInstance:
    def __init__(self,GameObject, name, quality, spentIn, rewardFor):
        self.GameObject = GameObject
        self.name = name
        self.quality = quality
        self.spentIn = spentIn
        self.rewardFor = rewardFor

class Inventory:
    def __init__(self,Player, GameObject):
        self.Player = Player
        self.GameObject = GameObject

    def insert_into_db(self,conn):
        
        sql = ''' INSERT INTO Inventory(playerID, GameObjectID)
                VALUES("{}","{}") '''.format(self.Player.id, self.GameObject.id)
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()        
        self.id = cur.lastrowid
        return cur.lastrowid


class Wallet:
    def __init__(self,player, Currency):
        self.player = player
        self.Currency = Currency

class StoreItem:
    def __init__(self, prices, GameObject):
        self.prices = prices
        self.GameObject = GameObject

class Purchase:
    def __init__(self, Player, GameObject, TimeStamp):
        self.GameObject = GameObject
        self.Player = Player
        self.TimeStamp = TimeStamp
    
    def insert_into_db(self,conn):
        
        sql = ''' INSERT INTO Purchase(playerID, GameObjectID, purchase_timestamp)
                VALUES("{}","{}","{}") '''.format(self.Player.id, self.GameObject.id, self.TimeStamp)
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()        
        self.id = cur.lastrowid
        return cur.lastrowid