from collections import OrderedDict, defaultdict
from django.db.models import signals
from django.core.cache import cache
from django.utils import timezone
from mainframe import settings
from django.db import models
from functools import reduce
import pytz
from . import handicap
#from .resources import FullNameResource

#to set a date for an event
#current_tz = timezone.activate(pytz.timezone(settings.TIME_ZONE))
#def normalise(date):
#    return current_tz.normalize(date)
date_format = '%m/%d/%Y'

class Team(models.Model):
    """
    A model for a Team in a League. 
    Links to players and and scoring to determine standings in a League.
    """
    team = models.CharField(max_length=150, default='', primary_key=True, blank=False)
    points = models.IntegerField(blank=True, default=0)

    def __str__(self):
        return "%s %s" %  (self.team, self.points)


class Player(models.Model):
    """
    A model for a Human player.
    """ 
    full_name = models.CharField(max_length=100, default='',unique=True)
    team_name = models.ForeignKey(Team,on_delete=models.SET_DEFAULT,to_field='team',default='',)
    #email_address = models.EmailField(blank=True, null=True)
    #phone_number = models.CharField(max_length=50, blank=True, null=True)
    initial_handicap = models.FloatField(blank=True, null=True, default=None)
    #jon added: 
    handicap = models.IntegerField(default=0, blank=True, null=True)


#    @property
 #   def full_name(self):
  #      return "%s %s" % (self.first_name, self.last_name)

   # @property
    #def name(self):
     #   return self.full_name

    #@property
    #def last_name_initial(self):
     #   return self.last_name[0]

   # @property
   # def shortest_name(self):
        
        #Returns first name if unique, else first_name + last_name_initial if unique,
        #else first_name + last name
        
    #    same_first_names = Player.objects.filter(first_name__iexact=self.first_name)
     #   if len(same_first_names) == 1:
      #      return self.first_name
       # else:
        #    same_last_name_initial = defaultdict(int)
         #   for player in same_first_names:
          #      same_last_name_initial[player.last_name_initial] += 1
           # if same_last_name_initial[self.last_name_initial] == 1:
            #    return "%s %s" % (self.first_name, self.last_name_initial)
        #return self.full_name
    
    def __str__(self):
       return "(%s) - %s - Team: %s" % (self.league_set.all() and self.league_set.get() or "None", self.full_name, self.team_name)

#class Handicap(models.Model):
    """
    A model for storing handicaps by player.
    """ 


#class Contestant(models.Model):
    """
    A model for a Contestant in a League. 
    Links to a player and and adds an optional initial handicap which will be used in the related League of which a Player is a member.
    This design allows for separate Handicap tracking per league for players.
    """
    #player = models.ForeignKey(Player,on_delete=models.CASCADE,)
    #initial_handicap = models.FloatField(blank=True, null=True, default=None)
    

#    def __str__(self):
#        return "(%s) %s" % (self.league_set.all() and self.league_set.get() or "None", self.player.full_name)


#class Hole(models.Model):
 #   number = models.IntegerField()
  #  par = models.IntegerField(default=3)
   # length = models.IntegerField(blank=True, null=True)
    #notes = models.TextField(blank=True, null=True)

    #def __str__(self):
     #   return "Hole %s (Par %s)%s" % (self.number, self.par, self.layout_set.all() and " - %s" % self.layout_set.filter() or "")


#class Layout(models.Model):
 #   name = models.CharField(max_length=50)
  #  holes = models.ManyToManyField(Hole)

   # @property
    #def par(self):
     #   return sum([h.par for h in self.holes.all()])

#    def __str__(self):
 #       return "%s (Par %s)" % (self.name, self.par)

  #  @property
   # def hole_count(self):
    #    return self.holes.count()


#class Course(models.Model):
 #   name = models.CharField(max_length=50, null=True,default="")
    #layouts = models.ManyToManyField(Layout)

  #  def __str__(self):
   #     return self.name


class Score(models.Model):
    """
    Model for overall scratch score for a player on a card after their round
    """
    contestant = models.OneToOneField(Player,on_delete=models.CASCADE, to_field='full_name', default='')
    strokes = models.IntegerField(blank=True, null=True)
    date = models.DateField()

    def __str__(self):
        return "%s - %s - %s" % (self.strokes or "DNF", self.date.strftime(date_format), self.contestant.full_name)


class Card(models.Model):
    """
    Model for card to be added to an event
    """
    #course = models.ForeignKey(Course,null=True,default="",on_delete=models.CASCADE,)
    #layout = models.ForeignKey(Layout,on_delete=models.CASCADE,)
    date = models.DateField()
    scores = models.ManyToManyField(Score, blank=True)

    @property
    def players(self, render=True):
        """
        Returns a list of Players who are competing on this card
        Returns a string if render=True, else a list of Player objects.
        """
        result = [s.contestant.full_name for s in self.scores.all()]
        if render:
            return ", ".join(result)
        return result

    def __str__(self):
        return "%s (%s)" % (self.date, self.players)

    def render_date(self):
        return self.date.strftime(date_format)

    @property
    def result(self):
        result = OrderedDict()
        for score in self.scores.all():
            contestant = score.contestant
            scratch_score = score.strokes
            result[contestant] = {}
            if scratch_score == None:
                result[contestant]["scratch_score"] = "DNF"
                result[contestant]["scratch_delta"] = "-"
            else:
                scratch_delta = scratch_score - 36  #self.layout.par
                result[contestant]["scratch_score"] = scratch_score
                result[contestant]["scratch_delta"] = str(scratch_delta) if scratch_delta < 1 else "+%s" % scratch_delta
        # sort by rank
        result = OrderedDict(sorted(iter(result.items()), key=lambda x: x[1]["scratch_score"]))
        return result

    def completed(self, contestant):
        if contestant not in [s.contestant for s in self.scores.all()]:
            return None
        dnf_contestants = [s.contestant for s in self.scores.filter(strokes=None)]
        if contestant in dnf_contestants:
            return False
        return True


class Award(models.Model):
    """
    Generic award model, eg. Closest to Pin
    """
    name = models.CharField(max_length=50, blank=True, null=True)
    contestant = models.ForeignKey(Player,on_delete=models.CASCADE)

    def __str__(self):
        return "%s: %s" % (self.name, self.contestant.full_name)


class Event(models.Model):
    """
    Generic event model, eg. a league day
    """
    name = models.CharField(max_length=50, blank=True, null=True, help_text="Name of event, e.g. 'Week 1 - March 31'")
    date = models.DateField()
    rounds = models.IntegerField(help_text="Number of rounds that players are required to complete during this league event",default=1)
    awards = models.ManyToManyField(Award, blank=True)
    cards = models.ManyToManyField(Card, blank=True)

    def get_latest_cards(self, contestant, n=1):
        """
        returns up to n latest score cards for contestant, sorted 
        """
        result = []
        all_events = self.league_set.get().events.filter(date__lte=self.date)
        for event in all_events:
            cards = event.cards.all()
            for card in cards:
                if card.scores.filter(contestant=contestant):
                    if card.completed(contestant):
                        # this card counts
                        result.append(card)
        result = sorted(result, key=lambda x: x.date, reverse=True)[:n]
        result = [int(c.result[contestant]['scratch_delta']) for c in result]
        result = sorted(result)
        return result

    @property
    def render_date(self):
        return self.date.strftime(date_format)

    
    @staticmethod
    def get_previous_handicap(event, contestant):
        try:
            previous_event = event.get_previous_by_date()
        except event.DoesNotExist:
            return contestant.initial_handicap
        try:
            return previous_event.get_result(for_contestant=contestant)[contestant]['handicap']
        except KeyError:
            # contestant did not compete in previous event, check the next previous
            return Event.get_previous_handicap(previous_event, contestant)

    @property
    def result(self):
        return self.get_result()

    def get_result(self, for_contestant=None):
        """
        Returns a per-player results dict including points earned by contestants during this event, ordered by rank.
        Returns result for specified for_contestant or all if None.
        """
        league = self.league_set.get()
        event_result = {}
        for card in self.cards.all():
            card_result = card.result
            for contestant in card_result:
                if for_contestant and contestant != for_contestant:
                    continue
                if not contestant in event_result:
                    event_result[contestant] = defaultdict(int)
                event_result[contestant]['awards'] = [a.name for a in self.awards.filter(contestant=contestant)]
                if card.completed(contestant):
                    event_result[contestant]['round_count'] += 1
                event_result[contestant]['completed_event'] = event_result[contestant]['round_count'] >= self.rounds 
                # only count a scratch score if the contestant has not exceeded the max number of rounds required in this event.
                if event_result[contestant]['round_count'] <= self.rounds and card_result[contestant]['scratch_score'] != "DNF":
                    event_result[contestant]['scratch_score'] += card_result[contestant]['scratch_score']
        for contestant in event_result:
            # calculate handicap score
            previous_handicap = Event.get_previous_handicap(self, contestant)
            if previous_handicap == None:
                event_result[contestant]['previous_handicap'] = None
                event_result[contestant]['handicap_score'] = None
            else:
                event_result[contestant]['previous_handicap'] = previous_handicap
                event_result[contestant]['handicap_score'] = int(event_result[contestant]['scratch_score'] - \
                        (round(previous_handicap) * event_result[contestant]['round_count']))
            # calculate new handicap
            latest_n_results = self.get_latest_cards(contestant, league.handicap_max_rounds_avg)
            # calculate average:
            best_scratch_deltas = latest_n_results[:league.handicap_min_rounds_avg]
            if not best_scratch_deltas:
                event_result[contestant]['handicap'] = previous_handicap
            else:
                handicap = reduce(lambda x, y: float(x) + float(y), best_scratch_deltas) / len(best_scratch_deltas)
                # round to 2 decimal places
                handicap = round(handicap * league.handicap_multiplier, 2)
                event_result[contestant]['handicap'] = handicap
                # inject the handicap into the contestant's initial handicap value if they played the required number of rounds
                total_rounds = sum([sum([c.scores.filter(contestant=contestant).count() for c in e.cards.all()]) for e in self.league_set.last().events.all()])
                if contestant.initial_handicap == None and total_rounds == league.handicap_min_rounds:
                    contestant.initial_handicap = handicap
                    contestant.save()

        # sort event_result by players who completed all required rounds, then by handicap score, then by scratch score
        # group first
        result = {}
        incomplete_result = {}
        no_hc_result = {}
        # sort groups
        for contestant in event_result:
            if event_result[contestant]["handicap_score"] == None:
                no_hc_result[contestant] = event_result[contestant]
            elif not event_result[contestant]['completed_event']:
                incomplete_result[contestant] = event_result[contestant]
            else:
                result[contestant] = event_result[contestant]
        result = OrderedDict(sorted(iter(result.items()), key=lambda x: x[1]["handicap_score"]))
        incomplete_result = OrderedDict(sorted(iter(incomplete_result.items()), key=lambda x: (-x[1]["round_count"], x[1]["handicap_score"])))
        no_hc_result = OrderedDict(sorted(iter(no_hc_result.items()), key=lambda x: x[1]["scratch_score"]))
        # aggregate into a single result dict
        incomplete_result.update(no_hc_result)
        result.update(incomplete_result)
        event_result = result
        # add rank data
        rank = 0
        for contestant in event_result:
            index = list(event_result.keys()).index(contestant)
            if index > 0 and (event_result[list(event_result.keys())[index - 1]]['handicap_score'] != (event_result[contestant]['handicap_score'] or 0)):
                rank = index
            event_result[contestant]['rank'] = rank + 1
        # assign points earned
        #for contestant in event_result:
         #   if event_result[contestant]['handicap_score'] == None:
          #      event_result[contestant]['points_earned'] = None
           # elif event_result[contestant]['round_count'] < self.rounds:
                # player completed less than the required rounds, assign minimum possible points. 
            #    event_result[contestant]['points_earned'] = self.get_points(-1)
            #else:
             #   event_result[contestant]['points_earned'] = self.get_points(event_result[contestant]["rank"] - 1)
        return event_result

    def __str__(self):
        name = self.name or "Event"
        return "%s - %s" % (name, self.date.strftime(date_format))


class League(models.Model):
    name = models.CharField(max_length=50)
    contestants = models.ManyToManyField(Player, blank=True)
    events = models.ManyToManyField(Event, blank=True)
    league_points = models.CharField(verbose_name="League Points Assignment", max_length=50, default="10,9,8,7,6,5,4,3,2,1", help_text="""
Points assignments for league event ranking (based on HC adjusted total score).
Index of list is rank, value is points earned. Last element of list is used as the
minimum attainable points for a contestant who does not complete a league event, or
who does not yet have enough rounds recorded in league to calculate a HC. Must be a comma separated list of integers.
            """)
    handicap_multiplier = models.FloatField(default=0.8, help_text="""
A value that is multiplied against a contestant's raw HC delta average. The result of this calculation becomes the contestant's current HC.""")
    handicap_min_rounds = models.IntegerField(verbose_name="Min rounds for HC", default=2, help_text="""
The minimum number of rounds required before a HC is evaluated for a contestant if they
do not have an initial HC. The contestant will still earn min attainable points for
the league attendance even without an initial HC while they are accruing the requisite
number of rounds for a HC. Previous events will be retro-calculated using newly calculated
HC meaning points and ranks will move in retrospect when a contestant finally plays enough rounds to get a HC.
""")
    handicap_min_rounds_avg = models.IntegerField(verbose_name="Best Cards to use for HC", default=5, help_text="""
The max number of best score cards to use to calculate a player's current HC
""")
    handicap_max_rounds_avg = models.IntegerField(verbose_name="Max Cards to consider for HC", default=8, help_text="""
The number of past cards to consider when chosing the best cards for a player for their HC calculation. This value needs to be larger than the number of best cards used for HC calculation above.
""")

    def __str__(self):
        return "%s" % self.name

    #def get_league_points(self):
     #   return [int(p.strip()) for p in self.league_points.split(',')]

    @property
    def result(self):
        standings = OrderedDict()
        for event in self.events.all():
            result = event.result
            for contestant in result:
                player = contestant.full_name
                if not player in standings:
                    standings[player] = defaultdict(int)
                standings[player]['initial_handicap'] = contestant.initial_handicap
                #standings[player]['points'] += result[contestant]['points_earned'] or 0
                standings[player]['handicap'] = result[contestant]['handicap']
                standings[player]['events_attended'] += 1 
                standings[player]['rounds_played'] += sum([c.scores.filter(contestant=contestant).count() for c in event.cards.all()])
        # flag playeres who have not completed enough rounds to be ranked
        for player in standings:
            if standings[player]['initial_handicap'] == None and standings[player]['rounds_played'] < self.handicap_min_rounds:
                standings[player]['valid_hc'] = False
            else:
                standings[player]['valid_hc'] = True

        # add rank data
        #standings = OrderedDict(sorted(iter(standings.items()), key=lambda x: x[1]['points'], reverse=True))
        rank = 0
        for player in standings:
            index = list(standings.keys()).index(player)
            if index > 0 and (standings[list(standings.keys())[index - 1]]['points'] != standings[player]['points']):
                rank = index
            standings[player]['rank'] = rank + 1
        # sort by rank
        standings = OrderedDict(sorted(iter(standings.items()), key=lambda x: x[1]['rank']))
        return standings


def model_change_handler(sender, instance, **kwargs):
    # Model changed, invalidate cache. Next view will be a lengthy recalculation to re-populate our cache.
    cache.clear() 

signals.post_save.connect(model_change_handler)
signals.post_delete.connect(model_change_handler)