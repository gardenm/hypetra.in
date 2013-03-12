__author__ = 'matthewgarden'

import datetime
import requests
import logging
import re
from bs4 import BeautifulSoup
from reviewparser import ReviewParser


class Pitchfork:
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
		self.url = url
		self.parser = ReviewParser(re.compile('(?P<artist>.+): (?P<album>.+)'), 10, 'score', 'feedburner:origlink')
		self.ignore_before = ignore_before

	@property
	def reviews(self):
		"""
		Yields each review currently in the RSS feed.
		"""
		rss_req = requests.get(self.url)
		if rss_req.status_code != 200:
			logging.error('Failed to get RSS feed from "%s" with status %s' % (self.url, rss_req.status_code))
			return

		for item in BeautifulSoup(rss_req.text).find_all('item')[0:3]:
			review = self.parser.parse(item, self.ignore_before)
			if review:
				yield review