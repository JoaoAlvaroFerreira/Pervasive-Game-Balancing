class Game:
    def __init__(self,name, locationbased, timebased, socialexpansion):
        self.name = name
        self.locationbased = locationbased
        self.timebased = timebased
        self.socialexpansion = socialexpansion


class PlayMoment:
     def __init__(self, player, latitude, longitude, time, session):
         self.player = player
         self.latitude = latitude
         self.longitude = longitude
         self.session = session
         self.time = time

     def insert_into_db(self,conn):
        query = ''' SELECT id FROM Player WHERE name == "{}"''' .format(self.player.name)
        cur = conn.execute(query)
        for row in cur:
            cht_id = row[0]

        sql = ''' INSERT INTO PlayMoment(playerID, gameSession, latitude, longitude, play_timestamp)
                VALUES("{}","{}","{}","{}") '''.format(cht_id, self.session, self.latitude, self.longitude, self.time)
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()        
        self.id = cur.lastrowid
        return cur.lastrowid

