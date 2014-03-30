__author__ = 'matthewgarden'

import logging
import requests
from bs4 import BeautifulSoup
from wordof import models


class ReviewSite:
	"""
	Class to represent a music review site.
	"""

	def __init__(self, source, parser, ignore_before, logger=logging):
		"""
		:param url: URL for the site's RSS feed.

		:param parser: Object to parse individual reviews.
		:type parser: ReviewParser

		:param logger: Object to log errors and warnings. By default the logging library. Override for testing.
		"""
		self.source = source
		self.parser = parser
		self.ignore_before = ignore_before
		self.logger = logger

	@property
	def reviews(self):
		"""
		Yields each review currently in the site's RSS feed.
		"""
		rss_req = requests.get(self.source.feed)
		if rss_req.status_code != 200:
			self.logger.error('Failed to get RSS feed from "%s" with status %s' % (self.source.feed, rss_req.status_code))
			return

		for item in BeautifulSoup(rss_req.text).find_all('item'):
			raw = self.parser.parse(item, self.ignore_before)
			if raw:
				artist, created = models.Artist.objects.get_or_create(name=raw.artist)
				artifact, created  = models.Artifact.objects.get_or_create(artist=artist, title=raw.album)
				review, created = models.Review.objects.get_or_create(artifact=artifact, source=self.source,  defaults={'url': raw.link, 'description': raw.description, 'score':raw.score, 'pub_date': raw.pub_date})
				yield review
