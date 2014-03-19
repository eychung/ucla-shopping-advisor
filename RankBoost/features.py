import csv
import cPickle
import itertools
import random
import sys

dataPath = "../Dataset/"
trainPath = "train/"
testPath = "test/"

userTableFile = "userData.csv"
productTableFile = "products.txt"
trainFile = "Train.csv"
testFile = "Test.csv"

# Note that "code" (2) and "industry" (3) can be tree nodes or leaf nodes.
userAttributesLevel1 = ["work", "casual"]
userAttributesLevel2 = ["code1", "admin", "gaming", "applications"]
userAttributesLevel3 = ["graphic_intensive", "data_intensive", "advance_usage", "simple_usage", "hardcore", "softcore", "browsing", "software"]
userAttributesLevel4 = ["game_dev", "artist", "scientist", "engineer", "comm", "data", "word_processing", "pos", "repetitive", "strategic", "real_time", "casino_games", "media", "website", "writing", "designing"]
userAttributesLevel5 = ["graphic_design", "game_engine", "vector", "animator", "research", "industry1", "school", "industry2", "high_end_user", "low_end_user", "operator", "system_admin", "student", "industry3", "small_business", "large_business", "pictures", "video", "online_gaming", "social", "long_form", "short_form", "code2", "art"]
userAttributes = userAttributesLevel1 + userAttributesLevel2 + userAttributesLevel3 + userAttributesLevel4 + userAttributesLevel5

class User():
	def __init__(self):
		self.reviews = []

class Review():
	def __init__(self):
		self.product = -1
		self.rating = -1
		self.userAttributes = []

class Product():
	def __init__(self):
		self.base = -1
		self.technicalAttributes = []

def loadUsersProducts():
	users = {}
	products = {}
	
	with open(dataPath + userTableFile) as csvfile:
		reader = csv.reader(csvfile)
		reader.next()
		for userId, productId, rating, userAttributes in reader:
			userId, productId = int(userId), int(productId)
			if userId not in users:
				users[userId] = User()
			userReview = Review()
			userReview.product = productId
			userReview.rating = rating
			userReview.userAttributes.append(userAttributes)
			users[userId].reviews.append(userReview)

	with open(dataPath + productTableFile) as csvfile:
		reader = csv.reader(csvfile)
		reader.next()
		for productId, base, technicalAttributes in reader:
			productId = int(productId)
			products[productId] = Product()
			products[productId].base = base
			products[productId].technicalAttributes.append(technicalAttributes)
	
	return users, products

def saveFeature(feature, name, mode):
	path = ""
	if mode == 'train':
		path = trainPath
	elif mode == 'test':
		path = testPath
	filename = path + name + '.' + mode
	print 'saving feature to', filename, '...'
	cPickle.dump(feature, open(filename, 'wb'))

def csvGenerator(mode):
	if mode == 'train':
		with open(dataPath + trainFile) as csvfile:
			reader = csv.reader(csvfile)
			reader.next()
			for productId, rating, correctUserAttributes, incorrectUserAttributes in reader:
				yield productId, correctUserAttributes, incorrectUserAttributes

	elif mode == 'test':
		with open(dataPath + testFile) as csvfile:
			reader = csv.reader(csvfile)
			reader.next()
			for productId, rating, userAttributes in reader:
				yield productId, userAttributes

	else:
		print 'mode must be "train" or "test"'
		raise ValueError

def labels(mode='train'):
	labels = []
	if mode == 'train':
		with open(dataPath + trainFile) as csvfile:
			reader = csv.reader(csvfile)
			reader.next()
			for productId, rating, correctUserAttributes, incorrectUserAttributes in reader:
				mylabels = []
				correctUserAttributes = [ua for ua in correctUserAttributes.split(' ')]
				incorrectUserAttributes = [ua for ua in incorrectUserAttributes.split(' ')]
				for cua in correctUserAttributes:
					mylabels.append(1) # 1 = correct
				for iua in incorrectUserAttributes:
					mylabels.append(0) # 0 - incorrect
				labels.append(mylabels)
	
	elif mode == 'test':
		for productId, userAttributes in csvGenerator(mode=mode):
			labels.append([productId, userAttributes])
	
	else:
		print 'mode must be "train" or "test"'
		raise ValueError

	saveFeature(labels, name='labels', mode=mode)

def createFeatureFiles(users, products, mode='train'):
	# Create a file for each user attribute (node in decision tree).
	for userAttribute in userAttributes:
		features = []
		# Iterate through each user.
		for userId in users:
			myfeatures = []
			# Iterate through each product (that has been reviewed by user).
			for productReview in users[userId].reviews:
				if userAttribute in productReview.userAttributes:
					myfeatures.append(1) # 1 = present
				else:
					myfeatures.append(0) # 0 = not present
			features.append(myfeatures)

		saveFeature(features, name=userAttribute, mode=mode)

if __name__ == '__main__':
	users, products = loadUsersProducts()
	
	for mode in ['train', 'test']:
		labels(mode=mode)

	createFeatureFiles(users, products)
