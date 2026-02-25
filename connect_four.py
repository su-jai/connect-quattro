import numpy as np
import copy
import random

# Config variables
X = 'X'
O = 'O'
EMPTY = "-"
height = 6
width = 7

def subarr(arr1, arr2):
    l1 = len(arr1)
    l2 = len(arr2)
    if l1 == l2:
        return arr1 == arr2
    
    elif l1 < l2:
        for i in range(l2 - l1 + 1):
            if arr2[i: i + l1] == arr1:
                return True

    elif l1 > l2:
        for i in range(l1 - l2 + 1):
            if arr1[i: i + l2] == arr2:
                return True
    
    return False


def winner(board):
        """
        Returns X if X wins and O if O wins and None if no winner
        """
        # Check rows
        for row in board:
            for i in range(width - 4):
                if np.array_equal(row[i:i+4], np.array([X,X,X,X])):
                    return X
                elif np.array_equal(row[i:i+4], np.array([O,O,O,O])):
                    return O
                
        # Check columns
        for row in np.rot90(board):
            for i in range(width - 4):
                if np.array_equal(row[i:i+4], np.array([X,X,X,X])):
                    return X
                elif np.array_equal(row[i:i+4], np.array([O,O,O,O])):
                    return O
        
        # Top row:
        for i in range(width):
            # Check left
            diag = [board[j][i - j] for j in range(min(height, i + 1))]
            l = len(diag)
            if subarr(diag, [X,X,X,X]) and l > 3:
                return X
            elif subarr(diag, [O,O,O,O]) and l > 3:
                return O
            
            # Check right
            diag = [board[j][i + j] for j in range(min(height, width - i))]            
            l = len(diag)
            if subarr(diag, [X,X,X,X]) and l > 3:
                return X
            elif subarr(diag, [O,O,O,O]) and l > 3:
                return O
                
        # Left edge
        for i in range(1, height):
            # Check right
            diag = [board[i + j][j] for j in range(min(width, height - i))]            
            l = len(diag)
            if subarr(diag, [X,X,X,X]) and l > 3:
                return X
            elif subarr(diag, [O,O,O,O]) and l > 3:
                return O

        # Right edge
        for i in range(1, height):
            # Check left
            diag = [board[i + j][width - 1 - j] for j in range(min(height - i, width))]        
            l = len(diag)
            if subarr(diag, [X,X,X,X]) and l > 3:
                return X
            elif subarr(diag, [O,O,O,O]) and l > 3:
                return O

        return None


def add_token(board, player, col):
    """
    Adds a token to the board and returns new board
    """
    new_board = copy.deepcopy(board)
    if new_board[0][col] != EMPTY:
        raise ValueError("column is full")
    if player not in {X,O}:
        raise ValueError("set player to either X or O")
    for i in range(height):
        if new_board[i][col] != EMPTY:
            new_board[i - 1][col] = player
            return new_board
        elif i == height - 1:
            new_board[i][col] = player
            return new_board


def actions(board):
    """
    Returns which moves are possible given a board
    """
    actions = set()
    for col in range(width):
        if board[0][col] == EMPTY:
            actions.add(col)
    return actions


def player(board):
    """
    Returns which player has the next turn
    For simplicity X always starts first
    """
    no_tokens = 0
    for i in range(height):
        for j in range(width):
            if board[i][j] in {X,O}:
                no_tokens += 1

    if no_tokens % 2 == 0:
        return X
    else:
        return O
    

def terminal(board):
    """
    Given a board class returns True or False if it is a terminal state or not
    """
    if (winner(board) in {X, O}) or (actions(board) == set()):
        return True
    
    else:
        return False
    

def utility(board):
    """
    Given a board returns it's utility
    """
    if not terminal(board):
        raise ValueError("Not a terminal state")
    
    elif winner(board) == X:
        return 1

    elif winner(board) == O:
        return (-1)

    else:
        return 0


def max_value(board, depth):
    """
    Recursively generates the max value out of 
    the next possible moves for the maximizing player
    """
    v = -np.inf
    if terminal(board):
        return utility(board)
    
    elif depth > 2:
        return 0
    
    for action in actions(board):
        v = max(v, min_value(add_token(board, X, action), depth + 1))
    return v
    

def min_value(board, depth):
    """
    Recursively generates the min value out of 
    the next possible moves for the minimizing player
    """
    v = np.inf
    if terminal(board):
        return utility(board)
    
    elif depth > 2:
        return 0
    
    for action in actions(board):
        v = min(v, max_value(add_token(board, O, action), depth + 1))
    return v


board =  np.array([[EMPTY]*7]*6)
while not terminal(board):
    # Ask user (player X) to add a token. Check for correct user input.
    user_move = None
    while user_move not in range(width):   
        user_in = input("Enter move: ")
        if user_in.isdigit():
            user_move = int(user_in)
        else:
            print(f"Please enter a column number 0-{width-1}")
            user_move = None

    board = add_token(board, player(board), user_move)

    # AI looks at resulting game state and evaluates min value (since AI is playing O)
    # AI then makes the move corresponding to that min value, updating the board
    
    minval = min_value(board, 0)

    next_player = player(board)

    # add a random chance that the AI makes a random move
    r = random.random()
    if r < 0.3 :
        print("I'm a crazy AI making a random move!")
        board = add_token(board, next_player, random.choice(list(actions(board))))

    else:
        for action in actions(board):
            if max_value(add_token(board, next_player, action), 0) == minval:
                board = add_token(board, next_player, action)
                break

    # if the resulting state is a terminal state print the board and winner and exit while loop
    if terminal(board) and winner(board) == O:
        print(board)
        print("AI wins!")

    elif terminal(board) and winner(board) == X:
        print(board)
        print("Player wins!")
        
    # else print the board
    else:
        print(board)









