__author__ = 'matthewgarden'

import logging
import requests
from bs4 import BeautifulSoup


class ReviewSite:
	"""
	Class to represent a music review site.
	"""

	def __init__(self, url, parser, ignore_before, logger=logging):
		"""
		:param url: URL for the site's RSS feed.
		:type url: basestring

		:param parser: Object to parse individual reviews.
		:type parser: ReviewParser

		:param logger: Object to log errors and warnings. By default the logging library. Override for testing.
		"""
		self.url = url
		self.parser = parser
		self.ignore_before = ignore_before
		self.logger = logger

	@property
	def reviews(self):
		"""
		Yields each review currently in the site's RSS feed.
		"""
		rss_req = requests.get(self.url)
		if rss_req.status_code != 200:
			self.logger.error('Failed to get RSS feed from "%s" with status %s' % (self.url, rss_req.status_code))
			return

		for item in BeautifulSoup(rss_req.text).find_all('item')[0:3]:
			review = self.parser.parse(item, self.ignore_before)
			if review:
				yield review