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
    
    def empty_players_database(self) :
        print("Aucun joueur n'est présent dans la base de données, veuillez en ajouter.")
 
   
    
###### PLAYER RELATED ######
    def show_all_players(self, players ) -> str :
        i = 1 
        print("\n")
        str = " Liste des joueurs "
        self.justify_text(str.upper())
        print('\n')
        for i, player in enumerate(players) :
            print("Joueur", i + 1," : ", player["lastname"].upper(), player["firstname"])
            i = i + 1
        print("\n")


    def get_new_player_info(self) -> str  : 
        print("\nCRÉATION D'UN NOUVEAU JOUEUR : ")
        lastname =  input("\nVeuillez renseigner le nom du nouveau joueur : \n")
        firstname = input("Veuillez renseigner le prénom du nouveau joueur : \n")
        birthdate = int(input("Renseignez l'année de naissance du joueur : \n "))
        return lastname, firstname, birthdate
    
    def player_successfully_saved(self) : 
        success = print("\nPlayer succesfully saved !\n")
        return success
    
    def select_a_player(self) : 
        return int(input('Sélectionnez un joueur (par son numéro) : '))
    
    def error_adding_player(self) : 
        print("Veuillez saisir un index valide")

    def already_selected_player(self) : 
        print("Ce joueur a déjà été sélectionné")



###### TOURNAMENT RELATED ######


    def justify_text(self, str_to_justify): 
        print(str_to_justify.center(40, "*"))

    def no_tournament_found(self): 
        text= "No tournament found"
        self.justify_text(text)

    def select_tournament_error(self): 
        return print("\n \nVeuillez saisir un numéro de tournoi valide \n \n")
    



    def create_tournament(self) : 
        print("\n")
        text = " Création d'un tournoi "  
        self.justify_text(text)
        print("\n")
        pass

    def show_tournament_options(self) :
        print("1. Lancer / reprendre le tournoi")
        print("2. Afficher les rounds")
        print("3. Afficher les joueurs")
        print("4. Retour")
        user_choice = input("Sélectionnez une option : ")
        return user_choice
    

    def tournament_options_selector(self, user_choice, selected_tournament) -> str :
        if user_choice == '2':
            print("Affichage des rounds : \n")
            number_of_rounds = selected_tournament["nb_rounds"]
            for _, round in enumerate(selected_tournament["rounds"]) : 
                
                round = round.to_dict()
                print(f"=== Round {_ + 1} ==== \nNom : " + round["name"])
                print("Matches : ")
                for i, match in enumerate(round["matches"]) :
                    player1_info, score1 = match[0]  # Joueur 1 et son score
                    player2_info, score2 = match[1]  # Joueur 2 et son score

                    player1_name = f"{player1_info['firstname']} {player1_info['lastname']}"
                    player2_name = f"{player2_info['firstname']} {player2_info['lastname']}"

                    print(f"🎯 Match {i+1} : {player1_name.ljust(20)} [{score1}]  ⚔️  {player2_name.ljust(20)} [{score2}]")
                if round["end_time"] :
                    print(f"Round terminé à {round['end_time']}")
                else:
                    print("Round en cours")
                print('\n')        
        elif user_choice == '3':
            #TO DO : Afficher les joueurs
            print("Affichage des joueurs")
            for player in selected_tournament["players"] : 
                print(player)
        elif user_choice == '4':
            print("Retour")
        else:
            print("Veuillez saisir une option valide")

    
    def show_selected_tournament(self, tournament) :
        return print("Tournoi Selectionné : ", tournament["name"])
        
        

    def resume_or_start_message(self, current_round) -> str: 
        print("\nLe tournoi démarre ! Que le meilleur gagne \n") if current_round == 1 else print("\nLe tournoi va reprendre ! Nous sommes actuellement au round", current_round)
    
        
    def finished_tournament(self) : 
        print("\nCe tournoi est terminé ! Vous pouvez consulter les résultats, mais il n'est plus possible de jouer de matchs.\n")


    def show_tournaments(self, tournaments) : 
          for i, tournament in enumerate(tournaments["tournaments"], 0) : 
            print(f"\n=== Tournoi  : {i+1} ===")
            print(f"Nom : {tournament['name']}")
            print(f"Lieu : {tournament['location']}")
            print(f"Date de début : {tournament['debut_date']}")
            print(f"Date de fin : {tournament['end_date']}")
            print(f"Nombre de rounds : {tournament['nb_rounds']}")
            print(f"Nombre de joueurs : {tournament['nb_players']}")
            print(f"Round actuel : {tournament['current_round']}")
            print(f"Description : {tournament['description']}")
            print(f"Matches déjà joués : {len(tournament['previous_matches'])} \n")
 

    def create_tournament_input(self) :
        name = input("Nom du tournament : ")
        location = input("\nLieu du tournament : ")
        debut_date = input("\nDate de début du tournament : ")
        end_date = input("\nDate de fin du tournament : ")
        nb_rounds = int(input("\nNombre de rounds : "))
        nb_players = int(input("\nNombre de joueurs : "))
        description = input("\nOPTIONAL) Write a description for the tournament : ")
        return name, location, debut_date, end_date, nb_rounds, nb_players, description
    
    def empty_tournament_list(self) :
        error = print("\n\nError : The file seems to be empty or corrupted \n\nPlease check that the key 'tournaments' is present in the JSON file\n")
        return error
    
    def select_tournament_input(self) -> str : 
        selected_index = int(input("Sélectionnez un tournoi via son numéro : "))
        return selected_index
    

    def tournament_successfully_saved(self) : 
        success = print("Le tournoi a été enregistré avec succès ! Vous pouvez désormais le sélectionner au sein de menu\n")
        return success
    

    def show_current_score(self, sorted_players) : 
        print("Les scores actuels sont : \n ")
        for player in sorted_players :
            print(f"\n{player['firstname']} {player['lastname']} : {player['score']} points")

       
    
###### MATCH RELATED ######
    def find_matching_player(player_score, player_info):
        """Trouve un joueur dans player_score en fonction de son firstname et lastname."""
        player_data = player_info[0]  # Extraire le dictionnaire contenant firstname et lastname

        for player in player_score:
            if player["firstname"] == player_data["firstname"] and player["lastname"] == player_data["lastname"]:
                return player  # Retourne le joueur correspondant
        return None  # Si aucun joueur n'est trouvé


    def show_match(self, match, players_score) :   
        player1_info = match[0] 
        player2_info = match[1]
        matched_player1 = Views.find_matching_player(players_score, player1_info)
        matched_player2 = Views.find_matching_player(players_score, player2_info)
        print("\n🎲 Match en cours :")
        print(f"   🟢 {player1_info[0]['lastname']} {player1_info[0]['firstname']} ({matched_player1['score']})")
        print("       ⚔️   VS   ⚔️")
        print(f"   🔴 {player2_info[0]['lastname']} {player2_info[0]['firstname']} ({matched_player2['score']} points)")
        print("\n")

    def ask_winner_index(self) : 
        winner_index = int(input("Entrez l'index du joueur vainqueur (1 ou 2) : "))
        return winner_index
    
    def first_round_matches_creation(self) :
        return print("\nCréation des matchs du premier round en cours..\n")
    
    def show_round_matches(self, matches):
        print("\n🔹 Matchs du premier round :\n")
        for match in matches:
            # print(f"{match['player1']} 🆚 {match['player2']}\n")
            print(f"Match : {match[0][0]['firstname']} {match[0][0]['lastname']} 🆚 {match[1][0]['firstname']} {match[1][0]['lastname']}")
    
###### ROUNDS RELATED ######

    def find_current_round_error(self) : 
        return print("Erreur : Impossible de trouver le round actuel")
    

    def create_next_round(self) : 
        str = "Création du prochain round en cours..."
        self.justify_text(str)
        print("\n")

    def created_round_successfully(self, current_round) : 
        print("Round ", current_round, " créé avec succès ! \n")
