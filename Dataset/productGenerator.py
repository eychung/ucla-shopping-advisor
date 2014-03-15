from random import randint

# Product attribute list
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

finalProductSet = baseProductSet # apparently this assigns a reference to baseProductSet instead of copying the contents over

pid = 24

for i in range(24):
	addedList = [] # list of variations already added to current base product
	for j in range(min(8, len(baseProductSet[i].split()))): # 8 variations for each base case to yield approx 200		
		attrList = baseProductSet[i].split() # tokenized list of attributes for ith product
		k = randint(0, 11)
		while pal[k] in attrList or k in addedList: # product attribute chosen to add at random already assigned to current product, choose another
				k = randint(0, 11)
		addedList.append(k)
		attrList.append(pal[k])
		finalProductSet[pid] = ' '.join(attrList)
		print "Adding " + str(pid) + " " + finalProductSet[pid] + "\n"
		pid += 1

newlim = len(baseProductSet)

for i in range(newlim):
	addedList = [] # list of variations already added to current base product
	for j in range(min(8, len(baseProductSet[i].split()))): # 8 variations for each base case to yield approx 200		
		attrList = baseProductSet[i].split() # tokenized list of attributes for ith product
		k = randint(0, 11)
		while pal[k] in attrList or k in addedList: # product attribute chosen to add at random already assigned to current product, choose another
				k = randint(0, 11)
		addedList.append(k)
		attrList.append(pal[k])
		finalProductSet[pid] = ' '.join(attrList)
		print "Adding " + str(pid) + " " + finalProductSet[pid] + "\n"
		pid += 1
		if pid > 200:
			break

for i in baseProductSet:
	print i, baseProductSet[i]

with open('testop.txt', 'w') as outfile:
	for i in finalProductSet:
		outfile.write(str(i) + ' ' + finalProductSet[i] + '\n')

