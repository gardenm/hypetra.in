__author__ = 'matthewgarden'

import datetime
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

	def parse_review(self, item, ignore_before=datetime.date.min):
		"""
		Gather all information from a review entry in the RSS feed and return the corresponding Review object.
		Returns None if the parse fails for any reason (reason will be logged).

		:param item: should be a BeautifulSoup object representing an item from the RSS feed.
		:type item: BeautifulSoup

		:param ignore_before: Ignore any reviews that were published before this date.
		:type ignore_before: datetime.date
		"""
		pubdate_raw = item.find('pubdate').string.strip()
		pubdate = datetime.datetime.strptime(pubdate_raw, '%a, %d %b %Y %H:%M:%S -0500')

		if pubdate.date() <= ignore_before:
			return None

		try:
			artist, album = [s.strip() for s in item.find('title').string.split(':')]
		except ValueError:
			logging.error('Failed to unpack review title: "%s"' % item.find('title').string)
			return None

		link = item.find('feedburner:origlink').string.strip()
		desc = item.find('description').string.strip()

		item_req = requests.get(link)
		if item_req.status_code != 200:
			logging.error('Failed to get review at %s with status %s' % (link, item_req.status_code))
			return None

		item_html = BeautifulSoup(item_req.text)
		score_raw = item_html.find('span', {'class': 'score'}).string.strip()
		try:
			score = float(score_raw) / 10
		except ValueError:
			logging.error('Failed to parse score "%s" at %s' % (score_raw, link))
			return None

		return Review(artist, album, link, desc, score)

	def reviews(self, **kwargs):
		"""
		Yields each review currently in the RSS feed.

		:param kwargs: Caller may specify 'after', a dict with 'year', 'month', and 'day'. If present, only reviews published
			after this date will be returned.
		"""
		rss_req = requests.get(self.url)
		if rss_req.status_code != 200:
			logging.error('Failed to get RSS feed from "%s" with status %s' % (self.url, rss_req.status_code))
			return

		after = datetime.date.min
		if kwargs.has_key('after'):
			after = datetime.date(kwargs['after']['year'], kwargs['after']['month'], kwargs['after']['day'])

		for item in BeautifulSoup(rss_req.text).find_all('item')[0:3]:
			review = self.parse_review(item, after)
			if review:
				yield review