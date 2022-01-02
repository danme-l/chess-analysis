import chess.pgn 
import uuid
import numpy as np
import pandas as pd
import os


# path to where I store my data
data_dir = os.path.expanduser('~/Documents/code/chess-analysis/data/')

class ChessMachine():

    # random uuid to generate the games primary key
    NAMESPACE = uuid.UUID('{32a189be-b1c7-4021-b9a7-ef1795e9ed99}')

    # list of columns for the games dataframe
    columns = ['GameKey', 'Event', 'Site', 'Date', 'Round', 'White', 'Black', 'Result', 'BlackElo', 'BlackRatingDiff', 'ECO', 'Opening', 'Termination', 'TimeControl', 'UTCDate', 
'UTCTime', 'Variant', 'WhiteElo', 'WhiteRatingDiff', 'Game']

    def __init__(self, gameFile):
        """
        - The Chess machine must be initialized with a pgn file to one or more games
        - The games must have the headers defined by the columns list, other than the key (a unique ID created by ChessMachine.getGameRecord)
        - Also must finish with the games' moves
        """
        self.gameFile = gameFile


    def extractAllGames(self, gameFile, limit=None):
        """
        - Takes a filename (string)
        - Reads the file and stores every game object in a list
        - Optional: limit the number of games  
        """

        games = []

        print(f"Reading {gameFile}...")
        try:
            pgn = open(gameFile)
            
        except (Exception, FileNotFoundError) as error:
            print(error)


        print("Extracting games...")

        num = 0
        if limit==None:
            # read them all
            while chess.pgn.read_game(pgn) is not None:
                games.append(chess.pgn.read_game(pgn))

        else:
            # read to the limit
            while num <=limit:
                games.append(chess.pgn.read_game(pgn))
                num+=1

        pgn.close()
        print(f"File closed. Read {len(games)} games.")

        return games


    def getGameRecord(self, game):
        """
        - Takes the games dataframe and a chess game object as input
        - Uses a dictionary as a new row to be inserted 
        - Encodes the primary key
        - Adds the headers
        - Adds the game with result
        - Inserts the new row and returns the Dataframe 
        """

        # primary key is UUID5 composed of date, time, black, white
        # creates it based off a random UUID as the namespace
        # reproduceable this way
        if game is None:
            print("No more games.")
            return None
        
        new_game = {'GameKey': str(uuid.uuid5(self.NAMESPACE, f"{game.headers['UTCDate']}-{game.headers['UTCTime']}-{game.headers['Black']}-{game.headers['White']}"))}
        
        # insert information contained in game headers 
        for h in game.headers:
            new_game[h] = game.headers[h]
        
        # split opening and variation
        if ':' in new_game['Opening']:
            new_game['Variation'] = new_game['Opening'][new_game['Opening'].find(':')+2:]
            new_game['Opening'] = new_game['Opening'][:new_game['Opening'].find(':')]

        # insert the game moves + winner     
        new_game['Game'] = str(game.mainline()) + " " + game.headers['Result']

        return new_game


    def loadGames(self, games_list):
        """
        - Takes Games dataframe and list of game objects
        - Puts all the games from the list into the df 
        """
        print("Loading games...")

        games_df = pd.DataFrame(columns=self.columns)

        for game in games_list:
            # convert it to record in a dict, add it to the df
            if game is not None:
                games_df = games_df.append(self.getGameRecord(game), ignore_index=True)

        print(f"Loaded {len(games_list)} games.")

        return games_df
