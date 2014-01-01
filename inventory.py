class item(object):
    def __init__(self, itemName, itemID):
        self.name = str(itemName)
        self.ID = itemID
        self.amount = 0


class slot(object):
    def __init__(self, pos, slotID):
        self.containsItem = False
        self.rect = pygame.rect(pos[0], pos[1], 32, 32)

        def assignItem(self, item):
            self.item = item
            self.containsItem = True