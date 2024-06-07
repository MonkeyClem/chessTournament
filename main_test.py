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
            # ICI ON VA AFFICHER TOUS LES TOURNOIS
            pass
        elif choix == '3':
            # ICI ON VA AFFICHER TOUS LES JOUEURS
            pass
        elif choix == '4':
            # DONE :  VA CREER UN JOUEUR
            controller.create_player()
            pass
        elif choix == '5':
            break


main()
     