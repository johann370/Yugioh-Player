class Card:
    def __init__(self, name, card_type):
        self.name = name
        self.card_type = card_type
        self.face_up = None
        self.owner = None
        self.current_owner = None
        self.options = []
        self.location = None

    def set_owner(self, owner):
        self.owner = owner
        self.current_owner = self.owner
