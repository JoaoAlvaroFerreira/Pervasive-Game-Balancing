class ChallengeType :
	def __init__(self,game ,
	name  ,
	temporary ,
	narrative ,
	uniqueChallenge):

        self.game = game 
        self.name = name 
        self.temporary = temporary 
        self.narrative = narrative
        self.uniqueChallenge  = uniqueChallenge,
      


class Challenge:
	def __init__(self,
	ChallengeType  ,
	name  ,
	TimeRestraint  ,
	SpaceRestraint,
    Multiplayer ):
        self.ChallengeType = ChallengeType
        self.name = name
        self.TimeRestraint = TimeRestraint
        self.SpaceRestraint = SpaceRestraint
        self.Multiplayer = Multiplayer

	


class ChallengeInstance:
    def __init__(self,Challenge
	name ,
	startDateAvailable,
    endDateAvailable,
    radiusLocationAvailable,
    radiusLocationVisible,
	latitude,
	longitude,
	completed  ,
	player  ,
	player2  ):
        self.Challenge = Challenge
        self.name = name
        self.startDateAvailable = startDateAvailable
        self.endDateAvailable = endDateAvailable
        self.radiusLocationAvailable = radiusLocationAvailable
        self.radiusLocationVisible = radiusLocationVisible
        self.latitude = latitude
        self.longitude = longitude
        self.completed = completed
        self.player = player
        self.player2 = player2

class ChallengeTarget: 
    def __init__(self,targetOrder, challengeInstance, dateSpawned, dateCompleted, completed, latitudeCompleted, longitudeCompleted):
        self.targetOrder = targetOrder
        self.challengeInstance = challengeInstance
        self.dateSpawned = dateSpawned
        self.dateCompleted = dateCompleted
        self.completed = completed
        self.latitudeCompleted = latitudeCompleted
        self.longitudeCompleted = longitudeCompleted

	
#remember to allow the option for activation ranges as well as temporal and social ranges (ie. need 5-7 people for raid)!!!!!!! otherwise poke stops get owned