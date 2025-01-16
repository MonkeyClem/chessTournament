import json
import random
import sys
from Models.tour import Round
from Models.match import Match
from Models.tournament import Tournament
from Models.player import PlayerScore
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
        # print("Tournament data : ", tournament_data)
        
        if(tournament_data["rounds"] != 0):
            pass
        # else:
        #     tournament_data["rounds"] = [round.to_dict() for round in tournament.rounds]
        tournament_data["rounds"] = [
            round.to_dict() if not isinstance(round, dict) else round
            for round in tournament_data["rounds"]
        ]
        # print("\n \n \n Tournament data before saving : ", tournament_data, "\n \n \n")
        try:
            # Ouvre le fichier en mode lecture pour charger les données existantes
            with open(filename, 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            # Si le fichier n'existe pas, on initialise avec une structure vide
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
        
        print("Tournament succesfully saved !")


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
            match = Match(selected_players[i], selected_players[i+1])
            match = match.to_tuple()
            matches.append(match)
            print("Match : ", match)
        print("Matchs du premier round : ", matches)
        first_round = Round("Round 1", matches)
        print(first_round.to_dict()) 
        return first_round
        

  
    def create_tournament(self):
        print("Création d'un tournament, veuillez renseigner les informations suivantes : ")
        name, location, debut_date, end_date, nb_rounds, nb_players, description = self.view.create_tournament_input()
        select_players= self.select_players(nb_players)
        current_round = 1
        first_round = self.create_first_round_matches(select_players)
        first_round = first_round.to_dict()
        print("First round : ", first_round)
        rounds=[first_round]
        players = [select_players]
        previous_matches = []   
        players_score = set_players_score(select_players)
        tournament = Tournament(name, location, debut_date, end_date, nb_rounds, nb_players, current_round, players, description, rounds, previous_matches, players_score)
        self.save_tournament(tournament)
        return tournament
    
    def show_tournaments(self):
        try: 
            with open('data/tournaments.json', "r") as file : 
                tournaments = json.load(file)
        except FileNotFoundError:
            print("No tournament found")
            return None
        
        user_choice = self.view.show_tournaments(tournaments)
        selected_tournament = self.select_tournament(tournaments) 
        print("Tournament selected : ", selected_tournament["name"])
        selected_tournament = Tournament.from_dict(selected_tournament)
        user_choice = self.tournament_options()
        if user_choice == '1':
            print("Lancement du tournoi !")
            self.resume_tournament(selected_tournament)
            # tournament_status = self.check_round_status(selected_tournament)
            # if tournament_status : 
            #     self.resume_tournament(selected_tournament)
            # else:
            #     print("Ce tournoi est terminé !")
        elif user_choice == '2':
            print("Affichage des rounds")
        elif user_choice == '3':
            print("Affichage des joueurs")
        elif user_choice == '4':
            print("Retour")
        else:
            print("Veuillez saisir une option valide")


    def select_tournament(self, tournaments):
        while True : 
            selected_index = input("Sélectionnez un tournoi via son numéro : ")
            try:
                selected_tournament = tournaments["tournaments"][int(selected_index) - 1]
                return selected_tournament
            except (IndexError, ValueError):
                print("\n \nVeuillez saisir un numéro de tournoi valide \n \n")

    def tournament_options(self):
        print("1. Lancer / reprendre le tournoi")
        print("2. Afficher les rounds")
        print("3. Afficher les joueurs")
        print("4. Retour")
        user_choice = input("Sélectionnez une option : ")
        return user_choice


    def create_next_round(self, selected_tournament): 
        print("Création du prochain round... \n")
        print("Les scores actuels sont : \n ")
        sorted_players = sorted(selected_tournament.players_score, key=lambda x: x['score'], reverse=True)
        for player in sorted_players:
            print(f"\n{player['firstname']} {player['lastname']} : {player['score']} points")

        # Convertir `previous_matches` pour simplifier la recherche de paires déjà jouées
        # previous_matches_set = {
        #     frozenset((match[0][0]["firstname"] + match[0][0]["lastname"], match[1][0]["firstname"] + match[1][0]["lastname"]))
        #     for match in selected_tournament.previous_matches
        # }
         # Convertir `previous_matches` pour simplifier la recherche de paires déjà jouées
        previous_matches_set = {
            frozenset((
                match[0][0][0]["firstname"] + match[0][0][0]["lastname"],  # Joueur 1
                match[0][1][0]["firstname"] + match[0][1][0]["lastname"]   # Joueur 2
            ))
            for match in selected_tournament.previous_matches
        }

        print(" \nPrevious matches set : ", previous_matches_set)
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
        for match in matches:
            print(f"{match[0][0]['firstname']} {match[0][0]['lastname']} vs {match[1][0]['firstname']} {match[1][0]['lastname']}")
            
        # matches = []
        # for i in range(0, len(sorted_players), 2):
        #     match = Match(sorted_players[i], sorted_players[i+1])
        #     match = match.to_tuple()
        #     matches.append(match)        
        # round = Round(f"Round {selected_tournament.current_round}", matches)
        # selected_tournament.rounds.append(round)
        # # print(" \n \n Round : ", round, "\n \n")
        # # print(" \n \n Round : ", round.to_dict())
        self.save_tournament(selected_tournament)
        pass


    def check_round_status(self, selected_tournament):
        pass

    def check_tournament_status(self, selected_tournament):
        if selected_tournament.current_round <= selected_tournament.nb_rounds:
                print("Le tournoi n'est pas terminé ! On passe au round suivant")
                return True
        # elif selected_tournament.current_round > selected_tournament.nb_rounds:
        #     print("Le tournoi est terminé !")
        #     self.save_tournament(selected_tournament)
        #     return False


    def find_current_round(self, selected_tournament):
        # Vérifier si l'index current_round existe dans la liste rounds
        try:
            current_round_index = selected_tournament.current_round - 1  # Convertir en index (0-based)
            current_round = selected_tournament.rounds[current_round_index]
            
            # Si le round est un dictionnaire, le convertir en instance Round
            if isinstance(current_round, dict):
                current_round = Round.from_dict(current_round)
            
            print("Current round : ", current_round)
            print("On sélectionne le round numéro ", current_round_index + 1)
            return current_round
        except IndexError:
            print(f"Le round {selected_tournament.current_round} est introuvable.")
            return None

    
    def resume_tournament(self, selected_tournament):
        while True :
            print("Resume tournament")
            print(selected_tournament)
            print(selected_tournament.rounds)
            found_round = self.find_current_round(selected_tournament)
            # print("Found round : ", found_round.to_dict())
            # if selected_tournament.current_round == 2:
            #     sys.exit("DEBUG PURPOSE")
            if selected_tournament.current_round > selected_tournament.nb_rounds:
                print("Ce tournoi est terminé ! Vous pouvez consulter les résultats, mais il n'est plus possible de jouer de matchs.")
                # self.save_tournament(selected_tournament)
                return
            # TO DO : Find actual round and play matches
            if isinstance(found_round, dict):
                found_round = Round.from_dict(found_round)
                print("Found round : ", found_round.to_dict())
            for match in found_round.matches:
                played_match = self.play_match(match, selected_tournament.players_score)
                selected_tournament.previous_matches.append(played_match)
                # Conversion de round en object JSON serializable
                # Vérifier si chaque élément de 'selected_tournament.rounds' est un dictionnaire ou un objet (peut changer en fonction de si l'on crée ou met à jour un tournoi)
                if selected_tournament.rounds and isinstance(selected_tournament.rounds[0], dict):
                    # Les rounds sont déjà des dictionnaires, pas besoin de les convertir
                    pass
                else:
                    # Convertir chaque round en dictionnaire en appelant 'to_dict()'
                    selected_tournament.rounds = [round.to_dict() for round in selected_tournament.rounds]
                self.save_tournament(selected_tournament)
            selected_tournament.current_round += 1
            self.save_tournament(selected_tournament)
            if selected_tournament.current_round <= selected_tournament.nb_rounds:
                print("\n \n Le tournoi n'est pas terminé ! Passons au round suivant... \n \n")
                print("Tournament previous matches : ", selected_tournament.previous_matches)
                # sys.exit("DEBUG PURPOSE")
                self.create_next_round(selected_tournament)
                self.save_tournament(selected_tournament)
                pass
            else:
                print(" \n\n Le tournoi est terminé \n !")
                self.save_tournament(selected_tournament)
                return
            pass     


            # for round in selected_tournament.rounds:
            #     if isinstance(round, dict):
            #         round = Round.from_dict(round)
            #         print("Round : ", round)
            #     for match in round.matches:
            #         played_match = self.play_match(match, selected_tournament.players_score)
            #         selected_tournament.previous_matches.append(played_match)
            #         # Conversion de round en object JSON serializable
            #         # Vérifier si chaque élément de 'selected_tournament.rounds' est un dictionnaire ou un objet (peut changer en fonction de si l'on crée ou met à jour un tournoi)
            #         if selected_tournament.rounds and isinstance(selected_tournament.rounds[0], dict):
            #             # Les rounds sont déjà des dictionnaires, pas besoin de les convertir
            #             pass
            #         else:
            #             # Convertir chaque round en dictionnaire en appelant 'to_dict()'
            #             selected_tournament.rounds = [round.to_dict() for round in selected_tournament.rounds]
            #         self.save_tournament(selected_tournament)
            #     selected_tournament.current_round += 1  
            #     self.save_tournament(selected_tournament)
            #     if selected_tournament.current_round <= selected_tournament.nb_rounds:
            #         print("\n \n Le tournoi n'est pas terminé ! Passons au round suivant... \n \n")
            #         self.create_next_round(selected_tournament)
            #         self.save_tournament(selected_tournament)
            #         pass
            #     else:
            #         print(" \n\n Le tournoi est terminé \n !")
            #         self.save_tournament(selected_tournament)
            #         return
            # pass    
                
    def play_match(self, match, players_score):
        print("Match : ", match)
        player_1 = match[0][0]
        player_2 = match[1][0]
        print(f"1: {player_1['firstname']} {player_1['lastname']}")
        print(f"2: {player_2['firstname']} {player_2['lastname']}")
        # Demander à l'utilisateur de saisir l'index du vainqueur
        while True:
            try:
                winner_index = int(input("Entrez l'index du joueur vainqueur (1 ou 2) : "))
                update_players_score(player_1, player_2, winner_index, players_score)
                if winner_index not in [1, 2]:
                    raise ValueError("L'index doit être 1 ou 2.")
                break
            except ValueError as e:
                print(e)
        # Mettre à jour le score du joueur gagnant
        if winner_index == 1:
            match[0][1] += 1
        else:
            match[1][1] += 1

        return match, players_score


            
def set_players_score(selected_players):
    # print('selected players ==> ', selected_players)
    players_score = []
    for player in selected_players:
        # Utilisation des clés de dictionnaire pour accéder aux valeurs
        player_score = PlayerScore(
            firstname=player['firstname'],
            lastname=player['lastname'],
            score=0  # Initialiser le score à 0
        )
        players_score.append(player_score.to_dict())  # Convertir en dict
    print('players score ==> ', players_score)
    return players_score



def update_players_score(player_1, player_2, winner_index, players_score):
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
    
        



        

    