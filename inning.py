import pandas as pd
from atbat import AtBat

class Inning():
    def __init__(self, data, inning, top_bottom):
        self.game_data = data
        self.top_bottom = top_bottom
        self.inning_data = self.game_data[self.game_data['Inning'] == inning]

        if top_bottom == 'top':
            self.data = self.inning_data[self.inning_data['Top/Bottom'] == 'Top']
        elif top_bottom == 'bottom':
            self.data = self.inning_data[self.inning_data['Top/Bottom'] == 'Bottom']
        else:
            raise ValueError(f"top_bottom parameter requires either 'top' or 'bottom' not '{top_bottom}'")

        self.number = inning

    def at_bats(self):
        at_bats = []
        for i in range(len(set(self.data['PAofInning']))):
            at_bats.append(AtBat(self.game_data, self.number, i+1, self.top_bottom))
        return at_bats
    
    def pitcherStatline(self, pitcher_id):
        #Define what a hit is
        hits = ['Single', 'Double', 'Triple', 'HomeRun']
        #Get pitcher data
        pitcher_data = self.data[self.data['PitcherId'] == pitcher_id]

        K = len(pitcher_data[pitcher_data['KorBB'] == 'Strikeout'])
        R = pitcher_data.RunsScored.sum()
        H = len(pitcher_data[pitcher_data['PlayResult'].isin(hits)])
        BB = len(pitcher_data[pitcher_data['KorBB'] == 'Walk'])
        HBP = len(pitcher_data[pitcher_data['PitchCall'] == 'HitByPitch'])

        return f'{K} K, {R} R, {H} H, {BB} BB, {HBP} HBP'
