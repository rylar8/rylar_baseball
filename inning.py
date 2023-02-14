import pandas as pd
from atbat import AtBat

class Inning():
    def __init__(self, csv, inning):
        self.game_data = pd.read_csv(csv)
        self.data = self.game_data[self.game_data['Inning'] == inning]
        self.number = inning
        self.top = self.data[self.data['Top/Bottom'] == 'Top']
        self.bottom = self.data[self.data['Top/Bottom'] == 'Bottom']
        self.at_bats = self.getAtBats(csv, inning)

    def getAtBats(self, csv, inning, top_bottom):
        i = 1
        at_bats = []
        while True: 
            if len(AtBat(csv, inning, top_bottom, i).data) > 0:
                at_bats.append(AtBat(csv, inning, top_bottom, i))
                i += 1
            else:
                break
        return {'top' : at_bats}