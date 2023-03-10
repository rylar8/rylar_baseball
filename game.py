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
            print(f'Game already in games table: {self.away.trackman_id} at {self.home.trackman_id} on {self.date} (gameID - {self.trackman_id})')
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
            #Get batter side id
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


    def writeHitterReports():
        pass

    def writePitcherReports():
        pass