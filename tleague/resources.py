from import_export import fields, resources
from import_export.widgets import ForeignKeyWidget
from .models import *

#Team Name resource for Team class to set import ID to team
class TeamIdResource(resources.ModelResource):

    class Meta:
        model = Team
        exclude = ('id',)
        import_id_fields = ['team']
        #fields = ('id','team','points')



#team resource for import/export to the Players
class PlayerTeamResource(resources.ModelResource):
    team_name = fields.Field(
        column_name='team_name',
        attribute='team_name',
        widget=ForeignKeyWidget(Team, 'team')
        )
    class Meta:
        model = Player
        exclude = ('id',)
        import_id_fields = ['full_name']
        fields = ('id','team_name__team','full_name','initial_handicap','handicap')


#Score model resource for import/export to the Players full_name
class ScoreFullName(resources.ModelResource):

    class Meta:
      model = Score
      exclude = ('id',) 
      import_id_fields = ['contestant']
