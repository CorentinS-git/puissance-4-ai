# Puissance 4 — Moteur de Jeu & IA Minimax

Projet d'implémentation complète du jeu Puissance 4 en Python avec interface graphique Pygame et moteur d'intelligence artificielle basé sur l'algorithme Minimax et l'élagage Alpha-Bêta.

## Fonctionnalités

- **Interface graphique 2D (Pygame) :** Menu interactif, écran de sélection de niveau, suivi du curseur et écran récapitulatif de fin de partie avec statistiques (durée, nombre de coups).
- **Moteur formel :** Gestion complète des règles (gravité, détection des alignements dans les 4 axes, gestion des colonnes pleines et matchs nuls).
- **Trois niveaux de difficulté :**
  - **Facile :** Coups aléatoires avec taux d'étourderie calibré.
  - **Moyen :** Minimax à profondeur réduite (profondeur 3).
  - **Difficile :** Minimax avec élagage Alpha-Bêta à profondeur 5, ordonnancement central des coups et heuristique de fenêtres d'alignement.

## Structure du projet

puissance4/
├── assets/             # Ressources visuelles (logo)
├── core/               # Logique pure et état du plateau (board.py)
├── ai/                 # Heuristiques et algorithme Minimax (minimax.py, evaluation.py)
├── ui/                 # Rendu visuel et composants graphiques (gui.py)
├── game_gui.py         # Point d'entrée de l'application graphique
├── main.py             # Point d'entrée de la version console (PvP / PvIA)
└── .gitignore          # Fichiers temporaires exclus de Git

## Installation & Lancement

1. Cloner le dépôt :
   git clone https://github.com/CorentinS-git/puissance-4-ai.git
   cd puissance-4-ai

2. Installer les dépendances :
   pip install pygame-ce

3. Lancer le jeu :
   python game_gui.py