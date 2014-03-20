import math

from random import randint
from decimal import *

""" 
Similar to ShoppingAdvisor's synthetic dataset, we create relationships between
user attributes explicitly rather than randomly, in order to make sense of the
correlation of tags in a realisitic environment. Therefore, we constructed a
static decision tree and introduced an incorrectness variable to consider all
cases.
"""

userTableFilePath = "userData.csv"
productTableFilePath = "products.txt"
trainFilePath = "Train.csv"
testFilePath = "Test.csv"
productUserAttributesFilePath = "productUserAttributes.csv"

# Note that "code" (2) and "industry" (3) can be tree nodes or leaf nodes.
userAttributesLevel1 = ["work", "casual"]
userAttributesLevel2 = ["code1", "admin", "gaming", "applications"]
userAttributesLevel3 = ["graphic_intensive", "data_intensive", "advance_usage", "simple_usage", "hardcore", "softcore", "browsing", "software"]
userAttributesLevel4 = ["game_dev", "artist", "scientist", "engineer", "comm", "data", "word_processing", "pos", "repetitive", "strategic", "real_time", "casino_games", "media", "website", "writing", "designing"]
userAttributesLevel5 = ["graphic_design", "game_engine", "vector", "animator", "research", "industry1", "school", "industry2", "high_end_user", "low_end_user", "operator", "system_admin", "student", "industry3", "small_business", "large_business", "pictures", "video", "online_gaming", "social", "long_form", "short_form", "code2", "art"]
userAttributes = userAttributesLevel1 + userAttributesLevel2 + userAttributesLevel3 + userAttributesLevel4 + userAttributesLevel5

# Defined separately to preserve order defined in our encoded decision tree design that holds a one-to-one mapping to product ids. Note ids start at index 0.
userAttributesLeafNodes = ["graphic_design", "game_engine", "vector", "animator", "research", "industry1", "school", "industry2", "high_end_user", "low_end_user", "operator", "system_admin", "student", "industry3", "small_business", "large_business", "repetitive", "strategic", "real_time", "casino_games", "pictures", "video", "online_gaming", "social", "long_form", "short_form", "code2", "art"]
userAttributesLeafNodesEncoded = ['00000', '00001', '00010', '00011', '00100', '00101', '00110', '00111', '01000', '01001', '01010', '01011', '01100', '01101', '01110', '01111', '1000', '1001', '1010', '1011', '11000', '11001', '11010', '11011', '11100', '11101', '11110', '11111']

# Dictionary mapping that represents our staticly generated decision tree.
userAttributesEncodedDictionary = {'0' : "work", '1' : "casual", '00' : "code1", '01' : "admin", '10' : "gaming", '11' : "applications", '000' : "graphic_intensive", '001' : "data_intensive", '010' : "advance_usage", '011' : "simple_usage", '100' : "hardcore", '101' : "softcore", '110' : "browsing", '111' : "software", '0000' : "game_dev", '0001' : "artist", '0010' : "scientist", '0011' : "engineer", '0100' : "comm", '0101' : "data", '0110' : "word_processing", '0111' : "pos", '1000' : "repetitive", '1001' : "strategic", '1010' : "real_time", '1011' : "casino_games", '1100' : "media", '1101' : "website", '1110' : "writing", '1111' : "designing", '00000' : "graphic_design", '00001' : "game_engine", '00010' : "vector", '00011' : "animator", '00100' : "research", '00101' : "industry1", '00110' : "school", '00111' : "industry2", '01000' : "high_end_user", '01001' : "low_end_user", '01010' : "operator", '01011' : "system_admin", '01100' : "student", '01101' : "industry3", '01110' : "small_business", '01111' : "large_business", '11000' : "pictures", '11001' : "video", '11010' : "online_gaming", '11011' : "social", '11100' : "long_form", '11101' : "short_form", '11110' : "code2", '11111' : "art"}

# Probability user inputs an uncommon user attribute and chooses accurate user preferences, respectively. Crossover probability calculated by 0.5 * x = 0.05.
crossoverProbability = 5
correctPathProbability = 97
incorrectBasePathProbability = 50
maxNumUserAttributes = 7
numLevels = 5

numErrorPrint = 0

totalNumProducts = 343

# Helper function for getRandUserAttributes.
def swapBit(association, index):
	# Special case where leaf nodes are not present in this part of the subtree.
	if association[:2] != '10':
		if association[index] == '1':
			newAssociation = association[:index] + '0' + association[index+1:]
			if newAssociation[:2] != '10':
				return newAssociation
			else:
				return association
		else:
			newAssociation = association[:index] + '1' + association[index+1:]
			if newAssociation[:2] != '10':
				return newAssociation
			else:
				return association
	else:
		if index < 4:
			if association[index] == '1':
				return association[:index] + '0' + association[index+1:]
			else:
				return association[:index] + '1' + association[index+1:]
		else:
			return association

# FIX: NEED MAPPING FOR 28-24 OF THE OTHER ASSOCIATIONS.
def getProductAssociation(pid):
	return userAttributesLeafNodesEncoded[pid]

# 28 total leaf nodes.
def getUserAttributes(association):
	global numErrorPrint
	attributes = []
	decodedAttributes = []
	absolute = []
	correct = []
	incorrect = []
	currentMaxLevel = len(association)

	for index in range(len(association)):
		node = association[:index+1]
		absolute.append(userAttributesEncodedDictionary[node])
		if randint(1, 100) <= correctPathProbability:
			attributes.append(node)
			correct.append(userAttributesEncodedDictionary[node])

	while currentMaxLevel > 0 and len(attributes) < maxNumUserAttributes:
		# User has a 5% chance of incorrectly inputting a user attribute to the product.
		if randint(1, 100) <= crossoverProbability and randint(1, 100) <= incorrectBasePathProbability/math.pow(2, numLevels - currentMaxLevel):
			newAssociation = swapBit(association, currentMaxLevel-1)
			if newAssociation not in attributes:
				attributes.append(newAssociation)
				incorrect.append(userAttributesEncodedDictionary[newAssociation])
			numErrorPrint += 1
		currentMaxLevel -= 1
	
	return absolute, correct, incorrect

def parseProduct(line):
	line = line.strip()
	pid = line[:line.index(",")]
	
	part = line[line.index(",")+1:]
	base = part[:part.index(",")]

	technicalAttributes = part[part.index(",")+1:]

	return pid, base, technicalAttributes

# Create training set consisting of 500 users.
def createTrainingSet():
	trainFile = open(trainFilePath, mode="w")
	trainFile.write("ProductId,Rating,CorrectUserAttributes,IncorrectUserAttributes\n")

	products = []

	productTableFile = open(productTableFilePath, mode='r')
	for line in productTableFile:
		products.append(line)

	productIndex = 0

	for user in range(500):
		numRatings = randint(1, 20)
		userPreferences = []
		for row in range(numRatings):
			if productIndex <= totalNumProducts-1:
				pid, base, technicalAttributes = parseProduct(products[productIndex])
				productIndex += 1
			else:
				pid, base, technicalAttributes = parseProduct(products[0])
				productIndex = 1

			absolute, correct, incorrect = getUserAttributes(getProductAssociation(int(base)))
			skewRating = 0			

			for item in correct + incorrect:
				if item not in userPreferences:
					userPreferences.append(item)
				else:
					skewRating = 1

			rating = (randint(1, 10))/2.0
			rating = min(round(rating, 1) + skewRating, 5.0)

			trainFile.write(str(pid) + ',' + str(rating) + ',' + ' '.join(correct) + ',' + ' '.join(incorrect) + '\n')

	trainFile.close()

# Create testing set consisting of 1000 users. This data set corresponds to the user table created.
def createTestingSet():
	testFile = open(testFilePath, mode='w')
	testFile.write("ProductId,Rating,UserAttributes\n")

	userTableFile = open(userTableFilePath, mode='w')
	userTableFile.write("UserId,ProductId,Rating,UserAttributes\n")

	products = []

	productTableFile = open(productTableFilePath, mode='r')
	for line in productTableFile:
		products.append(line)

	productIndex = 0

	for user in range(1000):
		numRatings = randint(1, 20)
		userPreferences = []
		for row in range(numRatings):
			if productIndex <= totalNumProducts-1:
				pid, base, technicalAttributes = parseProduct(products[productIndex])
				productIndex += 1
			else:
				pid, base, technicalAttributes = parseProduct(products[0])
				productIndex = 1

			absolute, correct, incorrect = getUserAttributes(getProductAssociation(int(base)))
			skewRating = 0			

			for item in correct + incorrect:
				if item not in userPreferences:
					userPreferences.append(item)
				else:
					skewRating = 1

			rating = (randint(1, 10))/2.0
			rating = min(round(rating, 1) + skewRating, 5.0)

			testFile.write(str(pid) + ',' + str(rating) + ',' + ' '.join(correct + incorrect) + '\n')
			userTableFile.write(str(user) + ',' + str(pid) + ',' + str(rating) + ',' + ' '.join(correct+incorrect) + '\n')

	testFile.close()
	userTableFile.close()

# Should be in productGenerator.py file.
def createProductUserAttributesFile():
	productUserAttributesFile = open(productUserAttributesFilePath, mode='w')
	productUserAttributesFile.write("ProductId,UserAttributes\n")

	products = []

	productTableFile = open(productTableFilePath, mode='r')
	for line in productTableFile:
		products.append(line)

	# Assume product id is from 0-342 (343 total).
	for productId in range(totalNumProducts):
		pid, base, technicalAttributes = parseProduct(products[productId])
		absolute, correct, incorrect = getUserAttributes(getProductAssociation(int(base)))
		productUserAttributesFile.write(str(productId) + ',' + ' '.join(absolute) + '\n')

	productUserAttributesFile.close()

if __name__ == '__main__':
	createTrainingSet()
	createTestingSet()

	createProductUserAttributesFile()
