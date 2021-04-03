"""Illustration of tournament.
Authors:
    Alejandro Bellogin <alejandro.bellogin@uam.es>
"""

from __future__ import annotations  # For Python 3.7

import numpy as np

from game import Player, TwoPlayerGameState, TwoPlayerMatch
from heuristic import simple_evaluation_function
from tournament import StudentHeuristic, Tournament
from reversi import (
    Reversi,
    from_array_to_dictionary_board,
)
from ourHeuristics import(
    PieceDifference,
    Corners,
    Edges,
    EdgesAndCorners,
    PiecesEdgesCorners,
    Weights,
    WeightsAndTimes,
    WeightsAndTimes2,
)


def create_match(player1: Player, player2: Player) -> TwoPlayerMatch:
    initial_player = player1

    game = Reversi(
        player1=player1,
        player2=player2,
        height=6,
        width=6,
    )

    game_state = TwoPlayerGameState(
        game=game,
        board=None,
        initial_player=initial_player,
    )

    return TwoPlayerMatch(game_state, max_sec_per_move=6000, gui=False)


tour = Tournament(max_depth=3, init_match=create_match)
strats = {'opt1': [PieceDifference], 'opt2': [Edges],
          'opt3': [Corners], 'opt4': [EdgesAndCorners],
          'opt5': [PiecesEdgesCorners], 'opt6': [Weights],
          'opt7': [WeightsAndTimes], 'opt8': [WeightsAndTimes2]}

n = 3
scores, totals, names = tour.run(
    student_strategies=strats,
    increasing_depth=False,
    n_pairs=n,
    allow_selfmatch=False,
)

print(
    'Results for tournament where each game is repeated '
    + '%d=%dx2 times, alternating colors for each player' % (2 * n, n),
)

print('\t\t\ttotal:', end='')
for name1 in names:
    print('\t%s' % (name1), end='')
print()
for name1 in names:
    if len(name1) > 18:
        print('%s\t%d:' % (name1, totals[name1]), end='')
    else:
        print('%s\t\t%d:' % (name1, totals[name1]), end='')
    for name2 in names:
        if name1 == name2:
            print('\t\t---', end='')
        else:
            print('\t\t%d' % (scores[name1][name2]), end='')
    print()
