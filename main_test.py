import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__)))

sys.path.append('../Models')
sys.path.append('../Controllers')
sys.path.append('../Views')


from Models.tournoi import Tournoi, Player
from Views.views import View
from Controllers.controller import Controller


def main():
    # Initialiser les composants
    view = View()
    controller = Controller(view)

    while True : 
        choix = view.show_menu()
        if choix == '1':
            # ICI ON VA CREER UN TOURNOI
            pass
        elif choix == '2':
            # ICI ON VA AFFICHER TOUS LES TOURNOIS, ET PERMETTRE A L'UTILISATEUR D'EN SELECTIONNER UN POUR AFFICHER LES DETAILS
            pass
        elif choix == '3':
            # DONE VA AFFICHER TOUS LES JOUEURS
            controller.show_all_players()
            pass
        elif choix == '4':
            # DONE :  CREER UN JOUEUR
            controller.create_player()
            pass
        elif choix == '5':
            break


main()
     