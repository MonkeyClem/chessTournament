import json
import random
import sys
from Models.tour import Round
from Models.tournament import Tournament
class Controller : 
    
    def __init__(self, view) -> None:
        pass



    # def load_players(self, filename = "data/players.json"):
    #     try : 
    #         with open(filename, "r") as file:
    #             players = json.load(file)
    #     except FileNotFoundError : 
    #         players = {'players' : []}
    #     return players
    def load_players(self, filename="data/players.json"):
        try:
            with open(filename, "r") as file:
                players = json.load(file)
        except FileNotFoundError:
            players = {'players': []}
        print("Players : ", players["players"])
        return players['players']
    



    def save_tournament(self, tournament, filename = "data/tournaments.json"):
        tournament_data = tournament.to_dict()
        try :
            with open(filename, 'r') as file : 
                data = json.load(file)
        except FileNotFoundError:
            data = {"tournaments" : []}

        data["tournaments"].append(tournament_data)

        with open(filename, 'w') as file :
            json.dump(data, file, indent=4)
        
        print("Tournament succesfully saved ! You can now launch the tournament")


    def select_players(self, nb_players):
        players = self.load_players()
        if not players:
            print("Aucun joueur n'est présent dans la base de données")
            return None
        print("Liste des joueurs disponibles : ")
        for index, player in enumerate(players, 1):
            print(f"{index}. {player['lastname']} {player['firstname']} - {player['birthdate']}")
        
        selected_players = []

        while len(selected_players) < nb_players:
            try:
                chosen_player = int(input("Sélectionnez un joueur (par numéro) : "))
                if chosen_player < 1 or chosen_player > len(players):
                    print("Veuillez saisir un joueur valide")
                    continue
                elif players[chosen_player - 1] in selected_players:
                    print("Ce joueur a déjà été sélectionné")
                    continue
                else:
                    selected_players.append(players[chosen_player - 1])
            except ValueError:
                print("Veuillez saisir l'index du joueur")
        return selected_players
    
  
        

    def create_first_round_matches(self, selected_players):
        print("Création des matchs du premier round")
        matches = []
        random.shuffle(selected_players)
        for i in range(0, len(selected_players), 2): 
            match = ([selected_players[i], selected_players[i+1]])
            matches.append(match)
        print("Matchs du premier round : ", matches)
        round_ = Round("Round 1", matches)
        print(round_.to_dict()) 
        return round_
        

  
    def create_tournament(self):
        print("Création d'un tournament, veuillez renseigner les informations suivantes : ")
        name = input("Nom du tournament : ")
        location = input("Lieu du tournament : ")
        debut_date = input("Date de début du tournament : ")
        end_date = input("Date de fin du tournament : ")
        nb_rounds = int(input("Nombre de rounds : "))
        nb_players = int(input("Nombre de joueurs : "))
        select_players= self.select_players(nb_players)
        current_round = 1
        description = input("OPTIONAL) Write a description for the tournament : ")
        first_round = self.create_first_round_matches(select_players)
        first_round = first_round.to_dict()
        rounds=[first_round]
        players = [select_players]
        previous_matches = []   
        tournament = Tournament(name, location, debut_date, end_date, nb_rounds, nb_players, current_round, players, description, rounds, previous_matches)
        self.save_tournament(tournament)
        return tournament
    
