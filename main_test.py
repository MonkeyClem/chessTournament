import sys
import os
from venv import logger

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
            # DONE :  CREER UN TOURNOI
            controller.create_tournoi()
            pass
        elif choix == '2':
            # ICI ON VA AFFICHER TOUS LES TOURNOIS, ET PERMETTRE A L'UTILISATEUR
            # D'EN SELECTIONNER UN POUR AFFICHER LES DETAILS
            select_tournament = controller.show_all_tournaments()
            logger.debug(f"select_tournament: {select_tournament}")
            if select_tournament:
                controller.ask_for_tournament_start(select_tournament)
            pass 

        elif choix == '3':
            # DONE : AFFICHER TOUS LES JOUEURS
            controller.show_all_players()
            pass
        elif choix == '4':
            # DONE :  CREER UN JOUEUR
            controller.create_player()
            pass
        elif choix == '5':
            break
        
        break


main()
     