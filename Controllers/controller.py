import json
import random
import sys
from Models.tour import Round
from Models.match import Match
from Models.tournament import Tournament
from Models.player import PlayerScore
import os
from datetime import datetime
class Controller : 

 
    def __init__(self, view) -> None:
        self.view = view
        pass
    
    def load_players(self, filename="data/players.json"):
        try:
            with open(filename, "r") as file:
                players = json.load(file)
        except FileNotFoundError:
            players = {'players': []}
        return players['players']
    
    def show_all_players(self):
        players = self.load_players()
        self.view.show_all_players(players)
        

    def set_players_score(players):
        players_score = []
        for player in players:
            player_score = PlayerScore(
                firstname=player.firstname,
                lastname=player.lastname,
                score=0  # Initialiser le score à 0
            )
            players_score.append(player_score)
        return players_score



    def save_tournament(self, tournament, filename = "data/tournaments.json"):
        tournament_data = tournament.to_dict()
        if(tournament_data["rounds"] != 0):
            pass

        tournament_data["rounds"] = [
            round.to_dict() if not isinstance(round, dict) else round
            for round in tournament_data["rounds"]
        ]
       # Vérification et lecture du fichier JSON
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                content = file.read().strip()  # Lire le contenu et retirer les espaces blancs

                if not content:  # Si le fichier est vide
                    data = {"tournaments": []}
                else:
                    data = json.loads(content)  # Charger les données JSON

        except FileNotFoundError:
            data = {"tournaments": []}
        except json.JSONDecodeError:  # Gestion du fichier corrompu ou vide
            data = {"tournaments": []}

        # Ajouter ou mettre à jour le tournoi dans les données
        tournament_found = False
        for i, existing_tournament in enumerate(data["tournaments"]):
            if existing_tournament["name"] == tournament_data["name"]:  # Utilisation du nom pour identifier le tournoi
                data["tournaments"][i] = tournament_data  # Mise à jour des données du tournoi
                tournament_found = True
                break
        if not tournament_found:
            # Si le tournoi n'existe pas encore dans la liste, on l'ajoute
            data["tournaments"].append(tournament_data)

        # Ouvre le fichier en mode écriture pour sauvegarder les modifications
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)
        
        self.view.tournament_successfully_saved()

    def select_players(self, nb_players):
        players = self.load_players()
        if not players:
            self.view.empty_players_database()
            return None
        self.view.show_all_players(players)
        selected_players = []

        while len(selected_players) < nb_players:
            try:
                # chosen_player = int(input("Sélectionnez un joueur (par numéro) : "))
                chosen_player = self.view.select_a_player()
                if chosen_player < 1 or chosen_player > len(players):
                    self.view.error_adding_player
                    continue
                elif players[chosen_player - 1] in selected_players:
                    self.view.already_selected_player
                    continue
                else:
                    selected_players.append(players[chosen_player - 1])
            except ValueError:
                self.view.error_adding_player
        return selected_players
        

    
    def create_first_round_matches(self, selected_players):
        self.view.first_round_matches_creation()
        matches = []
        random.shuffle(selected_players)
        for i in range(0, len(selected_players), 2): 
            match = Match(selected_players[i], selected_players[i+1])
            match = match.to_tuple()
            matches.append(match)
        first_round = Round("Round 1", matches)
        self.display_round_matches(first_round.to_dict())
        return first_round
    

    def display_round_matches(self, round_data):
    # Extraire les matchs depuis le dictionnaire du round
        matches = round_data["matches"]

        formatted_matches = []
        for i, match in enumerate(matches, start=1):
            p1_info = match[0][0]  
            p1_score = match[0][1]  
            p2_info = match[1][0] 
            p2_score = match[1][1] 

            formatted_matches.append({
                "match_number": i,
                "player1": f"{p1_info['firstname']} {p1_info['lastname']} ({p1_score} pts)",
                "player2": f"{p2_info['firstname']} {p2_info['lastname']} ({p2_score} pts)"
            })

        # Envoyer les données formatées à la vue
        self.view.show_round_matches(formatted_matches)

    
        


    def create_tournament(self):
        self.view.create_tournament()
        name, location, debut_date, end_date, nb_rounds, nb_players, description = self.view.create_tournament_input()
        select_players= self.select_players(nb_players)
        current_round = 1
        first_round = self.create_first_round_matches(select_players)
        first_round = first_round.to_dict()
        rounds=[first_round]
        players = [select_players]
        previous_matches = []   
        players_score = self.set_players_score(select_players)
        tournament = Tournament(name, location, debut_date, end_date, nb_rounds, nb_players, current_round, players, description, rounds, previous_matches, players_score)
        self.save_tournament(tournament)
        return tournament
    
    def show_tournaments(self):
        try: 
            with open('data/tournaments.json', "r") as file : 
                tournaments = json.load(file)
        except FileNotFoundError:
            self.view.no_tournament_found()
            return None
        except json.JSONDecodeError:
            #TO HANDLE EMPTY FILE
            self.view.empty_tournament_list()
            return None  
        user_choice = self.view.show_tournaments(tournaments)
        selected_tournament = self.select_tournament(tournaments) 
        self.view.show_selected_tournament(selected_tournament)
        selected_tournament = Tournament.from_dict(selected_tournament)
        user_choice = self.view.show_tournament_options()
        if user_choice == '1':
            self.resume_tournament(selected_tournament)
        else : 
            self.view.tournament_options_selector(user_choice, selected_tournament.to_dict())



    def select_tournament(self, tournaments):
        while True : 
            selected_index = self.view.select_tournament_input()
            try:
                selected_tournament = tournaments["tournaments"][int(selected_index) - 1]
                return selected_tournament
            except (IndexError, ValueError):
                self.view.select_tournament_error()


    def create_next_round(self, selected_tournament): 
        self.view.create_next_round()
        sorted_players = sorted(selected_tournament.players_score, key=lambda x: x['score'], reverse=True)
        self.view.show_current_score(sorted_players)
         # Convertir `previous_matches` pour simplifier la recherche de paires déjà jouées
        previous_matches_set = {
            frozenset((
                match[0][0][0]["firstname"] + match[0][0][0]["lastname"],  # Joueur 1
                match[0][1][0]["firstname"] + match[0][1][0]["lastname"]   # Joueur 2
            ))
            for match in selected_tournament.previous_matches
        }

        matches = []
        i = 0
        while i < len(sorted_players) - 1:
            # Essayer d'associer le joueur i avec le joueur i+1
            player1 = sorted_players[i]
            player2 = sorted_players[i + 1]

            # Vérifier si la paire a déjà joué ensemble
            player1_id = player1['firstname'] + player1['lastname']
            player2_id = player2['firstname'] + player2['lastname']
            if frozenset([player1_id, player2_id]) not in previous_matches_set:
                # Si la paire est nouvelle, créer le match
                match = Match(player1, player2).to_tuple()
                matches.append(match)
                previous_matches_set.add(frozenset([player1_id, player2_id]))
                i += 2  # Passer aux joueurs suivants
            else:
                # Si la paire a déjà joué ensemble, trouver un autre partenaire
                found_partner = False
                for j in range(i + 2, len(sorted_players)):
                    alt_player = sorted_players[j]
                    alt_player_id = alt_player['firstname'] + alt_player['lastname']
                    if frozenset([player1_id, alt_player_id]) not in previous_matches_set:
                        # Créer un match avec le joueur alternatif trouvé
                        match = Match(player1, alt_player).to_tuple()
                        matches.append(match)
                        previous_matches_set.add(frozenset([player1_id, alt_player_id]))
                        # Échanger les joueurs pour garantir l'ordre du parcours
                        sorted_players[i + 1], sorted_players[j] = sorted_players[j], sorted_players[i + 1]
                        found_partner = True
                        i += 2  # Passer aux joueurs suivants
                        break
                
                if not found_partner:
                    # Aucun partenaire n'a pu être trouvé, assigner le suivant
                    match = Match(player1, player2).to_tuple()
                    matches.append(match)
                    previous_matches_set.add(frozenset([player1_id, player2_id]))
                    i += 2  # Passer aux joueurs suivants

        # Créer le round et l'ajouter au tournoi
        round = Round(f"Round {selected_tournament.current_round}", matches)
        selected_tournament.rounds.append(round)
        print(f"Round {selected_tournament.current_round} créé avec les matchs :")
        self.view.show_round_matches(matches)
        # for match in matches:
        #     print(f"{match[0][0]['firstname']} {match[0][0]['lastname']} vs {match[1][0]['firstname']} {match[1][0]['lastname']}")
        self.save_tournament(selected_tournament)
        pass

    ##TODO : Implement a verification in order to set the end time of the round
    # def check_round_status(self, selected_tournament):
    #     print("Vérification du statut du round en cours...")
    #     # selected_tournament = selected_tournament.to_dict()
    #     current_round = selected_tournament.to_dict()["current_round"]
    #     print("current_round" , current_round)
    #     rounds = selected_tournament.to_dict()["rounds"]
    #     print("ROUNDS =>", rounds)
    #     print("CurrentRound round ==>", selected_tournament.to_dict()["rounds"][current_round - 1])
    #     print("CurrentRound round Matches =>", selected_tournament.to_dict()["rounds"][current_round - 1].to_dict()["matches"])
    

    #     pass

    
    def check_tournament_status(self, selected_tournament):
        if selected_tournament.current_round <= selected_tournament.nb_rounds:            
            self.create_next_round(selected_tournament)
            self.save_tournament(selected_tournament)
            pass
        else:
            self.view.finished_tournament()
            self.save_tournament(selected_tournament)
            return
    


    def find_current_round(self, selected_tournament):
        # round_status = self.check_round_status(selected_tournament)
        # Vérifier si l'index current_round existe dans la liste rounds
        try:
            current_round_index = selected_tournament.current_round - 1  # Convertir en index (0-based)
            current_round = selected_tournament.rounds[current_round_index]
            
            # Si le round est un dictionnaire, le convertir en instance Round
            if isinstance(current_round, dict):
                current_round = Round.from_dict(current_round)

            return current_round
        except IndexError:
            self.view.find_current_round_error()
            return None

    
    def resume_tournament(self, selected_tournament):
        while True :
            if selected_tournament.current_round > selected_tournament.nb_rounds:
                self.view.finished_tournament()
                return
            self.view.resume_or_start_message(selected_tournament.current_round)
            found_round = self.find_current_round(selected_tournament)
            if isinstance(found_round, dict):
                #TO DO : Vérifier pourquoi j'ai mis cette condition, probablement un cas de figure ou le round nous parvient sous forme de dict
                found_round = Round.from_dict(found_round)
            for match in found_round.matches:
                #TO DO: Sauvegarder après chaque match afin que le tournoi puisse être repris à tout moment
                played_match = self.play_match(match, selected_tournament.players_score, selected_tournament)
                selected_tournament.previous_matches.append(played_match)
                # Conversion de round en object JSON serializable
                # Vérifier si chaque élément de 'selected_tournament.rounds' est un dictionnaire ou un objet (peut changer en fonction de si l'on crée ou met à jour un tournoi)
                print("Type réel de selected_tournament.rounds[0] :", type(selected_tournament.rounds[selected_tournament.current_round - 1]))
            #     if selected_tournament.rounds and isinstance(selected_tournament.rounds[0], dict):
            #         # Les rounds sont déjà des dictionnaires, pas besoin de les convertir
            #         # selected_tournament.rounds[selected_tournament.current_round - 1]['end_time'] = datetime.now().strpti('%Y-%m-%d %H:%M:%S')
            #         pass
            #     else:
            #         # Convertir chaque round en dictionnaire en appelant 'to_dict()'
            #         # selected_tournament.rounds[selected_tournament.current_round - 1].end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            #         selected_tournament.rounds = [round.to_dict() for round in selected_tournament.rounds]
            # # selected_tournament.rounds[selected_tournament.current_round - 1]['end_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            index = selected_tournament.current_round - 1
            round_obj = selected_tournament.rounds[index]

            if not isinstance(round_obj, dict):
                selected_tournament.rounds = [r.to_dict() if not isinstance(r, dict) else r for r in selected_tournament.rounds]

            # Maintenant on peut accéder sans erreur
            selected_tournament.rounds[index]['end_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            print("\n \n On essaie d'accéder au end_time du round actuel")
            selected_tournament.rounds[selected_tournament.current_round - 1]['end_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            selected_tournament.current_round += 1
            self.save_tournament(selected_tournament)
            self.check_tournament_status(selected_tournament = selected_tournament)
            pass     

  
                
    def play_match(self, match, players_score, selected_tournament):
        self.view.show_match(match, players_score)
        player_1 = match[0][0]
        player_2 = match[1][0]
        # Demander à l'utilisateur de saisir l'index du vainqueur
        while True:
            try:
                winner_index = self.view.ask_winner_index()
                self.update_players_score(player_1, player_2, winner_index, players_score)
                if winner_index not in [1, 2]:
                    raise ValueError("L'index doit être 1 ou 2.")
                break
            except ValueError as e:
                print(e)
        # Mettre à jour le score du joueur gagnant
        if winner_index == 1:
            match[0][1] += 1
            print(match[0][1])
        else:
            match[1][1] += 1
            print(match[1][1])
            
        # Match.set_winner( winner_index = winner_index)
        # self.save_tournament(selected_tournament)

        return match, players_score


            
    def set_players_score(self, selected_players):
        players_score = []
        for player in selected_players:
            # Utilisation des clés de dictionnaire pour accéder aux valeurs
            player_score = PlayerScore(
                firstname=player['firstname'],
                lastname=player['lastname'],
                score=0  
            )
            players_score.append(player_score.to_dict())  # Convertir en dict
        return players_score



    def update_players_score(self, player_1, player_2, winner_index, players_score):
        if winner_index == 1:
            for player in players_score:
                if player['firstname'] == player_1['firstname'] and player['lastname'] == player_1['lastname']:
                    player['score'] += 1
                elif player['firstname'] == player_2['firstname'] and player['lastname'] == player_2['lastname']:
                    pass
        elif winner_index == 2:
            for player in players_score:
                if player['firstname'] == player_1['firstname'] and player['lastname'] == player_1['lastname']:
                    pass
                elif player['firstname'] == player_2['firstname'] and player['lastname'] == player_2['lastname']:
                    player['score'] += 1
        return players_score

    def get_new_player_info(self) : 
        lastname, firstname, birthdate = self.view.get_new_player_info()
        return lastname, firstname, birthdate

    def create_new_player(self) : 
        filename="data/players.json"
        lastname, firstname, birthdate = self.get_new_player_info()
        new_player = {
            'lastname' : lastname.upper(),
            "firstname": firstname,
            "birthdate": birthdate
        }
        
        if os.path.exists(filename) : 
            with open(filename, "r") as file : 
                try :
                    players_data = json.load(file)  # Charger tout le contenu
                    if not isinstance(players_data, dict) or "players" not in players_data:
                        players_data = {"players": []}
                except json.JSONDecodeError:
                    players_data = {"players": []}
        else : 
            players_data = {"players": []}

        players_data["players"].append(new_player)
        with open(filename, "w", encoding="utf-8") as file : 
            json.dump(players_data, file, indent= 4)
            # print("Joueur ajouté avec succès !")
            self.view.player_successfully_saved()
        return players_data
                



        

    