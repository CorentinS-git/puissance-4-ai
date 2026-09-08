"""
game_gui.py : Boucle principale et machine à états (Menu -> Choix -> Jeu -> Fin).
"""
import sys
import time
import pygame
from core.board import Board, JOUEUR_1, JOUEUR_2
from ai.minimax import choisir_coup_ia
from ui.gui import Puissance4GUI, Bouton, TAILLE_CASE, LARGEUR, HAUTEUR


def main():
    gui = Puissance4GUI()
    horloge = pygame.time.Clock()

    etat = "MENU"  # États possibles : MENU, CHOIX_DIFF, JEU, FIN
    difficulte = "moyen"

    # Variables de suivi de partie
    plateau = None
    joueur_actuel = JOUEUR_1
    gagnant_texte = ""
    temps_debut = 0.0
    temps_total = 0.0
    nb_coups = 0
    x_souris = LARGEUR // 2

    # Boutons du menu d'accueil
    boutons_menu = [
        Bouton((LARGEUR // 2 - 140, 310, 280, 55), "Start the game", "start"),
        Bouton((LARGEUR // 2 - 140, 390, 280, 55), "Quitter", "quitter", couleur=(192, 57, 43), couleur_survol=(231, 76, 60))
    ]

    # Boutons de sélection de difficulté
    boutons_diff = [
        Bouton((LARGEUR // 2 - 140, 230, 280, 50), "Facile", "facile"),
        Bouton((LARGEUR // 2 - 140, 300, 280, 50), "Moyen", "moyen"),
        Bouton((LARGEUR // 2 - 140, 370, 280, 50), "Difficile", "difficile"),
        Bouton((LARGEUR // 2 - 140, 450, 280, 45), "Retour", "retour_menu", couleur=(127, 140, 141), couleur_survol=(149, 165, 166))
    ]

    # Boutons de l'écran de fin
    boutons_fin = [
        Bouton((LARGEUR // 2 - 180, HAUTEUR // 2 + 40, 170, 45), "Rejouer", "rejouer"),
        Bouton((LARGEUR // 2 + 10, HAUTEUR // 2 + 40, 170, 45), "Menu", "retour_menu"),
        Bouton((LARGEUR // 2 - 100, HAUTEUR // 2 + 100, 200, 40), "Quitter", "quitter", couleur=(192, 57, 43), couleur_survol=(231, 76, 60))
    ]

    def demarrer_partie():
        nonlocal plateau, joueur_actuel, temps_debut, temps_total, nb_coups, etat
        plateau = Board()
        joueur_actuel = JOUEUR_1
        temps_debut = time.time()
        temps_total = 0.0
        nb_coups = 0
        etat = "JEU"

    while True:
        horloge.tick(60)
        souris_pos = pygame.mouse.get_pos()
        x_souris = souris_pos[0]

        # 1. Gestion des événements utilisateur
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if etat == "MENU":
                    for b in boutons_menu:
                        if b.est_clique(event.pos):
                            if b.action == "start":
                                etat = "CHOIX_DIFF"
                            elif b.action == "quitter":
                                pygame.quit()
                                sys.exit()

                elif etat == "CHOIX_DIFF":
                    for b in boutons_diff:
                        if b.est_clique(event.pos):
                            if b.action in ["facile", "moyen", "difficile"]:
                                difficulte = b.action
                                demarrer_partie()
                            elif b.action == "retour_menu":
                                etat = "MENU"

                elif etat == "JEU":
                    if joueur_actuel == JOUEUR_1:
                        colonne = event.pos[0] // TAILLE_CASE
                        if plateau.est_colonne_valide(colonne):
                            plateau.jouer_coup(colonne, JOUEUR_1)
                            nb_coups += 1

                            if plateau.verifier_victoire(JOUEUR_1):
                                temps_total = time.time() - temps_debut
                                gagnant_texte = "Victoire !"
                                etat = "FIN"
                            elif plateau.est_plein():
                                temps_total = time.time() - temps_debut
                                gagnant_texte = "Match Nul !"
                                etat = "FIN"
                            else:
                                joueur_actuel = JOUEUR_2

                elif etat == "FIN":
                    for b in boutons_fin:
                        if b.est_clique(event.pos):
                            if b.action == "rejouer":
                                demarrer_partie()
                            elif b.action == "retour_menu":
                                etat = "MENU"
                            elif b.action == "quitter":
                                pygame.quit()
                                sys.exit()

        # 2. Prise de décision de l'IA
        if etat == "JEU" and joueur_actuel == JOUEUR_2:
            gui.dessiner_plateau(plateau, time.time() - temps_debut, nb_coups)
            pygame.display.update()
            pygame.time.wait(250)

            col_ia = choisir_coup_ia(plateau, difficulte=difficulte, piece_ia=JOUEUR_2)
            plateau.jouer_coup(col_ia, JOUEUR_2)
            nb_coups += 1

            if plateau.verifier_victoire(JOUEUR_2):
                temps_total = time.time() - temps_debut
                gagnant_texte = "L'IA a gagné..."
                etat = "FIN"
            elif plateau.est_plein():
                temps_total = time.time() - temps_debut
                gagnant_texte = "Match Nul !"
                etat = "FIN"
            else:
                joueur_actuel = JOUEUR_1

        # 3. Affichage selon l'état
        if etat == "MENU":
            gui.dessiner_menu(boutons_menu, souris_pos)

        elif etat == "CHOIX_DIFF":
            gui.dessiner_choix_difficulte(boutons_diff, souris_pos)

        elif etat == "JEU":
            temps_ecoule = time.time() - temps_debut
            gui.dessiner_plateau(plateau, temps_ecoule, nb_coups)
            if joueur_actuel == JOUEUR_1:
                gui.dessiner_survol(x_souris, JOUEUR_1)
            pygame.display.update()

        elif etat == "FIN":
            gui.dessiner_plateau(plateau, temps_total, nb_coups)
            gui.dessiner_ecran_fin(gagnant_texte, temps_total, nb_coups, boutons_fin, souris_pos)


if __name__ == "__main__":
    main()