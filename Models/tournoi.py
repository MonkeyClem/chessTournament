
from datetime import datetime

class Tournoi : 
   

    def __init__(self, name, location, debut_date, end_date, nb_rounds, current_round, players, description : str, rounds, previous_matches : list ) -> None: 
        self.name = name
        self.location = location
        self.debut_date = datetime.strptime(debut_date, "%Y-%m-%d") if debut_date else datetime.now()
        self.end_date = datetime.strptime(end_date, "%Y-%m-%d") if end_date else None
        self.nb_rounds = nb_rounds if nb_rounds else 4
        self.current_round = current_round if current_round else 1
        self.rounds = rounds if rounds else []
        self.players = players if players else []
        self.description = description if description else ""
        self.previous_matches = previous_matches if previous_matches else []  
        
    def to_dict(self):
        return {
                "name": self.name,
                "location": self.location,
                "debut_date": self.debut_date.strftime("%Y-%m-%d") if self.debut_date else None,
                "end_date": self.end_date.strftime("%Y-%m-%d") if self.end_date else None,
                "nb_rounds": self.nb_rounds,
                "current_round": self.current_round,
                "rounds": self.rounds,
                "players": self.players,
                "description": self.description,
                "previous_matches": self.previous_matches
            }