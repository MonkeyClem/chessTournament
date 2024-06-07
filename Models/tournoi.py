from datetime import datetime
from Models.player import Player
from Models.match import Match

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



