from inning import Inning
from team import Team
import sqlite3
import pandas as pd

class Game:
    def __init__(self, data):
        self.data = data
        self.stadium = self.data.iloc[0]['Stadium']
        self.league = self.data.iloc[0]['Level']
        self.division = self.data.iloc[0]['League']
        self.trackman_id = self.data.iloc[0]['GameID']
        self.date = self.data.iloc[0]['Date']
        self.year = pd.to_datetime(self.data.iloc[0]['Date']).year
        self.time = self.data.iloc[0]['Time']
        self.home = Team(data.iloc[0]['HomeTeam'])
        self.away = Team(data.iloc[0]['AwayTeam'])

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

    def toDatabase(self):
        con = sqlite3.connect('rylar_baseball.db')
        cur = con.cursor()
        #Add league
        try:
            #Increment league id
            cur.execute('SELECT league_id FROM leagues')
            league_id = cur.fetchall()[-1][0] + 1
            #Add new league
            cur.execute('''INSERT INTO leagues (league_id, year, trackman_name)
            VALUES (?, ?, ?);''', (league_id, self.year, self.league))
            con.commit()
            #Get full league name
            league_name = input(f"Input new league name ({self.league}): ")
            cur.execute('UPDATE leagues SET league_name = ? WHERE league_id = ?', (league_name, league_id))
            con.commit()
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
            con.commit()
            #Get full division name
            division_name = input(f"Input new division name ({self.division}): ")
            cur.execute('UPDATE divisions SET division_name = ? WHERE division_id = ?', (division_name, division_id))
            con.commit()
        except:
            #Get division id
            cur.execute('SELECT division_id FROM divisions WHERE trackman_name = ? AND year = ?', (self.division, self.year))
            division_id = cur.fetchone()[0]
        #Add home team
        try:
            cur.execute('INSERT INTO teams (trackman_name, division_id, league_id, year) VALUES (?, ?, ?, ?)', 
                        (self.home.trackman_id, division_id, league_id, self.year))
            con.commit()
            #Get full team name
            home_name = input(f"Input new team name ({self.home.trackman_id}): ")
            cur.execute('UPDATE teams SET team_name = ? WHERE trackman_name = ?', (home_name, self.home.trackman_id))
            con.commit()
        except:
            pass
        #Add away team
        try:
            cur.execute('INSERT INTO teams (trackman_name, division_id, league_id, year) VALUES (?, ?, ?, ?)', 
                    (self.away.trackman_id, division_id, league_id, self.year))
            con.commit()
            #Get full team name
            away_name = input(f"Input new team name ({self.away.trackman_id}): ")
            cur.execute('UPDATE teams SET team_name = ? WHERE trackman_name = ?', (away_name, self.away.trackman_id))
            con.commit()
        except:
            pass
        try:
            cur.execute('INSERT INTO stadiums (trackman_name,) VALUES (?,)', (self.stadium,))
            con.commit()
            #Get full stadium name
            stadium_name = input(f"Input new stadium name ({self.stadium}): ")
            cur.execute('UPDATE stadiums SET stadium_name =? WHERE trackman_name = ?', (stadium_name, self.stadium))
            con.commit()
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
            VALUES (?,?,?,?,?,?,?,?)''', (self.trackman_id, self.date, self.time, stadium_id, league_id, division_id, home_id, away_id))
            con.commit()
        except:
            print(f'Game already in games table: {self.away.trackman_id} at {self.home.trackman_id} on {self.date} (gameID = {self.trackman_id})')
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
                con.commit()
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
                con.commit()
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
                con.commit()
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
            #Get auto type id
            cur.execute('SELECT type_id FROM pitches WHERE auto_pitch = ?', (pitch.AutoPitchType,))
            auto_type_id = cur.fetchone()[0]
            #Get tagged type id
            cur.execute('SELECT type_id FROM pitches WHERE tagged_pitch = ?', (pitch.TaggedPitchType,))
            tagged_type_id = cur.fetchone()[0]
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


        cur.executemany('''INSERT INTO trackman (game_id, pitch_num, inning, top_bottom_id, pa_of_inning, pitch_of_pa,
        pitcher_id, batter_id, catcher_id, league_id, division_id, home_id, away_id, outs, balls, strikes, velocity, 
        vertical, induced, horizontal, spin, axis, tilt, release_height, release_side, release_extension, auto_type_id,
        tagged_type_id, call_id, location_height, location_side, exit_velocity, launch_angle, hit_direction, hit_spin, 
        hit_type_id, distance, hang_time, hit_bearing, result_id, outs_made, runs_scored, catcher_velocity, catcher_pop)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 
        ?, ?, ?, ?, ?, ?, ?, ?, ?)''', pitches)
        con.commit()

    def writeHitterReports():
        pass

    def writePitcherReports():
        pass