"""
ai/evaluation.py : Fonction heuristique évaluant l'avantage d'une position.
"""
from core.board import LIGNES, COLONNES, VIDE, JOUEUR_1, JOUEUR_2


def evaluer_fenetre(fenetre, piece):
    """
    Attribue un score à un sous-segment de 4 cases contiguës.
    """
    score = 0
    adversaire = JOUEUR_1 if piece == JOUEUR_2 else JOUEUR_2

    nb_piece = fenetre.count(piece)
    nb_vide = fenetre.count(VIDE)
    nb_adv = fenetre.count(adversaire)

    if nb_piece == 4:
        score += 100000
    elif nb_piece == 3 and nb_vide == 1:
        score += 100
    elif nb_piece == 2 and nb_vide == 2:
        score += 10

    # Pénalité si l'adversaire prépare un alignement de 3
    if nb_adv == 3 and nb_vide == 1:
        score -= 80

    return score


def evaluer_position(board, piece):
    """
    Calcule le score global du plateau du point de vue de 'piece'.
    """
    score = 0

    # 1. Bonus pour le contrôle de la colonne centrale (colonne 3)
    colonne_centre = [board.grille[r][COLONNES // 2] for r in range(LIGNES)]
    score += colonne_centre.count(piece) * 6

    # 2. Évaluation des fenêtres horizontales
    for r in range(LIGNES):
        ligne = board.grille[r]
        for c in range(COLONNES - 3):
            fenetre = ligne[c:c + 4]
            score += evaluer_fenetre(fenetre, piece)

    # 3. Évaluation des fenêtres verticales
    for c in range(COLONNES):
        colonne = [board.grille[r][c] for r in range(LIGNES)]
        for r in range(LIGNES - 3):
            fenetre = colonne[r:r + 4]
            score += evaluer_fenetre(fenetre, piece)

    # 4. Évaluation diagonale descendante (\)
    for r in range(LIGNES - 3):
        for c in range(COLONNES - 3):
            fenetre = [board.grille[r + i][c + i] for i in range(4)]
            score += evaluer_fenetre(fenetre, piece)

    # 5. Évaluation diagonale ascendante (/)
    for r in range(3, LIGNES):
        for c in range(COLONNES - 3):
            fenetre = [board.grille[r - i][c + i] for i in range(4)]
            score += evaluer_fenetre(fenetre, piece)

    return score