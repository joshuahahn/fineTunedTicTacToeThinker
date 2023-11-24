"""
Deep Learning for Computer Vision Final Project
November 22, 2023

Joshua hahn jyh2134
Jimmy Zhang jz3443

Generates an annotated dataset of tic tac toe boards.
"""

import scorer

def generateIntermediate(n=3):
    """ Generates valid intermediate board representations.  """

    boards = []
    seen = set() # keep track of duplicate boards by storing each board state as a string

    # 0 represents an empty tile, 1 represents an O tile, and 2 represents an X tile.
    def dfs(curr_board, x_turn):
        # terminate after finding a board in a won or drawn state
        if scorer.win(curr_board) or scorer.draw(curr_board):
            return

        for row in range(n):
            for col in range(n):
                # find empty square
                if not curr_board[row][col]:
                    # insert either an X or an O depending on whose turn it is
                    if x_turn:
                        curr_board[row][col] = 2
                    else:
                        curr_board[row][col] = 1
                    
                    if str(curr_board) not in seen:
                        boards.append([[curr_board[row][col] for col in range(n)] for row in range(n)])
                        seen.add(str(curr_board))

                    dfs(curr_board, not x_turn)
                    curr_board[row][col] = 0 # reset square after recursing

    starting_board = [[0 for _ in range(n)] for _ in range(n)]
    boards.append(starting_board)
    seen.add(str(starting_board))
    dfs(starting_board, True) # assume X plays first

    return boards

def generateDataset():
    """ Generates an annotated dataset of tic tac toe boards.  """
<<<<<<< HEAD

generateDataset(generateIntermediate())
=======
    pass
>>>>>>> ba3da700b574f981378352b5c9627034ce7822a9
