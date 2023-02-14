import pandas as pd

def getInnings(csv):
    i = 1
    innings = []
    while True: 
        if len(Inning(csv, i).data) > 0:
            innings.append(Inning(csv, i))
            i += 1
        else:
            break
    return innings

class Game:
    def __init__(self, csv):
        self.data = pd.read_csv(csv)
        self.stadium = self.data.iloc[0]['Stadium']
        self.level = self.data.iloc[0]['Level']
        self.league = self.data.iloc[0]['League']
        self.trackman_id = self.data.iloc[0]['GameID']
        self.id = 'Insert local ID system?'
        self.date = self.data.iloc[0]['Date']
        self.time = self.data.iloc[0]['Time']
        self.home = 'Insert home team object'
        self.away = 'Insert away team object'
        self.innings = getInnings(csv)
        
class Inning():
    def __init__(self, csv, inning):
        self.game_data = pd.read_csv(csv)
        self.data = self.game_data[self.game_data['Inning'] == inning]
