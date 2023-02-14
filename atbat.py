import pandas as pd
from pitch import Pitch

class AtBat():
    def __init__(self, csv, inning, top_bottom, at_bat):
        self.game_data = pd.read_csv(csv)
        self.inning_data = self.game_data[self.game_data['Inning'] == inning]
        self.half_inning_data = self.inning_data[self.inning_data['Top/Bottom'] == top_bottom]
        self.data = self.half_inning_data[self.half_inning_data['PAofInning'] == at_bat]
        self.number = at_bat
        self.pitches = self.getPitches(csv, inning, at_bat, top_bottom)

    def getPitches(self, csv, inning, at_bat, top_bottom):
        i = 1
        pitches = []
        while True: 
            if len(Pitch(csv, inning, top_bottom, at_bat, i).data) > 0:
                pitches.append(Pitch(csv, inning, top_bottom, at_bat, i))
                i += 1
            else:
                break
        return pitches