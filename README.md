# rylar_baseball Library Documentation

**Please note that documentation is a work in progress, as is the rest of the library**

## Introduction
The **rylar_baseball** library was created to ease the handling of Trackman Baseball data. The library reads in game files, writes them to SQL, and creates relevant objects to make tool building and data visualization easier. The key objects provided by the library, include **Game**, **Inning**, **AtBat**, **Pitch**, **Team**, **Player**, etc. The library assigns all relevant Trackman data to each instance of these objects allowing database querying to be as simple as accessing a batter's average exit velocity with **sample_batter.avg_ev**.

## Installation
**rylar_baseball** library is currently not availble for download. Upon a workable project this will be updated. Currently **rylar_baseball** is only intended for private use by its owner.

## Getting Started
Importing **rylar_baseball** library into a Python script is as easy as `from rylar_baseball import *`

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

`Inning` object initializes by `inning.Inning()`

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

`AtBat` object initializes by `atbat.AtBat()`

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

`Pitch` object initializes by `pitch.Pitch()`


## Examples and Tutorials
Step-by-step tutorials demonstrating common use cases of the **rylar_baseball** library. In-depth examples showcasing advanced features and functionality. Interactive code snippets for users to try out different scenarios.

## Configuration and Customization
Documentation on any configuration options or settings available in the library. Instructions for customizing the behavior of the library based on user requirements. Best practices and recommendations for optimal configuration.

## Troubleshooting and FAQs
Common issues users may encounter when working with the **rylar_baseball** library. Troubleshooting steps and solutions for resolving these issues. Frequently asked questions and their corresponding answers.

## Contributing and Support
Guidelines for users who want to contribute to the **rylar_baseball** library. Information on how to report bugs, suggest new features, or submit pull requests. Contact details for getting support or assistance with the library.

## License and Acknowledgments
Licensing information for the **rylar_baseball** library. Acknowledgment and credits to any external libraries or resources used.
