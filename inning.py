import pandas as pd
from atbat import AtBat
import matplotlib.pyplot as plt

class Inning():
    def __init__(self, data, inning, top_bottom):
        self.game_data = data
        self.top_bottom = top_bottom
        self.inning_data = self.game_data[self.game_data['Inning'] == inning]
        self.date = pd.to_datetime(self.game_data.iloc[0]['Date']).date()
        self.game_id = self.game_data.iloc[0]['GameID']

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

    def movementPlot(self, pitcher_id, view = 'pitcher'):
        if view == 'pitcher':
            mirror = 1
        elif view == 'catcher':
            mirror = -1
        else:
            raise Exception('View must be either "pitcher" or "catcher"')
        
        #Colors for pitch types
        pitch_colors = {'Fastball': '#FF0000', 'Four-Seam': '#FF0000', 'ChangeUp': '#00BFFF', 'Changeup': '#00BFFF', 'Slider': '#00FA9A',
                        'Cutter': '#7CFC00','Curveball': '#32CD32', 'Splitter': '#ADD8E6', 'Sinker': '#FF7F50', 'Knuckleball': '#48D1CC'}

        pitcher_data = self.data[self.data['PitcherId'] == pitcher_id]
        
        #Initialize plot
        fig, ax = plt.subplots(figsize = (2.5, 2.95))
        ax.set_xlim(-30,30)
        ax.set_ylim(-30,30)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(True)
        ax.spines['left'].set_visible(True)
        ax.spines['left'].set_position('zero')
        ax.spines['bottom'].set_position('zero')
        ax.axes.xaxis.set_visible(True)
        ax.axes.yaxis.set_visible(True)
        ax.spines['bottom'].set_linewidth(2)
        ax.spines['left'].set_linewidth(2)
        ax.spines['left'].set_color('black')
        ax.spines['bottom'].set_color('black')
        ax.tick_params(axis = 'both', which= 'both', bottom = False, left = False, labelleft = False, labelbottom = False)

        #Create lists for plotting
        x = []
        y = []
        c = []

        #Get pitches from tagged, if an error occurs use auto type
        try:
            pitches = set(pitcher_data['TaggedPitchType'].dropna())
            for pitch in pitches:
                pitch_data = pitcher_data[pitcher_data['TaggedPitchType'] == pitch]
                x.append(mirror * pitch_data['HorzBreak'].mean())
                y.append(pitch_data['InducedVertBreak'].mean())
                c.append(pitch_colors[pitch])
        except:
            pitches = set(pitcher_data['AutoPitchType'].dropna())
            for pitch in pitches:
                pitch_data = pitcher_data[pitcher_data['TaggedPitchType'] == pitch]
                x.append(mirror * pitch_data['HorzBreak'].mean())
                y.append(pitch_data['InducedVertBreak'].mean())
                c.append(pitch_colors[pitch])
        
        df = pd.DataFrame({'x': x,
                    'y': y,
                    'c': c})

        groups = df.groupby('c')
        
        for name, group in groups:
            plt.scatter(group.x, group.y, s = 100, zorder = 3, color = group.c, edgecolors= 'Black', linewidths = .45)
        
        #Save figure in temporary holding spot so it can be anchored in excel sheet
        plt.tight_layout()
        plt.savefig(f'temporary_figures//{self.date}{self.game_id}{self.number}{pitcher_id}movement_plot.png', transparent = True)
        plt.close()

        return f'temporary_figures//{self.date}{self.game_id}{self.number}{pitcher_id}movement_plot.png'
        