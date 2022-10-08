import random
from utils import *


# Humain
def humain(legalMoves):
    print('legalmoves : ', legalMoves)
    move = input('move choice:  ?')
    message = 'humain :' + move
    try:
        move = int(move)
    except:
        move = None

    return move, message


# Random
def random_strategy(legalMoves_list):
    try:  # si liste n'est pas vide ==> random dans la site
        move = random.choice(legalMoves_list)
        message = "random :" + str(move)
        move = int(move)
    except:  # si liste vide ==> exception error
        print('Liste vide')
        move = None
        message = 'None'

    return move, message


Weights = [
    [500,   -100,   100,    50, 50, 100, -100, 500],
    [-50,   -100,    -5,    -5, -5, -5, -100, -50],
    [100,     -5,     5,    0, 0, 5, -5, 100],
    [50,      -5,     0,       1, 1, 0, -5, 50],
    [50,      -5,     0,       1, 1, 0, -5, 50],
    [100,     -5,     5,    0, 0, 5, -5, 100],
    [-50,    -75,    -5,    -5, -5, -5, -100, -50],
    [500,   -100,   100,    50, 50, 100, -100, 500]
]


def get_Weight(index):
    row, col = get_coordinates(index)
    weight = Weights[row][col]
    return weight


# Local Maximization
def weight_strategy(legalMoves_list):
    score = -9999
    move = None
    for cell in legalMoves_list:
        weight = get_Weight(cell)
        if weight > score:
            score = weight
            move = cell
    return move


# MiniMax
def play_move(board, move, current):
    '''
    :param board: Actual board
    :param move: next move
    :param current: witch player
    :return: the new board
    '''
    playerColors = set(board[current])
    otherColors = board[abs(current - 1)]
    for direction in directions:
        cells_to_flip = set()
        for cell in avancer(move, direction):
            if cell in otherColors:
                cells_to_flip.add(cell)
            elif cell in playerColors:
                if len(cells_to_flip) > 0:
                    playerColors = playerColors.union(cells_to_flip)
                    otherColors = [x for x in otherColors if (x not in cells_to_flip)]
                break
            else:
                break

    playerColors.add(move)
    if current == 0:
        newboard = [list(playerColors), otherColors]
    else:
        newboard = [otherColors, list(playerColors)]
    return newboard


def evaluation(board, current):
    evaluation = 0
    playerColors = board[current]
    otherColors = board[abs(current - 1)]

    for cell in playerColors:
        evaluation += get_Weight(cell)

    for cell in otherColors:
        evaluation -= get_Weight(cell)

    return evaluation


def minimax(playerIndex, board, depth, maximizingPlayer, alpha, beta):
    otherPlayerIndex = (playerIndex + 1) % 2
    if depth == 0 or isGameOver(board):
        return evaluation(board, current=playerIndex)

    if maximizingPlayer:
        maxEval = -1000000
        legal_Moves = get_legal_moves(board, playerIndex)
        if len(legal_Moves) == 0:
            maxEval = minimax(playerIndex, board, depth, False, alpha, beta)
        else:
            for move in legal_Moves:
                # play move , get new board
                newBoard = play_move(board, move, playerIndex)
                eval = minimax(playerIndex, newBoard, depth - 1, False, alpha, beta)
                maxEval = max(maxEval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
        return maxEval

    else:
        minEval = 100000
        legal_Moves = get_legal_moves(board, otherPlayerIndex)
        if len(legal_Moves) == 0:
            minEval = minimax(playerIndex, board, depth, True, alpha, beta)
        else:
            for move in legal_Moves:
                # play move , get new board
                newBoard = play_move(board, move, otherPlayerIndex)
                eval = minimax(playerIndex, newBoard, depth - 1, True, alpha, beta)
                minEval = min(minEval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
        return minEval
