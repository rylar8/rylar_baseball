import pandas as pd
from pitch import Pitch

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
        try:
            self.batter = self.data['Batter'].iloc[0]
            self.batter_id = self.data['BatterId'].iloc[0]
            self.pitcher = self.data['Pitcher'].iloc[0]
            self.pitcher_id = self.data['PitcherId'].iloc[0]
            self.catcher = self.data['Catcher'].iloc[0]
            self.catcher_id = self.data['CatcherId'].iloc[0]
        except IndexError:
            self.batter = self.data['Batter']
            self.batter_id = self.data['BatterId']
            self.pitcher = self.data['Pitcher']
            self.pitcher_id = self.data['PitcherId']
            self.catcher = self.data['Catcher']
            self.catcher_id = self.data['CatcherId']

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