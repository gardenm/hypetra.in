__author__ = 'matthewgarden'

from pymongo import MongoClient
from wordof import pitchfork, metacritic, review

if __name__ == '__main__':
	client = MongoClient()
	db = client.music

	p = pitchfork.Pitchfork()
	for r in p.reviews:
		if not db.reviews.find_one({'link': r.link}):
			db.reviews.insert(r.__dict__)

	m = metacritic.Metacritic()
	for r in m.reviews:
		if not db.reviews.find_one({'link': r.link}):
			db.reviews.insert(r.__dict__)
