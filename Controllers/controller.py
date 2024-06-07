import os
import json
import sys

sys.path.append(os.path.join(os.path.dirname(__file__)))



from Models.tournoi import Player
from Models.tournoi import Tournoi



class Controller :
    def __init__(self, view):
        self.view = view

    def load_data(self):
        if os.path.exists('data/data.json'):
            with open('data/data.json', 'r') as file:
                return json.load(file)
        return {"tournois": [], "joueurs": []}

    def save_data(self, data):
        with open('data/data.json', 'w') as file:
            json.dump(data, file, indent=4)

############################################ PLAYER ############################################
    def create_player(self):
        lastname, firstname, birthdate = self.vue.ask_player_information()
        new_player = Player(lastname, firstname, birthdate)
        
        data = self.load_data()
        data.setdefault("joueurs", []).append(new_player.to_dict())
        self.save_data(data)
        print("Joueur ajouté avec succès!")

    def show_all_players(self):
        data = self.load_data()
        self.view.show_all_players(data["joueurs"])


############################################ TOURNOI ############################################

    def create_tournoi(self):
        name, location, beginning_date, end_date, description, number_of_rounds = self.view.ask_tournoi_information()
        number_of_players = self.view.ask_number_of_players()

        data = self.load_data()
        available_players = data["joueurs"]

        if len(available_players) < number_of_players:
            print("Nombre insuffisant de joueurs disponibles pour ce tournoi.")
            return

        selected_players_dicts = self.view.select_players(available_players, number_of_players)
        selected_players = [Player.from_dict(player) for player in selected_players_dicts]
        new_tournoi = Tournoi(name, location, beginning_date, end_date, description, number_of_rounds)
        new_tournoi.joueurs = selected_players
        data.setdefault("tournois", []).append(new_tournoi.to_dict())
        self.save_data(data)
        print("Tournoi ajouté avec succès!")

    def show_all_tournaments(self):
        data = self.load_data()
        self.view.show_all_tournaments(data["tournois"])