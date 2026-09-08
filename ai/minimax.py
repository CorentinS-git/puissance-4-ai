"""
ai/minimax.py : Algorithme Minimax avec élagage Alpha-Bêta et sélection de coup.
"""
import math
import random
from core.board import JOUEUR_1, JOUEUR_2
from ai.evaluation import evaluer_position


def ordonner_colonnes(colonnes_valides):
    """
    Trie les colonnes pour tester le centre en priorité (3, puis 2 et 4, etc.).
    Cela maximise les coupes de branches dans l'élagage Alpha-Bêta.
    """
    ordre_ideal = [3, 2, 4, 1, 5, 0, 6]
    return [c for c in ordre_ideal if c in colonnes_valides]


def minimax(board, profondeur, alpha, beta, maximiser, piece_ia):
    adversaire = JOUEUR_1 if piece_ia == JOUEUR_2 else JOUEUR_2
    colonnes_valides = board.get_colonnes_valides()
    
    # Conditions d'arrêt : victoire, défaite, match nul ou profondeur limite
    if board.verifier_victoire(piece_ia):
        return (None, 10000000)
    if board.verifier_victoire(adversaire):
        return (None, -10000000)
    if len(colonnes_valides) == 0:
        return (None, 0)
    if profondeur == 0:
        return (None, evaluer_position(board, piece_ia))

    colonnes_triees = ordonner_colonnes(colonnes_valides)

    if maximiser:
        meilleur_score = -math.inf
        meilleure_colonne = random.choice(colonnes_valides)

        for col in colonnes_triees:
            board.jouer_coup(col, piece_ia)
            _, score = minimax(board, profondeur - 1, alpha, beta, False, piece_ia)
            board.annuler_coup(col)

            if score > meilleur_score:
                meilleur_score = score
                meilleure_colonne = col

            alpha = max(alpha, meilleur_score)
            if alpha >= beta:
                break  # Coupure bêta
        return meilleure_colonne, meilleur_score

    else:
        meilleur_score = math.inf
        meilleure_colonne = random.choice(colonnes_valides)

        for col in colonnes_triees:
            board.jouer_coup(col, adversaire)
            _, score = minimax(board, profondeur - 1, alpha, beta, True, piece_ia)
            board.annuler_coup(col)

            if score < meilleur_score:
                meilleur_score = score
                meilleure_colonne = col

            beta = min(beta, meilleur_score)
            if alpha >= beta:
                break  # Coupure alpha
        return meilleure_colonne, meilleur_score


def choisir_coup_ia(board, difficulte="moyen", piece_ia=JOUEUR_2):
    colonnes_valides = board.get_colonnes_valides()
    adversaire = JOUEUR_1 if piece_ia == JOUEUR_2 else JOUEUR_2

    if difficulte == "facile":
        # Comportement type enfant : 
        # Tente de gagner si l'occasion se présente immédiatement
        for col in colonnes_valides:
            board.jouer_coup(col, piece_ia)
            if board.verifier_victoire(piece_ia):
                board.annuler_coup(col)
                return col
            board.annuler_coup(col)

        # Bloque seulement 1 fois sur 3 (fait des étourderies)
        if random.random() < 0.35:
            for col in colonnes_valides:
                board.jouer_coup(col, adversaire)
                if board.verifier_victoire(adversaire):
                    board.annuler_coup(col)
                    return col
                board.annuler_coup(col)

        return random.choice(colonnes_valides)

    elif difficulte == "moyen":
        # Profondeur 2 ou 3 : voit les coups immédiats mais faillible sur les enchaînements
        colonne, _ = minimax(board, profondeur=3, alpha=-math.inf, beta=math.inf, maximiser=True, piece_ia=piece_ia)
        return colonne

    else:  # "difficile" 
        colonne, _ = minimax(board, profondeur=5, alpha=-math.inf, beta=math.inf, maximiser=True, piece_ia=piece_ia)
        return colonne