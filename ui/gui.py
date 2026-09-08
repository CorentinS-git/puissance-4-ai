"""
ui/gui.py : Rendu graphique des différents états du jeu (Menu, Choix, Jeu, Fin).
"""
import os
import pygame
from core.board import LIGNES, COLONNES, VIDE, JOUEUR_1, JOUEUR_2

# Dimensions
TAILLE_CASE = 100
LARGEUR = COLONNES * TAILLE_CASE
HAUTEUR = (LIGNES + 1) * TAILLE_CASE
RAYON = int(TAILLE_CASE / 2 - 8)

# Couleurs
BLANC = (255, 255, 255)
FOND_ECRAN = (245, 247, 250)
COULEUR_FOND = FOND_ECRAN  # Alias de sécurité
BLEU_PLATEAU = (25, 95, 180)
BLEU_BOUTON = (41, 128, 185)
BLEU_SURVOL = (52, 152, 219)
GRIS_VIDE = (230, 235, 240)
ROUGE_PION = (231, 76, 60)
JAUNE_PION = (241, 196, 15)
TEXTE_FONCE = (44, 62, 80)
FOND_POPUP = (255, 255, 255)


class Bouton:
    def __init__(self, rect, texte, action, couleur=BLEU_BOUTON, couleur_survol=BLEU_SURVOL):
        self.rect = pygame.Rect(rect)
        self.texte = texte
        self.action = action
        self.couleur = couleur
        self.couleur_survol = couleur_survol

    def dessiner(self, surface, police, x_souris, y_souris):
        survol = self.rect.collidepoint(x_souris, y_souris)
        c = self.couleur_survol if survol else self.couleur
        
        # Rectangle avec coins arrondis
        pygame.draw.rect(surface, c, self.rect, border_radius=12)
        
        texte_surf = police.render(self.texte, True, BLANC)
        rect_texte = texte_surf.get_rect(center=self.rect.center)
        surface.blit(texte_surf, rect_texte)

    def est_clique(self, pos):
        return self.rect.collidepoint(pos)



class Puissance4GUI:
    def __init__(self):
        pygame.init()
        self.ecran = pygame.display.set_mode((LARGEUR, HAUTEUR))
        pygame.display.set_caption("Puissance 4 - IA")
        self.police_titre = pygame.font.SysFont("segoe ui", 52, bold=True)
        self.police_texte = pygame.font.SysFont("segoe ui", 24, bold=True)
        self.police_stats = pygame.font.SysFont("segoe ui", 20)

        # Chargement en conservant le ratio carré (190x190)
        dossier_racine = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        chemin_logo = os.path.join(dossier_racine, "assets", "logo.jpg") # ou logo.png selon ton fichier

        if os.path.exists(chemin_logo):
            image_brute = pygame.image.load(chemin_logo).convert_alpha()
            self.logo = pygame.transform.smoothscale(image_brute, (190, 190))
        else:
            self.logo = None

    def dessiner_menu(self, boutons, souris_pos):
        self.ecran.fill(FOND_ECRAN)

        if self.logo is not None:
            # Centré en haut avec son ratio carré intact
            rect_logo = self.logo.get_rect(center=(LARGEUR // 2, 135))
            self.ecran.blit(self.logo, rect_logo)
        else:
            titre = self.police_titre.render("PUISSANCE 4", True, BLEU_PLATEAU)
            self.ecran.blit(titre, titre.get_rect(center=(LARGEUR // 2, 135)))

        sous_titre = self.police_stats.render("Sabatier Corentin", True, TEXTE_FONCE)
        self.ecran.blit(sous_titre, sous_titre.get_rect(center=(LARGEUR // 2, 255)))

        for b in boutons:
            b.dessiner(self.ecran, self.police_texte, souris_pos[0], souris_pos[1])
        pygame.display.update()

    def dessiner_choix_difficulte(self, boutons, souris_pos):
        self.ecran.fill(FOND_ECRAN)

        titre = self.police_titre.render("DIFFICULTÉ", True, BLEU_PLATEAU)
        self.ecran.blit(titre, titre.get_rect(center=(LARGEUR // 2, 140)))

        for b in boutons:
            b.dessiner(self.ecran, self.police_texte, souris_pos[0], souris_pos[1])
        pygame.display.update()

    def dessiner_plateau(self, board, temps_sec, nb_coups):
        pygame.draw.rect(self.ecran, BLANC, (0, 0, LARGEUR, TAILLE_CASE))
        
        info_temps = f"Temps : {int(temps_sec)}s"
        info_coups = f"Coups : {nb_coups}"
        txt_t = self.police_stats.render(info_temps, True, TEXTE_FONCE)
        txt_c = self.police_stats.render(info_coups, True, TEXTE_FONCE)
        self.ecran.blit(txt_t, (20, 15))
        self.ecran.blit(txt_c, (LARGEUR - 130, 15))

        for c in range(COLONNES):
            for r in range(LIGNES):
                x = c * TAILLE_CASE
                y = (r + 1) * TAILLE_CASE
                pygame.draw.rect(self.ecran, BLEU_PLATEAU, (x, y, TAILLE_CASE, TAILLE_CASE))

                centre_x = x + TAILLE_CASE // 2
                centre_y = y + TAILLE_CASE // 2

                val = board.grille[r][c]
                couleur = GRIS_VIDE if val == VIDE else (ROUGE_PION if val == JOUEUR_1 else JAUNE_PION)
                pygame.draw.circle(self.ecran, couleur, (centre_x, centre_y), RAYON)

    def dessiner_survol(self, x_souris, piece):
        couleur = ROUGE_PION if piece == JOUEUR_1 else JAUNE_PION
        pygame.draw.circle(self.ecran, couleur, (x_souris, TAILLE_CASE // 2 + 15), RAYON - 10)

    def dessiner_ecran_fin(self, gagnant_texte, temps_total, nb_coups, boutons, souris_pos):
        overlay = pygame.Surface((LARGEUR, HAUTEUR), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 140))
        self.ecran.blit(overlay, (0, 0))

        popup_rect = pygame.Rect(LARGEUR // 2 - 250, HAUTEUR // 2 - 200, 500, 400)
        pygame.draw.rect(self.ecran, FOND_POPUP, popup_rect, border_radius=16)

        surf_titre = self.police_titre.render(gagnant_texte, True, TEXTE_FONCE)
        self.ecran.blit(surf_titre, surf_titre.get_rect(center=(LARGEUR // 2, HAUTEUR // 2 - 130)))

        txt_stats1 = self.police_texte.render(f"Coups joués : {nb_coups}", True, TEXTE_FONCE)
        txt_stats2 = self.police_texte.render(f"Durée : {temps_total:.1f} secondes", True, TEXTE_FONCE)
        self.ecran.blit(txt_stats1, txt_stats1.get_rect(center=(LARGEUR // 2, HAUTEUR // 2 - 60)))
        self.ecran.blit(txt_stats2, txt_stats2.get_rect(center=(LARGEUR // 2, HAUTEUR // 2 - 20)))

        for b in boutons:
            b.dessiner(self.ecran, self.police_texte, souris_pos[0], souris_pos[1])
        pygame.display.update()