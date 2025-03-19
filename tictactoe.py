"""
Tic Tac Toe AI with Minimax Algorithm
"""

import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns the starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns the player who has the next turn on a board.
    """
    x_count = sum(row.count(X) for row in board)
    o_count = sum(row.count(O) for row in board)
    return X if x_count <= o_count else O


def actions(board):
    """
    Returns a set of all possible actions (i, j) available on the board.
    """
    return {(i, j) for i in range(3) for j in range(3) if board[i][j] == EMPTY}


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if board[action[0]][action[1]] is not EMPTY:
        raise ValueError("Invalid move: Cell already occupied")

    new_board = [row[:] for row in board]  # Copy board
    new_board[action[0]][action[1]] = player(board)
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for mark in (X, O):
        # Check rows and columns
        for i in range(3):
            if all(board[i][j] == mark for j in range(3)) or all(board[j][i] == mark for j in range(3)):
                return mark
        
        # Check diagonals
        if all(board[i][i] == mark for i in range(3)) or all(board[i][2 - i] == mark for i in range(3)):
            return mark

    return None  # No winner yet


def terminal(board):
    """
    Returns True if the game is over, False otherwise.
    """
    return winner(board) is not None or all(cell is not EMPTY for row in board for cell in row)


def utility(board):
    """
    Returns 1 if X has won, -1 if O has won, 0 otherwise.
    """
    win = winner(board)
    return 1 if win == X else -1 if win == O else 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None  # Game is over

    turn = player(board)
    
    if turn == X:
        best_val = -math.inf
        best_move = None
        for action in actions(board):
            val = min_value(result(board, action))
            if val > best_val:
                best_val = val
                best_move = action
    else:
        best_val = math.inf
        best_move = None
        for action in actions(board):
            val = max_value(result(board, action))
            if val < best_val:
                best_val = val
                best_move = action
    
    return best_move


def max_value(board):
    """
    Maximizing player's move (X)
    """
    if terminal(board):
        return utility(board)
    
    v = -math.inf
    for action in actions(board):
        v = max(v, min_value(result(board, action)))
    return v


def min_value(board):
    """
    Minimizing player's move (O)
    """
    if terminal(board):
        return utility(board)
    
    v = math.inf
    for action in actions(board):
        v = min(v, max_value(result(board, action)))
    return v

