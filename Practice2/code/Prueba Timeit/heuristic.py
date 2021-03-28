"""Heuristics to evaluate board.

    Authors:
        Fabiano Baroni <fabiano.baroni@uam.es>,
        Alejandro Bellogin <alejandro.bellogin@uam.es>
        Alberto Suárez <alberto.suarez@uam.es>

"""


from __future__ import annotations  # For Python 3.7

from typing import Callable, Sequence

import numpy as np

from game import TwoPlayerGameState


class Heuristic(object):
    """Encapsulation of the evaluation fucnction."""

    def __init__(
        self,
        name: str,
        evaluation_function: Callable[[TwoPlayerGameState], float],
    ) -> None:
        """Initialize name of heuristic & evaluation function."""
        self.name = name
        self.evaluation_function = evaluation_function

    def evaluate(self, state: TwoPlayerGameState) -> float:
        """Evaluate a state."""
        # Prevent modifications of the state.
        # Deep copy everything, except attributes related
        # to graphical display.
        state_copy = state.clone()
        return self.evaluation_function(state_copy)

    def get_name(self) -> str:
        """Name getter."""
        return self.name


def simple_evaluation_function(state: TwoPlayerGameState) -> float:
    """Return a random value, except for terminal game states."""
    state_value = 2*np.random.rand() - 1
    if state.end_of_game:
        scores = state.scores
        # Evaluation of the state from the point of view of MAX

        assert isinstance(scores, (Sequence, np.ndarray))
        score_difference = scores[0] - scores[1]

        if state.is_player_max(state.player1):
            state_value = score_difference
        elif state.is_player_max(state.player2):
            state_value = - score_difference
        else:
            raise ValueError('Player MAX not defined')

    return state_value


def complex_evaluation_function(state: TwoPlayerGameState) -> float:
    """Return zero, except for terminal game states."""
    state_value = 0
    if state.end_of_game:
        scores = state.scores
        # Evaluation of the state from the point of view of MAX

        assert isinstance(scores, (Sequence, np.ndarray))
        score_difference = scores[0] - scores[1]

        if state.is_player_max(state.player1):
            state_value = score_difference
        elif state.is_player_max(state.player2):
            state_value = - score_difference
        else:
            raise ValueError('Player MAX not defined')
    else:
        successors = state.game.generate_successors(state)
        # Minimize the number of your opponent moves (for MAX).
        score_difference = - len(successors)
        if state.is_player_max(state.player1):
            state_value = score_difference
        elif state.is_player_max(state.player2):
            state_value = - score_difference

    return state_value


def dummy(state: TwoPlayerGameState) -> float:
    return 123 + 4


def our_evaluation_function(state: TwoPlayerGameState) -> float:
    pieces = eval_pieces(state)
    edges = eval_edges(state)
    corners = eval_corners(state)
    value = 0.4 * pieces + 0.4 * edges + 0.2 * corners

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
    board = state.board

    height = game.height
    width = game.width
    corners = [board.get((1, 1)), board.get((width, 1)),
               board.get((1, height)), board.get((width, height))]
    corners1 = corners.count(game.player1.label)
    corners2 = corners.count(game.player2.label)
    if corners1 + corners2 == 0:
        return 0
    return 100 * (corners1 - corners2) / (corners1 + corners2)


heuristic = Heuristic(
    name='Simple heuristic',
    evaluation_function=simple_evaluation_function,
)
heuristic2 = Heuristic(
    name='Complex heuristic',
    evaluation_function=complex_evaluation_function,
)
Heuristic1 = Heuristic(
    name='Heuristic1',
    evaluation_function=dummy,
)
OurHeuristic = Heuristic(
    name='OurHeuristic',
    evaluation_function=our_evaluation_function,
)
