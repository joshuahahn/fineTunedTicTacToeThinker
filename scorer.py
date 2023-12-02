"""
Deep Learning for Computer Vision Final Project
November 22, 2023

Joshua Hahn jyh2134
Jimmy Zhang jz3443

Scores tic tac toe board states.

Intermediate board states are represented by a 3x3 array of numbers.
ex: [[001], [010], [220]]
Where 0 represents an empty tile, 1 represents an O tile, and 2
represents an X tile.

WLOG, we use +1 to denote a winning state for O, -1 to denote a winning
state for X, and 0 to denote a (roughly) tied state.
"""

def win(state):
    """ Determines if the game is won, and if so, by who. """

    # Check horizontal & vertical wins
    for i in range(3):
        if state[i][0] != 0 and state[i][0] == state[i][1] == state[i][2]:
            return state[i][0]
        if state[0][i] != 0 and state[0][i] == state[1][i] == state[2][i]:
            return state[0][i]

    # Check diagonal wins
    if state[0][0] != 0 and state[0][0] == state[1][1] == state[2][2]:
        return state[0][0]

    if state[0][2] != 0 and state[0][2] == state[1][1] == state[2][0]:
        return state[0][2]

    # No winner yet
    return 0

def draw(state):
    """ Determines if a game is drawn """

    # Check if game is already won
    if win(state):
        return False

    for row in range(len(state)):
        for col in range(len(state[0])):
            # If there is an empty square, there is a playable move.
            if state[row][col] == 0:
                return False

    return True

def score(state):
    """ Returns who is winning. 0: tied, 1: O is winning, 2: X is winning """

    # First check if the game is already over
    res = win(state)
    if res != 0:
        return res

    # We'll be using a few heuristics to meausre the state of the game,
    # with weight assigned in the following order:
    # 1. Number of rows / diagonals / columns with 2 claimed cells and
    #    an empty slot in the remaining cell. If there is such a row and
    #    it is that player's turn, we return that they are winning.
    # 2. Number of rows / diagonals / colums with 1 claimed cell and
    #    two empty slots in the remaining cells
    # 3. Who's turn it is

    tileCount = 0
    for row in state:
        for cell in row:
            if cell == 1:
                tileCount += 1
            elif cell == 2:
                tileCount -= 1

    if tileCount == 0:
        turn = "X"
    else:
        turn = "O"

    lines = []
    for i in range(3):
        lines.append(([state[0][i], state[1][i], state[2][i]]))
        lines.append(([state[i][0], state[i][1], state[i][2]]))

    lines.append(([state[0][0], state[1][1], state[2][2]]))
    lines.append(([state[0][2], state[1][1], state[2][0]]))
    
    for line in lines:
        if 0 in line:
            lineSum = sum(line)
            if 1 in line:
                if lineSum == 2: 
                    if turn == 'O':
                        return 1
                    res += 10  # 2 in a line, O
                elif lineSum == 1: res += 5 # 1 in a line, O
            if 2 in line:
                if lineSum == 4:
                    if turn == 'X':
                        return 2
                    
                    res -= 10  # 2 in a line, X
                elif lineSum == 2: res -= 5 # 1 in a line, X

    if abs(res) <= 5:
        return 0
    elif res > 5:
        return 1
    else:
        return 2
