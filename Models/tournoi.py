class Tournoi : 
   

    def init(self, name, location, debut_date, nb_rounds, players, description, previous_matches) : 
        self.name = name
        self.location = location
        self.debut_date = debut_date
        self.nb_rounds = nb_rounds if nb_rounds else 4
        self.players = players if players else []
        self.description = description
        self.rounds = []
        self.previous_matches = previous_matches if previous_matches else []   