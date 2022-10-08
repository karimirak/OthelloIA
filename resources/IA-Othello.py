"""
    Decroix Clément
    2022-02-19

    TP IA
    "Le Jeu D'Othello"

"""

# On import random pour le tirage ne nombre aléatoire
import copy
from random import *
import time


# -------------------------------------------------------------------------
# --------                    Fonctions                              ------
# -------------------------------------------------------------------------

def init_plateau(x, y):
    """ Fonction d'initialisation d'un plateau de jeu d'othello de taille (x,y)
        (Ici cela correspond à une matrice (x,y) remplit de " " caractère vide)
        Où x et y sont la taille du plateau (x la longueur et y la hauteur)
    """

    return ([[" " for i in range(x)] for j in range(y)])


def init_pion(plateau, numero):
    """ Fonction d'initialisation des pions sur le "plateau" vide
        selon différente forme définit grace à "numéro".
        Où "plateau" est une matrice de taille supérieur à 2 pour x et y
        et "numéro" est un entier compris en 1 et 2.
    """
    xSize, ySize = len(plateau), len(plateau[0])

    if (numero == 1):  # PREMIERE DISPOSITION DE PION
        plateau[xSize // 2 - 1][ySize // 2 - 1] = "☺"
        plateau[xSize // 2][ySize // 2 - 1] = "☻"
        plateau[xSize // 2 - 1][ySize // 2] = "☻"
        plateau[xSize // 2][ySize // 2] = "☺"
        return plateau

    elif (numero == 2):  # DEUXIEME DISPOSITION DE PION
        plateau[xSize // 2 - 1][ySize // 2 - 1] = "☻"
        plateau[xSize // 2][ySize // 2 - 1] = "☺"
        plateau[xSize // 2 - 1][ySize // 2] = "☺"
        plateau[xSize // 2][ySize // 2] = "☻"
        return plateau

    elif (numero == 3):
        for i in range(len(plateau)):
            for j in range(len(plateau[0])):
                plateau[i][j] = "☺"
        plateau[0][7] = "☻"
        plateau[1][7] = "☻"
        plateau[2][7] = "☻"
        plateau[4][6] = "☻"
        plateau[5][0] = "☻"
        plateau[5][1] = "☻"
        plateau[5][5] = "☻"
        plateau[5][6] = "☻"
        plateau[7][3] = "☻"
        plateau[7][4] = "☻"
        plateau[7][5] = "☻"

        plateau[1][6] = " "
        plateau[3][6] = " "
        plateau[3][7] = " "
        plateau[6][0] = " "
        plateau[6][1] = " "
        plateau[7][0] = " "
        plateau[7][2] = " "
        plateau[7][6] = " "

        return plateau


def afficher_plateau(plateau):
    """ Fonction d'affichage du plateau de jeu
        Où "pleateau" est une matrice de taille quelconque
    """

    xSize, ySize = len(plateau), len(plateau[0])
    affichage = ""
    # affichage = "_" * (xSize * 2 + 1) + "\n"

    for ligne in plateau:
        affichage += "|"
        for valeur in ligne:
            affichage += '%2s' % valeur + "|"
        affichage += "\n"

    # affichage = "\0332".join(affichage)
    print(affichage)


def coup_possible(plateau, pion_a_attaquer, pion_a_defendre):
    """ Fonction retournant le "plateau" avec les différentes possibilité
        de jeu pour le joueur possédant le "pion_a_defendre" pour prendre
        les "pion_a_attaquer" ainsi que le nombre de coups possible (donc m).
        Où "plateau" est une matrice de taille supérieur à 2 pour x et y
        et "pion_attaque" le pion du joueur pour lequel on veut attaquer
        et "pion_defence" le pion du joueur pour lequel on veut défendre.
    """
    m = 0  # nb_coup_possible
    for i in range(len(plateau)):
        for j in range(len(plateau[0])):
            if (plateau[i][j] == pion_a_defendre):
                # print("pion détécter en (" + str(i) + " , " + str(j) + ")")  #Commentaire de test et de compréhension

                # Ici on recherche dans les 8 directions si un coup est possible à l'opposé
                # recherche() + ajout()
                for k in range(-1, 2):
                    for l in range(-1, 2):
                        if not (k == 0 and l == 0):  # On ne cherche pas sur lui-même
                            # print("  On est pour k=" + str(k) + " et l=" + str(l))  #Commentaire de test et de compréhension
                            n = 1

                            while (i + (k * n) >= 0 and i + (k * n) < len(plateau) and j + (l * n) >= 0 and j + (
                                    l * n) < len(plateau[0])  # exeption si l'on sort du tableau
                                   and plateau[i + (k * n)][j + (l * n)] == pion_a_attaquer  # Si on saut un pion
                            ):
                                n += 1
                            # end while
                            if (i + (k * n) >= 0 and i + (k * n) < len(plateau) and j + (l * n) >= 0 and j + (
                                    l * n) < len(plateau[0])  # exeption si l'on sort du tableau
                                    and plateau[i + (k * n)][j + (l * n)] == " " and n >= 2
                            # n>=2 SINIFIE QUE L'ON SAUT AU MOINS 1 PION A ATTAQUER
                            ):
                                m += 1
                                # print(" Ajout de " + str(m) + " sur (" + str(i+(k*n)) + " , " + str(j+(l*n)) + ")" ) #Commentaire de test et de compréhension
                                plateau[i + (k * n)][j + (l * n)] = m
    return (plateau, m)


def jouer_numero(plateau, pion, numero):
    """ Fonction retournant le "plateau" en jouant (ajoutant) le pion
        "pion" en paramètre sur le numéro "numero" donnée par la fonction
        "coup_possible".
        Où "plateau" est une matrice de taille supérieur à 2 pour x et y avec les coups possible
        où "pion" un caractère à ajouter sur la case "numero"
        où "numéro" un entier dans plateau.
    """
    for i in range(len(plateau)):
        for j in range(len(plateau[0])):
            if (plateau[i][j] == numero):  # SI plateau[i][j] EST L'ENTIER A REMPLACER
                plateau[i][j] = pion
                # Ici on recherche dans les 8 directions pour modifier les pions attaqué
                for k in range(-1, 2):
                    for l in range(-1, 2):
                        if not (k == 0 and l == 0):  # On ne cherche pas sur lui-même
                            n = 1

                            while (i + (k * n) >= 0 and i + (k * n) < len(plateau) and j + (l * n) >= 0 and j + (
                                    l * n) < len(plateau[0])  # exeption si l'on sort du tableau
                                   and plateau[i + (k * n)][j + (l * n)] != pion and plateau[i + (k * n)][
                                       j + (l * n)] != " "  # Si on est sur un pion allié donc on peut modifier
                                   and not (isinstance(plateau[i + (k * n)][j + (l * n)], int))
                            ):
                                n += 1
                            # end while
                            if (i + (k * n) >= 0 and i + (k * n) < len(plateau) and j + (l * n) >= 0 and j + (
                                    l * n) < len(plateau[0])  # exeption si l'on sort du tableau
                                    and plateau[i + (k * n)][j + (l * n)] == pion and n >= 2
                            # n>=2 SINIFIE QUE L'ON SAUT AU MOINS 1 PION A ATTAQUER
                            ):
                                for m in range(n):  # sur toute la ligne on modifie les pion modifié
                                    # print(" Ajout de " + pion + " sur (" + str(i+(k*m)) + " , " + str(j+(l*m)) + ")" ) #Commentaire de test et de compréhension
                                    plateau[i + (k * m)][j + (l * m)] = pion
    return plateau


def supprimer_coup_possible(plateau):
    """ Fonction retournant le "plateau" en enlevant les coups possibles
        (donc les entier ;) ).
        Où "plateau" est une matrice de taille supérieur à 2 pour x et y.
    """
    for i in range(len(plateau)):
        for j in range(len(plateau[0])):
            if (isinstance(plateau[i][j], int)):  # SI plateau[i][j] EST UN ENTIER
                plateau[i][j] = " "
    return plateau


def est_plein(plateau):
    """ Fonction retournant un Boolean annoncant si le "plateau" en
        paramètre est plein.
        (donc ne possède pas d'espace ;) ).
        Où "plateau" est une matrice de taille supérieur à 2 pour x et y.
    """
    for i in range(len(plateau)):
        for j in range(len(plateau[0])):
            if (plateau[i][j] == " " or isinstance(plateau[i][j], int)):
                return False
    return True


def compter_pion(plateau, pion1, pion2):
    """ Fonction retourne d'abord le nombre de "pion1" puis de
        "pion2" sur le "plateau" en paramètre.
        Où "plateau" est une matrice de taille supérieur à 2 pour x et y.
    """
    nb_pion1 = 0
    nb_pion2 = 0
    for i in range(len(plateau)):
        for j in range(len(plateau[0])):
            if (plateau[i][j] == pion1):
                nb_pion1 += 1
            elif (plateau[i][j] == pion2):
                nb_pion2 += 1
    return (nb_pion1, nb_pion2)


""""MATRICE DE POSITION POUR OBTENIR LA VALEUR TACTIQUE DE CHAQUE PION"""
matrice_de_valeur_tactiques = [[500, -150, 30, 10, 10, 30, -150, 500],
                               [-150, -250, 0, 0, 0, 0, -250, -150],
                               [30, 0, 1, 2, 2, 1, 0, 30],
                               [10, 0, 2, 16, 16, 2, 0, 10],
                               [10, 0, 2, 16, 16, 2, 0, 10],
                               [30, 0, 1, 2, 2, 1, 0, 30],
                               [-150, -250, 0, 0, 0, 0, -250, -150],
                               [500, -150, 30, 10, 10, 30, -150, 500]]


def evaluation_positionnel(plateau, pion_du_joueur, pion_adverse):
    """ Fonction retournant l'évaluation du plateau en fonction de la stratégie
        positionnel.
        l’évaluation est la différence entre les poids associés des deux joueurs.
        Où "plateau" est une matrice de taille x et y et avec les coups possible.
        où "pion_du_joueur" un caractère caractérisant le pion du joueur.
        où "pion_adverse" un caractère caractérisant le pion adverse.
    """
    evaluation = 0
    for i in range(len(plateau)):
        for j in range(len(plateau[0])):
            if (plateau[i][j] == pion_du_joueur):
                evaluation += matrice_de_valeur_tactiques[i][j]
            elif (plateau[i][j] == pion_adverse):
                evaluation -= matrice_de_valeur_tactiques[i][j]
    return evaluation


def min_max_ordi_positionnel(min_or_max, plateau, pion_de_lordi, pion_adverse, profondeur, nb_coup_joueur1,
                             nb_coup_joueur2):
    """ Fonction min-max retournant la "valeur"  tactique (pour la récursivité) ainsi que
        le "nombre_a_jouer" après analyse suivant le profondeur pour "le pion_de_lordi"
        sur un des numéros avec la stratégie POSITIONNEL.
        POSITIONNEL : prise en compte des poids statique du tableau (Cf. cours),
        l’évaluation est la différence entre les poids associés des deux joueurs.
        Où "plateau" est une matrice de taille x et y superieur ou égal à 1
        et avec les coups possibles.
        où "pion_de_lordi" un caractère définisant le pion de l'ordi.
        où "pion_adverse" un caractère définisant le pion adverse.
        où "profondeur" un entier définisant la profondeur de l'analyse de l'IA.
        où "nb_coup_joueur1" un entier définisant le nombre de coup du joueur1.
        où "nb_coup_joueur2" un entier définisant le nombre de coup du joueur2.
            C'est 2 "nb_coup_joueur" servent a définir l'arrêt du jeu.
    """
    nombre_a_jouer = -1
    if (est_plein(plateau) == True or (nb_coup_joueur1 == 0 and nb_coup_joueur2 == 0) or profondeur <= 0):
        # Temps que ce n'est pas fini, afficher_plateau(plateau)      #Test : Vérification de toutes les posibilités
        return evaluation_positionnel(plateau, pion_de_lordi, pion_adverse), 0

    if (min_or_max == "max"):
        valeur = -10000
        if (nb_coup_joueur1 == 0):  # Si l'IA ne peut pas jouer alors
            plateau_bis = copy.deepcopy(plateau)  # Réalise une deep copy du plateau de jeu
            # On simule le fait que l'on ne jou pas (donc on fait rien)
            plateau_bis = supprimer_coup_possible(plateau_bis)
            plateau_bis, nb_coup_joueur2 = coup_possible(plateau_bis, pion_de_lordi, pion_adverse)

            result, _ = min_max_ordi_positionnel("min", plateau_bis, pion_de_lordi, pion_adverse, profondeur - 1,
                                                 nb_coup_joueur1, nb_coup_joueur2)
            valeur = max(valeur, result)
            return valeur, nombre_a_jouer

        else:
            for i in range(len(plateau)):
                for j in range(len(plateau[0])):
                    if (isinstance(plateau[i][j], int)):  # SI plateau[i][j] EST UN ENTIER // DONC UN COUP POSSIBLE

                        plateau_bis = copy.deepcopy(plateau)  # Réalise une deep copy du plateau de jeu
                        plateau_bis = jouer_numero(plateau_bis, pion_de_lordi,
                                                   plateau[i][j])  # On simule le fait que l'on jou sur la case
                        plateau_bis = supprimer_coup_possible(plateau_bis)
                        plateau_bis, nb_coup_joueur2 = coup_possible(plateau_bis, pion_de_lordi, pion_adverse)

                        result, _ = min_max_ordi_positionnel("min", plateau_bis, pion_de_lordi, pion_adverse,
                                                             profondeur - 1, nb_coup_joueur1, nb_coup_joueur2)
                        ancien_valeur = valeur
                        valeur = max(valeur, result)
                        if (valeur != ancien_valeur):  # si la valeur à changé alors on joue sur ce numéro
                            nombre_a_jouer = plateau[i][j]

            return valeur, nombre_a_jouer



    elif (min_or_max == "min"):
        valeur = 10000
        if (nb_coup_joueur2 == 0):  # Si l'IA ne peut pas jouer alors
            plateau_bis = copy.deepcopy(plateau)  # Réalise une deep copy du plateau de jeu
            # On simule le fait que l'on ne jou pas (donc on fait rien)
            plateau_bis = supprimer_coup_possible(plateau_bis)
            plateau_bis, nb_coup_joueur1 = coup_possible(plateau_bis, pion_adverse, pion_de_lordi)

            result, _ = min_max_ordi_positionnel("max", plateau_bis, pion_de_lordi, pion_adverse, profondeur - 1,
                                                 nb_coup_joueur1, nb_coup_joueur2)
            valeur = min(valeur, result)
            return valeur, nombre_a_jouer

        else:
            for i in range(len(plateau)):
                for j in range(len(plateau[0])):
                    if (isinstance(plateau[i][j], int)):  # SI plateau[i][j] EST UN ENTIER // DONC UN COUP POSSIBLE

                        plateau_bis = copy.deepcopy(plateau)  # Réalise une deep copy du plateau de jeu
                        plateau_bis = jouer_numero(plateau_bis, pion_adverse,
                                                   plateau[i][j])  # On simule le fait que l'on jou sur la case
                        plateau_bis = supprimer_coup_possible(plateau_bis)
                        plateau_bis, nb_coup_joueur1 = coup_possible(plateau_bis, pion_adverse, pion_de_lordi)

                        result, _ = min_max_ordi_positionnel("max", plateau_bis, pion_de_lordi, pion_adverse,
                                                             profondeur - 1, nb_coup_joueur1, nb_coup_joueur2)
                        ancien_valeur = valeur
                        valeur = min(valeur, result)
                        if (valeur != ancien_valeur):  # si la valeur à changé alors on joue sur ce numéro
                            nombre_a_jouer = plateau[i][j]

            return valeur, nombre_a_jouer


def alpha_beta_ordi_positionnel(min_or_max, alpha, beta, plateau, pion_de_lordi, pion_adverse, profondeur,
                                nb_coup_joueur1, nb_coup_joueur2):
    """ Fonction alpha-beta retournant la "valeur"  tactique (pour la récursivité) ainsi que
        le "nombre_a_jouer" après analyse suivant le profondeur pour "le pion_de_lordi"
        sur un des numéros avec la stratégie POSITIONNEL.
        POSITIONNEL : prise en compte des poids statique du tableau (Cf. cours),
        l’évaluation est la différence entre les poids associés des deux joueurs.
        Où "plateau" est une matrice de taille x et y superieur ou égal à 1
        et avec les coups possibles.
        où "alpha" et "beta" 2 entier pour le fonctionnement de l'algorithme.
        où "pion_de_lordi" un caractère définisant le pion de l'ordi.
        où "pion_adverse" un caractère définisant le pion adverse.
        où "profondeur" un entier définisant la profondeur de l'analyse de l'IA.
        où "nb_coup_joueur1" un entier définisant le nombre de coup du joueur1.
        où "nb_coup_joueur2" un entier définisant le nombre de coup du joueur2.
            C'est 2 "nb_coup_joueur" servent a définir l'arrêt du jeu.
    """
    nombre_a_jouer = -1
    if (est_plein(plateau) == True or (
            nb_coup_joueur1 == 0 and nb_coup_joueur2 == 0) or profondeur <= 0):  # Temps que ce n'est pas fini
        # afficher_plateau(plateau)      #Test : Vérification de toutes les posibilités
        return evaluation_positionnel(plateau, pion_de_lordi, pion_adverse), 0
    if (min_or_max == "max"):
        if (nb_coup_joueur1 == 0):  # Si l'IA ne peut pas jouer alors
            plateau_bis = copy.deepcopy(plateau)  # Réalise une deep copy du plateau de jeu
            # On simule le fait que l'on ne jou pas (donc on fait rien)
            plateau_bis = supprimer_coup_possible(plateau_bis)
            plateau_bis, nb_coup_joueur2 = coup_possible(plateau_bis, pion_de_lordi, pion_adverse)

            score, _ = alpha_beta_ordi_positionnel("min", alpha, beta, plateau_bis, pion_de_lordi, pion_adverse,
                                                   profondeur - 1, nb_coup_joueur1, nb_coup_joueur2)
            if (score >= beta):
                return beta, nombre_a_jouer
            if (score > alpha):
                alpha = score
            return alpha, nombre_a_jouer

        else:
            for i in range(len(plateau)):
                for j in range(len(plateau[0])):
                    if (isinstance(plateau[i][j], int)):  # SI plateau[i][j] EST UN ENTIER // DONC UN COUP POSSIBLE

                        plateau_bis = copy.deepcopy(plateau)  # Réalise une deep copy du plateau de jeu
                        plateau_bis = jouer_numero(plateau_bis, pion_de_lordi,
                                                   plateau[i][j])  # On simule le fait que l'on jou sur la case
                        plateau_bis = supprimer_coup_possible(plateau_bis)
                        plateau_bis, nb_coup_joueur2 = coup_possible(plateau_bis, pion_de_lordi, pion_adverse)

                        score, _ = alpha_beta_ordi_positionnel("min", alpha, beta, plateau_bis, pion_de_lordi,
                                                               pion_adverse, profondeur - 1, nb_coup_joueur1,
                                                               nb_coup_joueur2)
                        if (score >= beta):
                            nombre_a_jouer = plateau[i][j]
                            return beta, nombre_a_jouer
                        if (score > alpha):
                            nombre_a_jouer = plateau[i][j]
                            alpha = score

            return alpha, nombre_a_jouer

    elif (min_or_max == "min"):
        if (nb_coup_joueur2 == 0):  # Si l'IA ne peut pas jouer alors
            plateau_bis = copy.deepcopy(plateau)  # Réalise une deep copy du plateau de jeu
            # On simule le fait que l'on ne jou pas (donc on fait rien)
            plateau_bis = supprimer_coup_possible(plateau_bis)
            plateau_bis, nb_coup_joueur1 = coup_possible(plateau_bis, pion_adverse, pion_de_lordi)

            score, _ = alpha_beta_ordi_positionnel("max", alpha, beta, plateau_bis, pion_de_lordi, pion_adverse,
                                                   profondeur - 1, nb_coup_joueur1, nb_coup_joueur2)
            if (score <= alpha):
                return alpha, nombre_a_jouer
            if (score < beta):
                beta = score
            return beta, nombre_a_jouer

        else:
            for i in range(len(plateau)):
                for j in range(len(plateau[0])):
                    if (isinstance(plateau[i][j], int)):  # SI plateau[i][j] EST UN ENTIER // DONC UN COUP POSSIBLE

                        plateau_bis = copy.deepcopy(plateau)  # Réalise une deep copy du plateau de jeu
                        plateau_bis = jouer_numero(plateau_bis, pion_adverse,
                                                   plateau[i][j])  # On simule le fait que l'on jou sur la case
                        plateau_bis = supprimer_coup_possible(plateau_bis)
                        plateau_bis, nb_coup_joueur1 = coup_possible(plateau_bis, pion_adverse, pion_de_lordi)

                        score, _ = alpha_beta_ordi_positionnel("max", alpha, beta, plateau_bis, pion_de_lordi,
                                                               pion_adverse, profondeur - 1, nb_coup_joueur1,
                                                               nb_coup_joueur2)
                        if (score <= alpha):
                            nombre_a_jouer = plateau[i][j]
                            return alpha, nombre_a_jouer
                        if (score < beta):
                            nombre_a_jouer = plateau[i][j]
                            beta = score

            return beta, nombre_a_jouer


def evaluation_absolu(plateau, pion_du_joueur, pion_adverse):
    """ Fonction retournant l'évaluation du plateau en fonction de la stratégie
        absolu.
        l’évaluation est prise en compte de la différence du nombre de pions.
        Où "plateau" est une matrice de taille x et y et avec les coups possible.
        où "pion_du_joueur" un caractère caractérisant le pion du joueur.
        où "pion_adverse" un caractère caractérisant le pion adverse.
    """
    evaluation = 0
    nb_pion1, nb_pion2 = compter_pion(plateau, pion_du_joueur, pion_adverse)  # On compte les pions sur la simulation
    evaluation = nb_pion1 - nb_pion2
    return evaluation


def min_max_ordi_absolu(min_or_max, plateau, pion_de_lordi, pion_adverse, profondeur, nb_coup_joueur1, nb_coup_joueur2):
    """ Fonction min-max retournant la "valeur"  tactique (pour la récursivité) ainsi que
        le "nombre_a_jouer" après analyse suivant le profondeur pour "le pion_de_lordi"
        sur un des numéros avec la stratégie ABSOLU.
        ABSOLU : prise en compte de la différence du nombre de pions.
        Où "plateau" est une matrice de taille x et y superieur ou égal à 1
        et avec les coups possibles.
        où "pion_de_lordi" un caractère définisant le pion de l'ordi.
        où "pion_adverse" un caractère définisant le pion adverse.
        où "profondeur" un entier définisant la profondeur de l'analyse de l'IA.
        où "nb_coup_joueur1" un entier définisant le nombre de coup du joueur1.
        où "nb_coup_joueur2" un entier définisant le nombre de coup du joueur2.
            C'est 2 "nb_coup_joueur" servent a définir l'arrêt du jeu.
    """
    nombre_a_jouer = -1

    if (est_plein(plateau) == True or (
            nb_coup_joueur1 == 0 and nb_coup_joueur2 == 0) or profondeur <= 0):  # Temps que ce n'est pas fini
        # afficher_plateau(plateau)      #Test : Vérification de toutes les posibilités
        return evaluation_absolu(plateau, pion_de_lordi, pion_adverse), 0
    if (min_or_max == "max"):
        valeur = -10000
        if (nb_coup_joueur1 == 0):  # Si l'IA ne peut pas jouer alors
            plateau_bis = copy.deepcopy(plateau)  # Réalise une deep copy du plateau de jeu
            # On simule le fait que l'on ne jou pas (donc on fait rien)
            plateau_bis = supprimer_coup_possible(plateau_bis)
            plateau_bis, nb_coup_joueur2 = coup_possible(plateau_bis, pion_de_lordi, pion_adverse)

            result, _ = min_max_ordi_absolu("min", plateau_bis, pion_de_lordi, pion_adverse, profondeur - 1,
                                            nb_coup_joueur1, nb_coup_joueur2)
            valeur = max(valeur, result)
            return valeur, nombre_a_jouer
        else:
            for i in range(len(plateau)):
                for j in range(len(plateau[0])):
                    if (isinstance(plateau[i][j], int)):  # SI plateau[i][j] EST UN ENTIER // DONC UN COUP POSSIBLE

                        plateau_bis = copy.deepcopy(plateau)  # Réalise une deep copy du plateau de jeu
                        plateau_bis = jouer_numero(plateau_bis, pion_de_lordi,
                                                   plateau[i][j])  # On simule le fait que l'on jou sur la case
                        plateau_bis = supprimer_coup_possible(plateau_bis)
                        plateau_bis, nb_coup_joueur2 = coup_possible(plateau_bis, pion_de_lordi, pion_adverse)

                        result, _ = min_max_ordi_absolu("min", plateau_bis, pion_de_lordi, pion_adverse, profondeur - 1,
                                                        nb_coup_joueur1, nb_coup_joueur2)
                        ancien_valeur = valeur
                        valeur = max(valeur, result)
                        if (valeur != ancien_valeur):  # si la valeur à changé alors on joue sur ce numéro
                            nombre_a_jouer = plateau[i][j]

            return valeur, nombre_a_jouer



    elif (min_or_max == "min"):
        valeur = 10000
        if (nb_coup_joueur2 == 0):  # Si l'IA ne peut pas jouer alors
            plateau_bis = copy.deepcopy(plateau)  # Réalise une deep copy du plateau de jeu
            # On simule le fait que l'on ne jou pas (donc on fait rien)
            plateau_bis = supprimer_coup_possible(plateau_bis)
            plateau_bis, nb_coup_joueur1 = coup_possible(plateau_bis, pion_adverse, pion_de_lordi)

            result, _ = min_max_ordi_absolu("max", plateau_bis, pion_de_lordi, pion_adverse, profondeur - 1,
                                            nb_coup_joueur1, nb_coup_joueur2)
            valeur = min(valeur, result)
            return valeur, nombre_a_jouer

        else:
            for i in range(len(plateau)):
                for j in range(len(plateau[0])):
                    if (isinstance(plateau[i][j], int)):  # SI plateau[i][j] EST UN ENTIER // DONC UN COUP POSSIBLE

                        plateau_bis = copy.deepcopy(plateau)  # Réalise une deep copy du plateau de jeu
                        plateau_bis = jouer_numero(plateau_bis, pion_adverse,
                                                   plateau[i][j])  # On simule le fait que l'on jou sur la case
                        plateau_bis = supprimer_coup_possible(plateau_bis)
                        plateau_bis, nb_coup_joueur1 = coup_possible(plateau_bis, pion_adverse, pion_de_lordi)

                        result, _ = min_max_ordi_absolu("max", plateau_bis, pion_de_lordi, pion_adverse, profondeur - 1,
                                                        nb_coup_joueur1, nb_coup_joueur2)
                        ancien_valeur = valeur
                        valeur = min(valeur, result)
                        if (valeur != ancien_valeur):  # si la valeur à changé alors on joue sur ce numéro
                            nombre_a_jouer = plateau[i][j]

            return valeur, nombre_a_jouer


def alpha_beta_ordi_absolu(min_or_max, alpha, beta, plateau, pion_de_lordi, pion_adverse, profondeur, nb_coup_joueur1,
                           nb_coup_joueur2):
    """ Fonction alpha-beta retournant la "valeur"  tactique (pour la récursivité) ainsi que
        le "nombre_a_jouer" après analyse suivant le profondeur pour "le pion_de_lordi"
        sur un des numéros avec la stratégie ABSOLU.
        ABSOLU : prise en compte de la différence du nombre de pions.
        Où "plateau" est une matrice de taille x et y superieur ou égal à 1
        et avec les coups possibles.
        où "alpha" et "beta" 2 entier pour le fonctionnement de l'algorithme.
        où "pion_de_lordi" un caractère définisant le pion de l'ordi.
        où "pion_adverse" un caractère définisant le pion adverse.
        où "profondeur" un entier définisant la profondeur de l'analyse de l'IA.
        où "nb_coup_joueur1" un entier définisant le nombre de coup du joueur1.
        où "nb_coup_joueur2" un entier définisant le nombre de coup du joueur2.
            C'est 2 "nb_coup_joueur" servent a définir l'arrêt du jeu.
    """
    nombre_a_jouer = -1
    """
    afficher_plateau(plateau)
    print("min_or_max = " + str(min_or_max))
    print("profondeur = " + str(profondeur))
    print("estplein = "+str(est_plein(plateau)))
    print("plus de coup possible = "+str(nb_coup_joueur1 == 0 ))
    """
    if (est_plein(plateau) == True or (
            nb_coup_joueur1 == 0 and nb_coup_joueur2 == 0) or profondeur <= 0):  # Temps que ce n'est pas fini
        # afficher_plateau(plateau)      #Test : Vérification de toutes les posibilités
        return evaluation_absolu(plateau, pion_de_lordi, pion_adverse), 0

    if (min_or_max == "max"):
        if (nb_coup_joueur1 == 0):  # Si l'IA ne peut pas jouer alors
            plateau_bis = copy.deepcopy(plateau)  # Réalise une deep copy du plateau de jeu
            # On simule le fait que l'on ne jou pas (donc on fait rien)
            plateau_bis = supprimer_coup_possible(plateau_bis)
            plateau_bis, nb_coup_joueur2 = coup_possible(plateau_bis, pion_de_lordi, pion_adverse)

            score, _ = alpha_beta_ordi_absolu("min", alpha, beta, plateau_bis, pion_de_lordi, pion_adverse,
                                              profondeur - 1, nb_coup_joueur1, nb_coup_joueur2)
            if (score >= beta):
                return beta, nombre_a_jouer
            if (score > alpha):
                alpha = score
            return alpha, nombre_a_jouer
        else:
            for i in range(len(plateau)):
                for j in range(len(plateau[0])):
                    if (isinstance(plateau[i][j], int)):  # SI plateau[i][j] EST UN ENTIER // DONC UN COUP POSSIBLE
                        plateau_bis = copy.deepcopy(plateau)  # Réalise une deep copy du plateau de jeu
                        plateau_bis = jouer_numero(plateau_bis, pion_de_lordi,
                                                   plateau[i][j])  # On simule le fait que l'on jou sur la case
                        plateau_bis = supprimer_coup_possible(plateau_bis)
                        plateau_bis, nb_coup_joueur2 = coup_possible(plateau_bis, pion_de_lordi, pion_adverse)

                        score, _ = alpha_beta_ordi_absolu("min", alpha, beta, plateau_bis, pion_de_lordi, pion_adverse,
                                                          profondeur - 1, nb_coup_joueur1, nb_coup_joueur2)
                        if (score >= beta):
                            nombre_a_jouer = plateau[i][j]
                            return beta, nombre_a_jouer
                        if (score > alpha):
                            nombre_a_jouer = plateau[i][j]
                            alpha = score

            return alpha, nombre_a_jouer



    elif (min_or_max == "min"):
        if (nb_coup_joueur1 == 0):  # Si l'IA ne peut pas jouer alors
            plateau_bis = copy.deepcopy(plateau)  # Réalise une deep copy du plateau de jeu
            # On simule le fait que l'on ne jou pas (donc on fait rien)
            plateau_bis = supprimer_coup_possible(plateau_bis)
            plateau_bis, nb_coup_joueur1 = coup_possible(plateau_bis, pion_adverse, pion_de_lordi)

            score, _ = alpha_beta_ordi_absolu("max", alpha, beta, plateau_bis, pion_de_lordi, pion_adverse,
                                              profondeur - 1, nb_coup_joueur1, nb_coup_joueur2)
            if (score <= alpha):
                return alpha, nombre_a_jouer
            if (score < beta):
                beta = score
            return beta, nombre_a_jouer
        else:
            for i in range(len(plateau)):
                for j in range(len(plateau[0])):
                    if (isinstance(plateau[i][j], int)):  # SI plateau[i][j] EST UN ENTIER // DONC UN COUP POSSIBLE
                        plateau_bis = copy.deepcopy(plateau)  # Réalise une deep copy du plateau de jeu
                        plateau_bis = jouer_numero(plateau_bis, pion_adverse,
                                                   plateau[i][j])  # On simule le fait que l'on jou sur la case
                        plateau_bis = supprimer_coup_possible(plateau_bis)
                        plateau_bis, nb_coup_joueur1 = coup_possible(plateau_bis, pion_adverse, pion_de_lordi)

                        score, _ = alpha_beta_ordi_absolu("max", alpha, beta, plateau_bis, pion_de_lordi, pion_adverse,
                                                          profondeur - 1, nb_coup_joueur1, nb_coup_joueur2)
                        if (score <= alpha):
                            nombre_a_jouer = plateau[i][j]
                            return alpha, nombre_a_jouer
                        if (score < beta):
                            nombre_a_jouer = plateau[i][j]
                            beta = score

            return beta, nombre_a_jouer


def evaluation_mobilite(plateau, pion_du_joueur, pion_adverse):
    """ Fonction retournant l'évaluation du plateau en fonction de la stratégie
        mobilite.
        l'évaluation maximise le nombre de coups possibles et minimise les
        coups de l’adversaire tout en essayant de prendre les coins.
        Où "plateau" est une matrice de taille x et y et avec les coups possible.
        où "pion_du_joueur" un caractère caractérisant le pion du joueur.
        où "pion_adverse" un caractère caractérisant le pion adverse.
    """
    evaluation = 0
    plateau = supprimer_coup_possible(plateau)
    _, nb_coup_joueur1 = coup_possible(plateau, pion_du_joueur, pion_adverse)
    plateau = supprimer_coup_possible(plateau)
    _, nb_coup_joueur2 = coup_possible(plateau, pion_adverse, pion_du_joueur)
    evaluation = nb_coup_joueur1 - nb_coup_joueur2
    return evaluation


def min_max_ordi_mobilite(min_or_max, plateau, pion_de_lordi, pion_adverse, profondeur, nb_coup_joueur1,
                          nb_coup_joueur2):
    """ Fonction min-max retournant la "valeur"  tactique (pour la récursivité) ainsi que
        le "nombre_a_jouer" après analyse suivant le profondeur pour "le pion_de_lordi"
        sur un des numéros avec la stratégie MOBILITE.
        MOBILITE : maximise le nombre de coups possibles et minimise les
        coups de l’adversaire tout en essayant de prendre les coins.
        Où "plateau" est une matrice de taille x et y superieur ou égal à 1
        et avec les coups possibles.
        où "pion_de_lordi" un caractère définisant le pion de l'ordi.
        où "pion_adverse" un caractère définisant le pion adverse.
        où "profondeur" un entier définisant la profondeur de l'analyse de l'IA.
        où "nb_coup_joueur1" un entier définisant le nombre de coup du joueur1.
        où "nb_coup_joueur2" un entier définisant le nombre de coup du joueur2.
            C'est 2 "nb_coup_joueur" servent a définir l'arrêt du jeu.
    """
    nombre_a_jouer = -1

    if (est_plein(plateau) == True or (
            nb_coup_joueur1 == 0 and nb_coup_joueur2 == 0) or profondeur <= 0):  # Temps que ce n'est pas fini
        # afficher_plateau(plateau)      #Test : Vérification de toutes les posibilités
        return evaluation_mobilite(plateau, pion_de_lordi, pion_adverse), 0

    if (min_or_max == "max"):
        valeur = -100000000
        if (nb_coup_joueur1 == 0):  # Si l'IA ne peut pas jouer alors
            plateau_bis = copy.deepcopy(plateau)  # Réalise une deep copy du plateau de jeu
            # On simule le fait que l'on ne jou pas (donc on fait rien)
            plateau_bis = supprimer_coup_possible(plateau_bis)
            plateau_bis, nb_coup_joueur2 = coup_possible(plateau_bis, pion_de_lordi, pion_adverse)

            result, _ = min_max_ordi_mobilite("min", plateau_bis, pion_de_lordi, pion_adverse, profondeur - 1,
                                              nb_coup_joueur1, nb_coup_joueur2)
            valeur = max(valeur, result)
            return valeur, nombre_a_jouer

        else:
            for i in range(len(plateau)):
                for j in range(len(plateau[0])):
                    if (isinstance(plateau[i][j], int)):  # SI plateau[i][j] EST UN ENTIER // DONC UN COUP POSSIBLE

                        plateau_bis = copy.deepcopy(plateau)  # Réalise une deep copy du plateau de jeu
                        plateau_bis = jouer_numero(plateau_bis, pion_de_lordi,
                                                   plateau[i][j])  # On simule le fait que l'on jou sur la case
                        plateau_bis = supprimer_coup_possible(plateau_bis)
                        plateau_bis, nb_coup_joueur2 = coup_possible(plateau_bis, pion_de_lordi, pion_adverse)

                        result, _ = min_max_ordi_mobilite("min", plateau_bis, pion_de_lordi, pion_adverse,
                                                          profondeur - 1, nb_coup_joueur1, nb_coup_joueur2)
                        ancien_valeur = valeur
                        valeur = max(valeur, result)
                        if (valeur != ancien_valeur):  # si la valeur à changé alors on joue sur ce numéro
                            nombre_a_jouer = plateau[i][j]
                        if (((i == 0 and j == 0) or (i == len(plateau) - 1 and j == 0) or (
                                i == 0 and j == len(plateau[0]) - 1) or (i == len(plateau) - 1 and j == len(plateau[
                                                                                                                0]) - 1)) and valeur != -10000000):  # DONC SI ON EST DANS UN COIN ON LE JOUE OBLIGATOIREMENT
                            nombre_a_jouer = plateau[i][j]
                            # print("On doit jouer le " + str(plateau[i][j]))
                            valeur = 10000000  # Alors on le joue obligatoirement

            return valeur, nombre_a_jouer



    elif (min_or_max == "min"):
        valeur = 100000000
        if (nb_coup_joueur2 == 0):  # Si l'IA ne peut pas jouer alors
            plateau_bis = copy.deepcopy(plateau)  # Réalise une deep copy du plateau de jeu
            # On simule le fait que l'on ne jou pas (donc on fait rien)
            plateau_bis = supprimer_coup_possible(plateau_bis)
            plateau_bis, nb_coup_joueur1 = coup_possible(plateau_bis, pion_adverse, pion_de_lordi)

            result, _ = min_max_ordi_mobilite("max", plateau_bis, pion_de_lordi, pion_adverse, profondeur - 1,
                                              nb_coup_joueur1, nb_coup_joueur2)
            valeur = min(valeur, result)
            return valeur, nombre_a_jouer

        else:
            for i in range(len(plateau)):
                for j in range(len(plateau[0])):
                    if (isinstance(plateau[i][j], int)):  # SI plateau[i][j] EST UN ENTIER // DONC UN COUP POSSIBLE

                        plateau_bis = copy.deepcopy(plateau)  # Réalise une deep copy du plateau de jeu
                        plateau_bis = jouer_numero(plateau_bis, pion_adverse,
                                                   plateau[i][j])  # On simule le fait que l'on jou sur la case
                        plateau_bis = supprimer_coup_possible(plateau_bis)
                        plateau_bis, nb_coup_joueur1 = coup_possible(plateau_bis, pion_adverse, pion_de_lordi)

                        result, _ = min_max_ordi_mobilite("max", plateau_bis, pion_de_lordi, pion_adverse,
                                                          profondeur - 1, nb_coup_joueur1, nb_coup_joueur2)
                        ancien_valeur = valeur
                        valeur = min(valeur, result)
                        if (valeur != ancien_valeur):  # si la valeur à changé alors on joue sur ce numéro
                            nombre_a_jouer = plateau[i][j]
                        if (((i == 0 and j == 0) or (i == len(plateau) - 1 and j == 0) or (
                                i == 0 and j == len(plateau[0]) - 1) or (i == len(plateau) - 1 and j == len(plateau[
                                                                                                                0]) - 1)) and valeur != 10000000):  # DONC SI ON EST DANS UN COIN ON LE JOUE OBLIGATOIREMENT
                            nombre_a_jouer = plateau[i][j]
                            valeur = -10000000  # Alors on le joue obligatoirement

            return valeur, nombre_a_jouer


def alpha_beta_ordi_mobilite(min_or_max, alpha, beta, plateau, pion_de_lordi, pion_adverse, profondeur, nb_coup_joueur1,
                             nb_coup_joueur2):
    """ Fonction alpha-beta retournant la "valeur"  tactique (pour la récursivité) ainsi que
        le "nombre_a_jouer" après analyse suivant le profondeur pour "le pion_de_lordi"
        sur un des numéros avec la stratégie MOBILITE.
        MOBILITE : maximise le nombre de coups possibles et minimise les
        coups de l’adversaire tout en essayant de prendre les coins.
        Où "plateau" est une matrice de taille x et y superieur ou égal à 1
        et avec les coups possibles.
        où "alpha" et "beta" 2 nombre entier qui servent au fonctionnement de l'algorithme
        où "pion_de_lordi" un caractère définisant le pion de l'ordi.
        où "pion_adverse" un caractère définisant le pion adverse.
        où "profondeur" un entier définisant la profondeur de l'analyse de l'IA.
        où "nb_coup_joueur1" un entier définisant le nombre de coup du joueur1.
        où "nb_coup_joueur2" un entier définisant le nombre de coup du joueur2.
            C'est 2 "nb_coup_joueur" servent a définir l'arrêt du jeu.
    """
    nombre_a_jouer = -1

    if (est_plein(plateau) == True or (
            nb_coup_joueur1 == 0 and nb_coup_joueur2 == 0) or profondeur <= 0):  # Temps que ce n'est pas fini
        # afficher_plateau(plateau)      #Test : Vérification de toutes les posibilités
        return evaluation_mobilite(plateau, pion_de_lordi, pion_adverse), 0

    if (min_or_max == "max"):
        if (nb_coup_joueur1 == 0):
            plateau_bis = copy.deepcopy(plateau)  # Réalise une deep copy du plateau de jeu
            # On simule le fait que l'on ne jou pas (donc on fait rien)
            plateau_bis = supprimer_coup_possible(plateau_bis)
            plateau_bis, nb_coup_joueur2 = coup_possible(plateau_bis, pion_de_lordi, pion_adverse)

            score, _ = alpha_beta_ordi_mobilite("min", alpha, beta, plateau_bis, pion_de_lordi, pion_adverse,
                                                profondeur - 1, nb_coup_joueur1, nb_coup_joueur2)
            if (score >= beta):
                return beta, nombre_a_jouer
            if (score > alpha):
                alpha = score
            return alpha, nombre_a_jouer

        else:
            for i in range(len(plateau)):
                for j in range(len(plateau[0])):
                    if (isinstance(plateau[i][j], int)):  # SI plateau[i][j] EST UN ENTIER // DONC UN COUP POSSIBLE

                        plateau_bis = copy.deepcopy(plateau)  # Réalise une deep copy du plateau de jeu
                        plateau_bis = jouer_numero(plateau_bis, pion_de_lordi,
                                                   plateau[i][j])  # On simule le fait que l'on jou sur la case
                        plateau_bis = supprimer_coup_possible(plateau_bis)
                        plateau_bis, nb_coup_joueur2 = coup_possible(plateau_bis, pion_de_lordi, pion_adverse)

                        score, _ = alpha_beta_ordi_mobilite("min", alpha, beta, plateau_bis, pion_de_lordi,
                                                            pion_adverse, profondeur - 1, nb_coup_joueur1,
                                                            nb_coup_joueur2)
                        if ((i == 0 and j == 0) or (i == len(plateau) - 1 and j == 0) or (
                                i == 0 and j == len(plateau[0]) - 1) or (i == len(plateau) - 1 and j == len(
                                plateau[0]) - 1)):  # DONC SI ON EST DANS UN COIN ON LE JOUE OBLIGATOIREMENT
                            nombre_a_jouer = plateau[i][j]
                            # print("On doit jouer le " + str(plateau[i][j]))
                            valeur = 10000000  # Alors on le joue obligatoirement
                            return valeur, nombre_a_jouer
                        if (score >= beta):
                            nombre_a_jouer = plateau[i][j]
                            return beta, nombre_a_jouer
                        if (score > alpha):
                            nombre_a_jouer = plateau[i][j]
                            alpha = score

            return alpha, nombre_a_jouer




    elif (min_or_max == "min"):
        if (nb_coup_joueur2 == 0):
            plateau_bis = copy.deepcopy(plateau)  # Réalise une deep copy du plateau de jeu
            # On simule le fait que l'on ne jou pas (donc on fait rien)
            plateau_bis = supprimer_coup_possible(plateau_bis)
            plateau_bis, nb_coup_joueur1 = coup_possible(plateau_bis, pion_adverse, pion_de_lordi)

            score, _ = alpha_beta_ordi_mobilite("max", alpha, beta, plateau_bis, pion_de_lordi, pion_adverse,
                                                profondeur - 1, nb_coup_joueur1, nb_coup_joueur2)
            if (score <= alpha):
                return alpha, nombre_a_jouer
            if (score < beta):
                beta = score
            return beta, nombre_a_jouer

        else:
            for i in range(len(plateau)):
                for j in range(len(plateau[0])):
                    if (isinstance(plateau[i][j], int)):  # SI plateau[i][j] EST UN ENTIER // DONC UN COUP POSSIBLE

                        plateau_bis = copy.deepcopy(plateau)  # Réalise une deep copy du plateau de jeu
                        plateau_bis = jouer_numero(plateau_bis, pion_adverse,
                                                   plateau[i][j])  # On simule le fait que l'on jou sur la case
                        plateau_bis = supprimer_coup_possible(plateau_bis)
                        plateau_bis, nb_coup_joueur1 = coup_possible(plateau_bis, pion_adverse, pion_de_lordi)

                        score, _ = alpha_beta_ordi_mobilite("max", alpha, beta, plateau_bis, pion_de_lordi,
                                                            pion_adverse, profondeur - 1, nb_coup_joueur1,
                                                            nb_coup_joueur2)
                        if ((i == 0 and j == 0) or (i == len(plateau) - 1 and j == 0) or (
                                i == 0 and j == len(plateau[0]) - 1) or (i == len(plateau) - 1 and j == len(
                                plateau[0]) - 1)):  # DONC SI ON EST DANS UN COIN ON LE JOUE OBLIGATOIREMENT
                            nombre_a_jouer = plateau[i][j]
                            valeur = -10000000  # Alors on le joue obligatoirement
                            return valeur, nombre_a_jouer
                        if (score <= alpha):
                            nombre_a_jouer = plateau[i][j]
                            return alpha, nombre_a_jouer
                        if (score < beta):
                            nombre_a_jouer = plateau[i][j]
                            beta = score

            return beta, nombre_a_jouer


def min_max_ordi_mixte(plateau, pion_de_lordi, pion_adverse, profondeur, nb_coup_joueur1, nb_coup_joueur2, coup_numero):
    """ Fonction min-max retournant le plateau après que les fonctions min-max appelé
        par MIXTE est joué sur la position pour cette stratégie.
        MIXTE : le jeu est divisé en trois phases où les stratégies peuvent différer
        : (i) en début de partie (20 à 25 premiers coups), le joueur IA choisit
        une stratégie de type ’positionnel’, au milieu de partie, sélectionne une
        stratégie de ’mobilité’ ; et enfin en fin de partie (10 à 16 derniers coups),
        sélectionne la stratégie ’absolu’.

        Où "plateau" est une matrice de taille x et y superieur ou égal à 1
        et avec les coups possibles.
        où "pion_de_lordi" un caractère définisant le pion de l'ordi.
        où "pion_adverse" un caractère définisant le pion adverse.
        où "profondeur" un entier définisant la profondeur de l'analyse de l'IA.
        où "nb_coup_joueur1" un entier définisant le nombre de coup du joueur1.
        où "nb_coup_joueur2" un entier définisant le nombre de coup du joueur2.
            C'est 2 "nb_coup_joueur" servent a définir l'arrêt du jeu.
    """

    coup_possible_max_sur_plateau = len(plateau) * len(plateau[0])

    if (coup_numero > 0 and coup_numero < 25):
        print("L'IA MIXTE donne la main à l'IA POSITIONNEL 'min-max' pour le coup n°" + str(coup_numero) + " :")
        return jouer(2, plateau, pion_de_lordi, pion_adverse, coup_numero, nb_coup_joueur1, nb_coup_joueur2, profondeur)
    elif (coup_numero >= 25 and coup_numero < (coup_possible_max_sur_plateau - 16)):
        print("L'IA MIXTE donne la main à l'IA MOBILITE 'min-max' pour le coup n°" + str(coup_numero) + " :")
        return jouer(6, plateau, pion_de_lordi, pion_adverse, coup_numero, nb_coup_joueur1, nb_coup_joueur2, profondeur)
    else:  # (coup_numero >= (coup_possible_max_sur_plateau - 16) and coup_numero < coup_possible_max_sur_plateau)
        print("L'IA MIXTE donne la main à l'IA ABSOLU 'min-max' pour le coup n°" + str(coup_numero) + " :")
        return jouer(4, plateau, pion_de_lordi, pion_adverse, coup_numero, nb_coup_joueur1, nb_coup_joueur2, profondeur)


def alpha_beta_ordi_mixte(plateau, pion_de_lordi, pion_adverse, profondeur, nb_coup_joueur1, nb_coup_joueur2,
                          coup_numero):
    """ Fonction alpha-beta retournant le plateau après que les fonctions alpha-beta appelé
        par MIXTE est joué sur la position pour cette stratégie.
        MIXTE : le jeu est divisé en trois phases où les stratégies peuvent différer
        : (i) en début de partie (20 à 25 premiers coups), le joueur IA choisit
        une stratégie de type ’positionnel’, au milieu de partie, sélectionne une
        stratégie de ’mobilité’ ; et enfin en fin de partie (10 à 16 derniers coups),
        sélectionne la stratégie ’absolu’.

        Où "plateau" est une matrice de taille x et y superieur ou égal à 1
        et avec les coups possibles.
        où "pion_de_lordi" un caractère définisant le pion de l'ordi.
        où "pion_adverse" un caractère définisant le pion adverse.
        où "profondeur" un entier définisant la profondeur de l'analyse de l'IA.
        où "nb_coup_joueur1" un entier définisant le nombre de coup du joueur1.
        où "nb_coup_joueur2" un entier définisant le nombre de coup du joueur2.
            C'est 2 "nb_coup_joueur" servent a définir l'arrêt du jeu.
    """

    coup_possible_max_sur_plateau = len(plateau) * len(plateau[0])

    if (coup_numero > 0 and coup_numero < 25):
        print("L'IA MIXTE donne la main à l'IA POSITIONNEL 'alpha-beta' pour le coup n°" + str(coup_numero) + " :")
        return jouer(3, plateau, pion_de_lordi, pion_adverse, coup_numero, nb_coup_joueur1, nb_coup_joueur2, profondeur)
    elif (coup_numero >= 25 and coup_numero < (coup_possible_max_sur_plateau - 16)):
        print("L'IA MIXTE donne la main à l'IA MOBILITE 'alpha-beta' pour le coup n°" + str(coup_numero) + " :")
        return jouer(7, plateau, pion_de_lordi, pion_adverse, coup_numero, nb_coup_joueur1, nb_coup_joueur2, profondeur)
    else:  # (coup_numero >= (coup_possible_max_sur_plateau - 16) and coup_numero < coup_possible_max_sur_plateau)
        print("L'IA MIXTE donne la main à l'IA ABSOLU 'alpha-beta' pour le coup n°" + str(coup_numero) + " :")
        return jouer(5, plateau, pion_de_lordi, pion_adverse, coup_numero, nb_coup_joueur1, nb_coup_joueur2, profondeur)


def saisir_entier(nb_max):
    """ Fonction retournant un entier entre 1 et "nb_max" suivant la valeur saisie.
        (et faire en sorte que la valeur saisi soit correct).
    """
    sorti = -1
    temp = 0
    while (sorti == -1):
        try:
            temp = int(input(""))
            if (temp > 0 and temp <= nb_max):
                sorti = temp
            else:
                print("La valeur saisi n'est pas un coup proposé. Veuillez ressayer...")
        except:
            print("La valeur saisi n'a pas était reconnu comme un entier. Veuillez ressayer...")

    return sorti


def jouer(indice, plateau, pion_joueur, pion_adverse, coup_numero, nb_coup_possible_joueur1, nb_coup_possible_joueur2,
          profondeur):
    """ Fonction retournant le résultat de la bonne fonction en fonction de
        l'"indice" en paramètre. (et il faut que nb_coup_possible soit supérieur
        strictement à 0)

        Où "indice" est un entier définisant la fonction à utiliser
        où "plateau" est une matrice de taille supérieur à 2 pour x et y
        et avec les coups possible.
        où "pion_joueur" un caractère à ajouter sur la case "numero_retenu"
        où "pion_adverse" un catactère définisant e pion adverse
        où "coup_numero" entier correspondant au nombre de coups jouer depuis le debut
        où "nb_coup_possible_joueur1" le nombre coups possible max à faire sur le plateau
        qui doit etre superieur à 0.
    """

    if (indice == 1):  # On a définit l'humain qui joue
        if (nb_coup_possible_joueur1 > 0):
            print("Saisir l'entier a jouer : ", end="")
            plateau = jouer_numero(plateau, pion_joueur, saisir_entier(nb_coup_possible_joueur1))
        else:
            print("Le joueur n'a pas pu jouer, car pas de coup possible")
        return plateau



    elif (indice == 2):  # On a définit l'IA MIN-MAX avec la strategie POSITIONNEL
        # return jouer_ordi_positionnel(plateau, pion_joueur, pion_adverse)   #PREMIER FONCTION TEST POUR LA COMPREHENSION
        _, numero_a_jouer = min_max_ordi_positionnel("max", plateau, pion_joueur, pion_adverse, profondeur,
                                                     nb_coup_possible_joueur1, nb_coup_possible_joueur2)

        if (numero_a_jouer != -1):
            plateau = jouer_numero(plateau, pion_joueur, numero_a_jouer)
            print("L'IA POSITIONNEL 'min-max' avec une profondeur de " + str(
                profondeur) + " à jouer sur le numéro " + str(numero_a_jouer) + "\n")
        else:
            print("L'IA POSITIONNEL 'min-max' n'a pas pu jouer :(. Elle doit donner la main à l'adversaire..\n")
        return plateau
    elif (indice == 3):  # On a définit l'IA ALPHA-BETA avec la strategie POSITIONNEL
        _, numero_a_jouer = alpha_beta_ordi_positionnel("max", -1000000000, 1000000000, plateau, pion_joueur,
                                                        pion_adverse, profondeur, nb_coup_possible_joueur1,
                                                        nb_coup_possible_joueur2)

        if (numero_a_jouer != -1):
            plateau = jouer_numero(plateau, pion_joueur, numero_a_jouer)
            print("L'IA POSITIONNEL 'alpha-beta' avec une profondeur de " + str(
                profondeur) + " à jouer sur le numéro " + str(numero_a_jouer) + "\n")
        else:
            print("L'IA POSITIONNEL 'alpha-beta' n'a pas pu jouer :(. Elle doit donner la main à l'adversaire..\n")
        return plateau



    elif (indice == 4):  # On a définit l'IA MIN-MAX avec la strategie ABSOLU
        _, numero_a_jouer = min_max_ordi_absolu("max", plateau, pion_joueur, pion_adverse, profondeur,
                                                nb_coup_possible_joueur1, nb_coup_possible_joueur2)

        if (numero_a_jouer != -1):
            plateau = jouer_numero(plateau, pion_joueur, numero_a_jouer)
            print("L'IA ABSOLU 'min-max' avec une profondeur de " + str(profondeur) + " à jouer sur le numéro " + str(
                numero_a_jouer) + "\n")
        else:
            print("L'IA ABSOLU 'min-max' n'a pas pu jouer :(. Elle doit donner la main à l'adversaire..\n")
        return plateau
    elif (indice == 5):  # On a définit l'IA ALPHA-BETA avec la strategie ABSOLU
        _, numero_a_jouer = alpha_beta_ordi_absolu("max", -1000000000000, 1000000000000, plateau, pion_joueur,
                                                   pion_adverse, profondeur, nb_coup_possible_joueur1,
                                                   nb_coup_possible_joueur2)

        if (numero_a_jouer != -1):
            plateau = jouer_numero(plateau, pion_joueur, numero_a_jouer)
            print(
                "L'IA ABSOLU 'alpha-beta' avec une profondeur de " + str(profondeur) + " à jouer sur le numéro " + str(
                    numero_a_jouer) + "\n")
        else:
            print("L'IA ABSOLU 'alpha-beta' n'a pas pu jouer :(. Elle doit donner la main à l'adversaire..\n")
        return plateau



    elif (indice == 6):  # On a définit l'IA MIN-MAX avec la strategie MOBILITE
        _, numero_a_jouer = min_max_ordi_mobilite("max", plateau, pion_joueur, pion_adverse, profondeur,
                                                  nb_coup_possible_joueur1, nb_coup_possible_joueur2)

        if (numero_a_jouer != -1):
            plateau = jouer_numero(plateau, pion_joueur, numero_a_jouer)
            print("L'IA MOBILITE 'min-max' avec une profondeur de " + str(profondeur) + " à jouer sur le numéro " + str(
                numero_a_jouer) + "\n")
        else:
            print("L'IA MOBILITE 'min-max' n'a pas pu jouer :(. Elle doit donner la main à l'adversaire..\n")
        return plateau
    elif (indice == 7):  # On a définit l'IA ALPHA-BETA avec la strategie MOBILITE
        _, numero_a_jouer = alpha_beta_ordi_mobilite("max", -1000000000, 1000000000, plateau, pion_joueur, pion_adverse,
                                                     profondeur, nb_coup_possible_joueur1, nb_coup_possible_joueur2)

        if (numero_a_jouer != -1):
            plateau = jouer_numero(plateau, pion_joueur, numero_a_jouer)
            print("L'IA MOBILITE 'alpha-beta' avec une profondeur de " + str(
                profondeur) + " à jouer sur le numéro " + str(numero_a_jouer) + "\n")
        else:
            print("L'IA MOBILITE 'alpha-beta' n'a pas pu jouer :(. Elle doit donner la main à l'adversaire..\n")
        return plateau



    elif (indice == 8):  # On a définit l'IA MIN-MAX avec la strategie MIXTE
        # return jouer_ordi_mixte(plateau, pion_joueur, pion_adverse, coup_numero)     #PREMIER FONCTION TEST POUR LA COMPREHENSION
        plateau = min_max_ordi_mixte(plateau, pion_joueur, pion_adverse, profondeur, nb_coup_possible_joueur1,
                                     nb_coup_possible_joueur2, coup_numero)
        return plateau
    elif (indice == 9):  # On a définit l'IA ALPHA-BETA avec la strategie MIXTE
        # return jouer_ordi_mixte(plateau, pion_joueur, pion_adverse, coup_numero)     #PREMIER FONCTION TEST POUR LA COMPREHENSION
        plateau = alpha_beta_ordi_mixte(plateau, pion_joueur, pion_adverse, profondeur, nb_coup_possible_joueur1,
                                        nb_coup_possible_joueur2, coup_numero)
        return plateau


def jouer_silencieux(indice, plateau, pion_joueur, pion_adverse, coup_numero, nb_coup_possible_joueur1,
                     nb_coup_possible_joueur2, profondeur):
    """ Fonction qui fait la même chose que "jouer" mais de facon silencieux
        Fonction retournant le résultat de la bonne fonction en fonction de
        l'"indice" en paramètre. (et il faut que nb_coup_possible soit supérieur
        strictement à 0)

        Où "indice" est un entier définisant la fonction à utiliser
        où "plateau" est une matrice de taille supérieur à 2 pour x et y
        et avec les coups possible.
        où "pion_joueur" un caractère à ajouter sur la case "numero_retenu"
        où "pion_adverse" un catactère définisant e pion adverse
        où "coup_numero" entier correspondant au nombre de coups jouer depuis le debut
        où "nb_coup_possible_joueur1" le nombre coups possible max à faire sur le plateau
        qui doit etre superieur à 0.
    """

    if (indice == 1):  # On a définit l'humain qui joue
        plateau = jouer_numero(plateau, pion_joueur, saisir_entier(nb_coup_possible_joueur1))
        return plateau

    elif (indice == 2):  # On a définit l'IA MIN-MAX avec la strategie POSITIONNEL
        _, numero_a_jouer = min_max_ordi_positionnel("max", plateau, pion_joueur, pion_adverse, profondeur,
                                                     nb_coup_possible_joueur1, nb_coup_possible_joueur2)
        plateau = jouer_numero(plateau, pion_joueur, numero_a_jouer)
        return plateau
    elif (indice == 3):  # On a définit l'IA ALPHA-BETA avec la strategie POSITIONNEL
        _, numero_a_jouer = alpha_beta_ordi_positionnel("max", -1000000000, 1000000000, plateau, pion_joueur,
                                                        pion_adverse, profondeur, nb_coup_possible_joueur1,
                                                        nb_coup_possible_joueur2)
        plateau = jouer_numero(plateau, pion_joueur, numero_a_jouer)
        return plateau

    elif (indice == 4):  # On a définit l'IA MIN-MAX avec la strategie ABSOLU
        _, numero_a_jouer = min_max_ordi_absolu("max", plateau, pion_joueur, pion_adverse, profondeur,
                                                nb_coup_possible_joueur1, nb_coup_possible_joueur2)
        plateau = jouer_numero(plateau, pion_joueur, numero_a_jouer)
        return plateau
    elif (indice == 5):  # On a définit l'IA ALPHA-BETA avec la strategie ABSOLU
        _, numero_a_jouer = alpha_beta_ordi_absolu("max", -1000000000000, 1000000000000, plateau, pion_joueur,
                                                   pion_adverse, profondeur, nb_coup_possible_joueur1,
                                                   nb_coup_possible_joueur2)
        plateau = jouer_numero(plateau, pion_joueur, numero_a_jouer)
        return plateau

    elif (indice == 6):  # On a définit l'IA MIN-MAX avec la strategie MOBILITE
        _, numero_a_jouer = min_max_ordi_mobilite("max", plateau, pion_joueur, pion_adverse, profondeur,
                                                  nb_coup_possible_joueur1, nb_coup_possible_joueur2)
        plateau = jouer_numero(plateau, pion_joueur, numero_a_jouer)
        return plateau
    elif (indice == 7):  # On a définit l'IA ALPHA-BETA avec la strategie MOBILITE
        _, numero_a_jouer = alpha_beta_ordi_mobilite("max", -1000000000, 1000000000, plateau, pion_joueur, pion_adverse,
                                                     profondeur, nb_coup_possible_joueur1, nb_coup_possible_joueur2)
        plateau = jouer_numero(plateau, pion_joueur, numero_a_jouer)
        return plateau

    elif (indice == 8):  # On a définit l'IA MIN-MAX avec la strategie MIXTE
        # return jouer_ordi_mixte(plateau, pion_joueur, pion_adverse, coup_numero)     #PREMIER FONCTION TEST POUR LA COMPREHENSION
        plateau = min_max_ordi_mixte_silencieux(plateau, pion_joueur, pion_adverse, profondeur,
                                                nb_coup_possible_joueur1, nb_coup_possible_joueur2, coup_numero)
        return plateau
    elif (indice == 9):  # On a définit l'IA ALPHA-BETA avec la strategie MIXTE
        # return jouer_ordi_mixte(plateau, pion_joueur, pion_adverse, coup_numero)     #PREMIER FONCTION TEST POUR LA COMPREHENSION
        plateau = alpha_beta_ordi_mixte_silencieux(plateau, pion_joueur, pion_adverse, profondeur,
                                                   nb_coup_possible_joueur1, nb_coup_possible_joueur2, coup_numero)
        return plateau


def alpha_beta_ordi_mixte_silencieux(plateau, pion_de_lordi, pion_adverse, profondeur, nb_coup_joueur1, nb_coup_joueur2,
                                     coup_numero):
    """ Fonction qui fait la même chose que "alpha_beta_ordi_mixte" mais de facon silencieux
    """
    coup_possible_max_sur_plateau = len(plateau) * len(plateau[0])
    if (coup_numero > 0 and coup_numero < 25):
        return jouer_silencieux(3, plateau, pion_de_lordi, pion_adverse, coup_numero, nb_coup_joueur1, nb_coup_joueur2,
                                profondeur)
    elif (coup_numero >= 25 and coup_numero < (coup_possible_max_sur_plateau - 16)):
        return jouer_silencieux(7, plateau, pion_de_lordi, pion_adverse, coup_numero, nb_coup_joueur1, nb_coup_joueur2,
                                profondeur)
    else:  # (coup_numero >= (coup_possible_max_sur_plateau - 16) and coup_numero < coup_possible_max_sur_plateau)
        return jouer_silencieux(5, plateau, pion_de_lordi, pion_adverse, coup_numero, nb_coup_joueur1, nb_coup_joueur2,
                                profondeur)


def min_max_ordi_mixte_silencieux(plateau, pion_de_lordi, pion_adverse, profondeur, nb_coup_joueur1, nb_coup_joueur2,
                                  coup_numero):
    """ Fonction qui fait la même chose que "min_max_ordi_mixte" mais de facon silencieux
    """
    coup_possible_max_sur_plateau = len(plateau) * len(plateau[0])
    if (coup_numero > 0 and coup_numero < 25):
        return jouer_silencieux(2, plateau, pion_de_lordi, pion_adverse, coup_numero, nb_coup_joueur1, nb_coup_joueur2,
                                profondeur)
    elif (coup_numero >= 25 and coup_numero < (coup_possible_max_sur_plateau - 16)):
        return jouer_silencieux(6, plateau, pion_de_lordi, pion_adverse, coup_numero, nb_coup_joueur1, nb_coup_joueur2,
                                profondeur)
    else:  # (coup_numero >= (coup_possible_max_sur_plateau - 16) and coup_numero < coup_possible_max_sur_plateau)
        return jouer_silencieux(4, plateau, pion_de_lordi, pion_adverse, coup_numero, nb_coup_joueur1, nb_coup_joueur2,
                                profondeur)


# -------------------------------------------------------------------------
# --------                     Execution                             ------
# -------------------------------------------------------------------------

plateau = init_plateau(8, 8)  # Initialise le plateau de jeu de taille 8*8
plateau = init_pion(plateau, 1)  # Initialise les pions avec les positions de pions "1"

print("Quel mode de jeu voulez-vous ? :" +
      "\n\t1/Mode classique (1 seul partie avec les joueurs que vous voulez)" +
      "\n\t2/Mode évalutation (effecte IA vs IA pour chaque type différent, en " +
      "enlevant l'affichage) avec une profondeur allant de 1 à 5 " +
      "(et stockage des résultats dans un TXT)")
print("Saisir un entier : ", end="")
mode_de_jeu = saisir_entier(2)

print("\n\n\n")

if (mode_de_jeu == 1):
    # Demande qui joue en joueur 1 avec la profondeur de l'IA si s'en est une.
    profondeur_joueur1 = 1
    print("Bonjour qui est le joueur 1 ? :" +
          "\n\t1/Un Humain" +
          "\n\t2/Une IA : Stratégie POSITIONNEL 'min-max'" +
          "\n\t3/Une IA : Stratégie POSITIONNEL 'alpha-beta'" +
          "\n\t4/Une IA : Stratégie ABSOLU 'min-max'" +
          "\n\t5/Une IA : Stratégie ABSOLU 'alpha-beta'" +
          "\n\t6/Une IA : Stratégie MOBILITE 'min-max'" +
          "\n\t7/Une IA : Stratégie MOBILITE 'alpha-beta'" +
          "\n\t8/Une IA : Stratégie MIXTE 'min-max'" +
          "\n\t9/Une IA : Stratégie MIXTE 'alpha-beta'")
    print("Saisir un entier : ", end="")
    indice_joueur1 = saisir_entier(9)
    if (indice_joueur1 > 1 and indice_joueur1 < 10):
        print("Veuillez saisir une profondeur pour l'IA : ", end="")
        profondeur_joueur1 = saisir_entier(100)

    print("\n")

    # Demande qui joue en joueur 2 avec la profondeur de l'IA si s'en est une.
    profondeur_joueur2 = 1
    print("Et qui est le joueur 2 ? :" +
          "\n\t1/Un Humain" +
          "\n\t2/Une IA : Stratégie POSITIONNEL 'min-max'" +
          "\n\t3/Une IA : Stratégie POSITIONNEL 'alpha-beta'" +
          "\n\t4/Une IA : Stratégie ABSOLU 'min-max'" +
          "\n\t5/Une IA : Stratégie ABSOLU 'alpha-beta'" +
          "\n\t6/Une IA : Stratégie MOBILITE 'min-max'" +
          "\n\t7/Une IA : Stratégie MOBILITE 'alpha-beta'" +
          "\n\t8/Une IA : Stratégie MIXTE 'min-max'" +
          "\n\t9/Une IA : Stratégie MIXTE 'alpha-beta'")
    print("Saisir un entier : ", end="")
    indice_joueur2 = saisir_entier(9)
    if (indice_joueur2 > 1 and indice_joueur2 < 10):
        print("Veuillez saisir une profondeur pour l'IA : ", end="")
        profondeur_joueur2 = saisir_entier(100)

    print("\n-------------------------------------------------------\n")
    print("\n=======================================================\n")
    print("\n-------------------------------------------------------\n")

    nb_coup_possible_joueur1 = 1  # indique le nombre de coup possible pour le joueur 1
    nb_coup_possible_joueur2 = 1  # indique le nombre de coup possible pour le joueur 2
    coup_numero = 0  # indique le nombre de coup au quel on joue (pour mixte // car joue différement en fonction du nombre de coup deja joué
    joueur = 1  # le joueur numeor 1 commence
    while (est_plein(plateau) == False and (
            nb_coup_possible_joueur1 > 0 or nb_coup_possible_joueur2 > 0)):  # Si le tableau est plein ou que aucun des 2 joueurs ne peut jouer
        nb_pion1, nb_pion2 = compter_pion(plateau, "☺", "☻")  # On compte les pion
        print("\n\nIl y a " + str(nb_pion1) + " pions ☺ // Il y a " + str(
            nb_pion2) + " pions ☻")  # Et on affiche le résultat
        if (joueur == 1):  # Si C'est le joueur 1 qui joue
            coup_numero += 1
            print("Coups possibles pour le joueur possédant le pion ☺ : ")
            plateau, nb_coup_possible_joueur1 = coup_possible(plateau, "☻", "☺")
            afficher_plateau(plateau)
            plateau = jouer(indice_joueur1, plateau, "☺", "☻", coup_numero, nb_coup_possible_joueur1,
                            nb_coup_possible_joueur2, profondeur_joueur1)
            plateau = supprimer_coup_possible(plateau)
            joueur = 2  # On donne le jeu à l'autre joueur
        else:  # if(joueur == 2): #Si C'est le joueur 2 qui joue
            coup_numero += 1
            print("Coups possibles pour le joueur possédant le pion ☻ : ")
            plateau, nb_coup_possible_joueur2 = coup_possible(plateau, "☺", "☻")
            afficher_plateau(plateau)
            plateau = jouer(indice_joueur2, plateau, "☻", "☺", coup_numero, nb_coup_possible_joueur2,
                            nb_coup_possible_joueur1, profondeur_joueur2)
            plateau = supprimer_coup_possible(plateau)
            joueur = 1  # On donne le jeu à l'autre joueur
        print("\n-------------------------------------------------------\n")

    # FIN DE LA PARTIE CAR ON EST SORTI DE LA BOUCLE

    print("\n\n")
    afficher_plateau(plateau)

    # Indique le résultat final
    nb_pion1, nb_pion2 = compter_pion(plateau, "☺", "☻")
    print("\n\nFIN DE LA PARTIE DE JEU!!!\n\n" +
          "Il y a " + str(nb_pion1) + " pions ☺ VS " + str(nb_pion2) + " pions ☻")
    if (nb_pion1 == nb_pion2):
        print("\n=========================\nEgalité !!!\n=========================")
    elif (nb_pion1 > nb_pion2):
        print("\n=========================\nLe joueur N°1 A GAGNE !!!\n=========================")
    else:
        print("\n=========================\nLe joueur N°2 A GAGNE !!!\n=========================")

    print("\n\n")







elif (mode_de_jeu == 2):
    indice_joueur1 = 0
    indice_joueur1 = 0
    profondeur_joueur1 = 0
    profondeur_joueur1 = 0

    with open("resultat.txt", 'wb', 0) as f:
        f.write(bytes(
            'profondeur IA:1vs1,1vs2,1vs3,1vs4,1vs5,2vs1,2vs2,2vs3,2vs4,2vs5,3vs1,3vs2,3vs3,3vs4,3vs5,4vs1,4vs2,4vs3,4vs4,4vs5,5vs1,5vs2,5vs3,5vs4,5vs5\n',
            'utf-8'))

        for indice_joueur1 in range(3, 10, 2):
            for indice_joueur2 in range(3, 10, 2):
                result_ = []
                for profondeur_joueur1 in range(1, 6):
                    for profondeur_joueur2 in range(1, 6):

                        plateau = init_plateau(8, 8)  # Initialise le plateau de jeu de taille 8*8
                        plateau = init_pion(plateau, 1)  # Initialise les pions avec les positions de pions "1"

                        print("Evaluation de l'IA n°" + str(indice_joueur1) + " avec une profondeur de " + str(
                            profondeur_joueur1) + " contre l'IA n°" + str(
                            indice_joueur2) + " avec une profondeur de " + str(profondeur_joueur2) + ".......")

                        nb_coup_possible_joueur1 = 1  # indique le nombre de coup possible pour le joueur 1
                        nb_coup_possible_joueur2 = 1  # indique le nombre de coup possible pour le joueur 2
                        coup_numero = 0  # indique le nombre de coup au quel on joue (pour mixte // car joue différement en fonction du nombre de coup deja joué
                        joueur = 1  # le joueur numeor 1 commence
                        while (est_plein(plateau) == False and (
                                nb_coup_possible_joueur1 > 0 or nb_coup_possible_joueur2 > 0)):  # Si le tableau est plein ou que aucun des 2 joueurs ne peut jouer
                            nb_pion1, nb_pion2 = compter_pion(plateau, "☺", "☻")  # On compte les pion
                            # print("\n\nIl y a " + str(nb_pion1) + " pions ☺ // Il y a " + str(nb_pion2) + " pions ☻")   #Et on affiche le résultat
                            if (joueur == 1):  # Si C'est le joueur 1 qui joue
                                coup_numero += 1
                                # print("Coups possibles pour le joueur possédant le pion ☻ : ")
                                plateau, nb_coup_possible_joueur1 = coup_possible(plateau, "☻", "☺")
                                # afficher_plateau(plateau)
                                plateau = jouer_silencieux(indice_joueur1, plateau, "☺", "☻", coup_numero,
                                                           nb_coup_possible_joueur1, nb_coup_possible_joueur2,
                                                           profondeur_joueur1)
                                plateau = supprimer_coup_possible(plateau)
                                joueur = 2  # On donne le jeu à l'autre joueur
                            else:  # if(joueur == 2): #Si C'est le joueur 2 qui joue
                                coup_numero += 1
                                # print("Coups possibles pour le joueur possédant le pion ☺ : ")
                                plateau, nb_coup_possible_joueur2 = coup_possible(plateau, "☺", "☻")
                                # afficher_plateau(plateau)
                                plateau = jouer_silencieux(indice_joueur2, plateau, "☻", "☺", coup_numero,
                                                           nb_coup_possible_joueur2, nb_coup_possible_joueur1,
                                                           profondeur_joueur2)
                                plateau = supprimer_coup_possible(plateau)
                                joueur = 1  # On donne le jeu à l'autre joueur
                            # print("\n-------------------------------------------------------\n")

                        # FIN DE LA PARTIE CAR ON EST SORTI DE LA BOUCLE

                        # print("\n\n")
                        # afficher_plateau(plateau)

                        # Indique le résultat final
                        nb_pion1, nb_pion2 = compter_pion(plateau, "☺", "☻")
                        print("\n\nFIN DE LA PARTIE DE JEU!!!\n" +
                              "Il y a " + str(nb_pion1) + " pions ☺ VS " + str(nb_pion2) + " pions ☻")
                        if (nb_pion1 == nb_pion2):
                            print("\nLe joueur 1 (l'IA n°" + str(indice_joueur1) + " avec une profondeur de " + str(
                                profondeur_joueur1) + ") est à égalité contre le joueur 2 (l'IA n°" + str(
                                indice_joueur2) + " avec une profondeur de " + str(profondeur_joueur2))
                            result_.append(0)
                            # print(str(result_))
                        elif (nb_pion1 > nb_pion2):
                            print("\nLe joueur 1 (l'IA n°" + str(indice_joueur1) + " avec une profondeur de " + str(
                                profondeur_joueur1) + ") à gagner contre le joueur 2 (l'IA n°" + str(
                                indice_joueur2) + " avec une profondeur de " + str(profondeur_joueur2))
                            result_.append(1)
                            # print(str(result_))
                        else:
                            print("\nLe joueur 2 (l'IA n°" + str(indice_joueur2) + " avec une profondeur de " + str(
                                profondeur_joueur2) + ") à gagner contre le joueur 1 (l'IA n°" + str(
                                indice_joueur1) + " avec une profondeur de " + str(profondeur_joueur1))
                            result_.append(2)
                            # print(str(result_))

                        print("\n-------------------------------------------------------\n")

                print("\n-------------------------------------------------------\n")
                print("-------------------------------------------------------")
                print("\n-------------------------------------------------------\n")
                print(str(result_))
                f.write(bytes("IA n°" + str(indice_joueur1) + " contre IA n°" + str(indice_joueur2) + " : ", 'utf-8'))
                f.write(bytes(str(result_) + "\n", 'utf-8'))


#             ----------------------            #
#           FONCTION DE COMPREHENSION           #
#             ----------------------            #
#               FONCTION DE TEST                #
#             ----------------------            #


def jouer_ordi_absolu(plateau, pion_de_lordi, pion_adverse):
    """ Fonction retournant le "plateau" en jouant (ajoutant) le pion
        "pion_de_lordi" en paramètre sur un des numéros avec la stratégie
        ABSOLU.
        ABSOLU : prise en compte de la différence du nombre de pions.
        Où "plateau" est une matrice de taille supérieur à 2 pour x et y
        et avec les coups possible.
        où "pion_de_lordi" un caractère à ajouter sur la case "numero_retenu".
    """

    numero_retenu = -1
    valeur_tactique_retenu = -1000  # nb pion ordi - nb pion adverse
    temp_plateau = copy.deepcopy(plateau)  # Réalise une deep copy du plateau de jeu

    for i in range(len(plateau)):
        for j in range(len(plateau[0])):
            if (isinstance(plateau[i][j], int)):  # SI plateau[i][j] EST UN ENTIER
                temp_plateau = copy.deepcopy(plateau)  # Réalise une deep copy du plateau de jeu
                jouer_numero(temp_plateau, pion_de_lordi, plateau[i][j])  # On simule le fait que l'on jou sur la case
                nb_pion1, nb_pion2 = compter_pion(temp_plateau, pion_de_lordi,
                                                  pion_adverse)  # On compte les pions sur la simulation
                valeur_tactique = nb_pion1 - nb_pion2
                if (valeur_tactique > valeur_tactique_retenu):
                    valeur_tactique_retenu = valeur_tactique
                    numero_retenu = plateau[i][j]

    if (numero_retenu != -1):
        plateau = jouer_numero(plateau, pion_de_lordi, numero_retenu)
        print("L'IA ABSOLU a jouer sur le numéro " + str(numero_retenu) + "\n")
    else:
        print("L'IA ABSOLU n'a pas pu jouer :(. Elle doit donner la main à l'adversaire..\n")

    return plateau


def jouer_ordi_positionnel(plateau, pion_de_lordi):
    """ Fonction retournant le "plateau" en jouant (ajoutant) le pion
        "pion_de_lordi" en paramètre sur un des numéros avec la stratégie
        POSITIONNEL.
        POSITIONNEL : prise en compte des poids statique du tableau (Cf. cours),
        l’évaluation est la différence entre les poids associés des deux joueurs.
        Où "plateau" est une matrice de taille 8 et 8 pour x et y
        et avec les coups possible.
        où "pion_de_lordi" un caractère à ajouter sur la case "numero_retenu".
    """
    matrice_de_valeur_tactiques = [[500, -150, 30, 10, 10, 30, -150, 500],
                                   [-150, -250, 0, 0, 0, 0, -250, -150],
                                   [30, 0, 1, 2, 2, 1, 0, 30],
                                   [10, 0, 2, 16, 16, 2, 0, 10],
                                   [10, 0, 2, 16, 16, 2, 0, 10],
                                   [30, 0, 1, 2, 2, 1, 0, 30],
                                   [-150, -250, 0, 0, 0, 0, -250, -150],
                                   [500, -150, 30, 10, 10, 30, -150, 500]]

    numero_retenu = -1
    valeur_tactique_retenu = -1000

    for i in range(len(plateau)):
        for j in range(len(plateau[0])):
            if (isinstance(plateau[i][j], int)):  # SI plateau[i][j] EST UN ENTIER
                if (matrice_de_valeur_tactiques[i][j] > valeur_tactique_retenu):
                    valeur_tactique_retenu = matrice_de_valeur_tactiques[i][j]
                    numero_retenu = plateau[i][j]

    if (numero_retenu != -1):
        plateau = jouer_numero(plateau, pion_de_lordi, numero_retenu)
        print("L'IA POSITIONNEL a jouer sur le numéro " + str(numero_retenu) + "\n")
    else:
        print("L'IA POSITIONNEL n'a pas pu jouer :(. Elle doit donner la main à l'adversaire..\n")

    return plateau, valeur_tactique_retenu, numero_retenu


def jouer_ordi_mobilite(plateau, pion_de_lordi, pion_adverse):
    """ Fonction retournant le "plateau" en jouant (ajoutant) le pion
        "pion_de_lordi" en paramètre sur un des numéros avec la stratégie
        MOBILITE.
        MOBILITE : maximise le nombre de coups possibles et minimise les
        coups de l’adversaire tout en essayant de prendre les coins.
        Où "plateau" est une matrice de taille supérieur à 2 pour x et y
        et avec les coups possible.
        où "pion_de_lordi" un caractère à ajouter sur la case "numero_retenu".
    """

    numero_retenu = -1
    valeur_tactique_retenu = -1000  # nb pion ordi - nb pion adverse
    temp_plateau = copy.deepcopy(plateau)  # Réalise une deep copy du plateau de jeu
    poubelle = ""

    poubelle, nb_coup_possible_pion1 = coup_possible(plateau, pion_adverse, pion_de_lordi)

    for i in range(len(plateau)):
        for j in range(len(plateau[0])):
            if (isinstance(plateau[i][j], int)):  # SI plateau[i][j] EST UN ENTIER
                if ((i == 0 and j == 0) or (i == len(plateau) - 1 and j == 0) or (
                        i == 0 and j == len(plateau[0]) - 1) or (i == len(plateau) - 1 and j == len(plateau[0]) - 1)):
                    numero_retenu = plateau[i][j]
                    break  # break de la double loop grâce au "else: continu     break"
                else:
                    temp_plateau = copy.deepcopy(plateau)  # Réalise une deep copy du plateau de jeu
                    jouer_numero(temp_plateau, pion_de_lordi,
                                 plateau[i][j])  # On simule le fait que l'on jou sur la case
                    poubelle, nb_coup_possible_pion2_apres_coup = coup_possible(temp_plateau, pion_de_lordi,
                                                                                pion_adverse)  # On compte les pions sur la simulation
                    valeur_tactique = nb_coup_possible_pion1 - nb_coup_possible_pion2_apres_coup
                    if (valeur_tactique > valeur_tactique_retenu):
                        valeur_tactique_retenu = valeur_tactique
                        numero_retenu = plateau[i][j]
        else:
            continue
        break

    if (numero_retenu != -1):
        plateau = jouer_numero(plateau, pion_de_lordi, numero_retenu)
        print("L'IA MOBILITE à jouer sur le numéro " + str(numero_retenu) + "\n")
    else:
        print("L'IA MOBILITE n'a pas pu jouer :(. Elle doit donner la main à l'adversaire..\n")

    return plateau


def jouer_ordi_mixte(plateau, pion_de_lordi, pion_adverse, coup_numero):
    """ Fonction retournant le "plateau" en jouant (ajoutant) le pion
        "pion_de_lordi" en paramètre sur un des numéros avec la stratégie
        MIXTE.
        MIXTE : le jeu est divisé en trois phases où les stratégies peuvent différer
        : (i) en début de partie (20 à 25 premiers coups), le joueur IA choisit
        une stratégie de type ’positionnel’, au milieu de partie, sélectionne une
        stratégie de ’mobilité’ ; et enfin en fin de partie (10 à 16 derniers coups),
        sélectionne la stratégie ’absolu’.

        Où "plateau" est une matrice de taille supérieur à 2 pour x et y
        et avec les coups possible.
        où "pion_de_lordi" un caractère à ajouter sur la case "numero_retenu"
        où "pion_adverse" un catactère définisant e pion adverse
        où "coup_numero" entier correspondant au nombre de coups jouer depuis le debut.
    """
    coup_possible_max_sur_plateau = len(plateau) * len(plateau[0])

    if (coup_numero > 0 and coup_numero < 25):
        print("L'IA MIXTE donne la main à l'IA POSITIONNEL pour ce coup :")
        return jouer_ordi_positionnel(plateau, pion_de_lordi)
    elif (coup_numero >= 25 and coup_numero < (coup_possible_max_sur_plateau - 16)):
        print("L'IA MIXTE donne la main à l'IA MOBILITE pour ce coup :")
        return jouer_ordi_mobilite(plateau, pion_de_lordi, pion_adverse)
    else:  # (coup_numero >= (coup_possible_max_sur_plateau - 16) and coup_numero < coup_possible_max_sur_plateau)
        print("L'IA MIXTE donne la main à l'IA ABSOLU pour ce coup :")
        return jouer_ordi_absolu(plateau, pion_de_lordi, pion_adverse)


"""

#Test couleur
print("\033[1;32;40m Bright Green  \n")

"""
