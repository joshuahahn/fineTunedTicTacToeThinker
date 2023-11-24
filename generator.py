"""
Deep Learning for Computer Vision Final Project
November 22, 2023

Joshua hahn jyh2134
Jimmy Zhang jz3443

Generates an annotated dataset of tic tac toe boards.
"""

import scorer
import numpy as np
import numpy.random as rand

# Global variables for generating images.
lineDistribution = [0,1,1,2,2,3]
tileDistribution = [0,1,1,1,2,2,2,2,3,3,3,3,4,4,4,5]
tilePositions = [[(1,1),  (1,12),  (1,21) ], \
                 [(12,1), (12,12), (12,21)], \
                 [(21,1), (21,12), (21,21)]
horizontalLines = []
verticalLines = []
Xs= []
Os = []

def generateIntermediate(n=3):
    """ Generates valid intermediate board representations.  """

    # Keep track of duplicate boards by storing each state as a string
    boards = []
    seen = set()

    # 0: empty tile, 1: O tile, 2: X tile
    def dfs(curr_board, x_turn):
        # Terminate after finding a board in a won or drawn state
        if scorer.win(curr_board) or scorer.draw(curr_board):
            return

        for row in range(n):
            for col in range(n):
                # Find empty square
                if not curr_board[row][col]:
                    # Insert an X or an O depending on whose turn it is
                    if x_turn:
                        curr_board[row][col] = 2
                    else:
                        curr_board[row][col] = 1

                    if str(curr_board) not in seen:
                        boards.append([[curr_board[row][col] for col in range(n)] for row in range(n)])
                        seen.add(str(curr_board))

                    dfs(curr_board, not x_turn)
                    curr_board[row][col] = 0 # Reset square

    starting_board = [[0 for _ in range(n)] for _ in range(n)]
    boards.append(starting_board)
    seen.add(str(starting_board))
    dfs(starting_board, True) # Assume X plays first

    return boards

def generateDataset(states):
    """ Generates an annotated dataset of tic tac toe boards.  """

    # We represent images as a 28x28 np array with values in [0, 255].
    # We create these images by first drawing a board, then adding
    # 5x5 tiles where the image should be. We apply noise so that there
    # is some shifting with the cells, creating noise.
    # Finally, we add gaussian blurring and extra noise throughout the
    # image to (1) prevent overfitting and (2) make the sample space
    # more interesting.

    # With the generateIntermediate function with n=3, we have a total of
    # 5478 boards. Generating 3 images from each state gives us
    # 5478 * 2 = 16434 images to train over.

    images = []
    for state in states:
        images.append((generateImage(state), scorer.score(state)))

    return images

def generateImage(state):
    """ Generates an image based on an intermediate step.  """
    board = np.zeros((28,28))

    # First add the horizontal lines. Refer to the tile heatmap for
    # distributions of the lines and tiles.
    line = rand.choice(horizontalLines)
    startRow = 8 + rand.choice(lineDistribution)

    for i in range(2):
        for j in range(9):
            board[i+startRow][j] += line[i][j]

    line = rand.choice(horizontalLines)
    startRow = 18 + rand.choice(lineDistribution)

    for i in range(2):
        for j in range(9):
            board[i+startRow][j] += line[i][j]

    # Now add the vertical lines.
    line = rand.choice(verticalLines)
    startCol = 8 + rand.choice(lineDistribution)

    for i in range(9):
        for j in range(2):
            board[i][j+startCol] += line[i][j]

    line = rand.choice(verticalLines)
    startCol = 18 + rand.choice(lineDistriution)

    for i in range(9):
        for j in range(2):
            board[i][j+startCol] += line[i][j]

    # Now add the tiles one by one.
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                continue
            elif state[i][j] == 1:
                tile = rand.choice(Os)
            elif state[i][j] == 2:
                tile = rand.choice(Xs)

            startRow, startCol = tilePositions[i][j]
            startRow += rand.choice(tileDistribution)
            startCol += rand.choice(tileDistribution)

            for y in range(5):
                for x in range(5):
                    if startRow + y >= 28 or startCol + x >= 28:
                        break

                    board[startRow+y][startCol+x] += tile[y][x]

    return board

generateDataset(generateIntermediate())
