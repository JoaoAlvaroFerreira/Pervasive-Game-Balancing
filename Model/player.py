class Player:
    name = "aaaaaa"

    def __init__(self, name):
        self.name = name

        #create random players from Europe
        #start by simulating ONE PERSONALITY YOU FUCK

        #for player behavior simulation, use moments-to-catches ratio as a way to measure dead air.
        #use completion rate as well as pure volume of catches as metrics for conclusions.
    
    def insert_into_db(self,conn):
        sql = ''' INSERT INTO Player(name)
                VALUES("{}") '''.format(self.name)
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        return cur.lastrowid

class Personality: #0-10
    def __init__(self, Concentration,Competitiveness,PlayerSkills,UserControl,ClearGoals,Feedback,Immersion,SocialInteraction,PersonalityType):
        self.Concentration = Concentration
        self.Competitiveness = Competitiveness
        self.PlayerSkills = PlayerSkills
        self.UserControl = UserControl
        self.ClearGoals = ClearGoals
        self.Feedback = Feedback
        self.Immersion = Immersion
        self.SocialInteraction = SocialInteraction
        self.PersonalityType = PersonalityType

class Demographic:
    def __init__(self,Age,Education, Ethnicity, SocioEconomicStatus):
        self.Age = Age
        self.Education = Education
        self.Ethnicity = Ethnicity
        self.SocioEconomicStatus = SocioEconomicStatus

class PlayerLocationInfo:
    def __init__(self,latitude,longitude,city,typicalWeather):
        self.latitude = latitude
        self.longitude = longitude
        self.city = city
        self.typicalWeather

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