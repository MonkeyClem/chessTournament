from datetime import datetime


class Tournoi:
    def __init__(self, nom, lieu, date_debut, date_fin, description, nombre_tours=4):
        self.nom = nom
        self.lieu = lieu
        self.date_debut = datetime.strptime(date_debut, "%Y-%m-%d")
        self.date_fin = datetime.strptime(date_fin, "%Y-%m-%d")
        self.nombre_tours = nombre_tours
        self.tour_actuel = 0
        self.tours = []
        self.joueurs = []
        self.description = description

    def ajouter_joueur(self, joueur):
        self.joueurs.append(joueur)

    def commencer_tour(self):
        if self.tour_actuel < self.nombre_tours:
            self.tour_actuel += 1
            tour = Tour(f'Tour {self.tour_actuel}')
            self.tours.append(tour)
        else:
            print("Le nombre maximum de tours est atteint.")

    def terminer_tour_actuel(self):
        if self.tours:
            self.tours[-1].terminer_tour()

    def __str__(self):
        tours_str = "\n".join(str(tour) for tour in self.tours)
        return (f"Tournoi: {self.nom}\n"
                f"Lieu: {self.lieu}\n"
                f"Date de début: {self.date_debut.strftime('%Y-%m-%d')}\n"
                f"Date de fin: {self.date_fin.strftime('%Y-%m-%d')}\n"
                f"Nombre de tours: {self.nombre_tours}\n"
                f"Tour actuel: {self.tour_actuel}\n"
                f"Joueurs: {', '.join(self.joueurs)}\n"
                f"Description: {self.description}\n"
                f"Tours:\n{tours_str}\n")

class Player:
    def __init__(self, lastname,firtsname, birthdate):
        self.lastname = lastname
        self.firtsname = firtsname
        self.birthdate = birthdate

    def to_dict(self):
        return {
            "lastname": self.lastname,
            "firstname": self.firtsname,
            "birthdate": self.birthdate,
        }
    
    @staticmethod
    def from_dict(data):
        return Player(data["lastname"], data["firstname"], data["birthdate"])

class Match:
    def __init__(self, joueur1, score1, joueur2, score2):
        self.match = ([joueur1, score1], [joueur2, score2])

    def __str__(self):
        return f"{self.match[0][0]} vs {self.match[1][0]} : {self.match[0][1]} - {self.match[1][1]}"

class Tour:
    def __init__(self, nom):
        self.nom = nom
        self.date_debut = datetime.now()
        self.date_fin = None
        self.matchs = []

    def ajouter_match(self, joueur1, score1, joueur2, score2):
        match = Match(joueur1, score1, joueur2, score2)
        self.matchs.append(match)

    def terminer_tour(self):
        self.date_fin = datetime.now()

    def __str__(self):
        matchs_str = "\n".join(str(match) for match in self.matchs)
        return (f"{self.nom}\n"
                f"Date de début: {self.date_debut.strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"Date de fin: {self.date_fin.strftime('%Y-%m-%d %H:%M:%S') if self.date_fin else 'En cours'}\n"
                f"Matchs:\n{matchs_str}\n")
