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
        match.player2[1] = match_tuple[1][1]
        return match