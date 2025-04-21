import django_filters

from .models import *

from django_filters import filters,CharFilter, ModelChoiceFilter


def players(request):
    if request is None:
        return Player.objects.none()

    player = request.handicap.player
    return player.handicap_set.all()

class PlayerFilter(django_filters.FilterSet):
	"""To filter backend data in a form in the HTML table for Players model"""

	
	player = filters.ModelChoiceFilter(queryset=players)
	#(field_name="player", lookup_expr='icontains')

	class Meta:
		model = Player
		fields = "__all__"
		exclude = ["handicap","player"]