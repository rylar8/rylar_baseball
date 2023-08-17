import sqlite3
import pandas as pd

class Player():
    def __init__(self, trackman_id):
        self.trackman_id = trackman_id
        self.conn = sqlite3.connect('rylar_baseball.db')
        self.cur = self.conn.cursor()

class Pitcher(Player):
    def __init__(self, trackman_id):
        super().__init__(trackman_id)
        #Get player name from database
        self.cur.execute('SELECT pitcher_name FROM pitchers WHERE trackman_id = ?', (trackman_id,))
        self.name = self.cur.fetchone()[0]
        #Get player id from database
        self.cur.execute('SELECT pitcher_id FROM pitchers WHERE trackman_id = ?', (trackman_id,))
        self.pitcher_id = self.cur.fetchone()[0]
        #Get player side from database
        self.cur.execute('''SELECT sides.side FROM sides
                            JOIN pitchers ON sides.side_id = pitchers.pitcher_side_id
                            WHERE pitchers.trackman_id = ?''', (trackman_id,))
        self.side = self.cur.fetchone()[0]
        #Get player team id from database
        self.cur.execute('SELECT team_id FROM pitchers WHERE trackman_id = ?', (trackman_id,))
        self.team_id = self.cur.fetchone()[0]
        #Get player team name from database
        self.cur.execute('SELECT team_name FROM teams WHERE team_id = ?', (self.team_id,))
        self.team_name = self.cur.fetchone()[0]
        #Get player team trackman id from database
        self.cur.execute('SELECT trackman_name FROM teams WHERE team_id = ?', (self.team_id,))
        self.team_trackman_id = self.cur.fetchone()[0]
        self.conn.close()

    class Pitch():

        def __init__(self, pitcher_id, type_id, tagged = True):
            self.pitcher_id = pitcher_id
            self.type_id = type_id
            conn = sqlite3.connect('rylar_baseball.db')
            if tagged:
                self.pitch_id = f'1{self.pitcher_id}{self.type_id}'
            else:
                self.pitch_id = f'2{self.pitcher_id}{self.type_id}'
            self.info = pd.read_sql('SELECT * FROM arsenal_stats_info WHERE pitch_id = ?', conn, params =[self.pitch_id])


        def battedBallStats(self):
            conn = sqlite3.connect('rylar_baseball.db')
            df = pd.read_sql('SELECT * FROM arsenal_stats_batted_ball WHERE pitch_id = ?', conn, params=[self.pitch_id])
            conn.close()
            return df
    
        def disciplineStats(self):
            conn = sqlite3.connect('rylar_baseball.db')
            df = pd.read_sql('SELECT * FROM arsenal_stats_discipline WHERE pitch_id = ?', conn, params=[self.pitch_id])
            conn.close()
            return df
        
        def standardStats(self):
            conn = sqlite3.connect('rylar_baseball.db')
            df = pd.read_sql('SELECT * FROM arsenal_stats_standard WHERE pitch_id = ?', conn, params=[self.pitch_id])
            conn.close()
            return df
        
        def statcastStats(self):
            conn = sqlite3.connect('rylar_baseball.db')
            df = pd.read_sql('SELECT * FROM arsenal_stats_statcast WHERE pitch_id = ?', conn, params=[self.pitch_id])
            conn.close()
            return df
            
    def advancedStats(self):
        conn = sqlite3.connect('rylar_baseball.db')
        df = pd.read_sql('SELECT * FROM pitching_stats_advanced WHERE pitcher_id = ?', conn, params=[self.pitcher_id])
        conn.close()
        return df

    def battedBallStats(self):
        conn = sqlite3.connect('rylar_baseball.db')
        df = pd.read_sql('SELECT * FROM pitching_stats_batted_ball WHERE pitcher_id = ?', conn, params=[self.pitcher_id])
        conn.close()
        return df
    
    def disciplineStats(self):
        conn = sqlite3.connect('rylar_baseball.db')
        df = pd.read_sql('SELECT * FROM pitching_stats_discipline WHERE pitcher_id = ?', conn, params=[self.pitcher_id])
        conn.close()
        return df
    
    def standardStats(self):
        conn = sqlite3.connect('rylar_baseball.db')
        df = pd.read_sql('SELECT * FROM pitching_stats_standard WHERE pitcher_id = ?', conn, params=[self.pitcher_id])
        conn.close()
        return df
    
    def statcastStats(self):
        conn = sqlite3.connect('rylar_baseball.db')
        df = pd.read_sql('SELECT * FROM pitching_stats_statcast WHERE pitcher_id = ?', conn, params=[self.pitcher_id])
        conn.close()
        return df
    
    def arsenal(self, tagged = True):
        conn = sqlite3.connect('rylar_baseball.db')
        type_ids = pd.read_sql('SELECT type_id FROM arsenal_stats_standard WHERE pitcher_id = ?', conn, params=[self.pitcher_id])
       
        return [self.Pitch(self.pitcher_id, type_id, tagged) for type_id in set(type_ids.type_id)]

class Batter(Player):
    def __init__(self, trackman_id):
        super().__init__(trackman_id)
        #Get player name from database
        self.cur.execute('SELECT batter_name FROM batters WHERE trackman_id = ?', (trackman_id,))
        self.name = self.cur.fetchone()[0]
        #Get player id from database
        self.cur.execute('SELECT batter_id FROM batters WHERE trackman_id = ?', (trackman_id,))
        self.batter_id = self.cur.fetchone()[0]
        #Get player side from database
        self.cur.execute('''SELECT sides.side FROM sides
                            JOIN batters ON sides.side_id = batters.batter_side_id
                            WHERE batters.trackman_id = ?''', (trackman_id,))
        self.side = self.cur.fetchone()[0]
        #Get player team id from database
        self.cur.execute('SELECT team_id FROM batters WHERE trackman_id = ?', (trackman_id,))
        self.team_id = self.cur.fetchone()[0]
        #Get player team name from database
        self.cur.execute('SELECT team_name FROM teams WHERE team_id = ?', (self.team_id,))
        self.team_name = self.cur.fetchone()[0]
        #Get player team trackman id from database
        self.cur.execute('SELECT trackman_name FROM teams WHERE team_id = ?', (self.team_id,))
        self.team_trackman_id = self.cur.fetchone()[0]
        self.conn.close()

    def advancedStats(self):
        conn = sqlite3.connect('rylar_baseball.db')
        df = pd.read_sql('SELECT * FROM batting_stats_advanced WHERE batter_id = ?', conn, params=[self.batter_id])
        conn.close()
        return df

    def battedBallStats(self):
        conn = sqlite3.connect('rylar_baseball.db')
        df = pd.read_sql('SELECT * FROM batting_stats_batted_ball WHERE batter_id = ?', conn, params=[self.batter_id])
        conn.close()
        return df
    
    def disciplineStats(self):
        conn = sqlite3.connect('rylar_baseball.db')
        df = pd.read_sql('SELECT * FROM batting_stats_discipline WHERE batter_id = ?', conn, params=[self.batter_id])
        conn.close()
        return df
    
    def standardStats(self):
        conn = sqlite3.connect('rylar_baseball.db')
        df = pd.read_sql('SELECT * FROM batting_stats_standard WHERE batter_id = ?', conn, params=[self.batter_id])
        conn.close()
        return df
    
    def statcastStats(self):
        conn = sqlite3.connect('rylar_baseball.db')
        df = pd.read_sql('SELECT * FROM batting_stats_statcast WHERE batter_id = ?', conn, params=[self.batter_id])
        conn.close()
        return df

    def probableStrikezone():
        #Use binary classification to find estimate for player's strikezone height, would width change by hitter? probably not.
        pass

class Catcher(Player):
    def __init__(self, trackman_id):
        super().__init__(trackman_id)
        #Get player name from database
        self.cur.execute('SELECT catcher_name FROM catchers WHERE trackman_id = ?', (trackman_id,))
        self.name = self.cur.fetchone()[0]
        #Get player id from database
        self.cur.execute('SELECT catcher_id FROM catchers WHERE trackman_id = ?', (trackman_id,))
        self.player_id = self.cur.fetchone()[0]
        #Get player side from database
        self.cur.execute('''SELECT sides.side FROM sides
                            JOIN catchers ON sides.side_id = catchers.catchers_side_id
                            WHERE catchers.trackman_id = ?''', (trackman_id,))
        self.side = self.cur.fetchone()[0]
        #Get player team id from database
        self.cur.execute('SELECT team_id FROM catchers WHERE trackman_id = ?', (trackman_id,))
        self.team_id = self.cur.fetchone()[0]
        #Get player team name from database
        self.cur.execute('SELECT team_name FROM teams WHERE team_id = ?', (self.team_id,))
        self.team_name = self.cur.fetchone()[0]
        #Get player team trackman id from database
        self.cur.execute('SELECT trackman_name FROM teams WHERE team_id = ?', (self.team_id,))
        self.team_trackman_id = self.cur.fetchone()[0]
        self.conn.close()

class Baserunner(Batter):
    def __init__(self, trackman_id):
        super().__init__(trackman_id)
        self.conn.close()