from inning import Inning
from team import Team
from atbat import AtBat
import player
import sqlite3
import pandas as pd
from openpyxl import load_workbook
import os

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
        conn = sqlite3.connect('rylar_baseball.db')
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
                    catcher_teams.trackman_name AS catcher_team_trackman_id

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

                    WHERE games.trackman_id = ?''', (game_id,))
        #Set column names to match raw trackman columns
        cols = ['game_id', 'PitchNo', 'Inning', 'top_bottom_id', 'PAofInning', 'PitchofPA', 'pitcher_id', 'batter_id',
                'catcher_id', 'league_id', 'division_id', 'home_id', 'away_id', 'Outs', 'Balls', 'Strikes',
                'RelSpeed', 'VertBreak', 'InducedVertBreak', 'HorzBreak', 'SpinRate', 'SpinAxis', 'Tilt', 'RelHeight', 'RelSide', 
                'Extension', 'auto_type_id', 'tagged_type_id', 'call_id', 'PlateLocHeight', 'PlateLocSide', 'ExitSpeed',
                'Angle', 'Direction', 'HitSpinRate', 'hit_type_id', 'Distance', 'HangTime', 'Bearing', 'result_id',
                'OutsOnPlay', 'RunsScored', 'ThrowSpeed', 'PopTime', 'GameID', 'Batter', 'BatterId',
                'BatterSide', 'home_name', 'HomeTeam', 'away_name', 'AwayTeam', 'Top/Bottom', 'Pitcher', 
                'PitcherId', 'PitcherThrows', 'Catcher', 'CatcherId', 'CatcherThrows', 'league_name', 
                'Level', 'division_name', 'League', 'stadium_name', 'Stadium', 'AutoPitchType',
                'TaggedPitchType', 'PitchCall', 'TaggedHitType', 'PlayResult', 'BatterTeam', 'PitcherTeam', 'CatcherTeam']
        #Filter columns to get rid of database ids
        filt = ['GameID', 'PitchNo', 'Inning', 'Top/Bottom', 'PAofInning', 'PitchofPA', 'Pitcher',
                'PitcherId', 'PitcherThrows', 'PitcherTeam', 'Batter', 'BatterId', 'BatterSide', 'BatterTeam', 'Catcher',
                'CatcherId', 'CatcherThrows', 'CatcherTeam', 'league_name', 'Level', 'division_name', 'League',
                'home_name', 'HomeTeam', 'away_name', 'AwayTeam', 'Outs', 'Balls', 'Strikes', 'RelSpeed', 'VertBreak',
                'InducedVertBreak', 'HorzBreak', 'SpinRate', 'SpinAxis', 'Tilt', 'RelHeight', 'RelSide', 'Extension', 'AutoPitchType',
                'TaggedPitchType', 'PitchCall', 'PlateLocHeight','PlateLocSide', 'ExitSpeed', 'Angle', 'Direction',
                'HitSpinRate', 'TaggedHitType', 'Distance', 'HangTime', 'Bearing','PlayResult', 'OutsOnPlay', 'RunsScored', 'ThrowSpeed',
                'PopTime']
        
        self.data = pd.DataFrame(cur.fetchall(), columns=cols)[filt]
        conn.close()

    def innings(self, top_bottom):
        i = 1
        innings = []
        while True: 
            if len(Inning(self.data, i, top_bottom).data) > 0:
                innings.append(Inning(self.data, i, top_bottom))
                i += 1
            else:
                break
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

    def toDatabase(self):
        conn = sqlite3.connect('rylar_baseball.db')
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

            pitches.append((game_id, pitch_num, inning, top_bottom_id, pa_of_inning, pitch_of_pa,
            pitcher_id, batter_id, catcher_id, league_id, division_id, home_id, away_id, outs, balls, strikes, velocity, 
            vertical, induced, horizontal, spin, axis, tilt, release_height, release_side, release_extension, auto_type_id,
            tagged_type_id, call_id, location_height, location_side, exit_velocity, launch_angle, hit_direction, hit_spin, 
            hit_type_id, distance, hang_time, hit_bearing, result_id, outs_made, runs_scored, catcher_velocity, catcher_pop))

        try:
            cur.executemany('''INSERT INTO trackman (game_id, pitch_num, inning, top_bottom_id, pa_of_inning, pitch_of_pa,
            pitcher_id, batter_id, catcher_id, league_id, division_id, home_id, away_id, outs, balls, strikes, velocity, 
            vertical, induced, horizontal, spin, axis, tilt, release_height, release_side, release_extension, auto_type_id,
            tagged_type_id, call_id, location_height, location_side, exit_velocity, launch_angle, hit_direction, hit_spin, 
            hit_type_id, distance, hang_time, hit_bearing, result_id, outs_made, runs_scored, catcher_velocity, catcher_pop)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 
            ?, ?, ?, ?, ?, ?, ?, ?, ?)''', pitches)
            conn.commit()
        except:
            print(f'Data already in trackman table: {self.away.trackman_id} at {self.home.trackman_id} on {self.date} (game_id = {game_id}, trackman_id = {self.trackman_id})')
        conn.close()

    def writeHitterReports(self, team_id):
        temp_path = 'templates//postgame_hitter_template.xlsx'
        conn = sqlite3.connect('rylar_baseball.db')
        cur = conn.cursor()
        #Get batters from data
        batters = set(self.data[self.data['BatterTeam'] == team_id]['BatterId'])
        #Write a new report for each batter id
        for batter_id in batters:
            #Initialize batter object
            batter = player.Batter(batter_id)
            #Initialize template
            temp = load_workbook(temp_path)
            wb = temp.active

            #Get a tuple of unique at bats for batter and sort in order
            at_bats = sorted(set(self.data[self.data['BatterId'] == batter_id][['PAofInning', 'Inning', 'Top/Bottom']].apply(lambda row : (row['Inning'], row['PAofInning'], row['Top/Bottom']), axis=1)), key= lambda tup: (tup[0], tup[1]))
        
            #Fill an at bat on the sheet for each at bat, use i to control what cell to write in
            i = 0
            for ab in at_bats:
                #Initialize at_bat object
                wb[f'J{i+10}'] = inning = ab[0]
                pa_of_inning = ab[1]
                top_bottom = ab[2].lower()
                at_bat = AtBat(self.data, inning, pa_of_inning, top_bottom)
                
                wb[f'J{i+11}'] = at_bat.outs
                wb[f'J{i+12}'] = 'Coming Soon' #Runners

                #Initialize pitcher object
                pitcher = at_bat.pitcher()
                pitcher_id = pitcher.trackman_id

                wb[f'J{i+14}'] = pitcher.name.split(',')[0]
                wb[f'J{i+15}'] = pitcher.side

                wb['C3'] = batter.name #Player name
                wb['C5'] = self.date #Date
                wb['C7'] = f'v {pitcher.team_name.split()[-1]}' #Opponent
                pitches = {'Fastball' : 'FB' , 'Four-Seam': 'FB', 'ChangeUp' : 'CH', 'Changeup' : 'CH','Slider' : 'SL', 'Cutter' : 'CUT',
                'Curveball' : 'CB' , 'Splitter' : 'SP', 'Sinker' : '2FB', 'Knuckleball' : 'KN'}
                #Try using the tagged pitch type data, if an error occurs use the auto pitch type data
                #(embedded try/except statement because two different trackman versions exist)
                try:
                    #Get the mean and std pitcher fb velo for 4-seam or 2-seam fastballs
                    mean_fb = round(self.data[((self.data['TaggedPitchType'] == 'Fastball') | (self.data['TaggedPitchType'] == 'Sinker')) & (self.data['PitcherId'] == pitcher_id)]['RelSpeed'].dropna().mean())
                    #If only 1 fastball is thrown then std throws and error, replace std with 0
                    try:
                        std_fb = round(self.data[((self.data['TaggedPitchType'] == 'Fastball') | (self.data['TaggedPitchType'] == 'Sinker')) & (self.data['PitcherId'] == pitcher_id)]['RelSpeed'].dropna().std())
                    except:
                        std_fb = 0
                    wb[f'J{i+16}'] = f'{mean_fb-std_fb}-{mean_fb+std_fb} MPH'
                    #Get a list of the different pitches thrown, drop na
                    wb[f'J{i+17}'] = ','.join(set(self.data[self.data['PitcherId'] == pitcher_id]['TaggedPitchType'].dropna().map(pitches)))
                except:
                    try:
                        #Get the mean and std pitcher fb velo for 4-seam or 2-seam fastballs
                        mean_fb = round(self.data[((self.data['AutoPitchType'] == 'Four-Seam') | (self.data['AutoPitchType'] == 'Sinker')) & (self.data['PitcherId'] == pitcher_id)]['RelSpeed'].dropna().mean())
                        #If only 1 fastball is thrown then std throws and error, replace std with 0
                        try:
                            std_fb = round(self.data[((self.data['AutoPitchType'] == 'Four-Seam') | (self.data['AutoPitchType'] == 'Sinker')) & (self.data['PitcherId'] == pitcher_id)]['RelSpeed'].dropna().std())
                        except:
                            std_fb = 0
                        wb[f'J{i+16}'] = f'{mean_fb-std_fb}-{mean_fb+std_fb} MPH'
                        #Get a list of the different pitches thrown, drop na
                        wb[f'J{i+17}'] = ','.join(set(self.data[self.data['PitcherId'] == pitcher_id]['AutoPitchType'].dropna().map(pitches)))
                    except:
                        #Get the mean and std pitcher fb velo for 4-seam or 2-seam fastballs
                        mean_fb = round(self.data[((self.data['AutoPitchType'] == 'Fastball') | (self.data['AutoPitchType'] == 'Sinker')) & (self.data['PitcherId'] == pitcher_id)]['RelSpeed'].dropna().mean())
                        #If only 1 fastball is thrown then std throws and error, replace std with 0
                        try:
                            std_fb = round(self.data[((self.data['AutoPitchType'] == 'Fastball') | (self.data['AutoPitchType'] == 'Sinker')) & (self.data['PitcherId'] == pitcher_id)]['RelSpeed'].dropna().std())
                        except:
                            std_fb = 0
                        wb[f'J{i+16}'] = f'{mean_fb-std_fb}-{mean_fb+std_fb} MPH'
                        #Get a list of the different pitches thrown, drop na
                        wb[f'J{i+17}'] = ','.join(set(self.data[self.data['PitcherId'] == pitcher_id]['AutoPitchType'].dropna().map(pitches)))
                #Try to get exit velo on last pitch of at bat, if an error occurs leave it blank
                try:
                    if round(at_bat.pitches()[-1].exit_velocity != float('nan')):
                        wb[f'M{i+10}'] = f'{round(at_bat.pitches()[-1].exit_velocity, 2)} MPH'
                except:
                     wb[f'M{i+10}'] = ''
                #Try to get launch angle on last pitch of at bat, if an error occurs leave it blank
                try:
                     if round(at_bat.pitches()[-1].launch_angle != float('nan')):
                        wb[f'M{i+12}']  = f'{round(at_bat.pitches()[-1].launch_angle, 2)}{chr(176)}'
                except:
                     wb[f'M{i+12}']  = ''
                #Try to get hit type on last pitch of at bat, if an error occurs leave it blank
                hits = {'Popup' : 'Popup', 'LineDrive' : 'Line Drive', 'GroundBall' : 'Ground Ball', 'FlyBall' : 'Fly Ball', 'Bunt' : 'Bunt'}
                try:
                     wb[f'M{i+14}']  = hits[at_bat.pitches()[-1].hit_type]
                except:
                     wb[f'M{i+14}']  = ''
                #Try to get result on last pitch of at bat, if an error occurs leave it blank
                try:
                     wb[f'M{i+15}']  = at_bat.pitches()[-1].result
                except:
                     wb[f'M{i+15}']  = ''
                wb[f'M{i+16}']  = 'Coming Soon' #QAB
                
                #Jump to next at bat slot
                i += 9
                #Skip the second page header
                if i == 45:
                    i = 51
            #Create folders if they do not exist
            try:
                os.mkdir(f'postgame_hitter_reports//{batter.team_trackman_id}')
            except:
                pass
            try:
                os.mkdir(f'postgame_hitter_reports//{batter.team_trackman_id}//{self.date}')
            except:
                pass
            #Save file to folder with player name
            temp.save(f'postgame_hitter_reports//{batter.team_trackman_id}//{self.date}//{batter.name}.xlsx')
            temp.close()
        conn.close()

    def writePitcherReports():
        pass