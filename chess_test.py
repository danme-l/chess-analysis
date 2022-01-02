import numpy as np
import pandas as pd
import os
import uuid
from chessETL import ChessMachine

# path to where I store my data
data_dir = os.path.expanduser('~/Documents/code/chess-analysis/data/')

# Chess Machine Instance
chesser = ChessMachine(data_dir + 'all_blitz_games_251221.pgn')

# Bring in 30 games
games_list = chesser.extractAllGames(data_dir + 'all_blitz_games_251221.pgn',limit=30)

chess_games = chesser.loadGames(games_list)

# games into a csv if I want
# chess_games.to_csv(data_dir+'my_blitz_games_251221.csv' , index=False)

# print out a few columns of the dataframe
print(chess_games[['Opening','Variation']])
