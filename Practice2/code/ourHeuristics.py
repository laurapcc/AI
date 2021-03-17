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
        value = evalPieces(state)
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
        value = evalEdges(state)
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
        value = evalCorners(state)
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

        edges = evalEdges(state)
        corners = evalCorners(state)
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
        pieces = evalPieces(state)
        edges = evalEdges(state)
        corners = evalCorners(state)
        value = pieces + edges + corners

        if state.is_player_max(state.player1):
            return value
        elif state.is_player_max(state.player2):
            return -value
        raise ValueError('Player MAX not defined')


# Private functions
def evalPieces(state):
    scores = state.scores
    return 100 * (scores[0] - scores[1]) / (scores[0] + scores[1])


def evalEdges(state):
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


def evalCorners(state):
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
    return 100 * (corners1 - corners2) / (corners1 + corners2)

"""
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