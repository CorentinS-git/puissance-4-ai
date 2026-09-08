"""
main.py : Boucle de jeu principale en mode console (PvP ou PvIA).
"""
from core.board import Board, JOUEUR_1, JOUEUR_2
from ai.minimax import choisir_coup_ia


def demander_coup_humain(plateau, joueur, symbole):
    while True:
        try:
            colonne = int(input(f"Joueur {joueur} ({symbole}), choisis une colonne (0-6) : "))
            if plateau.est_colonne_valide(colonne):
                return colonne
            print("Colonne pleine ou invalide. Réessaie.")
        except ValueError:
            print("Entrée invalide. Choisis un entier entre 0 et 6.")


def lancer_partie():
    print("=== Puissance 4 ===")
    print("1. Joueur vs Joueur")
    print("2. Joueur vs IA")
    choix_mode = input("Choix du mode (1 ou 2) : ").strip()

    mode_ia = (choix_mode == "2")
    difficulte = "moyen"

    if mode_ia:
        print("\nDifficultés disponibles : facile, moyen, difficile")
        entree_diff = input("Choisis la difficulté (défaut: moyen) : ").strip().lower()
        if entree_diff in ["facile", "moyen", "difficile"]:
            difficulte = entree_diff

    plateau = Board()
    joueur_actuel = JOUEUR_1
    partie_terminee = False

    print("\nDébut de la partie !")
    print("Joueur 1 = X | Joueur 2 = O")
    plateau.afficher()

    while not partie_terminee:
        symbole = "X" if joueur_actuel == JOUEUR_1 else "O"

        # Tour du joueur 1 ou du joueur 2
        if joueur_actuel == JOUEUR_1 or not mode_ia:
            colonne = demander_coup_humain(plateau, joueur_actuel, symbole)
        else:
            print(f"L'IA ({difficulte}) réfléchit...")
            colonne = choisir_coup_ia(plateau, difficulte=difficulte, piece_ia=JOUEUR_2)
            print(f"L'IA a joué dans la colonne {colonne}.")

        plateau.jouer_coup(colonne, joueur_actuel)
        plateau.afficher()

        if plateau.verifier_victoire(joueur_actuel):
            gagnant = "L'IA" if (mode_ia and joueur_actuel == JOUEUR_2) else f"Le Joueur {joueur_actuel}"
            print(f"Partie terminée : {gagnant} a gagné !")
            partie_terminee = True
        elif plateau.est_plein():
            print("Match nul ! Le plateau est plein.")
            partie_terminee = True
        else:
            joueur_actuel = JOUEUR_2 if joueur_actuel == JOUEUR_1 else JOUEUR_1


if __name__ == "__main__":
    lancer_partie()