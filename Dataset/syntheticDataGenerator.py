from random import randint

uidcounter = 0
productaAttributeList = ["DiscreteGPU", "LargeHDD", "IntegratedWebCam", "IntegratedMic", "HighDPI", "HighBattery", "Rugged", "BackLitKeyboard", "LightWeight", "HighRAM", "SDCard", "OpticalDrive"]

writeFile= open("syntheticData.csv", mode="w")

attributeList = ""

for uidcounter in range(10000):
	attributeList = ""
	numberOfAttributes = randint(0,6)
	listOfAssignedAttributes = set()
	for attributeCount in range(numberOfAttributes):
		num = randint(0,9)
		while num in listOfAssignedAttributes:
			num = randint(0,9)

		listOfAssignedAttributes.add(num)
		
		if attributeCount == 0:
			attributeList = productAttributeList[num]
		else:
			attributeList = attributeList + "," + productAttributeList[num]
	
	print uidcounter
	product= "P" + str(uidcounter+1) + "," + str(numberOfAttributes) + ",\"" +  attributeList + "\""
	writeFile.write(product + "\n")
writeFile.close()