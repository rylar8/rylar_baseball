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
        i = 1
        at_bats = []
        while True: 
            if len(AtBat(self.game_data, self.number, i, self.top_bottom).data) > 0:
                at_bats.append(AtBat(self.game_data, self.number, i, self.top_bottom))
                i += 1
            else:
                break
        return at_bats