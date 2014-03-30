__author__ = 'matthewgarden'

import datetime
import re
from reviewsite import ReviewSite
from reviewparser import ReviewParser


class Metacritic(ReviewSite):
	"""
	Parser for metacritic.com album reviews
	"""

	def __init__(self, url='http://www.metacritic.com/rss/music', ignore_before=datetime.date.min):
		"""
		Metacritic RSS reader. Use a custom url for testing.

		:param url: URL for the review RSS feed to be processed. Override this for testing.
		:type url: basestring

		:param ignore_before: Only reviews published on or after this date will be handled.
		:type ignore_before: datetime.date
		"""
		parser = ReviewParser(re.compile('(?P<album>.+) by (?P<artist>.+)'), 100, 'score_value', 'link', '%b %d, %Y')
		ReviewSite.__init__(self, url, parser, ignore_before)