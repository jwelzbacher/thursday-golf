from django.views.generic.base import RedirectView
from django.conf.urls import include, url
from rest_framework import routers
from django.contrib import admin
from django.urls import path
from . import views



admin.autodiscover()

router = routers.DefaultRouter()
router.register(r'api/player', views.PlayerViewSet)
router.register(r'api/team', views.TeamViewSet)
#router.register(r'api/contestant', views.ContestantViewSet)
#router.register(r'api/hole', views.HoleViewSet)
#router.register(r'api/layout', views.LayoutViewSet)
#router.register(r'api/course', views.CourseViewSet)
router.register(r'api/score', views.ScoreViewSet)
router.register(r'api/card', views.CardViewSet)
router.register(r'api/award', views.AwardViewSet)
router.register(r'api/event', views.EventViewSet)
router.register(r'api/league', views.LeagueViewSet)
#router.register(r'api/handicaps', views.HandicapViewSet)

urlpatterns = [

#Home
	path('', views.tleague, name='tleague'),
    path('', include('gsheets.urls')),
    #path('standings/', views.standings, name='standings'),


#Rest Framework    
    url(r'^favicon\.ico$', RedirectView.as_view(permanent=False, url='/static/favicon.ico')),
    #url(r'^admin/', admin.site.urls),
    #url(r'^$', views.tleague, name='tleague'),
    url(r'^standings/', views.standings, name='standings'),
    url(r'^handicaps/', views.handicaps, name='handicaps'),
    url(r'^scores/', views.scores, name='scores'),
    url(r'^api/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/$', router.get_api_root_view()),
    #url(r'^api/docs/', include('rest_framework_swagger.urls')),
    url(r'^', include(router.urls)),
    
]
