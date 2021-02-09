#player class
from django import models

class Player(models.Model):
	"""docstring for Player"""
	def __init__(self):
		self.name = name
        self.handicap = handicap
        self.team = team
    
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email_address = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=50, blank=True, null=True)
    pdga_number = models.IntegerField(blank=True, null=True)
    
    def __str__(self):
    	return f' {self.name} handicap is {self.handicap}.'
		









#Copied from dgscored/dgs/models.py 
#class Player(models.Model):
#    """
 #   A model for a Human League player.
    """
    def __init__(self,handicap):
        

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email_address = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=50, blank=True, null=True)
    pdga_number = models.IntegerField(blank=True, null=True)

    
    def __str__(self):
        return f'Player {self.name} handicap is {int(self.handicap)}.'

   