from django.views.decorators.cache import cache_page
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.shortcuts import render
from rest_framework import viewsets
from .cache import cache_per
from tleague.api.serializers import *
from tleague import models
from .models import Player, Player
from django.db.models import Q
#from .filters import PlayerFilter
#from django.views.generic import FormView, ListView
#from .forms import SearchForm


##### App Views ####


@cache_per(None, username="all")
def tleague(request):
    return render(request,'index.html')

@cache_per(None, username="all")
def standings(request):
    teams = models.Team.objects.all()
    return render(request, 'standings.html', {"teams":teams})

@cache_per(None, username="all")
def scores(request):
    context = {
           'leagues': models.League.objects.all()
          }
    return render(request, 'scores.html', context)

#@cache_per(None, username="all")
def handicaps(request):
    search_post = request.GET.get('search')
    if search_post:
        handicaps = Player.objects.filter(Q(full_name__icontains=search_post))
    else:
        # If not searched, return default posts
        handicaps = Player.objects.all()

    #Filtering
    #myFilter = PlayerFilter(request.GET, queryset=handicaps)
    #handicaps=myFilter.qs


    return render(request, 'handicaps.html', {"handicaps":handicaps})



##### API Views ####

class PlayerViewSet(viewsets.ModelViewSet):
    """
    A model for a player. Create one instance per human.
    """
    queryset = models.Player.objects.all()
    serializer_class = PlayerSerializer

class TeamViewSet(viewsets.ModelViewSet):
    """
    A model for a player. Create one instance per human.
    """
    queryset = models.Team.objects.all()
    serializer_class = TeamSerializer

#class ContestantViewSet(viewsets.ModelViewSet):
    """
    A model for a contestant in a League. Extends a Player by adding an optional initial handicap for them.
    A League object relates to several Contestant objects. If initial HC is not specified, then it will be
    automatically calculated by default to be: 0.8 * avg(scratch delta of first two rounds played).
    """
#    queryset = models.Contestant.objects.all()
#    serializer_class = ContestantSerializer


#class HoleViewSet(viewsets.ModelViewSet):
    """
    A simple model to represent a hole.
    """
    #queryset = models.Hole.objects.all()
   # serializer_class = HoleSerializer


#class LayoutViewSet(viewsets.ModelViewSet):
    """
    A model to represent a Layout of a series of Hole objects.
    Courses relate to one or more Layouts.
    """
 #   queryset = models.Layout.objects.all()
  #  serializer_class = LayoutSerializer


#class CourseViewSet(viewsets.ModelViewSet):
    """
    A model to represent a DG course that can contain one or more Layouts.
    """
 #   queryset = models.Course.objects.all()
  #  serializer_class = CourseSerializer

class PlayerViewSet(viewsets.ModelViewSet):
    """
    A simple view that stores the scratch score of a Contestant after a round. Cards relate to
    one Score per player on a Card.
    """
    queryset = models.Player.objects.all()
    serializer_class = PlayerSerializer


class ScoreViewSet(viewsets.ModelViewSet):
    """
    A simple view that stores the scratch score of a Contestant after a round. Cards relate to
    one Score per player on a Card.
    """
    queryset = models.Score.objects.all()
    serializer_class = ScoreSerializer


class CardViewSet(viewsets.ModelViewSet):
    """
    A model for a Card that stores Course, Layout and one or more Scores.
    """
    queryset = models.Card.objects.all()
    serializer_class = CardSerializer


class AwardViewSet(viewsets.ModelViewSet):
    """
    A generic Award model to capture awards for a Contestant such as Ace (hole in one)
    or CTP (closest to pin). Event objects relate to one or more Awards.
    """
    queryset = models.Award.objects.all()
    serializer_class = AwardSerializer


class EventViewSet(viewsets.ModelViewSet):
    """
    A model to store a league day or a similar event. Records the requisite number of rounds a
    Contestant is required to play during the event as well as Awards and Cards created during the
    Event.
    """
    queryset = models.Event.objects.all()
    serializer_class = EventSerializer


class LeagueViewSet(viewsets.ModelViewSet):
    """
    A model to represent a League. Stores all Events and Contestants associated with it.
    """
    queryset = models.League.objects.all()
    serializer_class = LeagueSerializer
