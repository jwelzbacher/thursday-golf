#handicap stores the players handicap number as an integer (no floats)
class Handicap:
    #docstring for handicap
    def __init__(self, scores):
        print("A handicap is established")
        self.scores = scores
        self.handicap = 0
    
    def h_total(self):
        # initializing K  
        K = 5
        # Inverse K slice Sum 
        # using list slicing + sum() 
        res = sum(self.scores[-K:]) 
        #round the handicap
        self.handicap = round((res/5)-36)
        return self.handicap
        
        
    def __str__(self):
        return f'Player handicap is {self.handicap}'
        



