from random import randint
from decimal import *
userCounter = 0

writeFile= open("userData.csv", mode="w")

productList = ""

for userCounter in range(50000):
	noOfProducts =  randint(1,20)
	productRatings = ""
	productId = set()
	for i in range(noOfProducts-1):
		num = randint(1,10000)
		while num in productId:
			num = randint(1,10000)
		productId.add(num)
		Rating = (randint(1,10))/2.0
		Rating = round(Rating, 1)
		if i == 0:
			productRatings = "P" + str(num) + "=" + str(Rating)
		else: 
			productRatings = productRatings + ", P" + str(num) + "=" + str(Rating)
	
	print userCounter
	product = "User" + str(userCounter+1) + ",\"" + productRatings +"\""
	writeFile.write(product + "\n")
writeFile.close()

