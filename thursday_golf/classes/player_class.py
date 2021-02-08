#player class

class Player:
    
    def __init__(self,handicap):
        
        self.name = name
        self.handicap = []
        
    def remove_one(self):
        return self.all_cards.pop(0)
    
    #def add_cards(self, new_cards):
    	self.all_cards.append(new_cards)
    
    def __str__(self):
        return f'Player {self.name} handicap is {int(self.handicap)}.'

   