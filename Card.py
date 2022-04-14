class Card:
    def __init__(self, name, cardType):
        self.name = name
        self.cardType = cardType
        self.faceUp = None
        self.owner = None
        self.currentOwner = None
        self.options = []
        self.location = None

    def setOwner(self, owner):
        self.owner = owner
        self.currentOwner = self.owner
