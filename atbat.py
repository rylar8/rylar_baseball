import pandas as pd
from pitch import Pitch
import player

class AtBat():
    def __init__(self, data, inning, at_bat, top_bottom):
        self.inning = inning
        self.game_data = data
        self.top_bottom = top_bottom

        self.inning_data = self.game_data[self.game_data['Inning'] == inning]
        if top_bottom == 'top':
            self.half_inning_data = self.inning_data[self.inning_data['Top/Bottom'] == 'Top']
        elif top_bottom == 'bottom':
            self.half_inning_data = self.inning_data[self.inning_data['Top/Bottom'] == 'Bottom']
        else:
            raise ValueError(f"top_bottom parameter requires either 'top' or 'bottom' not '{top_bottom}'")
        
        self.data = self.half_inning_data[self.half_inning_data['PAofInning'] == at_bat]
        self.number = at_bat
        
        self.outs = list(self.data['Outs'])[0]

    def pitches(self):
        i = 1
        pitches = []
        while True: 
            if len(Pitch(self.game_data, self.inning, self.number, i, self.top_bottom).data) > 0:
                pitches.append(Pitch(self.game_data, self.inning, self.number, i, self.top_bottom))
                i += 1
            else:
                break
        return pitches
    
    def batter(self):
        return player.Batter(list(self.data['BatterId'])[0])

    def pitcher(self):
        return player.Pitcher(list(self.data['PitcherId'])[0])
    
    def catcher(self):
        return player.Catcher(list(self.data['CatcherId'])[0])