__author__ = 'matthewgarden'


class Review:
	"""Class to represent an album review.
	"""

	def __init__(self, artist, album, link, description, score):
		"""
		"""
		self.artist = artist
		self.album = album
		self.link = link
		self.description = description
		self.score = score

	def __str__(self):
		return '%s by %s: %0.2f' % (self.artist, self.album, self.score)