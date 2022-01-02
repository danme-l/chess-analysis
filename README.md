# chess-analysis

Tool in progress to upload and analyze chess games.

## ChessMachine
The chessETL.py file currently contains a single class ChessMachine. It takes a pgn file with multiple games and uses the [python-chess](https://python-chess.readthedocs.io/en/latest/) library to read it into a list of Game objects, optionally with a limited number of Games (default No limit, it'll read until the end of the file).

Tranformations:
* Generates a primary key using uuid's to uniquely define every game in a record from the time, date, and players. 
* Splits the Opening into seperate columns for Opening and Variation of that opening.
* Adds a column for the actual game notation.

The transformations are done in the getGameRecord() function. The loadGames() function will call getGameRecord() for each record and load it into a pandas DataFrame.

## EDA
Jupyter notebook where I'll be doing an exploratory data analysis of all of the blitz that I have played on lichess up to and including December 25, 2021. This is in progress and will be done as time permits. The purpose of this is mostly testing and exploring so the tool can be expanded for use.
