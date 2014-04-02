__author__ = 'matthewgarden'

import datetime
import re
from reviewsite import ReviewSite
from reviewparser import ReviewParser
from wordof.models import Critic, Category


class Pitchfork:
    """
    Parser for pitchfork.com album reviews
    """

    def __init__(self, ignore_before=datetime.date.min):
        """
        Pitchfork RSS reader. Use a custom url for testing.

        :param ignore_before: Only reviews published on or after this date will be handled.
        :type ignore_before: datetime.date
        """
        title_re = re.compile('(?P<artist>.+): (?P<album>.+)')
        parser = ReviewParser(title_re, 10, 'score', 'link', '%a, %d %b %Y %H:%M:%S')

        self.feeds = {}

        p = Critic.objects.get(name='Pitchfork')
        for category in p.category_set.all():
            self.feeds[category.name] = ReviewSite(category, parser, ignore_before)
