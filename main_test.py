import sys
import os
from venv import logger

sys.path.append(os.path.join(os.path.dirname(__file__)))

sys.path.append('../Models')
sys.path.append('../Controllers')
sys.path.append('../Views')


# from Models.tournament import Tournament, Player
from Views.views import Views
from Controllers.controller import Controller

def print_welcome_message() :
    chess_message = """
  ____ _                        --------- 
/ ___| |__   ___  ___ ___      | _______ |----   _  _ ___________
| |   | '_ \\ / _ \\/ __/ __|     | |  /  / \ \| || ||  |  __ |
| |   | '_ \\ / _ \\/ __/ __|      | |  /  / \ \| || ||  |  __ |
| |___| | | |  __/\\__ \\__ \\     | |  |  |_| |  || ||  |-|   |  |
 \\____|_| |_|\\___||___/___/      |_|   \____/ |____||__| |   |__|
                           
    """
    print(chess_message)

def main():
    # Initialiser les composants
    view = Views()
    controller = Controller(view)

    while True : 
        print_welcome_message()
        user_choice = view.show_main_menu()
        if user_choice == '1':
            # DONE :  CREER UN TOURNOI
            controller.create_tournament()
            pass
        elif user_choice == '2': 
            controller.show_tournaments()
        elif user_choice == '3':
            controller.show_all_players()
            pass
        elif user_choice == '4':
            controller.create_new_player()
            pass
        elif user_choice == '5':
            break
        
        break


main()
     