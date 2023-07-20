# rylar_baseball Library Documentation

**Please note that documentation is a work in progress, as is the rest of the library**

## Introduction
The **rylar_baseball** library was created to ease the handling of Trackman Baseball data. The library reads in game files, writes them to SQL, and creates relevant objects to make tool building and data visualization easier. The key objects provided by the library, include **Game**, **Inning**, **AtBat**, **Pitch**, **Team**, **Player**, etc. The library assigns all relevant Trackman data to each instance of these objects allowing database querying to be as simple as accessing a batter's average exit velocity with `sample_batter.avg_ev`.

## Installation
**rylar_baseball** library is currently not availble for download. Upon a workable project this will be updated. Currently **rylar_baseball** is only intended for private use by its owner.

## Getting Started
Importing **rylar_baseball** library into a Python script will be as easy as `from rylar_baseball import *`

Reading in a Trackman CSV is as easy as: 

```python
game1 = game.Game()
game1.loadCSV('csv//raw_trackman_file.csv')
```

The **Game** class has methods such as **toDatabase()**, **updateStats()**, **writeBatterReports()**, **writePitcherReports()**, and more.

## Objects and Methods Reference
### `Game`

`Game` object initializes by `game.Game()`

`__init__`
  - Nothing initializes until the `Game` object loads data via `.loadCSV`, `.loadDF`, or `.loadID`

`.loadCSV(csv, writeData=True)`
  - Reads in Trackman csv initializing basic attributes:
    - `.data` (pandas dataframe of game data)
    - `.stadium` (Trackman stadium name)
    - `.league` (Trackman level name)
    - `.division` (Trackman league name)
    - `.trackman_id` (Trackman GameID)
    - `.date` (date of game)
    - `.year` (year of game)
    - `.time` (time of first pitch)
    - `.home` (initializes `Team` object for home team)
    - `.away` (initializes `Team` object for away team)
    - `.timestamp` (time of file upload)
  - If `writeData` is set to the default True value then:
    - `.toDatabase()` and `.updateStats()` will run automatically
      
`.loadDF(data, writeData=True)`
  - Reads in dataframe initializing its basic attributes (see `loadCSV`)
  - If `writeData` is set to the default True value then:
    - `toDatabase()` and `updateStats()` will run automatically
      
`.loadID(game_id)`
  - Accesses the database, initializing a Game object and its basic attributes (see `loadCSV`) from the given Trackman GameID
    
`.innings(top_bottom)`
  - Returns a list of `Inning` objects for each half inning in the game according to the `top_bottom` argument
  - `top_bottom` strictly accepts either 'top' or 'bottom' to specify which half of each inning to populate the return list with
    
`.batters()`
  - Returns a list of `Batter` objects for every batter in the game
    
`.catchers()`
  - Returns a list of `Catcher` objects for every catcher in the game
    
`.pitchers()`
  - Returns a list of `Pitcher` objects for every pitcher in the game
    
`.adjustZone(stadium_id)`
  - A proposed method to roughly adjust Trackman data when it is obvious a miscalibration exists. The method would use all available data to provide a normal distribution of pitches. Each stadium would receive an adjustment X,Y,Z value to align closer with the normal distribution of pitches.
    
`.pitcherStatline(pitcher_id)`
  - Returns a statline (K, H, R, BB, HBP) for the `pitcher_id` provided
  - `pitcher_id` should reference a Trackman provided pitcher_id who pitched in the game

`.movementPlot(pitcher_id, view='pitcher')`
  - Saves a png image (saved as `{date}{game_id}{pitcher_id}movement_plot.png`) in a file named 'temporary_figures' of a pitcher's average movement by pitch type overlayed on a X-Y plane. Currently this is only used in `writePitcherReports`
  - `pitcher_id` should reference a Trackman provided pitcher_id who pitched in the game
  - `view` strictly accepts either 'pitcher' or 'catcher' to dictate which perspective the graph should be oriented. 'pitcher' is the default value

`.toDatabase()`
  - Writes the game to the database. If any object within the game file is new to the database then information may be requested to properly store the new object. ie. if the game contains a team who is not currently in the database then a proper team name will be requested

`.writeBatterReports(team_id)`
  - Uses an Excel template to generate a postgame breakdown of each batter's at bats, providing pitch locations, swing decisions, ball flight metrics, and more.
  - `team_id` expects a Trackman ID corresponding to the team of batters for which reports should be generated

`.writePitcherReports(team_id)`
  - Uses an Excel template to generate a postgame breakdown of each pitcher's inning pitched, providing pitch locations, pitch metrics, and more.
  - `team_id` expects a Trackman ID corresponding to the team of pitchers for which reports should be generated
    
`.updateStats()`
  - Updates the statistics tables in the database, using the `upload_timestamp` to only update players stats who were involved in recent game uploads. This method currently has efficiency issues and is being troubleshooted

### `Inning`

`Inning` object initializes by `inning.Inning(inning, top_bottom)`

*Note that an `Inning` object is really only a half inning*

`__init__(data, inning, top_bottom)`
  - `data` must be a data frame containing a full Trackman game
  - `inning` must be an integer indicating an inning within the game
  - `top_bottom` must be a string strictly containing either 'top' or 'bottom'

  - Initialized within the `Inning` object are:
    - `.game_data` (full game data from which this `Inning` is derived)
    - `.top_bottom` (a string containing 'top' or 'bottom' indicating the half of the inning)
    - `.inning_data` (full inning data (as opposed to half inning data) from which this `Inning` is derived)
    - `.date` (date of game)
    - `.game_id` (Trackman GameID)
    - `.data` (half inning data)
    - `.number` (inning number of the game)

`.at_bats()`
  - Returns a list of `AtBat` objects for every at bat within the inning

`.pitcherStatline(pitcher_id)`
  - Returns an inning statline (K, R, H, BB, HBP) for the `pitcher_id` provided
  - `pitcher_id` should reference a Trackman provided pitcher_id who pitched in the half inning

`.movementPlot(pitcher_id, view='pitcher')`
  - Saves a png image (saved as `{date}{game_id}{number}{pitcher_id}movement_plot.png`) in a file named 'temporary_figures' of a pitcher's average movement by pitch type overlayed on a X-Y plane. Currently this is only used in `writePitcherReports`
  - `pitcher_id` should reference a Trackman provided pitcher_id who pitched in the half inning
  - `view` strictly accepts either 'pitcher' or 'catcher' to dictate which perspective the graph should be oriented. 'pitcher' is the default value

### `AtBat`

`AtBat` object initializes by `atbat.AtBat(inning, top_bottom, at_bat)`

`__init__(data, inning, top_bottom, at_bat)`
  - `data` must be a data frame containing a full Trackman game
  - `inning` must be an integer indicating an inning within the game
  - `top_bottom` must be a string strictly containing either 'top' or 'bottom'
  - `at_bat` must be an integer indicating a plate appearance within the half inning
  
  - Initialized within the `AtBat` object are:
    - `.inning` (inning number of the game)
    - `.game_data` (full game data from which this `AtBat` is derived)
    - `.top_bottom` (a string containing 'top' or 'bottom' indicating the half of the inning)
    - `.inning_data` (full inning data (as opposed to half inning data) from which this `AtBat` is derived)
    - `.half_inning_data` (half inning data from which this `AtBat` is derived)
    - `.data` (at bat data)
    - `.number` (plate appearance number of the half inning)
    - `.outs` (number of outs when the at bat began)
    - `.date` (date of game)
  
`.pitches()`
  - Returns a list of `Pitch` objects for every pitch within the at bat

`.batter()`
  - Returns a `Batter` object of the batter who began the at bat

`.pitcher()`
  - Returns a `Pitcher` object of the pitcher who began the at bat

`.catcher()`
  - Returns a `Catcher` object of the catcher who began the at bat

`.zoneTracer(view='pitcher')`
  - Saves a png image (saved as `{date}{top_bottom}{inning}{number}zone_tracer.png`) in a file named 'temporary_figures' of a pitcher's pitch locations and pitch type overlayed on a strikezone
  - `view` strictly accepts either 'pitcher' or 'catcher' to dictate which perspective the graph should be oriented. 'pitcher' is the default value 

### `Pitch`

`Pitch` object initializes by `pitch.Pitch(inning, top_bottom, at_bat, pitch)`

`__init__(data, inning, top_bottom, at_bat, pitch)`
  - `data` must be a data frame containing a full Trackman game
  - `inning` must be an integer indicating an inning within the game
  - `top_bottom` must be a string strictly containing either 'top' or 'bottom'
  - `at_bat` must be an integer indicating a plate appearance within the half inning
  - `pitch` must be an integer indicating a pitch within the plate appearance

  - Initialized within the `Pitch` object are:
    - `.game_data` (full game data from which this `Pitch` is derived)
    - `.inning_data` (full inning data (as opposed to half inning data) from which this `Pitch` is derived)
    - `.half_inning_data` (half inning data from which this `Pitch` is derived)
    - `.at_bat_data` (at bat data from which this `Pitch` is derived)
    - `.data` (pitch data)
    - `.number` (pitch number of at bat)
    - `.velocity` (pitch velocity)
    - `.vertical` (vertical break)
    - `.induced` (induced vertical break)
    - `.horizontal` (horizontal break)
    - `.spin` (spin rate)
    - `.axis` (spin axis)
    - `.tilt` (pitch tilt)
    - `.release_height` (release height)
    - `.release_side` (release side)
    - `.release_extension` (pitcher extension)
    - `.auto_type` (auto tagged pitch type)
    - `.tagged_type` (tagger tagged pitch type)
    - `.call` (pitch call {ball, strike, swing, in play, etc.})
    - `.location_height` (pitch height when crossing the plate)
    - `.location_side` (pitch side location when crossing the plate)
    - `.exit_velocity` (exit speed of batted ball)
    - `.launch_angle` (exit angle of batted ball)
    - `.hit_direction` (exit direction of batted ball)
    - `.hit_spin` (spin rate of batted ball)
    - `.hit_type` (tagged hit type {ground ball, fly ball, etc.})
    - `.distance` (estimated distance travelled of batted ball)
    - `.hang_time` (estimated hang time of batted ball)
    - `.hit_bearing` (estimated landing direction of batted ball)
    - `.result` (play result {single, out, error, etc.})
    - `.outs_made` (number of outs recorded on the play)
    - `.runs_scored` (number of runs scored on play)
    - `.catcher_velocity` (velocity of catcher throw)
    - `.catcher_pop` (estimated pop time of catcher throw)
    - `.k_or_bb` (if a strikeout or walk was recorded)
    - `.vert_approach_angle` (vertical angle in which pitch crosses home plate)
    - `.horz_approach_angle` (horizontal angle in which pitch crosses home plate)
    - `.zone_speed` (velocity of pitch when crossing home plate)
    - `.zone_time` (estimated amount of time pitch is in the zone)
    - `.pos_at_110x` (position of batted ball in X direction when 110 feet from home plate)
    - `.pos_at_110y` (position of batted ball in Y direction when 110 feet from home plate)
    - `.pos_at_110z` (position of batted ball in Z direction when 110 feet from home plate)
    - `.last_tracked_distance` (distance from home plate batted ball was before Trackman lost track of ball)
    - `.pfxx` (an estimation of observed pfx movement in X direction)
    - `.pfxz` (an estimation of observed pfx movement in Z direction)
    - `.horz_loc_50` (X location when pitch is 50 feet from home)
    - `.from_home_loc_50` (Y location when pitch is 50 feet from home, should always be 50)
    - `.vert_loc_50` (Z location when pitch is 50 feet from home)
    - `.horz_velo_50` (velocity in X direction when pitch is 50 feet from home)
    - `.from_home_velo_50` (velocity in Y direction when pitch is 50 feet from home)
    - `.vert_velo_50` (velocity in Z direction when pitch is 50 feet from home)
    - `.horz_acc_50` (acceleration in X direction when pitch is 50 feet from home)
    - `.from_home_acc_50` (acceleration in Y direction when pitch is 50 feet from home)
    - `.vert_acc_50` (acceleration in Z direction when pitch is 50 feet from home)
    - `.con_pos_x` (where the pitch is contacted in X direction)
    - `.con_pos_y` (where the pitch is contacted in Y direction)
    - `.con_pos_z` (where the pitch is contacted in Z direction)
    - `.hit_spin_axis` (spin axis of batted ball)

`.batter()`
  - Returns a `Batter` object of the batter at bat during the pitch
      
`.pitcher()`
  - Returns a `Pitcher` object of the pitcher on record during the pitch
      
`.catcher()`
  - Returns a `Catcher` object of the catcher on record during the pitch
   
`.barreled(exit_velocity, launch_angle)`
    - Returns `True` if the pitch was barreled
    - `exit_velocity` must be a float containing the exit speed of the batted ball
    - `launch angle` must be a float containing the exit angle of the batted ball
   
### `GameState`

`GameState` object initializes by `gamestate.GameState()`

*This is a proposed module that would offer a simple way to tag base-out states and align the info with Trackman data for more in-depth analysis*

`__init__()`
  - Initialized within the `GameState` object are:
    - `.runners` (a dictionary containing base states)
    - `.outs` (the number of outs)
    - `.score` (a dictionary containing home and away score)
    - `.errors_made` (an error tracker, a proposed way to track which runners are earned or unearned by pitcher)
   
### `Team`

`Team` object initializes by `team.Team(trackman_id)`

`__init__(trackman_id)`
  - `trackman_id` must be a team Trackman ID
    
  - Initialized within the `Team` object are:
    - `.trackman_id` (team's Trackman ID)

`.games()`
  - Returns a list of `Game` objects containing every game the team has played in from the database

`.toDatabase()`
  - Proposed method to directly add or alter a team's information in the database without a game file

`.pitchers()`
  - Returns a list of `Pitcher` objects containing every pitcher the team has in the database

`.batters()`
  - Returns a list of `Batter` objects containing every batter the team has in the database

`.catchers()`
  - Returns a list of `Catcher` objects containing every catcher the team has in the database

`.addPlayer()`
  - Proposed method to connect a player to a team in the database, possibly removing or altering his connecting with a previous team

`.writeBatterScouting()`
  - Proposed method to generate batter scouting reports for every batter connected to the team, in a similar fashion of the `writeBatterScouting` method

`.writePitcherScouting()`
  - Proposed method to generate pitcher scouting reports for every pitcher connected to the team

`.writeSprayCharts`
  - Proposed method to generate spray charts for every batter on the team

`.writeRunCards`
  - Proposed method to generate run game cards for every pitcher and catcher on the team

`.optimizeLineup`
  - Proposed method to generate lineup optimization based on team success and projected pitching matchups

### `Player`

*The `Player` module is broken up into four different classes: `Pitcher`, `Batter`, `Catcher`, `Baserunner`. All four objects share a parent class: `Player`*

#### `Player`

`Player` object initializes by player.Player(trackman_id)

`__init__(trackman_id)`
  - `trackman_id` must be a player Trackman ID

  - Initialized within the `Player` object are:
    - `.trackman_id` (player's Trackman ID)
    - `.conn` (connection to database {easier to write once and then `super().__init__(trackman_id)` for the child classes})
    - `.cur` (cursor to database)

#### `Pitcher`

`Pitcher` object initializes by `player.Pitcher(trackman_id)`

`__init__(trackman_id)`
  - `super().__init__(trackman_id)` (see parent `Player` class)
  - `.name` (pitcher's name as in Trackman)
  - `.player_id` (pitcher's database ID)
  - `.side` (pitcher's throwing side)
  - `.team_id` (pitcher's team's database ID)
  - `.team_name` (pitcher's team's name)
  - `.team_trackman` (pitcher's team's Trackman ID)

#### `Batter`

`Batter` object initializes by `player.Batter(trackman_id)`

`__init__(trackman_id)`
  - `super().__init__(trackman_id)` (see parent `Player` class)
  - `.name` (batter's name as in Trackman)
  - `.player_id` (batter's database ID)
  - `.side` (batter's hitting side)
  - `.team_id` (batter's team's database ID)
  - `.team_name` (batter's team's name)
  - `.team_trackman` (batter's team's Trackman ID)

`.probableStrikezone()`
  - A proposed method to use binary classification to estimate the height and width of the batter's strike zone

#### `Catcher`

`Catcher` object initializes by `player.Catcher(trackman_id)`

`__init__(trackman_id)`
  - `super().__init__(trackman_id)` (see parent `Player` class)
  - `.name` (catcher's name as in Trackman)
  - `.player_id` (catcher's database ID)
  - `.side` (catcher's throwing side)
  - `.team_id` (catcher's team's database ID)
  - `.team_name` (catcher's team's name)
  - `.team_trackman` (catcher's team's Trackman ID)

#### `Baserunner`

`Baserunner` object initializes by `player.Baserunner(trackman_id)`

`__init__(trackman_id)`
  - `super().__init__(trackman_id)` (see parent `Batter` class)

## Examples and Tutorials


## Configuration and Customization


## Troubleshooting and FAQs


## Contributing and Support


## License and Acknowledgments
