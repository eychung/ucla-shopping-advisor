# Calculate product ranks at each node

# Uses driver.py authored by Eric

import driver
from sys import argv
from collections import OrderedDict

# Product attribute list
pal = ["DiscreteGPU", "LargeHDD", "IntegratedWebCam", "IntegratedMic", "HighDPI", "HighBattery", "Rugged", "BackLitKeyboard", "LightWeight", "HighRAM", "SDCard", "OpticalDrive"]

avg_scores = [0]*343
encodedAttrDict = {}

# Get average ratings for different products using driver.py
for pid in range(343):
	avg_scores[pid] = driver.getScoreOfProduct(pid)

# Extract the products from products.txt and encode their technical attributes in binary form
with open('products2.txt') as infile:
	for line in infile:
		extractedValues = line.split()
		pid = int(extractedValues[0])
		encodedAttr = [0]*12 # for each product, assume initially that it has no technical attributes
		for i in range(2, len(extractedValues)):
			index = pal.index(extractedValues[i])
			encodedAttr[index] = 1 # for those attributes that are present in the product, set their indices to 1.
			# Each product is then represented with a 12 character binary encoded string, eg - '010001000010', which we store in a dictionary
			encodedAttrDict[pid] = ''.join(str(x) for x in encodedAttr) # convert list of technical attributes to an encoded binary string before storing
			
# For each node, extract the weights from the corresponding file, calculate ranks and write the top 10 ranked products to file
# Store the ranks in a dictionary that can then be sorted and written to file

for i in range(1, 55): # there are 55 nodes in all, including a null root
	weights = [None]*12
	rankValues = {} # stores the floating point value rank(p) for each product
	# rank(p) is calculated as the sum of avg_scores[pid]*weight for all technical attributes
	with open('../RankSVM/coefficients/coeffnode' + str(i) + '.txt') as infile: # for each node, extract the weights
		j = 0
		for line in infile:
			weights[j] = float(line.split()[0]) # store these weights (12 per node) in a list
			j += 1
		attrList = [None]*343
		for k in range(343):
			attrList[k] = list(encodedAttrDict[k]) # extract binary encoded string (of technical attributes) for each product from dictionary, convert it to list
			rank = 0.0
			for l in range(12):
				rank += int(attrList[k][l])*weights[l]
			rankValues[k] = rank
	
	# sort the resulting rankValues dictionary and write the top 10 ranked product IDs and ranks to file
	orderedRankValues = OrderedDict(sorted(rankValues.items(), key=lambda t: t[1]))
	
	with open('../RankSVM/ranks/ranknode' + str(i) + '.txt', 'w') as outfile: # for each node, write top 10 ranked products to file
		for z in range(10):
			(val1, val2) = orderedRankValues.popitem(True)
			outfile.write(str(val1) + ' ' + str(val2) + '\n')
