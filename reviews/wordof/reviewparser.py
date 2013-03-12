__author__ = 'matthewgarden'

import datetime
import logging
import requests
from review import Review
from bs4 import BeautifulSoup


class ReviewParser:
	"""
	Class to parse an album review from an RSS feed's DOM.

	:param title_re: Regular expression object that can be used to get the artist and album from the RSS item's title.
	:param max_score: The maximum score the review site awards.
	:param score_class: The CSS class assigned to scores on a review page for the review site.
	:param orig_link_tag: The tag used in the RSS DOM for the original link (to the review on the site).
	:param pubdate_format: datetime.datetime.strptime format string for the pubdates used by the RSS feed.
	:param logger: Object to use to log errors and warnings. By default the logging library. Override to test error handling.
	"""
	def __init__(self, title_re, max_score, score_class, orig_link_tag, pubdate_format, logger=logging):
		self.title_re = title_re
		self.max_score = max_score
		self.score_class = score_class
		self.orig_link_tag = orig_link_tag
		self.pubdate_format = pubdate_format
		self.logger = logger

	def remove_utc(self, date_str):
		"""
		Remove the +0000 style UTC timezone specifier, since python's strptime doesn't support %z
		:param date_str: A date string.
		"""
		last_minus = date_str.rfind('-')
		last_plus = date_str.rfind('+')

		if last_minus != -1:
			return date_str[0:last_minus]
		elif last_plus != -1:
			return date_str[0:last_plus]

		# if the string doesn't contain the problematic substring then don't worry about it.
		return date_str

	def parse(self, item, ignore_before=datetime.date.min):
		"""
		Gather all information from a review entry in the RSS feed and return the corresponding Review object.
		Returns None if the parse fails for any reason (reason will be logged).

		:param item: should be a BeautifulSoup object representing an item from the RSS feed.
		:type item: BeautifulSoup

		:param ignore_before: Ignore any reviews that were published before this date.
		:type ignore_before: datetime.date
		"""
		pubdate_raw = self.remove_utc(item.find('pubdate').string).strip()

		try:
			pubdate = datetime.datetime.strptime(pubdate_raw, self.pubdate_format)
		except ValueError:
			self.logger.error('Failed to parse pubdate "%s" using format "%s"' % (pubdate_raw, self.pubdate_format))
			return None

		if pubdate.date() <= ignore_before:
			return None

		title_match = self.title_re.match(item.find('title').string.strip())

		if not title_match:
			self.logger.error('Failed to unpack review title "%s"' % item.find('title').string)
			return None

		artist = title_match.group('artist')
		album = title_match.group('album')

		link = item.find(self.orig_link_tag).string.strip()
		desc = item.find('description').text.strip()

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