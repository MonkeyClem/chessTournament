from datetime import datetime
import sys
from Models.player import Player
from Models.match import Match
from Models.tour import Tour

class Tournoi:
    def __init__(self, name, location, beginning_date, end_date, tours, description, previous_matchs, number_of_rounds=4):
        self.name = name
        self.place = location
        self.beginning_date = datetime.strptime(beginning_date, "%Y-%m-%d")
        self.date_fin = datetime.strptime(end_date, "%Y-%m-%d")
        self.nombre_tours = number_of_rounds
        self.tour_actuel = 0
        self.tours = [Tour]
        self.joueurs = []
        self.previous_matchs = []
        self.description = description

    def to_dict(self):
        ## VERIFIER OU SE TROUVE LA MODIF' DE TOURS
        print(self.tours)
        # tours = self.tours if isinstance(self.tours, dict) else [tour.to_dict() for tour in self.tours]
        return {
            "name": self.name,
            "place": self.place,
            "beginning_date": self.beginning_date.strftime("%Y-%m-%d"),
            "date_fin": self.date_fin.strftime("%Y-%m-%d"),
            "nombre_tours": self.nombre_tours,
            "tour_actuel": self.tour_actuel,
            "previous_matchs": self.previous_matchs, 
            "tours": [tour.to_dict(self) for tour in self.tours],
            # "tours": tours,
            # "tours": Tour.to_dict([self.tours]),
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
            number_of_rounds=data.get("nombre_tours", 4),
            previous_matchs = data.get("previous_matchs", []),
            tours = [Tour.from_dict(tour) for tour in data.get("tours", [])],

        )
        tournoi.tour_actuel = data.get("tour_actuel", 0)
        tournoi.tours = [Tour.from_dict(tour) for tour in data.get("tours", [])]
        tournoi.joueurs = [Player.from_dict(player) for player in data.get("joueurs", [])]
        return tournoi



