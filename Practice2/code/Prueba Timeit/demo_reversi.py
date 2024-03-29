"""Illustration of a Reversi match.

Authors:
    Fabiano Baroni <fabiano.baroni@uam.es>,
    Alejandro Bellogin <alejandro.bellogin@uam.es>
    Alberto Suárez <alberto.suarez@uam.es>

"""

from __future__ import annotations  # For Python 3.7
import timeit

from game import Player, TwoPlayerGameState, TwoPlayerMatch
from heuristic import (
    heuristic,
    Heuristic1,
    OurHeuristic,
)
from reversi import (
    Reversi,
    from_array_to_dictionary_board,
    from_dictionary_to_array_board,
)
from strategy import (
    ManualStrategy,
    MinimaxAlphaBetaStrategy,
    MinimaxStrategy,
    RandomStrategy,
)

player_manual = Player(
    name='Manual',
    strategy=ManualStrategy(verbose=0),
)

player_manual2 = Player(
    name='Manual_2',
    strategy=ManualStrategy(verbose=1),
)

player_random = Player(
    name='Random',
    strategy=RandomStrategy(verbose=0),
    delay=1,
)
player_random2 = Player(
    name='Random_2',
    strategy=RandomStrategy(verbose=1),
    delay=2,
)

player_minimax3 = Player(
    name='Minimax_3',
    strategy=MinimaxStrategy(
        heuristic=heuristic,
        max_depth_minimax=3,
        verbose=0,
    ),
)

player_minimax4 = Player(
    name='Minimax_4',
    strategy=MinimaxStrategy(
        heuristic=heuristic,
        max_depth_minimax=4,
        verbose=0,
    ),
)


player_alphaBeta = Player(
    name='AlphaBeta',
    strategy=MinimaxAlphaBetaStrategy(
        heuristic=heuristic,
        max_depth_minimax=3,
        verbose=0,
    ),
)

player_alphaBeta2 = Player(
    name='AlphaBeta_2',
    strategy=MinimaxAlphaBetaStrategy(
        heuristic=heuristic,
        max_depth_minimax=4,
        verbose=0,
    ),
)


"""""""""""""""""""""""""""""""""
        TIMEIT PLAYERS
"""""""""""""""""""""""""""""""""


timeMinMax1 = Player(
    name='timeMinMax1',
    strategy=MinimaxStrategy(
        heuristic=OurHeuristic,
        max_depth_minimax=3,
        verbose=0,
    ),
)

timeMinMax2 = Player(
    name='timeMinMax2',
    strategy=MinimaxStrategy(
        heuristic=OurHeuristic,
        max_depth_minimax=4,
        verbose=0,
    ),
)


timeAlphaBeta1 = Player(
    name='timeAlphaBeta1',
    strategy=MinimaxAlphaBetaStrategy(
        heuristic=OurHeuristic,
        max_depth_minimax=3,
        verbose=0,
    ),
)

timeAlphaBeta2 = Player(
    name='timeAlphaBeta2',
    strategy=MinimaxAlphaBetaStrategy(
        heuristic=OurHeuristic,
        max_depth_minimax=4,
        verbose=0,
    ),
)

# Time players
# player_a, player_b = timeMinMax1, timeMinMax2
player_a, player_b = timeAlphaBeta1, timeAlphaBeta2


# Manual vs manual player
# player_a, player_b = player_manual, player_manual2

# Manual vs minimax player
# player_a, player_b = player_manual, player_minimax4


# minimax vs minimax player
# player_a, player_b = player_minimax3, player_minimax4

# Minimax_AlphaBeta vs Minimax_AlphaBeta player
# player_a, player_b = player_alphaBeta, player_alphaBeta2


"""
Here you can initialize the player that moves first
and the board to any valid state.
E.g., it can be an intermediate state.
"""
initial_player = player_a  # Player who moves first.

# Board at an intermediate state of the game.
"""initial_board = (
    ['..B.B..',
     '.WBBW..',
     'WBWBB..',
     '.W.WWW.',
     '.BBWBWB']
)"""
initial_board = None

# NOTE Uncoment to use standard initial board.
# initial_board = None  # Standard initial board.

if initial_board is None:
    height, width = 6, 6
else:
    height = len(initial_board)
    width = len(initial_board[0])
    try:
        initial_board = from_array_to_dictionary_board(initial_board)
    except ValueError:
        raise ValueError('Wrong configuration of the board')
    else:
        print("Successfully initialised board from array")


# Initialize a reversi game.
game = Reversi(
    player1=player_a,
    player2=player_b,
    height=height,
    width=width,
)

# Initialize a game state.
game_state = TwoPlayerGameState(
    game=game,
    board=initial_board,
    initial_player=initial_player,
)

# Initialize a match.
match = TwoPlayerMatch(
    game_state,
    max_sec_per_move=1000,
    gui=False,              # True,
)

# Play match
scores = match.play_match()
# input('Press any key to finish.')

"""
# timeit command
reps = 2
tiempo = timeit.timeit("match.play_match()",
                       setup="from __main__ import match",
                       number=reps)
print(tiempo, tiempo/reps)
"""
