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
from game import TwoPlayerGameState

from tournament import StudentHeuristic
from reversi import Reversi



"""
Heuristic class whose evaluation function calculates the difference of each
player pieces with regard to the total amount of pieces placed in the board
"""


class PieceDifference(StudentHeuristic):

    def get_name(self) -> str:
        return "Piece_difference"

    def evaluation_function(self, state: TwoPlayerGameState) -> float:
        """
        scores = state.scores
        value = 100 * (scores[0] - scores[1]) / (scores[0] + scores[1])
        """
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
        return "Edges"

    def evaluation_function(self, state: TwoPlayerGameState) -> float:
        """
        game = state.game
        board = state.board
        assert isinstance(game, Reversi)  # only Reversi has height and width
        height = game.height
        width = game.width

        edgeLeft = [board.get((x, 1)) for x in range(1, height+1)]
        edgeRight = [board.get((x, width)) for x in range(1, height+1)]
        edgeTop = [board.get((1, x)) for x in range(1, width+1)]
        edgeBottom = [board.get((height, x)) for x in range(1, width+1)]

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
        """
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
        return "Corners"

    def evaluation_function(self, state: TwoPlayerGameState) -> float:
        """
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
        """
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
        return "EdgesAndCorners"

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
        return "PiecesEdgesCorners"

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
Heuristic class that ---------
"""

class Weights1(StudentHeuristic):
    def get_name(self) -> str:
        return "Weights1"

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
Heuristic class that ---------
"""

class WeightsAndTimes(StudentHeuristic):
    def get_name(self) -> str:
        return "Weights1"

    def evaluation_function(self, state: TwoPlayerGameState) -> float:
        pieces = eval_pieces(state)
        edges = eval_edges(state)
        corners = eval_corners(state)
        # ---- timessss ---
        value = 0.4 * pieces + 0.4 * edges + 0.2 * corners

        if state.is_player_max(state.player1):
            return value
        elif state.is_player_max(state.player2):
            return -value
        raise ValueError('Player MAX not defined')



"""
Heuristic class that ---------
"""

class Stability(StudentHeuristic):
    def get_name(self) -> str:
        return "Stability"

    def evaluation_function(self, state: TwoPlayerGameState) -> float:
        value = eval_stability(state)

        if state.is_player_max(state.player1):
            return value
        elif state.is_player_max(state.player2):
            return -value
        raise ValueError('Player MAX not defined')


# Private functions
def eval_pieces(state):
    scores = state.scores
    return 100 * (scores[0] - scores[1]) / (scores[0] + scores[1])


def eval_edges(state):
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


def eval_corners(state):
    game = state.game
    corners = get_corners(state)
    # corners = [board.get((1, 1)), board.get((width, 1)),
    #           board.get((1, height)), board.get((width, height))]
    corners1 = corners.count(game.player1.label)
    corners2 = corners.count(game.player2.label)
    if corners1 + corners2 == 0:
        return 0
    return 100 * (corners1 - corners2) / (corners1 + corners2)


def get_corners(state):
    game = state.game
    board = state.board
    assert isinstance(game, Reversi)  # only Reversi has height and width
    height = game.height
    width = game.width
    return [board.get((1, 1)), board.get((width, 1)),
            board.get((1, height)), board.get((width, height))]


def eval_stability(state):
    stable1 = player_stability(state, state.game.player1)
    stable2 = player_stability(state, state.game.player2)
    #print("stable1 =",stable1, "  stable2 =",stable2)

    if stable1 + stable2 == 0:
        return 0
    return 100 * (stable1 - stable2) / (stable1 + stable2)


def player_stability(state, player):
    game = state.game
    board = state.board
    corners = get_corners(state)
    # no corners captured => no stable pieces
    captured_corners = corners.count(player.label)
    if captured_corners == 0:
        return 0

    assert isinstance(game, Reversi)  # only Reversi has height and width
    width, height = game.width, game.height

    stab_matrix = np.zeros((height, width))
    stab_pieces = []
    # check corners captured by player
    for row in [1, height]:
        for col in [1, width]:
            if board.get((row, col)) == player.label:
                stab_matrix[row-1][col-1] = 1
                stab_pieces.append((row, col))

    while stab_pieces:
        piece = stab_pieces.pop()
        for pos in neighbours(height, width, piece):
            y, x = pos
            if stab_matrix[y][x] == 1:
                continue
            if board.get(pos) == player.label:
                if is_stable(pos, stab_matrix):
                    stab_matrix[y][x] = 1
                    stab_pieces.append(pos)

    # count stable pieces in matrix
    return np.sum(stab_matrix)


def neighbours(height, width, pos):
    adjacent = []
    y, x = pos
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            if dx == 0 and dy == 0:
                continue  # same position
            col, row = x + dx, y + dy
            if (col >= 0 and col < width) and (row >= 0 and row < height):
                adjacent.append((row, col))
    return adjacent


def is_stable(pos, matrix):
    x, y = pos
    height, width = len(matrix), len(matrix[0])

    def horizontal():
        return x <= 0 or x >= width-1 or \
            matrix[y-1][x-2] == 1 or matrix[y-1][x] == 1

    def vertical():
        return y <= 0 or y >= height-1 or \
            matrix[y-2][x-1] == 1 or matrix[y][x-1] == 1

    def diag_neg():
        return x <= 0 or x >= width-1 or \
            y <= 0 or y >= height-1 or \
            matrix[y-2][x-2] == 1 or matrix[y][x] == 1

    def diag_pos():
        return x <= 0 or x >= width-1 or \
            y <= 0 or y >= height-1 or \
            matrix[y][x-2] == 1 or matrix[y-2][x] == 1

    return horizontal() and vertical() and diag_neg() and diag_pos()


""" Funcion Jorge
def pieceIsStable(state, piece):
    game = state.game
    board = state.board
    assert isinstance(game, Reversi)  # only Reversi has height and width
    height = game.height
    width = game.width
    corners = [board.get((1, 1)), board.get((width, 1)),
               board.get((1, height)), board.get((width, height))]

    if board.get(piece) in corners:
        return True

    x = piece[0]
    y = piece[1]
    if x == 0:
        closePieces = []
    return False

"""
