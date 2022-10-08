# https://www.cs.iusb.edu/~danav/teach/c463/othello.py
# File: othello.el
# Athor: D. Vrajitoru
# C463 Artificial Intelligence
# March 2008

# An implementation of an agent capable of playing the game of Othello
# against a human, and the setup to be able to play the game.

dim = 8
board = []
directions = ['N', 'S', 'E', 'W', 'NE', 'NW', 'SE', 'SW']

# Initial state of the board
def init ():
    for i in range(dim):
        board.append([])
        for j in range(dim):
            board[i].append(0)
    board[3][3] = 1
    board[3][4] = -1
    board[4][3] = -1
    board[4][4] = 1

# Makes a copy of the current board and returns it.
def copy_board(b):
    newb = []
    for i in range(dim):
        newb.append([])
        for j in range(dim):
            newb[i].append(b[i][j])
    return newb

# Gives the directions in which the two coordinate increment for each
# of the 8 directions of movement. Incomplete - to be completed by
# the student.
def dir_move (dir):
    if dir == 'N':
        return -1, 0
    elif dir == 'E':
        return 0, 1
    elif dir == 'SW':
        return 1, -1
    else:
        return 1, 1

# Find out if by moving to position (i, j) we capture any of the
# opponents pieces in that direction of movement. This function
# returns the number of pieces of the opponent that can be captured
# this way, so that it can be used for evaluating the move in case you
# want to go only one level deep.
def find_opp_dir (b, i, j, who, dir):
    # di and dj are the increments for the row and column based on
    # the direction of movement
    di, dj = dir_move(dir)
    i1 = i + di
    j1 = j + dj
    tokens = 0
    # i1 and j1 are scanning indexes in the direction of
    # movement
    if not (i1 < dim and j1 >= 0 and j1 < dim):
        return 0
    # if the cell is not empty, return false
    if not (b[i][j] == 0 and b[i1][j1] == who * -1):
        return 0
    # while we're still on the board
    # and we haven't found one of our pieces
    while i1 >= 0 and i1 < dim and j1 >= 0 and j1 < dim:
        if b[i1][j1] == who * -1:
            # as long as we're on the opposite pieces
            # move in the directions di, dj
            i1 = i1 + di
            j1 = j1 + dj
            tokens += 1
        elif b[i1][j1] == who:
            # if we find our piece after a string of opponent pieces
            return tokens
        else:
            # if we run into a space return false
            return 0
    # If we ran out of the board we return false
    return 0

    
# Reverse all the opponents pieces in a given direction of
# movement. We can assume for this one that we already checked that
# we can capture something in that direction of movement.
def reverse_line_dir (b, i, j, who, dir):
    # to be completed by the student
    return True

# Compute the score for one particular player as the number of pieces
# on the board belonging to them minus the number of pieces belonging
# to the opponent.
def score (b, who):
    result = 0
    for i in range(dim):
        for j in range(dim):
            if b[i][j] == who:
                result += 1
            elif b[i][j] == who * -1:
                result -= 1
    return result


# Checks if the player "who" can play its token on the position
def move (b, i, j, who):
    # if the cell is not free, return nil.
    result = False
    if b[i][j] == 0:
        for dir in directions:
            # If we can capture anything in the direction of movement,
            # then we reverse all of the opponents pieces in that
            # direction and set the result to true. Since we never set
            # it back to false, if we can reverse anything from this
            # position, then the function will return true, otherwise
            # false.
            if find_opp_dir(b, i, j, who, dir):
                result = True
                reverse_line_dir(b, i, j, who, dir)
    # If the previous loop caused the result to be true, we set the
    # cell we're looking at to one of our pieces.
    if result :
        b[i][j] = who
    return result

# This function should return the two values i, j defining the
# position on the board of the next move of the player "who" based on
# the current situation on the board b. The function must return a
# legal move or -1, -1 if no move is possible for that player.
def next_move (b, who):
    # To be written by the student
    return -1, -1


# Print the board such that it's fairly easy to read.
def print_board (state):
    print "    0   1   2   3   4   5   6   7"
    print "  +---+---+---+---+---+---+---+---+"
    c = 0
    for i in range(dim):
        print i, "|",
        for j in range(dim):
            c = state[i][j]
            if c == 0:
                print " ",
            elif c == 1:
                print "*",
            else:
                print "O",
            print "|",
        print " "
        print "  +---+---+---+---+---+---+---+---+"


# Initial state of the board
#(print_board board)
##     0   1   2   3   4   5   6   7
##   +---+---+---+---+---+---+---+---+
## 0 |   |   |   |   |   |   |   |   |
##   +---+---+---+---+---+---+---+---+
## 1 |   |   |   |   |   |   |   |   |
##   +---+---+---+---+---+---+---+---+
## 2 |   |   |   |   |   |   |   |   |
##   +---+---+---+---+---+---+---+---+
## 3 |   |   |   | * | O |   |   |   |
##   +---+---+---+---+---+---+---+---+
## 4 |   |   |   | O | * |   |   |   |
##   +---+---+---+---+---+---+---+---+
## 5 |   |   |   |   |   |   |   |   |
##   +---+---+---+---+---+---+---+---+
## 6 |   |   |   |   |   |   |   |   |
##   +---+---+---+---+---+---+---+---+
## 7 |   |   |   |   |   |   |   |   |
##   +---+---+---+---+---+---+---+---+

# A function that find the best next move and does it. It also prints
# out what move it made. I added the parameter who so that we can play
# two programs against each other, so one will call this function with
# the parameter being 1, the other being -1.
def play_me(who):
    # Get the next move by calling the function
    i, j = next_move(board, who)
    if i >-1 and j>-1:
        print "My next move is:", i, j
        # Apply the move to the current board
        move(board, i, j, who)
    else:
        print "I have no move, pass"
    print_board (board)
    print "My score is:", score(board, who)

# This makes a move for the opponent. The parameters i and j are given
# in this case: the program of the other player will provide them. If
# the move cannot be made an error message will be given. This may not
# be a wrong move necessarily but a pass situation.
def play_other(i, j, who):
    if not move(board, i, j, who):
        print "Your move cannot be done, pass"
    print_board (board)
    print "Your score is:", score(board, who)

# Example of playing setup. One can import this module from the python
# console and then repeat the following except for the init() which
# should be called only once:

# Make sure to start from the initial state
# init()
# Repeat two function calls until there are no more moves:
# play_me(1)
# Replace i and j below with what your opponent's program gives you:
# play_other(i, j, -1)

if __name__ == '__main__':
    # This is only a test to see that the program works:
    init()
    print_board (board)
    # The next one works because I implemented the 'N' direction
    print move(board, 5, 3, 1)
    print score(board, 1)
    print_board (board)
    # The next one returns false because the 'W' direction is not yet
    # implemented.
    print move(board, 3, 5, 1)
    print_board (board)
