import time
import multiprocessing
from strategies import *


# request {'request': 'play',
# 'lives': 3,
# 'errors': [],
# 'state': {
#   'players': ['mehdi', 'ali'],
#   'current': 0,
#   'board': [[28, 35], [27, 36]]}
#  }
# board en entrée, retourner les cases possibles ou on peut jouer
# board de départ :
# 1ére liste : Noir
# 2éme liste : Blanc

# BOARD
# 00 01 02 03 04 05 06 07
# 08 09 10 11 12 13 14 15
# 16 17 18 19 20 21 22 23
# 24 25 26 27 28 29 30 31
# 32 33 34 35 36 37 38 39
# 40 41 42 43 44 45 46 47
# 48 49 50 51 52 53 54 55
# 56 57 58 59 60 61 62 63


def play(request, alg):
    board = request['state']['board']
    currentPlayer = request['state']['current']
    players = request['state']['players']
    player = players[currentPlayer]

    # Liste des coups possibles
    legalMoves = list(get_legal_moves(board, currentPlayer))
    move = None
    message = ''

    if alg == 'random':
        move, message = random_strategy(legalMoves)

    elif alg == 'weight':
        if len(legalMoves) == 0:  # s'il ne reste aucune possibilité, jouer None
            move = None
        elif len(legalMoves) == 1:  # s'il ne reste qu'une seule possibilité, la jouer
            move = legalMoves[0]
        else:
            move = weight_strategy(legalMoves)

        message = 'weight_maximise : ' + str(move)

    elif alg == 'humain':
        move, message = humain(legalMoves)

    elif alg == 'minimax':
        tic = time.perf_counter()
        if len(legalMoves) == 0:  # s'il ne reste aucune possibilité, jouer None
            move = None
        elif len(legalMoves) == 1:  # s'il ne reste qu'une seule possibilité, la jouer
            move = legalMoves[0]
        else:
            # Vérifier si un corner se trouve dans la liste
            try:
                best_move = getCorner(legalMoves)[0]
            # Sinon effectuer une recherche en profondeur avec l'algorithme minimax
            except:
                # nbr cases vides ?
                # empty = get_count_empty(board)
                DEPTH = 3
                best_val = -1000000
                best_move = None
                for move in legalMoves:
                    new_board = play_move(board, move, currentPlayer)

                    # p = multiprocessing.Process(target=minimax, name="Foo", args=(currentPlayer, new_board, DEPTH, False, -1000000, 1000000))
                    # p.start()
                    # # Wait 10 seconds for foo
                    # time.sleep(5)
                    # # Terminate foo
                    # p.terminate()
                    # # Cleanup
                    # p.join()

                    # move_val = minimax(currentPlayer, new_board, DEPTH, False, -1000000, 1000000)
                    if move_val > best_val:
                        best_val = move_val
                        best_move = move

            move = best_move

        toc = time.perf_counter()
        message = 'minimax alogrithm, best move is ' + str(move) + f", time : {toc - tic:0.4f} seconds"
        print('------------------------------------------------------')
        print(player, ' plays ', move, f" in {toc - tic:0.4f} seconds")
        print('-----------------------------------------------------')

    play = {
        "response": "move",
        "move": move,
        "message": message
    }
    return play
