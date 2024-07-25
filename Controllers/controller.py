from Models.tournoi import Tournoi
class Controller : 
    
    def __init__(self, view) -> None:
        pass

    def create_tournoi(self):
        print("Création d'un tournoi, veuillez renseigner les informations suivantes : ")
        name = input("Nom du tournoi : ")
        location = input("Lieu du tournoi : ")
        debut_date = input("Date de début du tournoi : ")
        end_date = input("Date de fin du tournoi : ")
        nb_rounds = input("Nombre de rounds : ")
        description = input("Description du tournoi : ")
        tournoi = Tournoi(name, location, debut_date, end_date, nb_rounds, description)
        print("Tournoi créé avec succès ! : " + tournoi)
        return tournoi

