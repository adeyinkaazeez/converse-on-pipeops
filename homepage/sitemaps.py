from newss.models import Political
from business.models import Business
from crimes.models import Crimes
from entertainments.models import Entertainments
from internationals.models import Internationals
from educations.models import Educations
from sciences.models import Science_AND_Techs
from sports.models import Sports
from health_articles.models import Healths
from political_articles.models import Political_Articless
from happening.models import Happenings
from innovations.models import Innovative_Articles
from lifestyles.models import Lifestyle_Articles
from religions.models import Religion_Articles
from sport_articles.models import Sport_Articles
from cultures.models import Cultures
from foods.models import Foods
from business__articles.models import Business_Articles
from howtos.models import Howtos
from celeb.models import Celeb
from loves.models import Loves
from campuss.models import Campuss
from personalitys.models import Personalities
from events.models import Events
from queryset_sequence import QuerySetSequence
from django.contrib.sitemaps import Sitemap

class PostSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        all_queryset = QuerySetSequence(Crimes.published.all(), Business.published.all(),
                                         Political.published.all(), Entertainments.published.all(),
                                         Internationals.published.all(),Educations.published.all(),
                                         Science_AND_Techs.published.all(), Sports.published.all(),
                                         Healths.published.all(), Political_Articless.published.all(),
                                         Happenings.published.all(), Innovative_Articles.published.all(),
                                         Lifestyle_Articles.published.all(), Religion_Articles.published.all(),
                                         Sport_Articles.published.all(), Cultures.published.all(),
                                         Foods.published.all(), Business_Articles.published.all(),
                                         Howtos.published.all(), Celeb.published.all(),
                                         Loves.published.all(), Campuss.published.all(),
                                         Personalities.published.all(), Events.published.all() )
        return all_queryset
def lastmod(self, obj):
    return obj.updated