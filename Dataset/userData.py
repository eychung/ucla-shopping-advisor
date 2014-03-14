import math

from random import randint
from decimal import *

# Note that "code" (2) and "industry" (3) can be tree nodes or leaf nodes.
userAttributesLevel1 = ["work", "casual"]
userAttributesLevel2 = ["code", "admin", "gaming", "applications"]
userAttributesLevel3 = ["graphic_intensive", "data_intensive", "advance_usage", "simple_usage", "hardcore", "softcore", "browsing", "software"]
userAttributesLevel4 = ["game_dev", "artist", "scientist", "engineer", "comm", "data", "word_processing", "pos", "repetitive", "strategic", "real_time", "casino_games", "media", "website", "writing", "designing"]
userAttributesLevel5 = ["graphic_design", "game_engine", "vector", "animator", "research", "industry", "school", "industry", "high_end_user", "low_end_user", "operator", "system_admin", "student", "industry", "small_business", "large_business", "pictures", "video", "online_gaming", "social", "long_form", "short_form", "code", "art"]
userAttributes = userAttributesLevel1 + userAttributesLevel2 + userAttributesLevel3 + userAttributesLevel4 + userAttributesLevel5

# Defined separately to preserve order defined in our encoded decision tree design that holds a one-to-one mapping to product ids. Note ids start at index 0.
userAttributesLeafNodes = ["graphic_design", "game_engine", "vector", "animator", "research", "industry", "school", "industry", "high_end_user", "low_end_user", "operator", "system_admin", "student", "industry", "small_business", "large_business", "repetitive", "strategic", "real_time", "casino_games", "pictures", "video", "online_gaming", "social", "long_form", "short_form", "code", "art"]
userAttributesLeafNodesEncoded = ['00000', '00001', '00010', '00011', '00100', '00101', '00110', '00111', '01000', '01001', '01010', '01011', '01100', '01101', '01110', '01111', '1000', '1001', '1010', '1011', '11000', '11001', '11010', '11011', '11100', '11101', '11110', '11111']

# Dictionary mapping that represents our staticly generated decision tree.
userAttributesEncodedDictionary = {'0' : "work", '1' : "casual", '00' : "code", '01' : "admin", '10' : "gaming", '11' : "applications", '000' : "graphic_intensive", '001' : "data_intensive", '010' : "advance_usage", '011' : "simple_usage", '100' : "hardcore", '101' : "softcore", '110' : "browsing", '111' : "software", '0000' : "game_dev", '0001' : "artist", '0010' : "scientist", '0011' : "engineer", '0100' : "comm", '0101' : "data", '0110' : "word_processing", '0111' : "pos", '1000' : "repetitive", '1001' : "strategic", '1010' : "real_time", '1011' : "casino_games", '1100' : "media", '1101' : "website", '1110' : "writing", '1111' : "designing", '00000' : "graphic_design", '00001' : "game_engine", '00010' : "vector", '00011' : "animator", '00100' : "research", '00101' : "industry", '00110' : "school", '00111' : "industry", '01000' : "high_end_user", '01001' : "low_end_user", '01010' : "operator", '01011' : "system_admin", '01100' : "student", '01101' : "industry", '01110' : "small_business", '01111' : "large_business", '11000' : "pictures", '11001' : "video", '11010' : "online_gaming", '11011' : "social", '11100' : "long_form", '11101' : "short_form", '11110' : "code", '11111' : "art"}

# Probability user inputs an uncommon user attribute and chooses accurate user preferences, respectively. Crossover probability calculated by 0.5 * x = 0.05.
crossoverProbability = 5
correctPathProbability = 97
incorrectBasePathProbability = 50
maxNumUserAttributes = 7
numLevels = 5

numErrorPrint = 0

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

# Returns an encoding that can be mapped to a list of products per leaf node that may satisfy query.
def getRandProductAssociation():
	return userAttributesLeafNodesEncoded[randint(0, 27)]

# Randomly selects a product based off encoding.
def getRandProduct(association):
	return randint(1, 200)

# 28 total leaf nodes.
def getRandUserAttributes(association):
	global numErrorPrint
	attributes = []
	currentMaxLevel = len(association)

	for index in range(len(association)):
		node = association[:index+1]
		if randint(1, 100) <= correctPathProbability:
			attributes.append(node)

	while currentMaxLevel > 0 and len(attributes) < maxNumUserAttributes:
		# User has a 5% chance of incorrectly inputting a user attribute to the product.
		if randint(1, 100) <= crossoverProbability and randint(1, 100) <= incorrectBasePathProbability/math.pow(2, numLevels - currentMaxLevel):
			newAssociation = swapBit(association, currentMaxLevel-1)
			if newAssociation not in attributes:
				attributes.append(newAssociation)
			numErrorPrint += 1
		currentMaxLevel -= 1
	
	return attributes

# Create 1000 users.
def createUserTable():
	writeFile = open("userData.csv", mode="w")
	writeFile.write("UserId,ProductId,Rating,UserAttributes\n")

	for user in range(1000):
		numRatings = randint(1, 20)
		for row in range(numRatings):
			association = getRandProductAssociation()
			product = getRandProduct(association)
			encodedAttributes = getRandUserAttributes(association)
			attributes = ""
			for encoding in encodedAttributes:
				attributes += userAttributesEncodedDictionary[encoding] + " "

			rating = (randint(1, 10))/2.0
			rating = round(rating, 1)

			# For now, we only assume each association (leaf node) represents only one product.
			writeFile.write(str(user) + ", " + str(product) + ", " + str(rating) + ", " + attributes + "\n")

	writeFile.close()

createUserTable()