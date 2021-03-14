"""Heuristics for tournament.

Authors:
    Jorge de Miguel Pires <jorge.miguelp@estudiante.uam.es>
    Laura de Paz Carbajo <laura.pazc@estudiante.uam.es>

"""

import time
from game import TwoPlayerGameState

from tournament import StudentHeuristic
from reversi import Reversi


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

"""
class Mobility(StudentHeuristic):

    def get_name(self) -> str:
        return "Mobility heuristic"

    def evaluation_function(self, state: TwoPlayerGameState) -> float:
        successors = state.generate_successor()
        if state.is_player_max(state.player1):
            return len(successors)
        elif state.is_player_max(state.player2):
            return -len(successors)
        raise ValueError('Player MAX not defined')
"""


class Edges(StudentHeuristic):

    def get_name(self) -> str:
        return "Mobility heuristic"

    def evaluation_function(self, state: TwoPlayerGameState) -> float:
        game = state.game
        board = state.board
        assert isinstance(game, Reversi)  # only Reversi has height and width
        height = game.height
        width = game.width

        # COMPROBAR QUE LAS X, WIDTH, HEIGHT Y LIMITES DEL RANGE ESTEN BIEN
        edgeLeft = [board.get((x, 0)) for x in range(0, height)]
        edgeRight = [board.get((x, width)) for x in range(0, height)]
        edgeTop = [board.get((0, x)) for x in range(0, width)]
        edgeBottom = [board.get((height, x)) for x in range(0, width)]

        edges1 = edgeLeft.count(game.player1.label) + \
            edgeRight.count(game.player1.label) + \
            edgeTop.count(game.player1.label) + \
            edgeBottom.count(game.player1.label)

        edges2 = edgeLeft.count(game.player2.label) + \
            edgeRight.count(game.player2.label) + \
            edgeTop.count(game.player2.label) + \
            edgeBottom.count(game.player2.label)

        if edges1 + edges2 == 0:
            return 0
        value = 100 * (edges1 - edges2) / (edges1 + edges2)
        if state.is_player_max(state.player1):
            return value
        elif state.is_player_max(state.player2):
            return -value
        raise ValueError('Player MAX not defined')


class Corners(StudentHeuristic):

    def get_name(self) -> str:
        return "Corners heuristic"

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
