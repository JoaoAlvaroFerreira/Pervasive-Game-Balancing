class ChallengeType :
    def __init__(self, game, name, temporary, narrative, locationRelevant, uniqueChallenge):
        self.game = game
        self.name = name 
        self.temporary = temporary 
        self.narrative = narrative
        self.locationRelevant = locationRelevant
        self.uniqueChallenge  = uniqueChallenge

    def insert_into_db(self,conn):

        
        sql = ''' INSERT INTO ChallengeType(name, temporary, narrative, locationRelevant, uniqueChallenge) VALUES("{}","{}","{}","{}","{}") '''.format(self.name, self.temporary, self.narrative, self.locationRelevant, self.uniqueChallenge)
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()        
        self.id = cur.lastrowid        
        return cur.lastrowid



class Challenge:
    def __init__(self,
    ChallengeType  ,
    name,
    startDateAvailable,
    endDateAvailable,
    radiusLocationAvailable,
    radiusLocationVisible,
    latitude,
    longitude,
    itemReward,
    itemSpend,
    Multiplayer ):
        self.ChallengeType = ChallengeType
        self.name = name
        self.startDateAvailable = startDateAvailable
        self.endDateAvailable = endDateAvailable
        self.radiusLocationAvailable = radiusLocationAvailable
        self.radiusLocationVisible = radiusLocationVisible
        self.latitude = latitude
        self.longitude = longitude
        self.itemReward = itemReward
        self.itemSpend = itemSpend
        self.Multiplayer = Multiplayer


    def insert_into_db(self,conn):
        query = ''' SELECT id FROM ChallengeType WHERE name == "{}"''' .format(self.ChallengeType.name)
        cur = conn.execute(query)
        for row in cur:
            cht_id = row[0]
        
        if self.itemReward is not None:
            query = ''' SELECT id FROM GameObject WHERE name == "{}"''' .format(self.itemReward.name)
            cur = conn.execute(query)
            for row in cur:
                go_id = row[0]
        else: 
            go_id = None
        
        if self.itemSpend is not None:
            query = ''' SELECT id FROM GameObject WHERE name == "{}"''' .format(self.itemSpend.name)
            cur = conn.execute(query)
            for row in cur:
                goS_id = row[0]
        else: goS_id = None
        


        sql = ''' INSERT INTO Challenge(ChallengeTypeID, name, startDateAvailable, endDateAvailable, radiusLocationAvailable, radiusLocationVisible, latitude, longitude, itemReward, itemSpend, Multiplayer)
                VALUES("{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}") '''.format(cht_id,self.name, self.startDateAvailable, self.endDateAvailable, self.radiusLocationAvailable, self.radiusLocationVisible, self.latitude, self.longitude, go_id, goS_id, self.Multiplayer)
        cur = conn.cursor()
        cur.execute(sql)
        self.id = cur.lastrowid                
        return cur.lastrowid


class ChallengeInstance:
    def __init__(self,Challenge, attempted, success,player, timestamp):
        self.Challenge = Challenge
        self.attempted = attempted
        self.success = success #change to int
        self.player = player
        self.timestamp = timestamp


    def insert_into_db(self,conn):
        
       

        sql = ''' INSERT INTO ChallengeInstance(ChallengeID, attempted, success, playerID, ch_timestamp)
                VALUES("{}","{}","{}","{}","{}") '''.format(self.Challenge.id, self.attempted, self.success, self.player.id, self.timestamp)
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        self.id = cur.lastrowid        
        return cur.lastrowid
