from message import Message

class Update:
    def __init__(self, json):
        self.message = Message(json["message"])
        self.update_id = json["update_id"]
    