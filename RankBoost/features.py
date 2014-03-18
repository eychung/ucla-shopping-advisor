import csv
import cPickle
import itertools
import random
import sys

pal = ["DiscreteGPU", "LargeHDD", "IntegratedWebCam", "IntegratedMic", "HighDPI", "HighBattery", "Rugged", "BackLitKeyboard", "LightWeight", "HighRAM", "SDCard", "OpticalDrive"]

# the ones that we came up with for the leaf nodes (24 base cases)
baseProductSet = { 0 : pal[0] + " " + pal[1] + " " + pal[4] + " " + pal[7] + " " + pal[9],
1 : pal[0] + " " + pal[1] + " " + pal[4] + " " + pal[7] + " " + pal[9] + " " + pal[11],
2 : pal[0] + " " + pal[1] + " " + pal[4] + " " + pal[9] + " " + pal[10],
3 : pal[0] + " " + pal[1] + " " + pal[2] + " " + pal[4] + " " + pal[9],
4 : pal[1] + " " + pal[2] + " " + pal[5] + " " + pal[9] + " " + pal[11],
5 : pal[1] + " " + pal[5] + " " + pal[6] + " " + pal[9] + " " + pal[11],
6 : pal[1] + " " + pal[2] + " " + pal[3] + " " + pal[5] + " " + pal[9],
7 : pal[1] + " " + pal[2] + " " + pal[3] + " " + pal[6] + " " + pal[9],
8 : pal[2] + " " + pal[3] + " " + pal[5] + " " + pal[7] + " " + pal[8] + " " + pal[11],
9 : pal[2] + " " + pal[3] + " " + pal[5] + " " + pal[7] + " " + pal[8],
10 : pal[1] + " " + pal[3] + " " + pal[7] + " " + pal[9] + " " + pal[11],
11 : pal[1] + " " + pal[2] + " " + pal[3] + " " + pal[6] + " " + pal[7] + " " + pal[9],
12 : pal[2] + " " + pal[3] + " " + pal[5] + " " + pal[6] + " " + pal[7],
13 : pal[2] + " " + pal[3] + " " + pal[5] + " " + pal[6] + " " + pal[9],
14 : pal[2] + " " + pal[3] + " " + pal[5] + " " + pal[6] + " " + pal[7] + " " + pal[9],
15 : pal[0] + " " + pal[1] + " " + pal[4] + " " + pal[6] + " " + pal[7],
16 : pal[0] + " " + pal[1] + " " + pal[4] + " " + pal[6] + " " + pal[7] + " " + pal[9],
17 : pal[2] + " " + pal[3] + " " + pal[5] + " " + pal[8] + " " + pal[11],
18 : pal[2] + " " + pal[3] + " " + pal[5] + " " + pal[6] + " " + pal[8],
19 : pal[1] + " " + pal[2] + " " + pal[5] + " " + pal[9] + " " + pal[10],
20 : pal[1] + " " + pal[2] + " " + pal[5] + " " + pal[9] + " " + pal[10] + " " + pal[11],
21 : pal[3] + " " + pal[4] + " " + pal[5] + " " + pal[6] + " " + pal[7] + " " + pal[8],
22 : pal[3] + " " + pal[4] + " " + pal[5] + " " + pal[6] + " " + pal[8],
23 : pal[5] + " " + pal[7] + " " + pal[8] + " " + pal[9] + " " + pal[10] + " " + pal[11] }

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
	
	with open('../Dataset/userData.csv') as csvfile:
		reader = csv.reader(csvfile)
		reader.next()
		for userId, productId, rating, userAttributes in reader:
			userId, productId = int(userId), int(productId)
			if userId not in users:
				users[userId] = User()
			users[userId].reviews = Review()
			users[userId].reviews.product = productId
			users[userId].reviews.rating = rating
			users[userId].reviews.userAttributes.append(userAttributes)

	with open('../Dataset/products.txt') as csvfile:
		reader = csv.reader(csvfile)
		reader.next()
		for productId, base, technicalAttributes in reader:
			productId = int(productId)
			products[productId] = Product()
			products[productId].base = base
			products[productId].technicalAttributes.append(technicalAttributes)
	
	return users, products

def csvGenerator(mode):
	if mode == 'train':
		with open("mylabels.train") as csvfile:
			reader = csv.reader(csvfile)
			reader.next() # skip header
			for node, techAttrPresenceEncoding in reader:
				node = int(node)
				techAttrPresenceEncoding = [int(num) for num in techAttrPresenceEncoding.split(' ')]
				yield node, techAttrPresenceEncoding 

	elif mode == 'test':
		with open('mylabels.train') as csvfile: # stub
			reader = csv.reader(csvfile)
			reader.next() # skip header
			for node, techAttrPresenceEncoding in reader:
				node = int(node)
				techAttrPresenceEncoding = [int(num) for num in techAttrPresenceEncoding.split(' ')]
				yield node, techAttrPresenceEncoding 

	else:
		print 'mode must be "train" or "test"'
		raise ValueError

def saveFeature(feature, name, mode):
	filename = name + '.' + mode
	print 'saving feature to', filename, '...'
	cPickle.dump(feature, open(filename, 'wb'))

# Helper function that puts all training labels for the 54 nodes into one .csv file.
def createLabelsFile(path='../Dataset/train/'):
	numNodes = 54

	writeFile = open("mylabels.train", mode="w")
	writeFile.write("Node,TechnicalAttributes" + "\n")
	for i in range(numNodes):
		writeFile.write(str(i+1) + ",")
		f = open(path + 'train.labels.node' + str(i+1), 'r')
		savedLine = ""
		for line in f:
			savedLine += line.strip() + " "
		writeFile.write(savedLine.strip())
		writeFile.write("\n")
	writeFile.close()

# Used to create the labels.train file that holds a 2D array, with the rows representing the 54 nodes in the decision tree and the columns contain the presence or absence of each of the 24 base products.
def labels(mode='train'):
	labels = []

	if mode == 'train':
		with open("mylabels.train") as csvfile:
			reader = csv.reader(csvfile)
			reader.next()
			for node, techAttrPresenceEncoding in reader:
				mylabels = []
				techAttrPresenceEncoding = [int(num) for num in techAttrPresenceEncoding.split(' ')]
				for tapenum in techAttrPresenceEncoding:
					mylabels.append(tapenum)
				labels.append(mylabels)
	
	elif mode == 'test':
		for node, techAttrPresenceEncoding in csvGenerator(mode=mode):
			labels.append([node, techAttrPresenceEncoding])
	
	else:
		print 'mode must be "train" or "test"'
		raise ValueError

	saveFeature(labels, name='labels', mode=mode)

def createFeatureFiles(mode='train'):
	for technicalAttribute in pal:
		features = []
		for baseProduct in baseProductSet:
			if str(technicalAttribute) in baseProductSet[baseProduct]:
				features.append(baseProduct)
		saveFeature(features, name=technicalAttribute, mode=mode)

if __name__ == '__main__':
	users, products = loadUsersProducts()
	
	createLabelsFile()
	for mode in ['train', 'test']:
		labels(mode=mode)

	createFeatureFiles()
