
#from golfclapp app
#class Score(models.Model):
 #   round = models.ForeignKey('Round', on_delete=models.SET_NULL, null=True)
  #  hole = models.ForeignKey('Hole', on_delete=models.SET_NULL, null=True)
   # strokes = models.IntegerField(validators=[MaxValueValidator(100), MinValueValidator(1)])


 class Scores():
 	"""docstring for Scores - Taking in Scores for each player and round to calculate handicap"""
 	def __init__(self,golfround):
 		self.golfround = golfround

 		