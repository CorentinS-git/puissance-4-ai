"""
board.py : Représentation du plateau de Puissance 4 et des règles du jeu.
"""

# Constantes du plateau
LIGNES = 6
COLONNES = 7

VIDE = 0
JOUEUR_1 = 1
JOUEUR_2 = 2


class Board:
    def __init__(self):
        # Grille représentée par une liste de listes (LIGNES x COLONNES)
        # La ligne 0 est le HAUT du plateau, la ligne 5 est le BAS.
        self.grille = [[VIDE for _ in range(COLONNES)] for _ in range(LIGNES)]

    def afficher(self):
        """Affiche la grille dans la console."""
        print()
        for ligne in self.grille:
            # Affiche chaque case entourée de séparateurs |
            symboles = []
            for case in ligne:
                if case == VIDE:
                    symboles.append("·")
                elif case == JOUEUR_1:
                    symboles.append("X")  # Joueur 1
                else:
                    symboles.append("O")  # Joueur 2
            print("| " + " ".join(symboles) + " |")
        
        # Affichage des numéros de colonnes (0 à 6)
        print("+" + "-" * (COLONNES * 2 + 1) + "+")
        print("  " + " ".join(str(c) for c in range(COLONNES)))
        print()

    def est_colonne_valide(self, col):
        """Une colonne est valide si elle est dans la grille et que sa case du haut est vide."""
        if col < 0 or col >= COLONNES:
            return False
        return self.grille[0][col] == VIDE

    def get_colonnes_valides(self):
        """Retourne la liste des indices de colonnes non pleines."""
        return [c for c in range(COLONNES) if self.est_colonne_valide(c)]

    def get_prochaine_ligne_libre(self, col):
        """
        Simule la gravité : cherche la case vide la plus basse dans la colonne.
        Retourne l'indice de ligne (de 5 vers 0), ou None si la colonne est pleine.
        """
        for r in range(LIGNES - 1, -1, -1):
            if self.grille[r][col] == VIDE:
                return r
        return None

    def jouer_coup(self, col, piece):
        """
        Joue un coup dans la colonne donnée pour le joueur 'piece'.
        Retourne True si le coup a été joué, False sinon.
        """
        ligne = self.get_prochaine_ligne_libre(col)
        if ligne is not None:
            self.grille[ligne][col] = piece
            return True
        return False

    def verifier_victoire(self, piece):
        """Vérifie si le joueur 'piece' a aligné 4 jetons."""
        # 1. Vérification horizontale
        for r in range(LIGNES):
            for c in range(COLONNES - 3):
                if (self.grille[r][c] == piece and
                    self.grille[r][c + 1] == piece and
                    self.grille[r][c + 2] == piece and
                    self.grille[r][c + 3] == piece):
                    return True

        # 2. Vérification verticale
        for r in range(LIGNES - 3):
            for c in range(COLONNES):
                if (self.grille[r][c] == piece and
                    self.grille[r + 1][c] == piece and
                    self.grille[r + 2][c] == piece and
                    self.grille[r + 3][c] == piece):
                    return True

        # 3. Vérification diagonale descendante (\)
        for r in range(LIGNES - 3):
            for c in range(COLONNES - 3):
                if (self.grille[r][c] == piece and
                    self.grille[r + 1][c + 1] == piece and
                    self.grille[r + 2][c + 2] == piece and
                    self.grille[r + 3][c + 3] == piece):
                    return True

        # 4. Vérification diagonale ascendante (/)
        for r in range(3, LIGNES):
            for c in range(COLONNES - 3):
                if (self.grille[r][c] == piece and
                    self.grille[r - 1][c + 1] == piece and
                    self.grille[r - 2][c + 2] == piece and
                    self.grille[r - 3][c + 3] == piece):
                    return True

        return False

    def est_plein(self):
        """Vérifie si le plateau est plein (match nul)."""
        return len(self.get_colonnes_valides()) == 0