import pandas as pd
from pitch import Pitch
import player
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon
from openpyxl.drawing.image import Image

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
        pitches = []
        for i in range(len(set(self.data['PitchofPA']))):
            pitches.append(Pitch(self.game_data, self.inning, self.number, i+1, self.top_bottom))
        return pitches
    
    def getZoneTracer(self):
        #Colors for pitch types
        pitch_colors = {'Fastball' : 'Red' , 'Four-Seam': 'Red', 'ChangeUp' : 'Blue', 'Changeup' : 'Blue','Slider' : 'Green', 'Cutter' : 'DarkGreen',
                'Curveball' : 'LimeGreen' , 'Splitter' : 'LightBlue', 'Sinker' : 'Orange', 'Knuckleball' : 'Turquoise'}
        
        #Initialize blank plot
        fig, ax = plt.subplots(figsize = (3, 6))
        ax.set_xlim(-1.5,1.5)
        ax.set_ylim(0,6)
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
            x.append(pitch.location_side)
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
        
        #Move pitches so that they show up on the plot
        x = [min(max(loc, -1.25), 1.25) for loc in x]
        y = [min(max(loc, 1), 5.5) for loc in y]

        #Make dataframe with the lists
        df = pd.DataFrame({'x' : x, 'y' : y, 'c' : c})

        #Make scatterplot from dataframe
        plt.scatter(x = df.x, y = df.y, c = df.c, s = 175, zorder = 3, linewidths = .35, edgecolors = 'Black')
        for i in range(len(x)):
            plt.annotate(l[i], (x[i], y[i]), xytext = (x[i]-.045, y[i]-.056), fontsize = 9)
        #Save figure in temporary holding spot so it can be anchored in excel sheet
        plt.savefig('temporary_figures//zone_tracer.png', transparent = True)
        plt.close()

        return Image('temporary_figures//zone_tracer.png')

    def batter(self):
        return player.Batter(list(self.data['BatterId'])[0])

    def pitcher(self):
        return player.Pitcher(list(self.data['PitcherId'])[0])
    
    def catcher(self):
        return player.Catcher(list(self.data['CatcherId'])[0])