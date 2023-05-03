import sqlite3
import pandas as pd

#not sure if this would make things easier or not so I will just leave this here for the potential future.

class Database():

    def __init__(self):
        self.conn = sqlite3.connect('rylar_baseball.db')
        self.cur = self.conn.cursor()

    def loadGame(self, game_id):

        self.cur.execute('''SELECT trackman.*, 
                    games.trackman_id AS trackman_game_id,
                    games.date AS Date, 
                    games.time AS Time,
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
                'ContactPositionX', 'ContactPositionY', 'ContactPositionZ', 'HitSpinAxis', 'GameID', 'Date', 'Time', 'Batter', 'BatterId',
                'BatterSide', 'home_name', 'HomeTeam', 'away_name', 'AwayTeam', 'Top/Bottom', 'Pitcher', 
                'PitcherId', 'PitcherThrows', 'Catcher', 'CatcherId', 'CatcherThrows', 'league_name', 
                'Level', 'division_name', 'League', 'stadium_name', 'Stadium', 'AutoPitchType',
                'TaggedPitchType', 'PitchCall', 'TaggedHitType', 'PlayResult', 'BatterTeam', 'PitcherTeam', 'CatcherTeam', 'KorBB']
        #Filter columns to get rid of database ids
        filt = ['GameID', 'Date', 'Time', 'PitchNo', 'Inning', 'Top/Bottom', 'PAofInning', 'PitchofPA', 'Pitcher',
                'PitcherId', 'PitcherThrows', 'PitcherTeam', 'Batter', 'BatterId', 'BatterSide', 'BatterTeam', 'Catcher',
                'CatcherId', 'CatcherThrows', 'CatcherTeam', 'league_name', 'Level', 'division_name', 'League',
                'home_name', 'HomeTeam', 'away_name', 'AwayTeam', 'Outs', 'Balls', 'Strikes', 'RelSpeed', 'VertBreak',
                'InducedVertBreak', 'HorzBreak', 'SpinRate', 'SpinAxis', 'Tilt', 'RelHeight', 'RelSide', 'Extension', 'AutoPitchType',
                'TaggedPitchType', 'PitchCall', 'PlateLocHeight','PlateLocSide', 'ExitSpeed', 'Angle', 'Direction',
                'HitSpinRate', 'TaggedHitType', 'Distance', 'HangTime', 'Bearing','PlayResult', 'KorBB', 'OutsOnPlay', 'RunsScored', 'ThrowSpeed',
                'PopTime', 'VertApprAngle', 'HorzApprAngle', 'ZoneSpeed', 'ZoneTime', 'PositionAt110X', 'PositionAt110Y',
                'PositionAt110Z', 'LastTrackedDistance', 'pfxx', 'pfxz', 'x0', 'y0', 'z0', 'vx0', 'vy0', 'vz0', 'ax0', 'ay0', 'az0', 
                'ContactPositionX', 'ContactPositionY', 'ContactPositionZ', 'HitSpinAxis', 'Stadium']
        
        self.data = pd.DataFrame(cur.fetchall(), columns=cols)[filt]
        self.stadium = self.data.iloc[0]['Stadium']
        self.league = self.data.iloc[0]['Level']
        self.division = self.data.iloc[0]['League']
        self.trackman_id = self.data.iloc[0]['GameID']
        self.date = pd.to_datetime(self.data.iloc[0]['Date']).date()
        self.year = pd.to_datetime(self.data.iloc[0]['Date']).year
        self.time = self.data.iloc[0]['Time']
        self.home = team.Team(self.data.iloc[0]['HomeTeam'])
        self.away = team.Team(self.data.iloc[0]['AwayTeam'])
        conn.close()