import pandas as pd
from inning import Inning
from team import Team

class Game:
    def __init__(self, data):
        self.data = data
        self.stadium = self.data.iloc[0]['Stadium']
        self.level = self.data.iloc[0]['Level']
        self.league = self.data.iloc[0]['League']
        self.trackman_id = self.data.iloc[0]['GameID']
        self.game_id = 'Insert local ID system?'
        self.date = self.data.iloc[0]['Date']
        self.time = self.data.iloc[0]['Time']
        self.home = Team(self, data.iloc[0]['HomeTeam'][0])
        self.away = Team(self, data.iloc[0]['AwayTeam'][0])

    def innings(self, top_bottom):
        i = 1
        innings = []
        while True: 
            if len(Inning(self.data, i, top_bottom).data) > 0:
                innings.append(Inning(self.data, i, top_bottom))
                i += 1
            else:
                break
        return innings
        
    def writeHitterReports():
        pass

    def writePitcherReports():
        pass

