class Player:
    def __init__(self, lastname, firstname, birthdate):
        self.lastname = lastname
        self.firstname = firstname
        self.birthdate = birthdate

    def to_dict(self):
        return {
            "lastname": self.lastname,
            "firstname": self.firstname,
            "birthdate": self.birthdate
        }

    @staticmethod
    def from_dict(data):
        return Player(
            lastname=data["lastname"],
            firstname=data["firstname"],
            birthdate=data["birthdate"]
        )
 
    # @staticmethod
    # def from_dict(data):
    #     return Player(data["lastname"], data["firstname"], data["birthdate"])

class PlayerScore:
    def __init__(self, firstname, lastname, score):
        self.firstname = firstname
        self.lastname = lastname
        self.score = score

    def to_dict(self):
        return {
            "firstname": self.firstname,
            "lastname": self.lastname,
            "score": self.score
        }
    
    @staticmethod
    def from_dict(data):
        return PlayerScore(
            firstname=data["firstname"],
            lastname=data["lastname"],
            score=data["score"]
        )
