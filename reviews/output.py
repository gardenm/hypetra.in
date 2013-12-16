__author__ = 'matthewgarden'

import json
import sys
from wordof import pitchfork, metacritic, review

class ReviewEncoder(json.JSONEncoder):
	def default(self, obj):
		if isinstance(obj, review.Review):
			data = {}
			for k in ['artist', 'album', 'description', 'link', 'score']:
				data[k] = getattr(obj, k, '')
			return data

		return json.JSONEncoder.default(self, obj)

if __name__ == '__main__':
	data = {'pitchfork': [], 'metacritic': []}
	
	p = pitchfork.Pitchfork('http://localhost:8000/PitchforkAlbumReviews')
	for r in p.reviews:
		data['pitchfork'].append(r)

	m = metacritic.Metacritic('http://localhost:8000/Metacritic')
	for r in m.reviews:
		data['metacritic'].append(r)

	json_str = json.dumps(data, cls=ReviewEncoder)

	if len(sys.argv) >= 2:
		try:
			with open(sys.argv[1], "w") as outfile:
				outfile.write(json_str)
		except IOError:
			    print 'oops!'
	else:
		print(json_str)

