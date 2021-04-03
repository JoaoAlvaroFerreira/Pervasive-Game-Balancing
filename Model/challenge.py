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
        self.Multiplayer = Multiplayer


    def insert_into_db(self,conn):
        query = ''' SELECT id FROM ChallengeType WHERE name == "{}"''' .format(self.ChallengeType.name)
        cur = conn.execute(query)
        for row in cur:
            cht_id = row[0]
        
        query = ''' SELECT id FROM GameObject WHERE name == "{}"''' .format(self.itemReward.name)
        cur = conn.execute(query)
        for row in cur:
            go_id = row[0]
        


        sql = ''' INSERT INTO Challenge(ChallengeTypeID, name, startDateAvailable, endDateAvailable, radiusLocationAvailable, radiusLocationVisible, latitude, longitude, itemReward, Multiplayer)
                VALUES("{}","{}","{}","{}","{}","{}","{}","{}","{}","{}") '''.format(cht_id,self.name, self.startDateAvailable, self.endDateAvailable, self.radiusLocationAvailable, self.radiusLocationVisible, self.latitude, self.longitude, go_id, self.Multiplayer)
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        self.id = cur.lastrowid                
        return cur.lastrowid


class ChallengeInstance:
    def __init__(self,Challenge, attempted, success,player, timestamp):
        self.Challenge = Challenge
        self.attempted = attempted
        self.success = success
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

class ChallengeTarget: 
    def __init__(self,targetOrder, challengeInstance, dateSpawned, dateCompleted, completed, latitudeCompleted, longitudeCompleted, itemReward):
        self.targetOrder = targetOrder
        self.challengeInstance = challengeInstance
        self.dateSpawned = dateSpawned
        self.dateCompleted = dateCompleted
        self.completed = completed
        self.latitudeCompleted = latitudeCompleted
        self.longitudeCompleted = longitudeCompleted
        self.itemReward = itemReward

	
#remember to allow the option for activation ranges as well as temporal and social ranges (ie. need 5-7 people for raid)!!!!!!! otherwise poke stops get owned