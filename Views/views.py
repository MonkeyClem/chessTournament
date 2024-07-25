class Views :

     
    def __init__(self) -> None:
        pass

    def main_menu_selector(self) -> str : 
        user_choice = input("Sélectionnez une option : ")
        return user_choice
    
    def show_show_menu(self) : 
        print("1. Créer un tournoi")
        print("2. Afficher tous les tournois")
        print("3. Afficher tous les joueurs")
        print("4. Créer un joueur")
        print("5. Quitter")
        user_choice = self.main_menu_selector()
        return user_choice
