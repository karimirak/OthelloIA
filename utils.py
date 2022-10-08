directions = [
    (0, -1),  # Up
    (1, -1),  # Up-Right
    (1, 0),  # Right
    (1, 1),  # Down-Right
    (0, 1),  # Down
    (-1, 1),  # Down-Left
    (-1, 0),  # Left
    (-1, -1),  # Up-Left
]


# BOARD
# 00 01 02 03 04 05 06 07
# 08 09 10 11 12 13 14 15
# 16 17 18 19 20 21 22 23
# 24 25 26 27 28 29 30 31
# 32 33 34 35 36 37 38 39
# 40 41 42 43 44 45 46 47
# 48 49 50 51 52 53 54 55
# 56 57 58 59 60 61 62 63

# Vérifier si les coordonnées sont à l'intérieur du plateau 8*8
def is_inside(row, col):
    '''
    :param row: ligne
    :param col: colonne
    :return boolean: True si row et col sont à l'intérieur du board
    '''
    return 0 <= row < 8 and 0 <= col < 8


# Retourner les coordonnées row, col à partir d'un numéro index
def get_coordinates(index):
    '''
    :param index: l'index de la case (entre 0 et 63)
    :return: les coordonnées à partir de l'index
    '''
    return index // 8, index % 8


# Retourner un index entre 0 et 63 à partir des coordonnées row, col
def get_index(row, col):
    '''
    :param row: ligne
    :param col: colonne
    :return: l'index sur le board
    '''
    return row * 8 + col


# retourner True si l'index dans le board est un corner
def isCorner(index):
    if index in [0, 7, 56, 63]:
        return True
    return False


# Vérifier si une liste de possibilité contient un corner, si oui le retourner
def getCorner(legalMoves_list):
    corner = list({*[0, 7, 56, 63]} & {*legalMoves_list})
    return corner


# retourner le nombre de cases vides
def get_count_empty(board):
    return 64 - (len(board[0]) + len(board[1]))


def isGameOver(board):
    # Si aucun coup n'est possible pour les joueurs, gameOver
    black_legal_moves = get_legal_moves(board, 0)
    white_legal_moves = get_legal_moves(board, 1)
    if black_legal_moves or white_legal_moves:
        return False
    return True


def avancer(tile, direction):
    currentTile = tile
    row, col = get_coordinates(currentTile)
    while is_inside(row + direction[0], col + direction[1]):
        row = row + direction[0]
        col = col + direction[1]
        currentTile = get_index(row, col)
        yield currentTile


def get_legal_moves(board, playerIndex):
    otherPlayerIndex = (playerIndex + 1) % 2  # si indexPlayer= 0 ==> otherPlayer = 1 sinon otherPlayer = 0
    legalMoves = set()
    for case in board[playerIndex]:
        for direction in directions:
            tiles_in_line = []
            for cell in avancer(case, direction):
                tiles_in_line.append(cell)
            # tiles_in_line.pop()

            continuer = False
            for tile in tiles_in_line:  # pour chaque case dans la liste de la direction
                # Vérifier si la case est de meme couleur ou non ==> board[0] ou board[1].
                # si case de couleur différente ==> continuer

                if tile in board[otherPlayerIndex]:
                    continuer = True
                # si de meme couleur
                elif tile in board[playerIndex]:
                    # garder la tile en mémoire et continuer vers la suivante
                    break
                # sinon, la case est vide.
                else:
                    if continuer:
                        legalMoves.add(tile)
                    break
    return legalMoves
