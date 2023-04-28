import pandas as pd
from pitch import Pitch
import player
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon

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
        self.date = pd.to_datetime(self.data.iloc[0]['Date']).date()

    def pitches(self):
        pitches = []
        for i in range(len(set(self.data['PitchofPA']))):
            pitches.append(Pitch(self.game_data, self.inning, self.number, i+1, self.top_bottom))
        return pitches
    
    def batter(self):
        return player.Batter(list(self.data['BatterId'])[0])

    def pitcher(self):
        return player.Pitcher(list(self.data['PitcherId'])[0])
    
    def catcher(self):
        return player.Catcher(list(self.data['CatcherId'])[0])
    
    def zoneTracer(self, view = 'pitcher'):
        
        if view == 'pitcher':
            mirror = 1
        elif view == 'catcher':
            mirror = -1
        else:
            raise Exception('View must be either "pitcher" or "catcher"')

        #Colors for pitch types
        pitch_colors = {'Fastball': '#FF0000', 'Four-Seam': '#FF0000', 'ChangeUp': '#00BFFF', 'Changeup': '#00BFFF', 'Slider': '#00FA9A',
                        'Cutter': '#7CFC00','Curveball': '#32CD32', 'Splitter': '#ADD8E6', 'Sinker': '#FF7F50', 'Knuckleball': '#48D1CC'}
        
        #Initialize blank plot
        fig, ax = plt.subplots(figsize = (2.5, 5))
        ax.set_xlim(-1.25,1.25)
        ax.set_ylim(0,5) 
        for spine in ax.spines.values():
            spine.set_visible(False)
        ax.axes.xaxis.set_visible(False)
        ax.axes.yaxis.set_visible(False)

        #Add rectangle representing the typically called strikezone, using pitchgrader universal strike zone dimensions for outer light gray estimating .07 feet for lw
        ax.add_patch(Rectangle((-0.7508, 1.5942), 1.5217, 2.0091, facecolor='DarkGray', edgecolor = 'LightGray', fill=True, lw=8))

        # Create home plate polygon and add to plot with the actual home plate dimensions
        ax.add_patch(Polygon([[0, 0.01], [-0.7083, .25], [-0.7083, .5], [0.7083, .5], [0.7083, .25]], facecolor='White', edgecolor='Black', lw=2))
        
        #Get lists of pitch locations and colors for dataframe, n will be used for pitch annotations
        x = []
        y = []
        l = []
        c = []
        n = 1
        for pitch in self.pitches():
            x.append(mirror * pitch.location_side)
            y.append(pitch.location_height)
            l.append(n)
            #Try to use tagged_type, if not auto type, if not just leave it white
            try:
                c.append(pitch_colors[pitch.tagged_type])
            except:
                try:
                    c.append(pitch_colors[pitch.auto_type])
                except:
                    c.append('White')
            n += 1
        
        #Move pitches so that they show up on the plot, with .25 of buffer from edges
        x = [min(max(loc, -1), 1) for loc in x]
        y = [min(max(loc, 0.25), 4.75) for loc in y]

        #Make dataframe with the lists
        df = pd.DataFrame({'x' : x, 'y' : y, 'c' : c})

        #Make scatterplot from dataframe
        plt.scatter(x = df.x, y = df.y, c = df.c, s = 225, zorder = 3, linewidths = .35, edgecolors = 'Black')
        #Annotate pitch number of at bat
        for i in range(len(x)):
            plt.annotate(l[i], (x[i], y[i]), xytext = (x[i]-.055, y[i]-.056), fontsize = 12)
        #Save figure in temporary holding spot so it can be anchored in excel sheet
        plt.tight_layout()
        plt.savefig(f'temporary_figures//{self.date}{self.top_bottom}{self.inning}{self.number}zone_tracer.png', transparent = True)
        plt.close()

        return f'temporary_figures//{self.date}{self.top_bottom}{self.inning}{self.number}zone_tracer.png'


        
