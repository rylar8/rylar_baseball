from inning import Inning
from team import Team
from atbat import AtBat
import player
import sqlite3
import pandas as pd
import numpy as np
from openpyxl import load_workbook
from openpyxl.drawing.image import Image as PYXLImage
from openpyxl.styles import PatternFill
from openpyxl.styles import Font
from PIL import Image as PILImage
import os
import matplotlib.pyplot as plt

class Game:
    def __init__(self):
        pass

    def loadCSV(self, csv, writeData = True):
        self.data = pd.read_csv(csv)
        self.stadium = self.data.iloc[0]['Stadium']
        self.league = self.data.iloc[0]['Level']
        self.division = self.data.iloc[0]['League']
        self.trackman_id = self.data.iloc[0]['GameID']
        self.date = pd.to_datetime(self.data.iloc[0]['Date']).date()
        self.year = pd.to_datetime(self.data.iloc[0]['Date']).year
        self.time = self.data.iloc[0]['Time']
        self.home = Team(self.data.iloc[0]['HomeTeam'])
        self.away = Team(self.data.iloc[0]['AwayTeam'])
        if writeData:
            self.toDatabase()

    def loadDF(self, data, writeData = True):
        self.data = data
        self.stadium = self.data.iloc[0]['Stadium']
        self.league = self.data.iloc[0]['Level']
        self.division = self.data.iloc[0]['League']
        self.trackman_id = self.data.iloc[0]['GameID']
        self.date = pd.to_datetime(self.data.iloc[0]['Date']).date()
        self.year = pd.to_datetime(self.data.iloc[0]['Date']).year
        self.time = self.data.iloc[0]['Time']
        self.home = Team(self.data.iloc[0]['HomeTeam'])
        self.away = Team(self.data.iloc[0]['AwayTeam'])
        if writeData:
            self.toDatabase()

    def loadID(self, game_id):
        conn = sqlite3.connect('..//rylar_baseball.db')
        cur = conn.cursor()

        cur.execute('''SELECT trackman.*, 
                    games.trackman_id AS trackman_game_id, 
                    batters.batter_name AS batter_name, batters.trackman_id AS batter_trackman_id, 
                    batter_side.side AS batter_side,
                    home_teams.team_name AS home_name, home_teams.trackman_name AS home_trackman_id,
                    away_teams.team_name AS away_name, away_teams.trackman_name AS away_trackman_id,
                    inning_split.split AS top_bottom,
                    pitchers.pitcher_name AS pitcher_name, pitchers.trackman_id AS pitcher_trackman_id,
                    pitcher_side.side AS pitcher_side,
                    catchers.catcher_name AS catcher_name, catchers.trackman_id AS catcher_trackman_id,
                    catcher_side.side AS catcher_side,
                    leagues.league_name AS league_name, leagues.trackman_name AS league_trackman_id,
                    divisions.division_name AS division_name, divisions.trackman_name AS division_trackman_id,
                    stadiums.stadium_name AS stadium_name, stadiums.trackman_name AS stadium_trackman_id,
                    auto_pitches.auto_pitch AS auto_pitch_type,
                    tagged_pitches.tagged_pitch AS tagged_pitch_type,
                    calls.call AS pitch_call,
                    hits.hit AS hit_type,
                    results.result AS result,
                    batter_teams.trackman_name AS batter_team_trackman_id,
                    pitcher_teams.trackman_name AS pitcher_team_trackman_id,
                    catcher_teams.trackman_name AS catcher_team_trackman_id,
                    k_or_bb.k_or_bb AS k_or_bb

                    FROM trackman 

                    LEFT JOIN games ON trackman.game_id = games.game_id
                    LEFT JOIN batters ON trackman.batter_id = batters.batter_id
                    LEFT JOIN sides AS batter_side ON batters.batter_side_id = batter_side.side_id
                    LEFT JOIN teams AS home_teams ON trackman.home_id = home_teams.team_id
                    LEFT JOIN teams AS away_teams ON trackman.away_id = away_teams.team_id
                    LEFT JOIN inning_split ON trackman.top_bottom_id = inning_split.split_id
                    LEFT JOIN pitchers ON trackman.pitcher_id = pitchers.pitcher_id
                    LEFT JOIN sides AS pitcher_side ON pitchers.pitcher_side_id = pitcher_side.side_id
                    LEFT JOIN catchers ON trackman.catcher_id = catchers.catcher_id
                    LEFT JOIN sides AS catcher_side ON catchers.catcher_side_id = catcher_side.side_id
                    LEFT JOIN leagues ON trackman.league_id = leagues.league_id
                    LEFT JOIN divisions ON trackman.division_id = divisions.division_id
                    LEFT JOIN stadiums ON games.stadium_id = stadiums.stadium_id
                    LEFT JOIN pitches AS auto_pitches ON trackman.auto_type_id = auto_pitches.type_id
                    LEFT JOIN pitches AS tagged_pitches ON trackman.tagged_type_id = tagged_pitches.type_id
                    LEFT JOIN calls ON trackman.call_id = calls.type_id
                    LEFT JOIN hits ON trackman.hit_type_id = hits.type_id
                    LEFT JOIN results ON trackman.result_id = results.type_id
                    LEFT JOIN teams AS batter_teams ON batters.team_id = batter_teams.team_id
                    LEFT JOIN teams AS pitcher_teams ON pitchers.team_id = pitcher_teams.team_id
                    LEFT JOIN teams AS catcher_teams ON catchers.team_id = catcher_teams.team_id
                    LEFT JOIN k_or_bb ON trackman.k_or_bb_id = k_or_bb.k_or_bb_id

                    WHERE games.trackman_id = ?''', (game_id,))
        #Set column names to match raw trackman columns
        cols = ['game_id', 'PitchNo', 'Inning', 'top_bottom_id', 'PAofInning', 'PitchofPA', 'pitcher_id', 'batter_id',
                'catcher_id', 'league_id', 'division_id', 'home_id', 'away_id', 'Outs', 'Balls', 'Strikes',
                'RelSpeed', 'VertBreak', 'InducedVertBreak', 'HorzBreak', 'SpinRate', 'SpinAxis', 'Tilt', 'RelHeight', 'RelSide', 
                'Extension', 'auto_type_id', 'tagged_type_id', 'call_id', 'PlateLocHeight', 'PlateLocSide', 'ExitSpeed',
                'Angle', 'Direction', 'HitSpinRate', 'hit_type_id', 'Distance', 'HangTime', 'Bearing', 'result_id',
                'OutsOnPlay', 'RunsScored', 'ThrowSpeed', 'PopTime', 'k_or_bb_id', 'VertApprAngle', 'HorzApprAngle', 'ZoneSpeed', 'ZoneTime', 'PositionAt110X', 'PositionAt110Y',
                'PositionAt110Z', 'LastTrackedDistance', 'pfxx', 'pfxz', 'x0', 'y0', 'z0', 'vx0', 'vy0', 'vz0', 'ax0', 'ay0', 'az0', 
                'ContactPositionX', 'ContactPositionY', 'ContactPositionZ', 'HitSpinAxis', 'GameID', 'Batter', 'BatterId',
                'BatterSide', 'home_name', 'HomeTeam', 'away_name', 'AwayTeam', 'Top/Bottom', 'Pitcher', 
                'PitcherId', 'PitcherThrows', 'Catcher', 'CatcherId', 'CatcherThrows', 'league_name', 
                'Level', 'division_name', 'League', 'stadium_name', 'Stadium', 'AutoPitchType',
                'TaggedPitchType', 'PitchCall', 'TaggedHitType', 'PlayResult', 'BatterTeam', 'PitcherTeam', 'CatcherTeam', 'KorBB']
        #Filter columns to get rid of database ids
        filt = ['GameID', 'PitchNo', 'Inning', 'Top/Bottom', 'PAofInning', 'PitchofPA', 'Pitcher',
                'PitcherId', 'PitcherThrows', 'PitcherTeam', 'Batter', 'BatterId', 'BatterSide', 'BatterTeam', 'Catcher',
                'CatcherId', 'CatcherThrows', 'CatcherTeam', 'league_name', 'Level', 'division_name', 'League',
                'home_name', 'HomeTeam', 'away_name', 'AwayTeam', 'Outs', 'Balls', 'Strikes', 'RelSpeed', 'VertBreak',
                'InducedVertBreak', 'HorzBreak', 'SpinRate', 'SpinAxis', 'Tilt', 'RelHeight', 'RelSide', 'Extension', 'AutoPitchType',
                'TaggedPitchType', 'PitchCall', 'PlateLocHeight','PlateLocSide', 'ExitSpeed', 'Angle', 'Direction',
                'HitSpinRate', 'TaggedHitType', 'Distance', 'HangTime', 'Bearing','PlayResult', 'KorBB', 'OutsOnPlay', 'RunsScored', 'ThrowSpeed',
                'PopTime', 'VertApprAngle', 'HorzApprAngle', 'ZoneSpeed', 'ZoneTime', 'PositionAt110X', 'PositionAt110Y',
                'PositionAt110Z', 'LastTrackedDistance', 'pfxx', 'pfxz', 'x0', 'y0', 'z0', 'vx0', 'vy0', 'vz0', 'ax0', 'ay0', 'az0', 
                'ContactPositionX', 'ContactPositionY', 'ContactPositionZ', 'HitSpinAxis']
        
        self.data = pd.DataFrame(cur.fetchall(), columns=cols)[filt]
        self.stadium = self.data.iloc[0]['Stadium']
        self.league = self.data.iloc[0]['Level']
        self.division = self.data.iloc[0]['League']
        self.trackman_id = self.data.iloc[0]['GameID']
        self.date = pd.to_datetime(self.data.iloc[0]['Date']).date()
        self.year = pd.to_datetime(self.data.iloc[0]['Date']).year
        self.time = self.data.iloc[0]['Time']
        self.home = Team(self.data.iloc[0]['HomeTeam'])
        self.away = Team(self.data.iloc[0]['AwayTeam'])
        conn.close()

    def innings(self, top_bottom):
        innings = []
        for i in range(len(set(self.data[self.data['Top/Bottom'] == top_bottom.capitalize()]['Inning']))):
            innings.append(Inning(self.data, i+1, top_bottom))
        return innings
    
    def batters(self):
        batter_ids = set(self.data['BatterId'])
        return [player.Batter(batter_id) for batter_id in batter_ids]

    def catchers(self):
        catcher_ids = set(self.data['CatcherId'])
        return [player.Catcher(catcher_id) for catcher_id in catcher_ids]

    def pitchers(self):
        pitcher_ids = set(self.data['PitcherId'])
        return [player.Pitcher(pitcher_id) for pitcher_id in pitcher_ids]

    def adjustZone(self, stadium_id):
        #Get a center of mass on the entire league and then adjust the points in this stadiums data so that the center of mass is the same
        pass
    
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
        plt.savefig(f'..//temporary_figures//{self.date}{self.trackman_id}{pitcher_id}movement_plot.png', transparent = True)
        plt.close()

        return f'..//temporary_figures//{self.date}{self.trackman_id}{pitcher_id}movement_plot.png'
        
    def toDatabase(self):
        conn = sqlite3.connect('..//rylar_baseball.db')
        cur = conn.cursor()
        #Add league
        try:
            #Increment league id
            cur.execute('SELECT league_id FROM leagues')
            league_id = cur.fetchall()[-1][0] + 1
            #Add new league
            cur.execute('''INSERT INTO leagues (league_id, year, trackman_name)
            VALUES (?, ?, ?);''', (league_id, self.year, self.league))
            conn.commit()
            #Get full league name
            league_name = input(f"Input new league name ({self.league}): ")
            cur.execute('UPDATE leagues SET league_name = ? WHERE league_id = ?', (league_name, league_id))
            conn.commit()
        except:
            #Get league id
            cur.execute('SELECT league_id FROM leagues WHERE trackman_name = ? AND year = ?', (self.league, self.year))
            league_id = cur.fetchone()[0]
        #Add division
        try:
            #Increment division id
            cur.execute('SELECT division_id FROM divisions')
            division_id = cur.fetchall()[-1][0] + 1
            #Add new division
            cur.execute('''INSERT INTO divisions (division_id, league_id, year, trackman_name)
            VALUES (?, ?, ?, ?);''', (division_id, league_id, self.year, self.division))
            conn.commit()
            #Get full division name
            division_name = input(f"Input new division name ({self.division}): ")
            cur.execute('UPDATE divisions SET division_name = ? WHERE division_id = ?', (division_name, division_id))
            conn.commit()
        except:
            #Get division id
            cur.execute('SELECT division_id FROM divisions WHERE trackman_name = ? AND year = ?', (self.division, self.year))
            division_id = cur.fetchone()[0]
        #Add home team
        try:
            cur.execute('INSERT INTO teams (trackman_name, division_id, league_id, year) VALUES (?, ?, ?, ?)', 
                        (self.home.trackman_id, division_id, league_id, self.year))
            conn.commit()
            #Get full team name
            home_name = input(f"Input new team name ({self.home.trackman_id}): ")
            cur.execute('UPDATE teams SET team_name = ? WHERE trackman_name = ?', (home_name, self.home.trackman_id))
            conn.commit()
        except:
            pass
        #Add away team
        try:
            cur.execute('INSERT INTO teams (trackman_name, division_id, league_id, year) VALUES (?, ?, ?, ?)', 
                    (self.away.trackman_id, division_id, league_id, self.year))
            conn.commit()
            #Get full team name
            away_name = input(f"Input new team name ({self.away.trackman_id}): ")
            cur.execute('UPDATE teams SET team_name = ? WHERE trackman_name = ?', (away_name, self.away.trackman_id))
            conn.commit()
        except:
            pass
        #Add stadium
        try:
            cur.execute('INSERT INTO stadiums (trackman_name) VALUES (?)', (self.stadium,))
            conn.commit()
            #Get full stadium name
            stadium_name = input(f"Input new stadium name ({self.stadium}): ")
            cur.execute('UPDATE stadiums SET stadium_name = ? WHERE trackman_name = ?', (stadium_name, self.stadium))
            conn.commit()
        except:
            pass
        #Get stadium id
        cur.execute('SELECT stadium_id FROM stadiums WHERE trackman_name = ?', (self.stadium,))
        stadium_id = cur.fetchone()[0]
        #Get home id
        cur.execute('SELECT team_id FROM teams WHERE trackman_name = ? AND year = ?', (self.home.trackman_id, self.year))
        home_id = cur.fetchone()[0]
        #Get away id
        cur.execute('SELECT team_id FROM teams WHERE trackman_name = ? AND year = ?', (self.away.trackman_id, self.year))
        away_id = cur.fetchone()[0]
        try:
            #Add game
            cur.execute('''INSERT INTO games (trackman_id, date, time, stadium_id, league_id, division_id, home_id, away_id)
            VALUES (?,?,?,?,?,?,?,?)''', (self.trackman_id, str(self.date), self.time, stadium_id, league_id, division_id, home_id, away_id))
            conn.commit()
        except:
            print(f'Game already in games table: {self.away.trackman_id} at {self.home.trackman_id} on {self.date} (trackman_id = {self.trackman_id})')
        #Add batters
        for batter_id in set(self.data['BatterId'].dropna()):
            batter_name = self.data[self.data['BatterId'] == batter_id].iloc[0]['Batter']
            #Get team id
            batter_team = self.data[self.data['BatterId'] == batter_id].iloc[0]['BatterTeam']
            cur.execute('SELECT team_id FROM teams WHERE trackman_name = ? AND year = ?',
                        (batter_team, self.year))
            team_id = cur.fetchone()[0]
            #Get batter side id
            batter_side = self.data[self.data['BatterId'] == batter_id].iloc[0]['BatterSide']
            cur.execute('SELECT side_id FROM sides WHERE side = ?',
                        (batter_side,))
            batter_side_id = cur.fetchone()[0]
            batter_id = int(batter_id)
            try:
                cur.execute('''INSERT INTO batters (batter_name, team_id, trackman_id, batter_side_id)
                VALUES (?, ?, ?, ?)''', (batter_name, team_id, batter_id, batter_side_id))
                conn.commit()
            except:
                pass
        #Add pitchers
        for pitcher_id in set(self.data['PitcherId'].dropna()):
            pitcher_name = self.data[self.data['PitcherId'] == pitcher_id].iloc[0]['Pitcher']
            #Get team id
            pitcher_team = self.data[self.data['PitcherId'] == pitcher_id].iloc[0]['PitcherTeam']
            cur.execute('SELECT team_id FROM teams WHERE trackman_name = ? AND year = ?',
                        (pitcher_team, self.year))
            team_id = cur.fetchone()[0]
            #Get pitcher side id
            pitcher_side = self.data[self.data['PitcherId'] == pitcher_id].iloc[0]['PitcherThrows']
            cur.execute('SELECT side_id FROM sides WHERE side = ?',
                        (pitcher_side,))
            pitcher_side_id = cur.fetchone()[0]
            pitcher_id = int(pitcher_id)
            try:
                cur.execute('''INSERT INTO pitchers (pitcher_name, team_id, trackman_id, pitcher_side_id)
                VALUES (?, ?, ?, ?)''', (pitcher_name, team_id, pitcher_id, pitcher_side_id))
                conn.commit()
            except:
                pass

        #Add catchers
        for catcher_id in set(self.data['CatcherId'].dropna()):
            catcher_name = self.data[self.data['CatcherId'] == catcher_id].iloc[0]['Catcher']
            #Get team id
            catcher_team = self.data[self.data['CatcherId'] == catcher_id].iloc[0]['PitcherTeam']
            cur.execute('SELECT team_id FROM teams WHERE trackman_name = ? AND year = ?',
                        (catcher_team, self.year))
            team_id = cur.fetchone()[0]
            #Get catcher side id
            catcher_side = self.data[self.data['CatcherId'] == catcher_id].iloc[0]['CatcherThrows']
            cur.execute('SELECT side_id FROM sides WHERE side = ?',
                        (catcher_side,))
            catcher_side_id = cur.fetchone()[0]
            catcher_id = int(catcher_id)
            try:
                cur.execute('''INSERT INTO catchers (catcher_name, team_id, trackman_id, catcher_side_id)
                VALUES (?, ?, ?, ?)''', (catcher_name, team_id, catcher_id, catcher_side_id))
                conn.commit()
            except:
                pass
        #Write Trackman data
        #Get game id
        cur.execute('SELECT game_id FROM games WHERE trackman_id = ?', (self.trackman_id,))
        game_id = cur.fetchone()[0]

        pitches = []
        for pitch in self.data.itertuples():
            pitch_num = pitch.PitchNo
            inning = pitch.Inning
            #Get top bottom id
            cur.execute('SELECT split_id FROM inning_split WHERE split = ?', (pitch._16,))
            top_bottom_id = cur.fetchone()[0]
            pa_of_inning = pitch.PAofInning
            pitch_of_pa = pitch.PitchofPA
            #Get pitcher id unless id does not exist, replace with example player
            try:
                cur.execute('SELECT pitcher_id FROM pitchers WHERE trackman_id = ?', (int(pitch.PitcherId),))
                pitcher_id = cur.fetchone()[0]
            except ValueError:
                pitcher_id = 0
            #Get batter id unless id does not exist, replace with example player
            try:
                cur.execute('SELECT batter_id FROM batters WHERE trackman_id = ?', (int(pitch.BatterId),))
                batter_id = cur.fetchone()[0]
            except ValueError:
                batter_id = 0
            #Get catcher id unless id does not exist, replace with example player
            try:
                cur.execute('SELECT catcher_id FROM catchers WHERE trackman_id = ?', (int(pitch.CatcherId),))
                catcher_id = cur.fetchone()[0]
            except ValueError:
                catcher_id = 0
            #Get league id
            cur.execute('SELECT league_id FROM leagues WHERE trackman_name = ? AND year = ?', (self.league, self.year))
            league_id = cur.fetchone()[0]
            #Get division id
            cur.execute('SELECT division_id FROM divisions WHERE trackman_name = ? AND year = ?', (self.division, self.year))
            division_id = cur.fetchone()[0]
            #Get home id
            cur.execute('SELECT team_id FROM teams WHERE trackman_name = ? AND year = ?', (self.home.trackman_id, self.year))
            home_id = cur.fetchone()[0]
            #Get away id
            cur.execute('SELECT team_id FROM teams WHERE trackman_name = ? AND year = ?', (self.away.trackman_id, self.year))
            away_id = cur.fetchone()[0]
            outs = pitch.Outs
            balls = pitch.Balls
            strikes = pitch.Strikes
            velocity = pitch.RelSpeed
            vertical = pitch.VertBreak
            induced = pitch.InducedVertBreak
            horizontal = pitch.HorzBreak
            spin = pitch.SpinRate
            axis = pitch.SpinAxis
            tilt = pitch.Tilt
            release_height = pitch.RelHeight
            release_side = pitch.RelSide
            release_extension = pitch.Extension
            #Get auto type id unless auto type is blank, set to null id
            try:
                cur.execute('SELECT type_id FROM pitches WHERE auto_pitch = ?', (pitch.AutoPitchType,))
                auto_type_id = cur.fetchone()[0]
            except TypeError:
                auto_type_id = 9
            #Get tagged type id unless tagged type is blank, set to null id
            try:
                cur.execute('SELECT type_id FROM pitches WHERE tagged_pitch = ?', (pitch.TaggedPitchType,))
                tagged_type_id = cur.fetchone()[0]
            except TypeError:
                tagged_type_id = 9
            #Get call id
            cur.execute('SELECT type_id FROM calls WHERE call = ?', (pitch.PitchCall,))
            call_id = cur.fetchone()[0]
            location_height = pitch.PlateLocHeight
            location_side = pitch.PlateLocSide
            exit_velocity = pitch.ExitSpeed
            launch_angle = pitch.Angle
            hit_direction = pitch.Direction
            hit_spin = pitch.HitSpinRate
            #Get hit type id
            cur.execute('SELECT type_id FROM hits WHERE hit = ?', (pitch.TaggedHitType,))
            hit_type_id = cur.fetchone()[0]
            distance = pitch.Distance
            hang_time = pitch.HangTime
            hit_bearing = pitch.Bearing
            #Get result id
            cur.execute('SELECT type_id FROM results WHERE result = ?', (pitch.PlayResult,))
            result_id = cur.fetchone()[0]
            outs_made = pitch.OutsOnPlay
            runs_scored = pitch.RunsScored
            catcher_velocity = pitch.ThrowSpeed
            catcher_pop = pitch.PopTime
            #Get k_or_bb id
            cur.execute('SELECT k_or_bb_id FROM k_or_bb WHERE k_or_bb = ?', (pitch.KorBB,))
            k_or_bb_id = cur.fetchone()[0]
            vert_approach_angle = pitch.VertApprAngle
            horz_approach_angle = pitch.HorzApprAngle
            zone_speed = pitch.ZoneSpeed
            zone_time = pitch.ZoneTime
            pos_at_110x = pitch.PositionAt110X
            pos_at_110y = pitch.PositionAt110Y
            pos_at_110z = pitch.PositionAt110Z
            last_tracked_distance = pitch.LastTrackedDistance
            last40_horz_break = pitch.pfxx
            last40_vert_break = pitch.pfxz
            horz_loc_50 = pitch.x0
            from_home_loc_50 = pitch.y0
            vert_loc_50 = pitch.z0
            horz_velo_50 = pitch.vx0
            from_home_velo_50 = pitch.vy0
            vert_velo_50 = pitch.vz0
            horz_acc_50 = pitch.ax0
            from_home_acc_50 = pitch.ay0
            vert_acc_50 = pitch.az0
            con_pos_x = pitch.ContactPositionX
            con_pos_y = pitch.ContactPositionY
            con_pos_z = pitch.ContactPositionZ
            hit_spin_axis = pitch.HitSpinAxis

            pitches.append((game_id, pitch_num, inning, top_bottom_id, pa_of_inning, pitch_of_pa,
            pitcher_id, batter_id, catcher_id, league_id, division_id, home_id, away_id, outs, balls, strikes, velocity, 
            vertical, induced, horizontal, spin, axis, tilt, release_height, release_side, release_extension, auto_type_id,
            tagged_type_id, call_id, location_height, location_side, exit_velocity, launch_angle, hit_direction, hit_spin, 
            hit_type_id, distance, hang_time, hit_bearing, result_id, outs_made, runs_scored, catcher_velocity, catcher_pop,
            k_or_bb_id, vert_approach_angle, horz_approach_angle, zone_speed, zone_time, pos_at_110x, pos_at_110y, pos_at_110z,
            last_tracked_distance, last40_horz_break, last40_vert_break, horz_loc_50, from_home_loc_50, vert_loc_50, horz_velo_50,
            from_home_velo_50, vert_velo_50, horz_acc_50, from_home_acc_50, vert_acc_50, con_pos_x, con_pos_y, con_pos_z, hit_spin_axis))

        try:
            cur.executemany('''INSERT INTO trackman (game_id, pitch_num, inning, top_bottom_id, pa_of_inning, pitch_of_pa,
            pitcher_id, batter_id, catcher_id, league_id, division_id, home_id, away_id, outs, balls, strikes, velocity, 
            vertical, induced, horizontal, spin, axis, tilt, release_height, release_side, release_extension, auto_type_id,
            tagged_type_id, call_id, location_height, location_side, exit_velocity, launch_angle, hit_direction, hit_spin, 
            hit_type_id, distance, hang_time, hit_bearing, result_id, outs_made, runs_scored, catcher_velocity, catcher_pop, k_or_bb_id,
            vert_approach_angle, horz_approach_angle, zone_speed, zone_time, pos_at_110x, pos_at_110y, pos_at_110z, last_tracked_distance,
            last_40_horz_break_batter_view, last_40_vert_break_batter_view, horz_loc_50, home_loc_50, vert_loc_50,
            horz_velo_50, home_velo_50, vert_velo_50, horz_acc_50, home_acc_50, vert_acc_50, contact_pos_x,
            contact_pos_y, contact_pos_z, hit_spin_axis)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', pitches)
            conn.commit()
        except:
            print(f'Data already in trackman table: {self.away.trackman_id} at {self.home.trackman_id} on {self.date} (game_id = {game_id}, trackman_id = {self.trackman_id})')
        conn.close()

    def writeHitterReports(self, team_id):
        temp_path = '..//templates//postgame_hitter_template.xlsx'
        #Get batters from data
        batters = set(self.data[self.data['BatterTeam'] == team_id]['BatterId'])

        #Define dictionaries to be used later
        pitches = {'Fastball' : 'FB' , 'Four-Seam': 'FB', 'ChangeUp' : 'CH', 'Changeup' : 'CH','Slider' : 'SL', 'Cutter' : 'CUT',
                'Curveball' : 'CB' , 'Splitter' : 'SP', 'Sinker' : '2FB', 'Knuckleball' : 'KN'}
        pitch_colors = {'Fastball': '00FF0000', 'Four-Seam': '00FF0000', 'ChangeUp': '0000BFFF', 'Changeup': '0000BFFF', 'Slider': '0000FA9A',
                'Cutter': '007CFC00','Curveball': '0032CD32', 'Splitter': '00ADD8E6', 'Sinker': '00FF7F50', 'Knuckleball': '0048D1CC'}
        hits = {'Popup' : 'Popup', 'LineDrive' : 'Line Drive', 'GroundBall' : 'Ground Ball', 'FlyBall' : 'Fly Ball', 'Bunt' : 'Bunt'}
        #Simplify pitch call to fit on sheet easier
        results = {'StrikeCalled' : 'Strike', 'StrikeSwinging' : 'Strike', 'FoulBall' : 'Foul', 'InPlay' : 'In Play',
                                'BallCalled' : 'Ball', 'HitByPitch' : 'HBP', 'BallinDirt' : 'Ball', 'Undefined' : '', 
                                'BallIntentional' : 'Ball'}
        #Use pitch call to decide if batter swung or not
        takes = ['StrikeCalled', 'BallCalled', 'HitByPitch', 'BallinDirt', 'BallIntentional']
        swings = ['InPlay', 'StrikeSwinging', 'FoulBall']

        #Write a new report for each batter id
        for batter_id in batters:
            #Initialize batter object
            batter = player.Batter(batter_id)
            #Initialize template
            wb = load_workbook(temp_path)
            ws = wb.active

            #Get a tuple of unique at bats for batter and sort in order
            at_bats = sorted(set(self.data[self.data['BatterId'] == batter_id][['PAofInning', 'Inning', 'Top/Bottom']].apply(lambda row : (row['Inning'], row['PAofInning'], row['Top/Bottom']), axis=1)), key= lambda tup: (tup[0], tup[1]))
        
            #Fill an at bat on the sheet for each at bat, use i to control what cell to write in
            i = 0
            for ab in at_bats:
                #Initialize at_bat object
                ws[f'J{i+10}'] = inning = ab[0]
                pa_of_inning = ab[1]
                top_bottom = ab[2].lower()
                at_bat = AtBat(self.data, inning, pa_of_inning, top_bottom)
                
                ws[f'J{i+11}'] = at_bat.outs
                ws[f'J{i+12}'] = 'Coming Soon' #Home
                ws[f'J{i+13}'] = 'Coming Soon' #Away
                ws[f'J{i+14}'] = 'Coming Soon' #Runners

                #Initialize pitcher object
                pitcher = at_bat.pitcher()
                pitcher_id = pitcher.trackman_id

                ws[f'J{i+16}'] = pitcher.name.split(',')[0]
                ws[f'J{i+17}'] = pitcher.side

                ws['C3'] = ws['C53'] = batter.name #Player name
                ws['C5'] = ws['C55'] = self.date #Date
                ws['C7'] = ws['C57'] = f'v {pitcher.team_name.split()[-1]}' #Opponent

                #Try using the tagged fastball data, if an error occurs use the auto pitch type data
                #(embedded try/except statement because two different trackman versions exist)
                try:
                    pitcher_fastballs = self.data[((self.data['TaggedPitchType'] == 'Fastball') | (self.data['TaggedPitchType'] == 'Sinker')) & (self.data['PitcherId'] == pitcher_id)]
                except:
                    try:
                        pitcher_fastballs = self.data[((self.data['AutoPitchType'] == 'Fastball') | (self.data['AutoPitchType'] == 'Sinker')) & (self.data['PitcherId'] == pitcher_id)]
                    except:
                        pitcher_fastballs = self.data[((self.data['AutoPitchType'] == 'Four-Seam') | (self.data['AutoPitchType'] == 'Sinker')) & (self.data['PitcherId'] == pitcher_id)]
                #Get the mean and std pitcher fb velo
                mean_fb = round(pitcher_fastballs['RelSpeed'].dropna().mean())
                #If only 1 fastball is thrown then std throws and error, replace std with 0
                try:
                    std_fb = round(pitcher_fastballs['RelSpeed'].dropna().std())
                except:
                    std_fb = 0
                    ws[f'J{i+18}'] = f'{mean_fb-std_fb}-{mean_fb+std_fb} MPH'
                try:
                    #Get a list of the different pitches thrown, drop na
                    ws[f'J{i+19}'] = ','.join(set(self.data[self.data['PitcherId'] == pitcher_id]['TaggedPitchType'].dropna().map(pitches)))
                except:
                    ws[f'J{i+19}'] = ','.join(set(self.data[self.data['PitcherId'] == pitcher_id]['AutoPitchType'].dropna().map(pitches)))
                   
                #Try to get exit velo on last pitch of at bat, if an error occurs leave it blank
                try:
                    if not np.isnan(at_bat.pitches()[-1].exit_velocity):
                        ws[f'M{i+10}'] = f'{round(at_bat.pitches()[-1].exit_velocity, 2)} MPH'
                    else:
                        ws[f'M{i+10}'] = ''
                except:
                     ws[f'M{i+10}'] = ''
                #Try to get launch angle on last pitch of at bat, if an error occurs leave it blank
                try:
                     if not np.isnan(at_bat.pitches()[-1].launch_angle):
                        ws[f'M{i+12}']  = f'{round(at_bat.pitches()[-1].launch_angle, 2)}{chr(176)}'
                     else:
                        ws[f'M{i+12}'] = ''
                except:
                     ws[f'M{i+12}']  = ''
                #Try to get hit type on last pitch of at bat, if an error occurs leave it blank
                try:
                     ws[f'M{i+14}']  = hits[at_bat.pitches()[-1].hit_type]
                except:
                     ws[f'M{i+14}']  = ''
                #Try to get result on last pitch of at bat, if an error occurs leave it blank
                try:
                    if at_bat.pitches()[-1].result != 'Undefined':
                        ws[f'M{i+16}']  = at_bat.pitches()[-1].result
                    elif at_bat.pitches()[-1].k_or_bb != 'Undefined':
                        ws[f'M{i+16}']  = at_bat.pitches()[-1].k_or_bb
                    elif at_bat.pitches()[-1].call == 'HitByPitch':
                        ws[f'M{i+16}']  = 'Hit By Pitch'
                    else:
                        ws[f'M{i+16}'] = ''
                except:
                     ws[f'M{i+16}']  = ''
                ws[f'M{i+18}']  = 'Coming Soon' #QAB
                
                #Fill a pitch slot on the sheet for each pitch, use i and j to control what cell to write in
                #Do not exceed 8 pitches in the pitch/choice/result columns
                j = 0
                for pitch in at_bat.pitches()[:10]:
                    #Try tagged pitch type, if not use auto pitch type, if error leave blank
                    try:
                        ws[f'F{i+j+10}'] = pitches[pitch.tagged_type]
                        ws[f'F{i+j+10}'].fill = PatternFill('solid', fgColor=pitch_colors[pitch.tagged_type])
                    except:
                        try:
                            ws[f'F{i+j+10}'] = pitches[pitch.auto_type]
                            ws[f'F{i+j+10}'].fill = PatternFill('solid', fgColor=pitch_colors[pitch.auto_type])
                        except:
                            ws[f'F{i+j+10}'] = ''
                            ws[f'F{i+j+10}'].fill = PatternFill('solid', fgColor='00000000')
                    
                    if pitch.call in takes:
                        ws[f'G{i+j+10}'] = 'Take'
                    elif pitch.call in swings:
                        ws[f'G{i+j+10}'] = 'Swing'
                    else:
                        ws[f'G{i+j+10}'] = ''
        
                    ws[f'H{i+j+10}'] = results[pitch.call]
                    j+=1

                #Get image from at_bat object
                img_path = at_bat.zoneTracer(view='catcher')

                #Resize the image to better fit excel sheet using PIL library
                img = PILImage.open(img_path)
                img_resized = img.resize((int(img.width*.83), int(img.height*.55)))
                img_resized.save(img_path, 'PNG')
                img.close()

                #Add image to at_bat
                ws.add_image(PYXLImage(img_path), f'C{i+10}')

                #Jump to next at bat slot
                i += 11
                #Skip the second page header
                if i == 44:
                    i = 50
            #Create folders if they do not exist
            try:
                os.mkdir(f'..//postgame_hitter_reports//{batter.team_trackman_id}')
            except:
                pass
            try:
                os.mkdir(f'..//postgame_hitter_reports//{batter.team_trackman_id}//{self.date}')
            except:
                pass
            #Save file to folder with player name
            wb.save(f'..//postgame_hitter_reports//{batter.team_trackman_id}//{self.date}//{batter.name}.xlsx')
            wb.close()
        
        #After writing all reports remove all of the temporary figures
        for filename in os.listdir('..//temporary_figures'):
            file_path = os.path.join('..//temporary_figures//', filename)
            os.remove(file_path)

    def writePitcherReports(self, team_id):
        conn = sqlite3.connect('..//rylar_baseball.db')
        cur = conn.cursor()

        temp_path = '..//templates//postgame_pitcher_template.xlsx'
        #Get pitchers from data
        pitchers = set(self.data[self.data['PitcherTeam'] == team_id]['PitcherId'])

        #Define dictionaries to be used later
        pitches = {'Fastball' : 'FB' , 'Four-Seam': 'FB', 'ChangeUp' : 'CH', 'Changeup' : 'CH','Slider' : 'SL', 'Cutter' : 'CUT',
                'Curveball' : 'CB' , 'Splitter' : 'SP', 'Sinker' : '2FB', 'Knuckleball' : 'KN'}
        pitch_colors = {'FB': '00FF0000', 'FB': '00FF0000', 'CH': '0000BFFF', 'CH': '0000BFFF', 'SL': '0000FA9A',
                    'CUT': '007CFC00','CB': '0032CD32', 'SP': '00ADD8E6', '2FB': '00FF7F50', 'KN': '0048D1CC'}
        results = {'StrikeCalled' : 'Strike', 'StrikeSwinging' : 'Strike', 'FoulBall' : 'Foul', 'InPlay' : 'In Play',
                        'BallCalled' : 'Ball', 'HitByPitch' : 'HBP', 'BallinDirt' : 'Ball', 'Undefined' : '', 
                        'BallIntentional' : 'Ball'}

        #Write a new report for each pitcher id
        for pitcher_id in pitchers:
            #Initialize pitcher object
            pitcher = player.Pitcher(pitcher_id)
            #Initialize template
            wb = load_workbook(temp_path)
            ws = wb.active
            
            #Get pitcher's overall game data
            overall_data = self.data[self.data['PitcherId'] == pitcher_id]

            #Get opponent team name from database
            cur.execute('SELECT team_name FROM teams WHERE trackman_name = ?', (overall_data.BatterTeam.iloc[0],))
            opponent = cur.fetchone()[0]

            ws['C3'] = ws['C84'] = pitcher.name #Player name
            ws['C5'] = ws['C86'] = self.date #Date
            ws['C7'] = ws['C88'] = f'v {opponent.split()[-1]}' #Opponent
            
            #Try using the tagged pitch type data, if an error occurs use the auto pitch type data
            #(embedded try/except statement because two different trackman versions exist in league data)

            #Get a set of the pitch types
            try:
                ovr_pitch_types = set(overall_data['TaggedPitchType'].dropna())
            except:
                ovr_pitch_types = set(overall_data['AutoPitchType'].dropna())
            
            #To protect against there being no pitch tagging data, if there is only 1 tagged type (likely Undefined), then default to auto
            if len(ovr_pitch_types) <= 1:
                ovr_pitch_types = set(overall_data['AutoPitchType'].dropna())

            #Sort the pitches by usage
            pitch_counts = overall_data['TaggedPitchType'].value_counts()
            sorted_pitches = sorted(ovr_pitch_types, key=lambda pitch_type : pitch_counts.loc[pitch_type], reverse=True)
            
            #Fill a row for each pitch type, using i to control the row
            i = 0
            for pitch_type in sorted_pitches:
                #Get pitch type data
                try:
                    pitch_data = overall_data[overall_data['TaggedPitchType'] == pitch_type]
                except:
                    pitch_data = overall_data[overall_data['AutoPitchType'] == pitch_type]
    
                ws[f'F{i+10}'] = pitches[pitch_type] #Pitch type
                ws[f'F{i+10}'].fill = PatternFill('solid', fgColor=pitch_colors[pitches[pitch_type]])
                ws[f'G{i+10}'] = round(pitch_data['RelSpeed'].dropna().max(), 1) #Max velo
                ws[f'H{i+10}'] = round(pitch_data['RelSpeed'].dropna().mean(), 1) #Mean velo
                ws[f'I{i+10}'] = round(pitch_data['InducedVertBreak'].dropna().mean(), 1) #Vert break
                ws[f'J{i+10}'] = round(pitch_data['HorzBreak'].dropna().mean(), 1) #Horz break
                ws[f'K{i+10}'] = f'{round(len(pitch_data) / len(overall_data) * 100, 1)}%' #Usage
        
                #Get strike rate
                calls = pitch_data['PitchCall'].map(results)
                ws[f'L{i+10}'] = f'{round(len(calls[(calls == "Strike") | (calls == "Foul") | (calls == "In Play")]) / len(pitch_data) * 100, 1)}%'
                
                #Get hard hit rate, leave blank if no balls in play
                if len(pitch_data[pitch_data["PitchCall"] == "InPlay"]) == 0:
                    ws[f'M{i+10}'] = '-'
                    ws[f'M{i+10}'].font = Font(bold=True, italic=True, size=20)
                else:
                    ws[f'M{i+10}'] = f'{round(len(pitch_data[(pitch_data["ExitSpeed"] >= 95) & (pitch_data["PitchCall"] == "InPlay")]) / len(pitch_data[pitch_data["PitchCall"] == "InPlay"]) * 100, 1)}%'

                #Get chase rate, leave blank if no balls thrown
                #Get balls based on universal strike zone
                balls = pitch_data[(pitch_data['PlateLocSide'] < -0.7508) | (pitch_data['PlateLocSide'] > 0.7508) | (pitch_data['PlateLocHeight'] < 1.5942) | (pitch_data['PlateLocHeight'] > 3.6033)]
                chase = balls[(balls['PitchCall'] == 'FoulBall') | (balls['PitchCall'] == 'InPlay') | (balls['PitchCall'] == 'StrikeSwinging')]
                if len(balls) == 0:
                    ws[f'N{i+10}'] = '-'
                    ws[f'N{i+10}'].font = Font(bold=True, italic=True, size=20)
                else:
                    ws[f'N{i+10}'] = f'{round(len(chase) / len(balls) * 100, 1)}%'

                #Get whiff rate, leave blank if no swings
                swings = pitch_data[(pitch_data['PitchCall'] == 'FoulBall') | (pitch_data['PitchCall'] == 'InPlay') | (pitch_data['PitchCall'] == 'StrikeSwinging')]
                whiffs = swings[swings['PitchCall'] == 'StrikeSwinging']
                if len(swings) == 0:
                    ws[f'O{i+10}'] = '-'
                    ws[f'O{i+10}'].font = Font(bold=True, italic=True, size=20)
                else:
                    ws[f'O{i+10}'] = f'{round(len(whiffs) / len(swings) * 100, 1)}%'
                
                #Advance to next pitch, if pitcher threw 6+ pitch types then skip the least used pitches
                i += 2
                if i == 10:
                    break

            #Fill overall data

            #Get strike rate
            calls = overall_data['PitchCall'].map(results)
            ws[f'L{20}'] = f'{round(len(calls[(calls == "Strike") | (calls == "Foul") | (calls == "In Play")]) / len(overall_data) * 100, 1)}%'
            
            #Get hard hit rate, leave blank if no balls in play
            if len(overall_data[overall_data["PitchCall"] == "InPlay"]) == 0:
                ws[f'M{20}'] = '-'
                ws[f'M{20}'].font = Font(bold=True, italic=True, size=20)
            else:
                ws[f'M{20}'] = f'{round(len(overall_data[(overall_data["ExitSpeed"] >= 95) & (overall_data["PitchCall"] == "InPlay")]) / len(overall_data[overall_data["PitchCall"] == "InPlay"]) * 100, 1)}%'

            #Get chase rate, leave blank if no balls thrown
            #Get balls based on universal strike zone
            balls = overall_data[(overall_data['PlateLocSide'] < -0.7508) | (overall_data['PlateLocSide'] > 0.7508) | (overall_data['PlateLocHeight'] < 1.5942) | (overall_data['PlateLocHeight'] > 3.6033)]
            chase = balls[(balls['PitchCall'] == 'FoulBall') | (balls['PitchCall'] == 'InPlay') | (balls['PitchCall'] == 'StrikeSwinging')]
            if len(balls) == 0:
                ws[f'N{20}'] = '-'
                ws[f'N{20}'].font = Font(bold=True, italic=True, size=20)
            else:
                ws[f'N{20}'] = f'{round(len(chase) / len(balls) * 100, 1)}%'

            #Get whiff rate, leave blank if no swings
            swings = overall_data[(overall_data['PitchCall'] == 'FoulBall') | (overall_data['PitchCall'] == 'InPlay') | (overall_data['PitchCall'] == 'StrikeSwinging')]
            whiffs = swings[swings['PitchCall'] == 'StrikeSwinging']
            if len(swings) == 0:
                ws[f'O{20}'] = '-'
                ws[f'O{20}'].font = Font(bold=True, italic=True, size=20)
            else:
                ws[f'O{20}'] = f'{round(len(whiffs) / len(swings) * 100, 1)}%'

            ws[f'G{22}'] = self.pitcherStatline(pitcher_id)

            #Get image from game method
            img_path = self.movementPlot(pitcher_id)

            #Resize the image to better fit excel sheet using PIL library
            img = PILImage.open(img_path)
            img_resized = img.resize((int(img.width*.83), int(img.height*.96)))
            img_resized.save(img_path, 'PNG')
            img.close()

            #Add image to overall
            ws.add_image(PYXLImage(img_path), f'C{10}')

            #Get a tuple of unique innings for pitcher and sort in order
            innings = sorted(set(self.data[self.data['PitcherId'] == pitcher_id][['Inning', 'Top/Bottom']].apply(lambda row : (row['Inning'], row['Top/Bottom']), axis=1)), key= lambda tup: (tup[0], tup[1]))

            #Fill an inning on the sheet for each inning pitched, use j to control what cell to write in
            j = 15
            for inn in innings:
                #Initialize inning object
                inn_num = inn[0]
                top_bottom = inn[1].lower()
                inning = Inning(self.data, inn_num, top_bottom)

                #Get pitcher's inning data
                inning_data = inning.data[inning.data['PitcherId'] == pitcher_id]
                
                #Try using the tagged pitch type data, if an error occurs use the auto pitch type data
                #(embedded try/except statement because two different trackman versions exist in league data)

                #Get a set of the pitch types
                try:
                    inn_pitch_types = set(inning_data['TaggedPitchType'].dropna())
                except:
                    inn_pitch_types = set(inning_data['AutoPitchType'].dropna())
                
                #To protect against there being no pitch tagging data, if there is only 1 tagged type (likely Undefined), then default to auto
                if len(inn_pitch_types) <= 1:
                    inn_pitch_types = set(inning_data['AutoPitchType'].dropna())

                #Sort the pitches by usage
                pitch_counts = inning_data['TaggedPitchType'].value_counts()
                sorted_pitches = sorted(inn_pitch_types, key=lambda pitch_type : pitch_counts.loc[pitch_type], reverse=True)

                #Fill a row for each pitch type, using i to control the row
                i = 0
                for pitch_type in sorted_pitches:
                    #Get pitch type data
                    try:
                        pitch_data = inning_data[inning_data['TaggedPitchType'] == pitch_type]
                    except:
                        pitch_data = inning_data[inning_data['AutoPitchType'] == pitch_type]
        
                    ws[f'F{i+10+j}'] = pitches[pitch_type] #Pitch type
                    ws[f'F{i+10+j}'].fill = PatternFill('solid', fgColor=pitch_colors[pitches[pitch_type]])
                    ws[f'G{i+10+j}'] = round(pitch_data['RelSpeed'].dropna().max(), 1) #Max velo
                    ws[f'H{i+10+j}'] = round(pitch_data['RelSpeed'].dropna().mean(), 1) #Mean velo
                    ws[f'I{i+10+j}'] = round(pitch_data['InducedVertBreak'].dropna().mean(), 1) #Vert break
                    ws[f'J{i+10+j}'] = round(pitch_data['HorzBreak'].dropna().mean(), 1) #Horz break
                    ws[f'K{i+10+j}'] = f'{round(len(pitch_data) / len(overall_data) * 100, 1)}%' #Usage
            
                    #Get strike rate
                    calls = pitch_data['PitchCall'].map(results)
                    ws[f'L{i+10+j}'] = f'{round(len(calls[(calls == "Strike") | (calls == "Foul") | (calls == "In Play")]) / len(pitch_data) * 100, 1)}%'
                    
                    #Get hard hit rate, leave blank if no balls in play
                    if len(pitch_data[pitch_data["PitchCall"] == "InPlay"]) == 0:
                        ws[f'M{i+10+j}'] = '-'
                        ws[f'M{i+10+j}'].font = Font(bold=True, italic=True, size=20)
                    else:
                        ws[f'M{i+10+j}'] = f'{round(len(pitch_data[(pitch_data["ExitSpeed"] >= 95) & (pitch_data["PitchCall"] == "InPlay")]) / len(pitch_data[pitch_data["PitchCall"] == "InPlay"]) * 100, 1)}%'

                    #Get chase rate, leave blank if no balls thrown
                    #Get balls based on universal strike zone
                    balls = pitch_data[(pitch_data['PlateLocSide'] < -0.7508) | (pitch_data['PlateLocSide'] > 0.7508) | (pitch_data['PlateLocHeight'] < 1.5942) | (pitch_data['PlateLocHeight'] > 3.6033)]
                    chase = balls[(balls['PitchCall'] == 'FoulBall') | (balls['PitchCall'] == 'InPlay') | (balls['PitchCall'] == 'StrikeSwinging')]
                    if len(balls) == 0:
                        ws[f'N{i+10+j}'] = '-'
                        ws[f'N{i+10+j}'].font = Font(bold=True, italic=True, size=20)
                    else:
                        ws[f'N{i+10+j}'] = f'{round(len(chase) / len(balls) * 100, 1)}%'

                    #Get whiff rate, leave blank if no swings
                    swings = pitch_data[(pitch_data['PitchCall'] == 'FoulBall') | (pitch_data['PitchCall'] == 'InPlay') | (pitch_data['PitchCall'] == 'StrikeSwinging')]
                    whiffs = swings[swings['PitchCall'] == 'StrikeSwinging']
                    if len(swings) == 0:
                        ws[f'O{i+10+j}'] = '-'
                        ws[f'O{i+10+j}'].font = Font(bold=True, italic=True, size=20)
                    else:
                        ws[f'O{i+10+j}'] = f'{round(len(whiffs) / len(swings) * 100, 1)}%'
                    
                    #Advance to next pitch, if pitcher threw 6+ pitch types then skip the least used pitches
                    i += 2
                    if i == 10:
                        break

                #Fill overall data

                #Get strike rate
                calls = inning_data['PitchCall'].map(results)
                ws[f'L{20+j}'] = f'{round(len(calls[(calls == "Strike") | (calls == "Foul") | (calls == "In Play")]) / len(inning_data) * 100, 1)}%'
                
                #Get hard hit rate, leave blank if no balls in play
                if len(inning_data[inning_data["PitchCall"] == "InPlay"]) == 0:
                    ws[f'M{20+j}'] = '-'
                    ws[f'M{20+j}'].font = Font(bold=True, italic=True, size=20)
                else:
                    ws[f'M{20+j}'] = f'{round(len(inning_data[(inning_data["ExitSpeed"] >= 95) & (inning_data["PitchCall"] == "InPlay")]) / len(inning_data[inning_data["PitchCall"] == "InPlay"]) * 100, 1)}%'

                #Get chase rate, leave blank if no balls thrown
                #Get balls based on universal strike zone
                balls = inning_data[(inning_data['PlateLocSide'] < -0.7508) | (inning_data['PlateLocSide'] > 0.7508) | (inning_data['PlateLocHeight'] < 1.5942) | (inning_data['PlateLocHeight'] > 3.6033)]
                chase = balls[(balls['PitchCall'] == 'FoulBall') | (balls['PitchCall'] == 'InPlay') | (balls['PitchCall'] == 'StrikeSwinging')]
                if len(balls) == 0:
                    ws[f'N{20+j}'] = '-'
                    ws[f'N{20+j}'].font = Font(bold=True, italic=True, size=20)
                else:
                    ws[f'N{20+j}'] = f'{round(len(chase) / len(balls) * 100, 1)}%'

                #Get whiff rate, leave blank if no swings
                swings = inning_data[(inning_data['PitchCall'] == 'FoulBall') | (inning_data['PitchCall'] == 'InPlay') | (inning_data['PitchCall'] == 'StrikeSwinging')]
                whiffs = swings[swings['PitchCall'] == 'StrikeSwinging']
                if len(swings) == 0:
                    ws[f'O{20+j}'] = '-'
                    ws[f'O{20+j}'].font = Font(bold=True, italic=True, size=20)
                else:
                    ws[f'O{20+j}'] = f'{round(len(whiffs) / len(swings) * 100, 1)}%'

                ws[f'G{22+j}'] = inning.pitcherStatline(pitcher_id)

                #Get image from inning method
                img_path = inning.movementPlot(pitcher_id)

                #Resize the image to better fit excel sheet using PIL library
                img = PILImage.open(img_path)
                img_resized = img.resize((int(img.width*.83), int(img.height*.96)))
                img_resized.save(img_path, 'PNG')
                img.close()

                #Add image to overall
                ws.add_image(PYXLImage(img_path), f'C{10+j}')

                j += 15

                if j == 75:
                    j = 81

             #Create folders if they do not exist
            try:
                os.mkdir(f'..//postgame_pitcher_reports//{pitcher.team_trackman_id}')
            except:
                pass
            try:
                os.mkdir(f'..//postgame_pitcher_reports//{pitcher.team_trackman_id}//{self.date}')
            except:
                pass
            #Save file to folder with player name
            wb.save(f'..//postgame_pitcher_reports//{pitcher.team_trackman_id}//{self.date}//{pitcher.name}.xlsx')
            wb.close()
        
        #After writing all reports remove all of the temporary figures
        for filename in os.listdir('..//temporary_figures'):
            file_path = os.path.join('..//temporary_figures//', filename)
            os.remove(file_path)

        conn.close()