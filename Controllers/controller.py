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
        first_round = Round("Round 1", matches)
        print(first_round.to_dict()) 
        return first_round
        

  
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
    
    def show_tournaments(self):
        try: 
            with open('data/tournaments.json', "r") as file : 
                tournaments = json.load(file)
        except FileNotFoundError:
            print("No tournament found")
            return None
        
        for i, tournament in enumerate(tournaments["tournaments"], 1) : 
            print(f"\n=== Tournoi numéro : {i} ===")
            print(f"Nom : {tournament['name']}")
            print(f"Lieu : {tournament['location']}")
            print(f"Date de début : {tournament['debut_date']}")
            print(f"Date de fin : {tournament['end_date']}")
            print(f"Nombre de rounds : {tournament['nb_rounds']}")
            print(f"Nombre de joueurs : {tournament['nb_players']}")
            print(f"Round actuel : {tournament['current_round']}")
            print(f"Description : {tournament['description']}")
            print(f"Matches précédents : {len(tournament['previous_matches'])}")

            print("\n=== Joueurs ===")
            for player_list in tournament["players"]:
                for player in player_list:
                    print(f"{player['firstname']} {player['lastname']} ({player['birthdate']})")

            print("\n=== Rounds ===")
            for round_ in tournament["rounds"]:
                print(f"\nNom du Round : {round_['name']}")
                print(f"Début : {round_['start_time']}")
                print(f"Fin : {round_['end_time'] if round_['end_time'] else 'En cours'}")
                print("\nMatches :")
                for match in round_["matches"]:
                    player1, player2 = match
                    print(f"{player1['firstname']} {player1['lastname']} VS {player2['firstname']} {player2['lastname']}")
        selected_tournament = self.select_tournament(tournaments) 
        print("Tournament selected : ", selected_tournament["name"])
        selected_tournament = Tournament.from_dict(selected_tournament)
        print("Tournament selected : ", selected_tournament)
        user_choice = self.tournament_options(selected_tournament)


    def select_tournament(self, tournaments):
        while True : 
            selected_index = input("Sélectionnez un tournoi via son numéro : ")
            try:
                selected_tournament = tournaments["tournaments"][int(selected_index) - 1]
                return selected_tournament
            except (IndexError, ValueError):
                print("\n \nVeuillez saisir un numéro de tournoi valide \n \n")

    def tournament_options(self, selected_tournament):
        print("1. Lancer le tournoi")
        print("2. Afficher les rounds")
        print("3. Afficher les joueurs")
        print("4. Retour")
        user_choice = input("Sélectionnez une option : ")
        return user_choice
                
            

        




        

    