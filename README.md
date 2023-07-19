# rylar_baseball Library Documentation

**Please note that documentation is a work in progress, as is the rest of the library**

## Introduction
The **rylar_baseball** library was created to ease the handling of Trackman Baseball data. The library reads in game files, writes them to SQL, and creates relevant objects to make tool building and data visualization easier. The key objects provided by the library, include **Game**, **Inning**, **AtBat**, **Pitch**, **Team**, **Player**, etc. The library assigns all relevant Trackman data to each instance of these objects allowing database querying to be as simple as accessing a batter's average exit velocity with **sample_batter.avg_ev**.

## Installation
**rylar_baseball** library is currently not availble for download. Upon a workable project this will be updated. Currently **rylar_baseball** is only intended for private use by its owner.

## Getting Started
Importing **rylar_baseball** library into a Python script is as easy as **from** rylar_baseball **import** *. Reading in a Trackman CSV is as easy as: 

```game1 = game.Game()

game1.loadCSV('csv//raw_trackman_file.csv').```

The Game class has methods such as **toDatabase()**, **updateStats()**, **writeBatterReports()**, **writePitcherReports()**, and more.

## Data Handling
Explanation of how the **rylar_baseball** library converts raw Trackman Baseball CSV data into objects. Overview of the key classes provided by the library, such as **Game**, **Player**, **Team**, etc. Usage examples demonstrating how to work with these objects and access their attributes.

## API Reference
**Game**
- `loadCSV(csv, writeData=True)`
  - Reads in Trackman csv initializing basic attributes:
    - `data` (pandas dataframe of game data)
    - `stadium` (Trackman stadium name)
    - `league` (Trackman level name)
    - `division` (Trackman league name)
    - `trackman_id` (Trackman GameID)
    - `date` (date of game)
    - `year` (year of game)
    - `time` (time of first pitch)
    - `home` (initializes Team object for home team)
    - `away` (initializes Team object for away team)
    - `timestamp` (time of file upload)
  - If `writeData` is set to the default True value then:
    - `toDatabase()` and `updateStats()` will run automatically
- `loadDF(csv, writeData=True)`
- `loadID(game_id)`
- `innings(top_bottom)`
- `batters()`
- `catchers()`
- `pitchers()`
- `adjustZone(stadium_id)`
- `pitcherStatline(pitcher_id)`
- `movementPlot(pitcher_id, view='pitcher')`
- `toDatabase()`
- `writeBatterReports(team_id)`
- `writePitcherReports(team_id)`
- `updateStats()`

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
