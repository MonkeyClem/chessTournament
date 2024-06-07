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