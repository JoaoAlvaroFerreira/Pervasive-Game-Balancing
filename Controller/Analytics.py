class Analytics:
    def __init__(self, game):
        self.game = game
    
    def analyse_players(self):
        print("THERE ARE THIS MANY GAMEPLAY MOMENTS:")
        print(len(self.game.gameplay_moments))
        


