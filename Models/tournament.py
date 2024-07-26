
from datetime import datetime
from Models.tour import Round   

class Tournament : 
   

    def __init__(self, name, location, debut_date, end_date, nb_rounds, nb_players, current_round, players, description : str, rounds, previous_matches : list ) -> None: 
        self.name = name
        self.location = location
        self.debut_date = datetime.strptime(debut_date, "%Y-%m-%d") if debut_date else datetime.now()
        self.end_date = datetime.strptime(end_date, "%Y-%m-%d") if end_date else None
        self.nb_rounds = nb_rounds if nb_rounds else 4
        self.nb_players = nb_players if nb_players else 8
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
                "nb_players": self.nb_players,
                "current_round": self.current_round,
                "rounds": self.rounds,
                "players": self.players,
                "description": self.description,
                "previous_matches": self.previous_matches
            }
    
    @classmethod
    def from_dict(cls, data):
        rounds = [Round.from_dict(round_data) for round_data in data["rounds"]]
        return cls(
            name=data["name"],
            location=data["location"],
            debut_date=data["debut_date"],
            end_date=data["end_date"],
            nb_rounds=data["nb_rounds"],
            nb_players=data["nb_players"],
            current_round=data["current_round"],
            rounds=rounds,
            players=data["players"],
            description=data["description"],
            previous_matches=data["previous_matches"]
        )