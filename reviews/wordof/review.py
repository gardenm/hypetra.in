__author__ = 'matthewgarden'


class Review:
	"""Class to represent an album review.
	"""

	def __init__(self, artist, album, link, description, score):
		"""
		"""
		self.artist = artist.encode('utf-8')
		self.album = album.encode('utf-8')
		self.link = link.encode('utf-8')
		self.description = description.encode('utf-8')
		self.score = score

	def __str__(self):
		return '%s by %s: %0.2f' % (self.album, self.artist, self.score)