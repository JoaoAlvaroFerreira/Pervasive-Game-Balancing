class Player:
    name = "aaaaaa"
    motivation = 0

    def __init__(self, name):
        self.name = name

        #create random players from Iberian Peninsula
        #start by simulating 

        #for player behavior simulation, use moments-to-catches ratio as a way to measure dead air.
        #use completion rate as well as pure volume of catches as metrics for conclusions.
    
    def insert_player(self,conn):
        id = self.insert_into_db(conn)
        #self.PlayerLocationInfo.insert_into_db(conn, id)
        #self.Demographic.insert_into_db(conn, id)
        #self.Personality.insert_into_db(conn, id)

    def insert_into_db(self,conn):
        sql = ''' INSERT INTO Player(name)
                VALUES("{}") '''.format(self.name)
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()    
        self.id = cur.lastrowid            
        return cur.lastrowid

    def load_player(self,conn, id):
        query = ''' SELECT latitude,longitude,country FROM PlayerLocationInfo WHERE playerID == {}'''.format(id)
        cur = conn.execute(query)
        for row in cur:
            self.PlayerLocationInfo = PlayerLocationInfo(row[0], row[1], row[2])

        query = ''' SELECT Age, Gender, SocioEconomicStatus FROM Demographic WHERE playerID == {}''' .format(id)
        cur = conn.execute(query)
        for row in cur:
            self.Demographic = Demographic(row[0], row[1], row[2])

        query = ''' SELECT Concentration,Competitiveness,PlayerSkills,UserControl,ClearGoals,Feedback,Immersion,SocialInteraction,Free2Play, PersonalityType from Personality WHERE playerID == {}''' .format(id)
        cur = conn.execute(query)
        for row in cur:
            self.Personality = Personality(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8], row[9])


        return self



class Personality: #0-5
    def __init__(self, Concentration,Competitiveness,PlayerSkills,UserControl,ClearGoals,Feedback,Immersion,SocialInteraction,Free2Play, PersonalityType):
        self.Concentration = Concentration
        self.Competitiveness = Competitiveness
        self.PlayerSkills = PlayerSkills
        self.UserControl = UserControl
        self.ClearGoals = ClearGoals
        self.Feedback = Feedback
        self.Immersion = Immersion
        self.SocialInteraction = SocialInteraction
        self.Free2Play = Free2Play
        self.PersonalityType = PersonalityType

    def insert_into_db(self,conn, playerID):
        sql = ''' INSERT INTO Personality(playerID, Concentration,Competitiveness,PlayerSkills,UserControl,ClearGoals,Feedback,Immersion,SocialInteraction,Free2Play, PersonalityType)
                VALUES("{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}") '''.format(playerID, self.Concentration,self.Competitiveness,self.PlayerSkills,self.UserControl,self.ClearGoals,self.Feedback,self.Immersion,self.SocialInteraction,self.Free2Play, self.PersonalityType)
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        return cur.lastrowid


class Demographic:
    def __init__(self,Age, Gender, SocioEconomicStatus):
        self.Age = Age
        self.Gender = Gender
        self.SocioEconomicStatus = SocioEconomicStatus

    def insert_into_db(self, conn, playerID):
        sql = ''' INSERT INTO Demographic(playerID, Age, Gender, SocioEconomicStatus)
                VALUES("{}","{}","{}","{}") '''.format(playerID, self.Age, self.Gender, self.SocioEconomicStatus)
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        return cur.lastrowid

class PlayerLocationInfo:
    def __init__(self,latitude,longitude,country):
        self.latitude = latitude
        self.longitude = longitude
        self.country = country

    def insert_into_db(self, conn, playerID):
        sql = ''' INSERT INTO PlayerLocationInfo(playerID, latitude, longitude, country)
                VALUES("{}","{}","{}","{}") '''.format(playerID, self.latitude, self.longitude, self.country)
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        return cur.lastrowid


class Faction:
    def __init__(self,name):
        self.name = name

class FactionMember:
    def __init__(self,player, faction):
        self.player = player
        self.faction = faction

class PlayerConnection:
    def __init__(self,player1, player2):
        self.player1 = player1
        self.player2 = player2