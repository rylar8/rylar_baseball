from . import game
import sqlite3

class Team():
    def __init__(self, trackman_id):
        self.trackman_id = trackman_id

        conn = sqlite3.connect('rylar_baseball.db')
        cur = conn.cursor()
        cur.execute('SELECT team_id FROM teams WHERE trackman_name = ?', (self.trackman_id,))
        self.team_id = cur.fetchone()[0]

    def games(self):
        conn = sqlite3.connect('rylar_baseball.db')
        cur = conn.cursor()

        #Get all trackman game IDs containing the team trackman name
        cur.execute('''SELECT games.trackman_id
        FROM games 
        JOIN teams AS home_team ON games.home_id = home_team.team_id
        JOIN teams AS away_team ON games.away_id = away_team.team_id 
        WHERE home_team.team_id = ? OR away_team.team_id = ?''', (self.team_id, self.team_id))

        #Make a list of Game objects for all the games
        games = [game.Game().loadID(tup[0]) for tup in cur.fetchall()]

        conn.close()
        return games

    def players(self):
        pass

    def pitchers(self):
        pass

    def hitters(self):
        pass

    def addGame(self, game):
        pass

    def addPlayer(self):
        pass

    def writeHitterScouting(self):
        pass

    def writePitcherScouting(self):
        pass

    def writeSprayCharts(self):
        pass

    def writeRunCards(self):
        pass

    def optimizeLineup(self):
        pass

