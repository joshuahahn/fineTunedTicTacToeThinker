"""
Deep Learning for Computer Vision Final Project
November 22, 2023

Joshua Hahn jyh2134
Jimmy Zhang jz3443

Generates an annotated dataset of tic-tac-toe boards.

Intermediate board states are represented by a 3x3 array of numbers.
ex: [[001], [010], [220]]
Where 0 represents an empty tile, 1 represents an O tile, and 2
represents an X tile.

WLOG, we denote + scores as an edge in favor of O, and - scores as an
edge in favor of X. Scores are in [-1, 1] where a score of -1 or 1
represents a finished game (one person has won)
"""

def win(state):
    """Determines if the game is won, and if so, by who."""

    # Check horizontal & vertical wins
    for i in range(3):
        if state[i][0] == state[i][1] == state[i][2]:
            return 3 - (2 * state[i][0])
        if state[0][i] == state[1][i] == state[2][i]:
            return 3 - (2 * state[i][0])

    # Check diagonal wins
    if state[0][0] == state[1][1] == state[2][2]:
        return 3 - (2 * state[0][0])

    if state[0][2] == state[1][1] == state[2][0]:
        return 3 - (2 * state[0][2])

    # No winner yet
    return 0

def score(state):
    """Returns who is winning"""

    # First check if the game is already over
    res = win(state)
    if res != 0:
        return res

    # We'll be using a few heuristics to meausre the state of the game,
    # with weight assigned in the following order:
    # 1. Number of rows / diagonals / columns with 2 claimed cells and
    #    an empty slot in the remaining cell
    # 2. Number of rows / diagonals / colums with 1 claimed cell and
    #    two empty slots in the remaining cells
    # 3. Who's turn it is
