//var Db = require('mongodb').Db;
//var Connection = require('mongodb').Connection;
//var Server = require('mongodb').Server;
//var BSON = require('mongodb').BSON;
//var ObjectID = require('mongodb').ObjectID;
var MongoClient = require('mongodb').MongoClient;
var Server = require('mongodb').Server;

function Reviews(host, port) {
	var mongoClient = new MongoClient(new Server(host, port));

	var reviews = this;
	mongoClient.open(function (err, mongoClient) {
		reviews.db = mongoClient.db('music');
	});
};

Reviews.prototype.getCollection = function (callback) {
	this.db.collection('reviews', function (error, collection) {
		if (error) callback(error);
		else callback(null, collection);
	});
};

Reviews.prototype.findAll = function (callback) {
	this.getCollection(function (error, collection) {
		if (error) callback(error);
		else {
			collection.find().toArray(function (error, results) {
				if (error) callback(error);
				else callback(null, results);
			});
		}
	});
};

exports.Reviews = Reviews;
