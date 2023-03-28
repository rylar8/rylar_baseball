import sqlite3


class Player():
    def __init__(self, trackman_id):
        self.trackman_id = trackman_id
        self.conn = sqlite3.connect('rylar_baseball.db')
        self.cur = self.conn.cursor()
    pass

class Pitcher(Player):
    def __init__(self, trackman_id):
        super().__init__(trackman_id)
        #Get player name from database
        self.cur.execute('SELECT pitcher_name FROM pitchers WHERE trackman_id = ?', (trackman_id,))
        self.name = self.cur.fetchone()[0]
        #Get player id from database
        self.cur.execute('SELECT pitcher_id FROM pitchers WHERE trackman_id = ?', (trackman_id,))
        self.player_id = self.cur.fetchone()[0]
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
        self.team_id = self.cur.fetchone()[0]
        #Get player team trackman id from database
        self.cur.execute('SELECT trackman_name FROM teams WHERE team_id = ?', (self.team_id,))
        self.team_trackman_id = self.cur.fetchone()[0]

class Batter(Player):
    def __init__(self, trackman_id):
        super().__init__(trackman_id)
        #Get player name from database
        self.cur.execute('SELECT batter_name FROM batters WHERE trackman_id = ?', (trackman_id,))
        self.name = self.cur.fetchone()[0]
        #Get player id from database
        self.cur.execute('SELECT batter_id FROM batters WHERE trackman_id = ?', (trackman_id,))
        self.player_id = self.cur.fetchone()[0]
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
        self.team_id = self.cur.fetchone()[0]
        #Get player team trackman id from database
        self.cur.execute('SELECT trackman_name FROM teams WHERE team_id = ?', (self.team_id,))
        self.team_trackman_id = self.cur.fetchone()[0]

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
        self.team_id = self.cur.fetchone()[0]
        #Get player team trackman id from database
        self.cur.execute('SELECT trackman_name FROM teams WHERE team_id = ?', (self.team_id,))
        self.team_trackman_id = self.cur.fetchone()[0]

class Baserunner(Batter):
    def __init__(self, trackman_id):
        super().__init__(trackman_id)