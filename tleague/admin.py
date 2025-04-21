from django.contrib.admin.widgets import FilteredSelectMultiple
from django.forms.widgets import Select
from django.contrib import admin
from django.db import models
from .models import *
#allows you to import/export data in the admin feature.
from import_export.admin import ImportExportModelAdmin
#creating widgets to be able to reference any field in the import or export of data instead of just the primary key

from import_export import fields, resources
from import_export.widgets import ForeignKeyWidget
from .resources import *

@admin.register(Player)
class TeamNameAdmin(ImportExportModelAdmin):
           resource_class = PlayerTeamResource
           list_display = 'id','full_name','team_name','initial_handicap', 'handicap'

@admin.register(Team)
class TeamAdmin(ImportExportModelAdmin):
           resource_class = TeamIdResource
           list_display = ('team','points')
#@admin.register(Handicap)
#class TeamAdmin(ImportExportModelAdmin):
 #          resource_class = HandicapPlayer
  #         list_display = ('player','handicap')

@admin.register(League)
@admin.register(Card)
#@admin.register(Course)
@admin.register(Event)
#@admin.register(Layout)
#@admin.register(Contestant)
#@admin.register(Hole)
@admin.register(Award)
@admin.register(Score)
class ScoreAdmin(ImportExportModelAdmin):
    resource_class = ScoreFullName
    #list_display = ("contestant", "strokes", "date")


class ModelAdmin(ImportExportModelAdmin):
    formfield_overrides = {
        models.ManyToManyField: {'widget': FilteredSelectMultiple( "items", False)},
        models.ForeignKey: {'widget': Select(attrs={"class": "form-control selectpicker", "data-live-search": "true"})},
        #models.ForeignKey: {'widget': Select(attrs={"class": "form-control"})},
        }

    class Media:
        #extend = False
        css = {'all': ('https://cdnjs.cloudflare.com/ajax/libs/bootstrap-select/1.9.4/css/bootstrap-select.min.css',)}
        js = ('https://cdnjs.cloudflare.com/ajax/libs/bootstrap-select/1.9.4/js/bootstrap-select.min.js',)


