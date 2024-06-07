from datetime import datetime

class Player:
    def __init__(self, lastname, firstname, birthdate):
        self.lastname = lastname
        self.firstname = firstname
        self.birthdate = birthdate

    def to_dict(self):
        return {
            "lastname": self.lastname,
            "firstname": self.firstname,
            "birthdate": self.birthdate
        }

    @staticmethod
    def from_dict(data):
        return Player(
            lastname=data["lastname"],
            firstname=data["firstname"],
            birthdate=data["birthdate"]
        )
 
    # @staticmethod
    # def from_dict(data):
    #     return Player(data["lastname"], data["firstname"], data["birthdate"])

class Tournoi:
    def __init__(self, name, location, beginning_date, end_date, description, number_of_rounds=4):
        self.name = name
        self.place = location
        self.beginning_date = datetime.strptime(beginning_date, "%Y-%m-%d")
        self.date_fin = datetime.strptime(end_date, "%Y-%m-%d")
        self.nombre_tours = number_of_rounds
        self.tour_actuel = 0
        self.tours = []
        self.joueurs = []
        self.description = description

    def to_dict(self):
        return {
            "name": self.name,
            "place": self.place,
            "beginning_date": self.beginning_date.strftime("%Y-%m-%d"),
            "date_fin": self.date_fin.strftime("%Y-%m-%d"),
            "nombre_tours": self.nombre_tours,
            "tour_actuel": self.tour_actuel,
            "tours": self.tours,
            "joueurs": [player.to_dict() for player in self.joueurs],
            "description": self.description
        }

    @staticmethod
    def from_dict(data):
        tournoi = Tournoi(
            name=data["name"],
            location=data["place"],
            beginning_date=data["beginning_date"],
            end_date=data["date_fin"],
            description=data["description"],
            number_of_rounds=data.get("nombre_tours", 4)
        )
        tournoi.tour_actuel = data.get("tour_actuel", 0)
        tournoi.tours = data.get("tours", [])
        tournoi.joueurs = [Player.from_dict(player) for player in data.get("joueurs", [])]
        return tournoi



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
