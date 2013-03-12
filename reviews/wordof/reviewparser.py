__author__ = 'matthewgarden'

import datetime
import logging
import requests
from review import Review
from bs4 import BeautifulSoup


class ReviewParser:
	"""
	Class to parse an album review from an RSS feed's DOM.

	:param title_separator: String that separates the artist and album in the review's title.
	:param max_score: The maximimum score the review site awards.
	:param score_class: The CSS class assigned to scores on a review page for the review site.
	:param orig_link_tag: The tag used in the RSS DOM for the original link (to the review on the site).
	:param logger: Object to use to log errors and warnings. By default the logging library. Override to test error handling.
	"""
	def __init__(self, title_separator, max_score, score_class, orig_link_tag, logger=logging):
		self.title_separator = title_separator
		self.max_score = max_score
		self.score_class = score_class
		self.orig_link_tag = orig_link_tag
		self.logger = logger

	def parse(self, item, ignore_before=datetime.date.min):
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
			artist, album = [s.strip() for s in item.find('title').string.split(self.title_separator)]
		except ValueError:
			self.logger.error('Failed to unpack review title: "%s"' % item.find('title').string)
			return None

		link = item.find(self.orig_link_tag).string.strip()
		desc = item.find('description').string.strip()

		item_req = requests.get(link)
		if item_req.status_code != 200:
			self.logger.error('Failed to get review at %s with status %s' % (link, item_req.status_code))
			return None

		item_html = BeautifulSoup(item_req.text)
		score_raw = item_html.find('span', {'class': self.score_class}).string.strip()
		try:
			score = float(score_raw) / self.max_score
		except ValueError:
			self.logger.error('Failed to parse score "%s" at %s' % (score_raw, link))
			return None

		return Review(artist, album, link, desc, score)