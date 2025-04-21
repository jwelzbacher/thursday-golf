from rest_framework import serializers
from tleague import models


class TeamSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Team
        #fields = ('first_name', 'last_name', 'email_address', 'phone_number', 'handicap_number')
        fields = ('team', 'points')


class PlayerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Player
        fields = '__all__'

#class HandicapSerializer(serializers.HyperlinkedModelSerializer):
 #   class Meta:
  #      model = models.Handicap
   #         fields = '__all__'
#class ContestantSerializer(serializers.HyperlinkedModelSerializer):
#    class Meta:
#        model = models.Contestant
#        fields = ('player', 'initial_handicap')


#class HoleSerializer(serializers.HyperlinkedModelSerializer):
 #   class Meta:
  #      model = models.Hole
   #     fields = ('number', 'par')


#class LayoutSerializer(serializers.HyperlinkedModelSerializer):
 #   class Meta:
  #      model = models.Layout
   #     fields = ('name', 'holes')


#class CourseSerializer(serializers.HyperlinkedModelSerializer):
 #   class Meta:
  #      model = models.Course
   #     fields = ('name', 'layouts')


class ScoreSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Score
        fields = ('contestant', 'strokes', 'date')


class CardSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Card
        fields = ('date', 'scores')


class AwardSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Award
        fields = ('name', 'contestant')


class EventSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Event
        fields = ('name', 'date', 'rounds', 'awards', 'cards')


class LeagueSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.League
        fields = '__all__'