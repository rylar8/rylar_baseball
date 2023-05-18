from . import game, player
import sqlite3

class Team():
    def __init__(self, trackman_id):
        self.trackman_id = trackman_id 

    def games(self):
        conn = sqlite3.connect('rylar_baseball.db')
        cur = conn.cursor()

        #Get all trackman game IDs containing the team trackman name
        cur.execute('''SELECT games.trackman_id
        FROM games 
        LEFT JOIN teams AS home_team ON games.home_id = home_team.team_id
        LEFT JOIN teams AS away_team ON games.away_id = away_team.team_id 
        WHERE home_team.team_id = ? OR away_team.team_id = ?''', (self.team_id, self.team_id))

        #Make a list of Game objects for all the games
        games = []
        for tup in cur.fetchall():
            g = game.Game()
            g.loadID(tup[0])
            games.append(g)

        conn.close()
        return games

    def toDatabase(self):
        pass

    def pitchers(self):
        conn = sqlite3.connect('rylar_baseball.db')
        cur = conn.cursor()

        #Get all trackman game IDs containing the team trackman name
        cur.execute('''SELECT pitchers.trackman_id
        FROM pitchers 
        LEFT JOIN teams ON pitchers.team_id = teams.team_id
        WHERE pitchers.team_id = ?''', (self.team_id,))

        #Make a list of Pitcher objects for all the games
        pitchers = [player.Pitcher(tup[0]) for tup in cur.fetchall()]

        conn.close()
        return pitchers

    def batters(self):
        conn = sqlite3.connect('rylar_baseball.db')
        cur = conn.cursor()

        #Get all trackman game IDs containing the team trackman name
        cur.execute('''SELECT batters.trackman_id
        FROM batters 
        LEFT JOIN teams ON batters.team_id = teams.team_id
        WHERE batters.team_id = ?''', (self.team_id,))

        #Make a list of Batter objects for all the games
        batters = [player.Batter(tup[0]) for tup in cur.fetchall()]

        conn.close()
        return batters

    def addGame(self, Game):
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

