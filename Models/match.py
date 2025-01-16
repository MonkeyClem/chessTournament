from Models.player import Player

class Match :

    def __init__(self, player_1, player_2) : 
        self.player_1 = [player_1, 0]
        self.player_2 = [player_2, 0]

    def set_winner(self, winner_index): 
        if winner_index == 1 :
            self.player_1[1] = 1
            self.player_2[1] = 0    
        elif winner_index == 2 :
            self.player_1[1] = 0
            self.player_2[1] = 1

    def to_tuple(self):
        return (self.player_1, self.player_2)
    
    @classmethod
    def from_tuple(cls, match_tuple) : 
        match = cls(match_tuple[0][0], match_tuple[1][0])
        match.player_1[1] = match_tuple[0][1]
        match.player_2[1] = match_tuple[1][1]
        return match


        
    def to_dict(self):
        return {
            "match": [
                {"player": self.match[0][0], "score": self.match[0][1]},
                {"player": self.match[1][0], "score": self.match[1][1]},
            ]
        }

    @classmethod
    def from_dict(cls, data):
        player1 = data["match"][0]["player"]
        score1 = data["match"][0]["score"]
        player2 = data["match"][1]["player"]
        score2 = data["match"][1]["score"]
        match = cls(player1, player2)
        match.match[0][1] = score1
        match.match[1][1] = score2
        return match

# match = Match(Player("John", "Doe"), Player("Jane", "Doe"))
    @classmethod 
    def from_list(cls, data):
        player1 = data[0][0]
        score1 = data[0][1]
        player2 = data[1][0]
        score2 = data[1][1]
        match = cls(player1, player2)
        match.player_1[1] = score1
        match.player_2[1] = score2
        return match