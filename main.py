"""
main.py : Boucle de jeu principale en mode console (Joueur vs Joueur).
"""
from core.board import Board, JOUEUR_1, JOUEUR_2


def lancer_partie():
    plateau = Board()
    joueur_actuel = JOUEUR_1
    partie_terminee = False

    print("=== Puissance 4 (Mode Console) ===")
    print("Joueur 1 = X | Joueur 2 = O")
    plateau.afficher()

    while not partie_terminee:
        symbole = "X" if joueur_actuel == JOUEUR_1 else "O"
        
        # Demander la colonne au joueur
        try:
            colonne = int(input(f"Joueur {joueur_actuel} ({symbole}), choisis une colonne (0-6) : "))
        except ValueError:
            print("Erreur : entre un chiffre entier entre 0 et 6.")
            continue

        # Vérifier si la colonne est valide
        if not plateau.est_colonne_valide(colonne):
            print("Coup invalide (colonne pleine ou inexistante). Réessaie.")
            continue

        # Jouer le coup
        plateau.jouer_coup(colonne, joueur_actuel)
        plateau.afficher()

        # Vérifier s'il y a victoire
        if plateau.verifier_victoire(joueur_actuel):
            print(f"Bravo ! Le Joueur {joueur_actuel} ({symbole}) a gagné !")
            partie_terminee = True
        elif plateau.est_plein():
            print("Match nul ! Le plateau est plein.")
            partie_terminee = True
        else:
            # Alterner le tour
            joueur_actuel = JOUEUR_2 if joueur_actuel == JOUEUR_1 else JOUEUR_1


if __name__ == "__main__":
    lancer_partie()