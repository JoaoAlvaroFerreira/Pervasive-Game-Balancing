class Game:
    def __init__(self,name, locationbased, timebased, socialexpansion):
        self.name = name
        self.locationbased = locationbased
        self.timebased = timebased
        self.socialexpansion = socialexpansion

class PlayMoment:
     def __init__(self, player, latitude, longitude, time):
         self.player = player
         self.latitude = latitude
         self.longitude = longitude
         self.time = time
