__author__ = 'matthewgarden'

import requests
import logging
from bs4 import BeautifulSoup
from review import Review


class Pitchfork:
	"""
	Parser for pitchfork.com album reviews
	"""

	def __init__(self, url='http://feeds2.feedburner.com/PitchforkAlbumReviews'):
		"""Pitchfork RSS reader. Use a custom url for testing."""
		self.url = url

	def reviews(self):
		"""Yields each review currently in the RSS feed.
		"""
		rss_req = requests.get(self.url)
		if rss_req.status_code != 200:
			logging.error('Failed to get RSS feed from "%s" with status %s' % (self.url, rss_req.status_code))

		for item in BeautifulSoup(rss_req.text).find_all('item'):
			try:
				artist, album = [s.strip() for s in item.find('title').string.split(':')]
			except ValueError:
				logging.error('Failed to unpack review title: "%s"' % item.find('title').string)
				continue

			link = item.find('feedburner:origlink').string.strip()
			desc = item.find('description').string.strip()

			yield Review(artist, album, link, desc, 1.0)
