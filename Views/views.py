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
    
    def show_all_players(self, players):
        for i, player in enumerate(players):
            print(f" {i + 1}, {player['lastname']} {player['firstname']} ({player['birthdate']})")

  
    