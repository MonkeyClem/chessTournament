import datetime
from Models.match import Match

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
