from datetime import datetime
class Round:
    def __init__(self, name, matches, start_time=None, end_time=None):
        self.name = name
        self.matches = matches if matches else []
        self.start_time = start_time if start_time else datetime.now()
        self.end_time = end_time

    def to_dict(self):
        return {
            "name": self.name,
            "matches": self.matches,
            "start_time": self.start_time.strftime("%Y-%m-%d %H:%M:%S") if self.start_time else None,
            "end_time": self.end_time.strftime("%Y-%m-%d %H:%M:%S") if self.end_time else None
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data["name"],
            matches=data["matches"],
            start_time=datetime.strptime(data["start_time"], "%Y-%m-%d %H:%M:%S") if data["start_time"] else None,
            end_time=datetime.strptime(data["end_time"], "%Y-%m-%d %H:%M:%S") if data["end_time"] else None
        )