__author__ = 'matthewgarden'

import datetime
import re
from reviewsite import ReviewSite
from reviewparser import ReviewParser


class Pitchfork(ReviewSite):
	"""
	Parser for pitchfork.com album reviews
	"""

	def __init__(self, url='http://feeds2.feedburner.com/PitchforkAlbumReviews', ignore_before=datetime.date.min):
		"""
		Pitchfork RSS reader. Use a custom url for testing.

		:param url: URL for the pitchfork review RSS feed to be processed.
		:type url: basestring

		:param ignore_before: Only reviews published on or after this date will be handled.
		:type ignore_before: datetime.date
		"""
		title_re = re.compile('(?P<artist>.+): (?P<album>.+)')
		parser = ReviewParser(title_re, 10, 'score', 'feedburner:origlink', '%a, %d %b %Y %H:%M:%S')
		ReviewSite.__init__(self, url, parser, ignore_before)