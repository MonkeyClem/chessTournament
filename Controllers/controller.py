from datetime import datetime
import os
import json
import random
import sys
from venv import logger

from Models.tour import Tour

sys.path.append(os.path.join(os.path.dirname(__file__)))

from Models.match import Match
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
    
    def generate_first_round(self, players):
        random.shuffle(players)
        matches = []
        print("players: ", len(players))
        num_players = len(players)
        if num_players % 2 != 0:
            print("Le nombre de joueurs est impair. Un joueur sera exempté ce tour.")
            players.append(None)  # Ajouter un emplacement vide pour un joueur exempté
        for i in range(0, len(players), 2):
            if players[i] is not None and players[i + 1] is not None:
                matches.append(Match(players[i], 0, players[i + 1], 0))
            elif players[i] is not None:
                print(f"{players[i].firstname} {players[i].lastname} est exempté ce tour.")
        return matches


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
        first_round_name = input("Entrez le nom du premier tour: ")
        generated_matches = self.generate_first_round(selected_players)
        first_round = Tour(first_round_name, datetime.now(), None, [match.to_dict() for match in generated_matches])
        new_tournoi = Tournoi(name, location, beginning_date, end_date, first_round, description, number_of_rounds)
        new_tournoi.tours.append(first_round)
        new_tournoi.joueurs = selected_players
        # new_tournoi.tours = [first_round.to_dict()]
        data.setdefault("tournois", []).append(new_tournoi.to_dict())
        print("new_tournoi: ", new_tournoi.to_dict())
        # sys.exit("DONE")
        self.save_data(data)
        print("Tournoi ajouté avec succès!")


    def show_all_tournaments(self):
        data = self.load_data()
        self.view.show_all_tournaments(data["tournois"])
        selected_tournoi = self.select_tournoi()
        return selected_tournoi
    
    def select_tournoi(self):
        data = self.load_data()
        # self.view.show_all_tournaments(data["tournois"])
        tournoi = int(input("Choisissez un tournoi: "))
        return data["tournois"][tournoi - 1]
    
    def ask_for_tournament_start(self, tournoi):
        start = input("Voulez-vous commencer le tournoi ? (O/N): ")
        print("tournoi au sein du ask for tournament start : ", tournoi)

        if start.lower() == "o":
            self.start_tournoi(tournoi)
        else:
            print('Très bien, ce sera pour une prochaine fois.')
            pass

    def start_tournoi(self, tournoi):
        # tournoi = Tournoi.from_dict(tournoi)
        # tournoi.tours = Tour.to_dict(tournoi.tours)
        # print("tournoi.tour au sein du start_tournoi : ", tournoi.tours)
        print('tournoi au sein du start_tournoi : ', tournoi)
        
        if tournoi['tour_actuel'] == 0:
            # tournoi.tours.append(self.generate_first_round(tournoi.joueurs))
            tournoi['tour_actuel'] += 1
            tournoi = Tournoi.from_dict(tournoi)
            tournoi_dict = Tournoi.to_dict(tournoi)
            print("tour de l'objet tournoi dans le start avant le save : ",tournoi.tours)
            print("round of the tournament_dict before saving the tournament into start_tournoi : ",tournoi_dict["tours"])
            self.save_tournament(tournoi_dict)
            print("Tournoi démarré avec succès ! Tour actuel : ", tournoi.tour_actuel)
            # print(f"Les matchs du premier tour sont : {tournoi_dict['tour_actuel']} ")
            # sys.exit("DONE")

            #TODO : lancer le tournoi, resume_tournament sera probablement suffisant    
        else:
            self.view.already_started_tournament(tournoi) 
            resume_tournament = self.view.ask_resume_tournament() 
            if resume_tournament.lower() == "o":
                self.resume_tournament(tournoi)

    
    # def resume_tournament(self, tournoi):
    #     tournoi = Tournoi.from_dict(tournoi)
    #     print("Tournoi au sein du resume_tournament : ", tournoi)
    #     print("tournoi.tours : ", tournoi.tours)    
    #     for match in tournoi.tours[0].matchs:
    #         print("match: ", match)
    #         winner_name = self.view.ask_for_match_result(match)
    #         for player in match.players:
    #             print("match.players ===> ", match.players)
    #             print("player ===> ", player)
    #             print(Player.to_dict(match.players[0]))
    #             if player[0].lastname == winner_name:
    #                 print("winner_name ===>",winner_name)
    #                 player[1] += 1
    #                 # dict_player = Player.to_dict(player)
    #                 # print(dict_player)
    #     tournoi.tour_actuel += 1


    def resume_tournament(self, tournoi):
        print("Tournoi au sein du resume_tournament : ", tournoi)
        tournoi = Tournoi.from_dict(tournoi)
        print("WARNING : Le tour à commencer. Veuillez entrer les résultats des matchs. ")
        for match in tournoi.tours[0].matchs:
            print("match: ", match)
            winner_name = self.view.ask_for_match_result(match)
            for player_tuple in match.players:
                player, score = player_tuple
                print("player ===> ", player)
                print(Player.to_dict(player))
                if player.lastname == winner_name:
                    player_tuple[1] += 1  # Update score directly in the tuple
                    print("player_tuple ===> ", player_tuple)
                    dict_player = Player.to_dict(player)
                    print(dict_player)
                    tournoi.previous_matchs.append(Match.to_dict(match))
                    dict_tournoi = Tournoi.to_dict(tournoi)
                    print("dict_tournoi avant la sauvegarde au sein du resume_tournament : ", dict_tournoi)   
                    self.save_tournament(dict_tournoi)
                
        tournoi.tour_actuel += 1
        dict_tournoi = Tournoi.to_dict(tournoi)
        self.save_tournament(dict_tournoi)


    def save_tournament(self, tournoi): 
        data = self.load_data()
        # print(f"tournoi: {tournoi}")
        # tournoi = Tournoi.to_dict(tournoi)
        # print(f"tournoi apres to dict : {tournoi}" )
        print('type de tournoi dans le save_tournament : ', type(tournoi))
        if isinstance(tournoi, dict):
            for i, t in enumerate(data['tournois']) : 
                if t['name'] == tournoi['name'] : 
                    data['tournois'][i] = tournoi
                    self.save_data(data)
                    break
        else : 
            tournoi_dict = Tournoi.to_dict(tournoi)
            print("tournoi_dict dans save_tournament ==> ", tournoi_dict)
            # print("tournoi.tours : ", tournoi['tours'])
            for i, t in enumerate(data['tournois']) : 
                if t['name'] == tournoi_dict['name'] : 
                    data['tournois'][i] = tournoi_dict
                    self.save_data(data)

                    break





