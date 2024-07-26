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
