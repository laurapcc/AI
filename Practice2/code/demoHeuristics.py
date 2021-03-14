"""Illustration of tournament.

Authors:
    Alejandro Bellogin <alejandro.bellogin@uam.es>

"""

from __future__ import annotations  # For Python 3.7

import numpy as np

from game import Player, TwoPlayerGameState, TwoPlayerMatch
from heuristic import simple_evaluation_function
from tictactoe import TicTacToe
from tournament import StudentHeuristic, Tournament
from reversi import (
    Reversi,
    from_array_to_dictionary_board,
    from_dictionary_to_array_board,
)


class PieceDifference(StudentHeuristic):

    def get_name(self) -> str:
        return "Piece difference heuristic"

    def evaluation_function(self, state: TwoPlayerGameState) -> float:
        scores = state.scores  # o score(state)[1]
        value = 100 * (scores[0] - scores[1]) / (scores[0] + scores[1])
        if state.is_player_max(state.player1):
            return value
        elif state.is_player_max(state.player2):
            return -value
        raise ValueError('Player MAX not defined')


class Mobility(StudentHeuristic):

    def get_name(self) -> str:
        return "Mobility"

    def evaluation_function(self, state: TwoPlayerGameState) -> float:
        """successors = state.generate_successor()
        if state.is_player_max(state.player1):
            return len(successors)
        elif state.is_player_max(state.player2):
            return -len(successors)
        raise ValueError('Player MAX not defined')"""
        if state.is_player_max(state.player1):
            return 1
        elif state.is_player_max(state.player2):
            return -1
        raise ValueError('Player MAX not defined')


class Corners(StudentHeuristic):

    def get_name(self) -> str:
        return "Corners"

    def evaluation_function(self, state: TwoPlayerGameState) -> float:
        game = state.game
        board = state.board
        assert isinstance(game, Reversi)  # only Reversi has height and width
        height = game.height
        width = game.width
        corners = [board.get((1, 1)), board.get((width, 1)),
                   board.get((1, height)), board.get((width, height))]
        corners1 = corners.count(game.player1.label)
        corners2 = corners.count(game.player2.label)
        if corners1 + corners2 == 0:
            return 0
        value = 100 * (corners1 - corners2) / (corners1 + corners2)
        if state.is_player_max(state.player1):
            return value
        elif state.is_player_max(state.player2):
            return -value
        raise ValueError('Player MAX not defined')


def create_match(player1: Player, player2: Player) -> TwoPlayerMatch:
    # Board at an intermediate state of the game.
    initial_board = (
        ['..B.B..',
         '.WBBW..',
         'WBWBB..',
         '.W.WWW.',
         '.BBWBWB']
    )

    # NOTE Uncoment to use standard initial board.
    # initial_board = None  # Standard initial board.

    if initial_board is None:
        height, width = 8, 8
    else:
        height = len(initial_board)
        width = len(initial_board[0])
        try:
            initial_board = from_array_to_dictionary_board(initial_board)
        except ValueError:
            raise ValueError('Wrong configuration of the board')
        else:
            print("Successfully initialised board from array")

    initial_player = player1

    game = Reversi(
        player1=player1,
        player2=player2,
        height=height,
        width=width,
    )

    game_state = TwoPlayerGameState(
        game=game,
        board=initial_board,
        initial_player=initial_player,
    )

    return TwoPlayerMatch(game_state, max_sec_per_move=5, gui=False)


tour = Tournament(max_depth=3, init_match=create_match)
strats = {'opt1': [PieceDifference], 'opt2': [Corners], 'opt3': [Corners]}

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

# print(totals)
# print(scores)

print('\t\ttotal:', end='')
for name1 in names:
    print('\t%s' % (name1), end='')
print()
for name1 in names:
    print('%s\t%d:' % (name1, totals[name1]), end='')
    for name2 in names:
        if name1 == name2:
            print('\t\t---', end='')
        else:
            print('\t\t%d' % (scores[name1][name2]), end='')
    print()
