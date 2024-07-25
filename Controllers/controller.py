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
        current_round = 1
        description = input("Description du tournoi : ")
        rounds=[]
        players = []
        previous_matches = []   
        tournoi = Tournoi(name, location, debut_date, end_date, nb_rounds, current_round, players, description, rounds, previous_matches)
        print("Tournoi créé avec succès ! : " , tournoi.to_dict())
        return tournoi

