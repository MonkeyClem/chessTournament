from Models.match import Match


class View :
    def show_menu(self):
        print("\nMenu Principal")
        print("1. Créer un tournoi")
        print("2. Afficher tous les tournois")
        print("3. Afficher tous les joueurs")
        print("4. Créer un joueur")
        print("5. Quitter")
        return input("Entrez votre choix: ")
    
    def ask_player_information(self):
        lastname = input("Entrez le nom de famille du joueur: ")
        firstname = input("Entrez le prénom du joueur: ")
        birthdate = int(input("Entrez l'année de naissance du joueur: "))
        return lastname, firstname, birthdate 
    
    def show_created_player(self, player):
        print(f"Le joueur {player['lastname']} {player['firstname']} a été créé avec succès !")
    
    def show_all_players(self, players):
        for i, player in enumerate(players):
            print(f" {i + 1}. {player['lastname']} {player['firstname']} ({player['birthdate']})")


    def ask_tournoi_information(self):
        name = input("Entrez le nom du tournoi: ")
        location = input("Entrez le lieu du tournoi: ")
        beginning_date = input("Entrez la date de début du tournoi (YYYY-MM-DD): ")
        end_date = input("Entrez la date de fin du tournoi (YYYY-MM-DD): ")
        description = input("Entrez une description pour le tournoi: ")
        number_of_rounds = int(input("Entrez le nombre de tours (par défaut 4): ") or 4)
        return name, location, beginning_date, end_date, description, number_of_rounds

    def ask_number_of_players(self):
        return int(input("Entrez le nombre de joueurs pour ce tournoi: "))

    def select_players(self, available_players, number_of_players):
        selected_players = []
        print("Sélectionnez les joueurs pour le tournoi :")
        for index, player in enumerate(available_players):
            print(f"{index + 1}. {player['firstname']} {player['lastname']}")

        for _ in range(number_of_players):
            player_index = int(input(f"Sélectionnez (via l'index) le joueur {_ + 1}/{number_of_players}: ")) - 1
            selected_players.append(available_players[player_index])
        return selected_players
    
    def show_all_tournaments(self, tournaments):
        for i, tournoi in enumerate(tournaments):
            print(f"{i + 1}. {tournoi['name']} ")

    def already_started_tournament(self, tournoi):
        # tournoi = tournoi.to_dict()
        # tour_actuel = tournoi["tour_actuel"]
        print(f"Le tournoi a déjà commencé. Nous en sommes actuellement au tour {tournoi['tour_actuel']}.")

    def ask_resume_tournament(self):
        resume_tournament = input("Souhaitez-vous reprendre le tournoi ? (O/N):")  
        return resume_tournament

    def ask_for_match_result(self, match):
        match = Match.to_dict(match)
        print("MATCH ==> ", match)
        # print(f"Entrez le score pour le match suivant : {match['joueur1']} vs {match['joueur2']}")
        players = match['players']
        # print("players ==> ", players)
        winner_name = input(f"Entrez le nom du vainqueur pour le match : {players[0]['player']['lastname']} {players[0]['player']['firstname']} vs {players[1]['player']['lastname']} {players[1]['player']['firstname']}: ")

        return winner_name