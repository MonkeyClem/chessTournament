import os
import json
import sys

sys.path.append(os.path.join(os.path.dirname(__file__)))



from Models.tournoi import Player



class Controller :
    def __init__(self, vue):
        self.vue = vue

    def load_data(self):
        if os.path.exists('data/data.json'):
            with open('data/data.json', 'r') as file:
                return json.load(file)
        return {"tournois": [], "joueurs": []}

    def save_data(self, data):
        with open('data/data.json', 'w') as file:
            json.dump(data, file, indent=4)

    def create_player(self):
        lastname, firstname, birthdate = self.vue.ask_player_information()
        new_player = Player(lastname, firstname, birthdate)
        
        data = self.load_data()
        data["joueurs"].append(new_player.to_dict())
        self.save_data(data)
        print("Joueur ajouté avec succès!")