import math

from random import randint
from decimal import *

productList = ""

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
userAttributesEncodedDictionary = {'0' : "work", '1' : "casual", '00' : "code", '01' : "admin", '10' : "gaming", '11' : "applications", '000' : "graphic_intensive", '001' : "data_intensive", '010' : "advance_usage", '011' : "simple_usage", '100' : "hardcore", '101' : "softcore", '110' : "browsing", '111' : "software", '0000' : "game_dev", '0001' : "artist", '0010' : "scientist", '0011' : "engineer", '0100' : "comm", '0101' : "data", '0110' : "word_processing", '0111' : "pos", '1000' : "repetitive", '1001' : "strategic", '1010' : "real_time", '1011' : "casino_games", '1100' : "media", '1101' : "website", '1110' : "writing", '1111' : "designing", '00000' : "graphic_design", '00001' : "game_engine", '00010' : "vector", '00011' : "animator", '00100' : "research", '00101' : "industry", '00110' : "school", '00111' : "industry", '01000' : "high_end_user", '01001' : "low_end_user", '01010' : "operator", '01011' : "system_admin", '01000' : "student", '01001' : "industry", '01010' : "small_business", '01011' : "large_business", '11000' : "pictures", '11001' : "video", '11010' : "online_gaming", '11011' : "social", '11100' : "long_form", '11101' : "short_form", '11110' : "code", '11111' : "art"}

writeFile = open("userData.csv", mode="w")
writeFile.write("UserId,ProductId,Rating,UserAttributes\n")

# userCounter also serves as UserId.
userCounter = 0

# Probability user inputs an uncommon user attribute and chooses accurate user preferences, respectively. Crossover probability calculated by 0.5 * x = 0.05.
crossoverProbability = 5
correctPathProbability = 97
incorrectBasePathProbability = 50
maxNumUserAttributes = 7
numLevels = 5

numErrorPrint = 0

def swapBit(productId, index):
	if productId[index] == '1':
		return productId[:index] + '0' + productId[index+1:]
	else:
		return productId[:index] + '1' + productId[index+1:]

# 28 total leaf nodes.
def getRandUserAttributesForProduct(productId):
	global numErrorPrint
	attributes = []
	currentMaxLevel = len(productId)
	for index in range(len(productId)):
		node = productId[:index]
		if randint(1, 100) <= correctPathProbability:
			attributes.append(node)

	while currentMaxLevel > 0 and len(attributes) < maxNumUserAttributes:
		# User has a 5% chance of incorrectly inputting a user attribute to the product.
		if randint(1, 100) <= crossoverProbability and randint(1, 100) <= incorrectBasePathProbability/math.pow(2, numLevels - currentMaxLevel):
			attributes.append(swapBit(productId, currentMaxLevel-1))
			numErrorPrint += 1
		currentMaxLevel -= 1

	return attributes

def getRandProduct():
	return userAttributesLeafNodesEncoded[randint(0, 27)]

for i in range(1000):
	getRandUserAttributesForProduct(getRandProduct())

print numErrorPrint