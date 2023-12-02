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

from PIL import Image
import os
from matplotlib import pyplot as plt

import torch
from torch.utils.data import TensorDataset
from torch.utils.data import DataLoader
from torchvision.transforms import ToTensor

# Global variables for generating images.
lineDistribution = [0.10, 0.40, 0.40, 0.10]
tileDistribution = [0.01, 0.14, 0.35, 0.35, 0.14, 0.01]
tilePositions = [[(1,1),  (1,12),  (1,21) ], \
                 [(12,1), (12,12), (12,21)], \
                 [(21,1), (21,12), (21,21)]]
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
    labels = []
    for i, state in enumerate(states):
        if i % 1000 == 0:
            print("State {}".format(i))

        score = scorer.score(state)

        # Add 3 versions of the same board
        for _ in range(3):
            images.append(torch.from_numpy(generateImage(state)))
            labels.append(score)

    data = TensorDataset(torch.stack(images), torch.Tensor(labels))
    print("Finished, dataset length: " + str(len(data)))
    torch.save(data, './data.pt')

def generateImage(state):
    """ Generates an image based on an intermediate step.  """
    board = np.zeros((28,28))

    # First add the horizontal lines. Refer to the tile heatmap for
    # distributions of the lines and tiles.

    line = horizontalLines[rand.choice(len(horizontalLines))]
    startRow = 8 + rand.choice(a=4, p=lineDistribution)

    for i in range(2):
        for j in range(28):
            board[i+startRow][j] += line[i][j]

    line = horizontalLines[rand.choice(len(horizontalLines))]
    startRow = 18 + rand.choice(a=4, p=lineDistribution)

    for i in range(2):
        for j in range(28):
            board[i+startRow][j] += line[i][j]

    # Now add the vertical lines.
    line = verticalLines[rand.choice(len(verticalLines))]
    startCol = 8 + rand.choice(a=4, p=lineDistribution)

    for i in range(28):
        for j in range(2):
            board[i][j+startCol] = max(board[i][j+startCol], line[i][j])

    line = verticalLines[rand.choice(len(verticalLines))]
    startCol = 18 + rand.choice(a=4, p=lineDistribution)

    for i in range(28):
        for j in range(2):
            board[i][j+startCol] = max(board[i][j+startCol], line[i][j])

    # Now add the tiles one by one.
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                continue
            elif state[i][j] == 1:
                tile = Os[rand.choice(len(Os))]
            elif state[i][j] == 2:
                tile = Xs[rand.choice(len(Xs))]

            startRow, startCol = tilePositions[i][j]
            startRow += rand.choice(a=6, p=tileDistribution)
            startCol += rand.choice(a=6, p=tileDistribution)

            for y in range(5):
                for x in range(5):
                    if startRow + y >= 28 or startCol + x >= 28:
                        break

                    board[startRow+y][startCol+x] = max(board[startRow+y][startCol+x], tile[y][x])

    # Make sure all values are in [0, 1]
    for i in range(28):
        for j in range(28):
            board[i][j] = 1 - min(board[i][j], 255) / 255

    #board = np.asarray([board[:], board[:], board[:]])
    board  = np.asarray([board[:]])

    return board

def importImages():
    Xdir = 'images/Xs/'
    Odir = 'images/Os/'
    horizontal_dir = 'images/horizontal/'
    vertical_dir = 'images/vertical/'

    directories = [Xdir, Odir, horizontal_dir, vertical_dir]
    image_arrays = [Xs, Os, horizontalLines, verticalLines]

    for i in range(4):
        for filename in os.listdir(directories[i]):
            if not filename[0].isnumeric():
                continue
            f = os.path.join(directories[i], filename)

            if os.path.isfile(f):
                image = Image.open(f).convert('L')
                image_array = np.asarray(image)
                image_arrays[i].append(image_array)


importImages()
generateDataset(generateIntermediate())