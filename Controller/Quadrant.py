class Quadrant:
    def __init__(self, minLat, maxLat, minLong, maxLong):
        self.minLat = minLat
        self.maxLat = maxLat
        self.minLong = minLong
        self.maxLong = maxLong
        self.population = 0

    def add_player(self, lat, long):
        #print("MIN LAT: {} LAT: {} MAXLAT: {}".format(self.minLat, lat, self.maxLat))
        
        if lat > self.minLat and lat < self.maxLat:
           
            if long > self.minLong and long < self.maxLong:
                self.population = self.population + 1
                
                return True
        
        return False