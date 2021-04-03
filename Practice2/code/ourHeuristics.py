###############################################
#                                             #
#        Heuristics for tournament            #
#                                             #
# Authors: Jorge de Miguel Pires              #
#          <jorge.miguelp@estudiante.uam.es>  #
#                                             #
#          Laura de Paz Carbajo               #
#          <laura.pazc@estudiante.uam.es>     #
# Team 07                                     #
# Group 2351                                  #
#                                             #
###############################################

import time
import numpy as np
from game import(
    TwoPlayerGameState,
    Player,
)

from tournament import StudentHeuristic
from reversi import Reversi



"""
Heuristic class whose evaluation function calculates the difference of each
player pieces with regard to the total amount of pieces placed in the board
"""


class PieceDifference(StudentHeuristic):

    def get_name(self) -> str:
        return "P07_Heuristic1"

    def evaluation_function(self, state: TwoPlayerGameState) -> float:
        value = eval_pieces(state)
        if state.is_player_max(state.player1):
            return value
        elif state.is_player_max(state.player2):
            return -value
        raise ValueError('Player MAX not defined')


"""
Heuristic class whose evaluation function calculates the amount of pieces each
player has on the edges of the board and computes its difference
"""


class Edges(StudentHeuristic):

    def get_name(self) -> str:
        return "P07_Heuristic2"

    def evaluation_function(self, state: TwoPlayerGameState) -> float:
        value = eval_edges(state)
        if state.is_player_max(state.player1):
            return value
        elif state.is_player_max(state.player2):
            return -value
        raise ValueError('Player MAX not defined')


"""
Heuristic class whose evaluation function calculates the amount of pieces each
player has on the corners of the board and computes its difference
A player should aim to capture these positions, as they can never be replaced
with the opponent's pieces.
"""


class Corners(StudentHeuristic):

    def get_name(self) -> str:
        return "P07_Heuristic3"

    def evaluation_function(self, state: TwoPlayerGameState) -> float:
        value = eval_corners(state)
        if state.is_player_max(state.player1):
            return value
        elif state.is_player_max(state.player2):
            return -value
        raise ValueError('Player MAX not defined')


"""
Heuristic class whose evaluation function calculates the amount of pieces each
player has on the edges and the corners of the board and computes its
difference
"""


class EdgesAndCorners(StudentHeuristic):

    def get_name(self) -> str:
        return "P07_Heuristic4"

    def evaluation_function(self, state: TwoPlayerGameState) -> float:
        """
        return Edges().evaluation_function(state) + \
            Corners().evaluation_function(state)
        """

        edges = eval_edges(state)
        corners = eval_corners(state)
        value = edges + corners

        if state.is_player_max(state.player1):
            return value
        elif state.is_player_max(state.player2):
            return -value
        raise ValueError('Player MAX not defined')


"""
Heuristic class whose evaluation function calculates the amount of pieces,
pieces in the edge of the bord and pieces in corners that both players
have and computes its difference
"""


class PiecesEdgesCorners(StudentHeuristic):
    def get_name(self) -> str:
        return "P07_Heuristic5"

    def evaluation_function(self, state: TwoPlayerGameState) -> float:
        pieces = eval_pieces(state)
        edges = eval_edges(state)
        corners = eval_corners(state)
        value = pieces + edges + corners

        if state.is_player_max(state.player1):
            return value
        elif state.is_player_max(state.player2):
            return -value
        raise ValueError('Player MAX not defined')


"""
Heuristic class whose evaluation function calculates the amount of pieces,
pieces in the edge of the bord and pieces in corners that both players
have and computes its difference and then gives each of these values a
specific weight when computing the final value
"""


class Weights(StudentHeuristic):
    def get_name(self) -> str:
        return "P07_Heuristic6"

    def evaluation_function(self, state: TwoPlayerGameState) -> float:
        pieces = eval_pieces(state)
        edges = eval_edges(state)
        corners = eval_corners(state)
        value = 0.4 * pieces + 0.4 * edges + 0.2 * corners

        if state.is_player_max(state.player1):
            return value
        elif state.is_player_max(state.player2):
            return -value
        raise ValueError('Player MAX not defined')


"""
Heuristic class whose evaluation function calculates the amount of pieces,
pieces in the edge of the bord and pieces in corners that both players
have and computes its difference and then gives each of these values a
specific weight when computing the final value depending on the stage
of the game
"""


class WeightsAndTimes(StudentHeuristic):
    def get_name(self) -> str:
        return "P07_Heuristic7"

    def evaluation_function(self, state: TwoPlayerGameState) -> float:
        pieces = eval_pieces(state)
        edges = eval_edges(state)
        corners = eval_corners(state)
        # ---- timessss ---
        turn = turn_number(state)

        if turn < 20:
            value = 0.2 * pieces + 0.4 * edges + 0.4 * corners
        elif 20 <= turn < 40:
            value = 0.4 * pieces + 0.4 * edges + 0.2 * corners
        else:
            value = 0.4 * pieces + 0.2 * edges + 0.4 * corners

        if state.is_player_max(state.player1):
            return value
        elif state.is_player_max(state.player2):
            return -value
        raise ValueError('Player MAX not defined')


"""
Heuristic class whose evaluation function calculates the amount of pieces,
pieces in the edge of the bord, pieces in corners and available moves that
both players have and computes its difference and then gives each of these
values a specific weight when computing the final value depending on the
stage of the game
"""


class WeightsAndTimes2(StudentHeuristic):
    def get_name(self) -> str:
        return "P07_Heuristic8"

    def evaluation_function(self, state: TwoPlayerGameState) -> float:
        pieces = eval_pieces(state)
        edges = eval_edges(state)
        corners = eval_corners(state)
        moves = num_possible_moves(state)
        turn = turn_number(state)

        if turn < 20:
            value = -0.1 * pieces + 0.5 * edges + 0.5 * corners + 0.1*moves
        elif 20 <= turn < 40:
            value = 0.1 * pieces + 0.4 * edges + 0.4 * corners + 0.1*moves
        else:
            value = 0.5 * pieces + 0.1 * edges + 0.2 * corners + 0.2*moves

        if state.is_player_max(state.player1):
            return value
        elif state.is_player_max(state.player2):
            return -value
        raise ValueError('Player MAX not defined')


# Private functions
def turn_number(state: TwoPlayerGameState) -> int:
    return state.scores[0] + state.scores[1] - 4


def eval_pieces(state: TwoPlayerGameState):
    scores = state.scores
    return 100 * (scores[0] - scores[1]) / (scores[0] + scores[1])


def eval_edges(state: TwoPlayerGameState):
    game = state.game
    board = state.board
    assert isinstance(game, Reversi)  # only Reversi has height and width
    height = game.height
    width = game.width

    edgeLeft = [board.get((x, 1)) for x in range(2, height)]
    edgeRight = [board.get((x, width)) for x in range(2, height)]
    edgeTop = [board.get((1, x)) for x in range(2, width)]
    edgeBottom = [board.get((height, x)) for x in range(2, width)]

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
    return 100 * (edges1 - edges2) / (edges1 + edges2)


def eval_corners(state: TwoPlayerGameState):
    game = state.game
    corners = get_corners(state)
    corners1 = corners.count(game.player1.label)
    corners2 = corners.count(game.player2.label)
    if corners1 + corners2 == 0:
        return 0
    return 100 * (corners1 - corners2) / (corners1 + corners2)


def get_corners(state: TwoPlayerGameState):
    game = state.game
    board = state.board
    assert isinstance(game, Reversi)  # only Reversi has height and width
    height = game.height
    width = game.width
    return [board.get((1, 1)), board.get((width, 1)),
            board.get((1, height)), board.get((width, height))]


# Returns the number of possible moves
def num_possible_moves(state: TwoPlayerGameState):
    return len(state.game._get_valid_moves(state.board,
                                           state.next_player.label))
