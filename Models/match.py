class Match:
    def __init__(self, joueur1, score1, joueur2, score2):
        self.match = ([joueur1, score1], [joueur2, score2])

    def __str__(self):
        return f"{self.match[0][0]} vs {self.match[1][0]} : {self.match[0][1]} - {self.match[1][1]}"