from Models.player import Player


# Models/tournoi.py
class Match:
    def __init__(self, joueur1, score1, joueur2, score2):
        self.players = ([joueur1, score1], [joueur2, score2])

    # def __init__(self, player1, player2):
    #     self.match = ( [player1, 0], [player2, 0] )  # Tuple containing two lists, each with a player and score


    def to_dict(self):
        return {
            "players": [
                {"player": self.players[0][0].to_dict(), "score": self.players[0][1]},
                {"player": self.players[1][0].to_dict(), "score": self.players[1][1]}
            ]
        }
    


    @staticmethod
    def from_dict(data):
        joueur1 = Player.from_dict(data["players"][0]["player"])
        score1 = data["players"][0]["score"]
        joueur2 = Player.from_dict(data["players"][1]["player"])
        score2 = data["players"][1]["score"]
        return Match(joueur1, score1, joueur2, score2)
    
    # def toJSON(self):
    #     return json.dumps(
    #         self,
    #         default=lambda o: o.__dict__, 
    #         sort_keys=True,
    #         indent=4)
