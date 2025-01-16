import sys
import os
import json

sys.path.append(os.path.join(os.path.dirname(__file__)))

sys.path.append('../Models')
sys.path.append('../Controllers')
sys.path.append('../Views')

from Models.match import Match

class Views :     
    def __init__(self) -> None:
        pass

    def main_menu_selector(self) -> str : 
        user_choice = input("Sélectionnez une option : ")
        return user_choice
    
    def show_main_menu(self) : 
        print("1. Créer un tournament")
        print("2. Afficher tous les tournaments")
        print("3. Afficher tous les joueurs")
        print("4. Créer un joueur")
        print("5. Quitter")
        user_choice = self.main_menu_selector()
        return user_choice
    
    def show_all_players(self, players ) -> str :
        i = 1 
        print("Voici la liste des joueurs : ")
        for player in players :
            print("Joueur", i," : ", player["lastname"], player["firstname"])
            i = i + 1
        

    def show_tournaments(self, tournaments) : 
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
                    match = Match(player1, player2)
         


    def create_tournament_input(self) :
        name = input("Nom du tournament : ")
        location = input("Lieu du tournament : ")
        debut_date = input("Date de début du tournament : ")
        end_date = input("Date de fin du tournament : ")
        nb_rounds = int(input("Nombre de rounds : "))
        nb_players = int(input("Nombre de joueurs : "))
        description = input("OPTIONAL) Write a description for the tournament : ")
        return name, location, debut_date, end_date, nb_rounds, nb_players, description
