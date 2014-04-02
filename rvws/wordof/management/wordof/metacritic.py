__author__ = 'matthewgarden'

import datetime
import re
from reviewsite import ReviewSite
from reviewparser import ReviewParser
from wordof.models import Critic


class Metacritic:
    """
    Parser for metacritic.com album reviews
    """

    def __init__(self, ignore_before=datetime.date.min):
        """
        Metacritic RSS reader. Use a custom url for testing.

        :param ignore_before: Only reviews published on or after this date will be handled.
        :type ignore_before: datetime.date
        """
        parser = ReviewParser(re.compile('(?P<album>.+) by (?P<artist>.+)'), 100, 'score_value', 'link', '%b %d, %Y')

        self.feeds = {}

        m = Critic.objects.get(name='Metacritic')
        for category in m.category_set.all():
            self.feeds[category.name] = ReviewSite(category, parser, ignore_before)