from datetime import datetime
import sys
from Models.match import Match

class Tour:
    def __init__(self, nom, date_debut, date_fin, matchs ):
        self.nom = nom
        self.date_debut = datetime.now() if date_debut is None else date_debut
        self.date_fin = None if date_fin is None else date_fin
        self.matchs = [Match.from_dict(match) if isinstance(match, dict) else match for match in matchs]

    def ajouter_match(self, joueur1, score1, joueur2, score2):
        match = Match(joueur1, score1, joueur2, score2)
        self.matchs.append(match)

    def end_round(self):
        self.date_fin = datetime.now()

    def to_dict(self):
        print("self to dict au sein du tour.py : ", self)
        
        return {
            "name": self.nom,
            "start_time": self.date_debut.strftime("%Y-%m-%d %H:%M:%S"),
            "end_time": self.date_fin.strftime("%Y-%m-%d %H:%M:%S") if self.date_fin else None,
            "matches": [match.to_dict() for match in self.matchs]
        }

    @staticmethod
    def from_dict(data):
        print("data au sein du from_dict de tour.py : ", data)
        print("data type ==>", type(data))
        if(isinstance(data, dict)):
            tour = Tour(
                nom=data["name"],
                date_debut=datetime.strptime(data["start_time"], "%Y-%m-%d %H:%M:%S"),
                date_fin=datetime.strptime(data["end_time"], "%Y-%m-%d %H:%M:%S") if data["end_time"] else None,
                matchs=data["matches"]
            )
            return tour
        elif(isinstance(data, list)):
            print("Data is a list")
            for tour in data:
                print("tour ==>", tour)
                print('tour name ==>', tour["name"])
                print("tour type ==>", type(tour))
                tour = Tour(
                    nom=tour["name"],
                    date_debut=datetime.strptime(tour["start_time"], "%Y-%m-%d %H:%M:%S"),
                    date_fin=datetime.strptime(tour["end_time"], "%Y-%m-%d %H:%M:%S") if tour["end_time"] else None,
                    matchs=tour["matches"]
                )
                return tour
        return tour 
        # sys.exit("DONE")

        # tour = Tour(
        #     nom=data["name"],
        #     date_debut=datetime.strptime(data["start_time"], "%Y-%m-%d %H:%M:%S"),
        #     date_fin=datetime.strptime(data["end_time"], "%Y-%m-%d %H:%M:%S") if data["end_time"] else None,
        #     matchs=data["matches"]
        # )
        # return tour
    