def get_aspect_ratio(ratio):
	
	# https://en.wikipedia.org/wiki/Aspect_ratio_(image)
	if ratio <= 1.09:
		return ("1:1", 1)
	elif ratio > 1.09 and ratio <= 1.2:
		return ("6:5", 1.2)
	elif ratio > 1.2 and ratio <= 1.3:
		return ("5:4", 1.25)
	#elif ratio > 1.26 and ratio <= 1.28:
	#	return ("11R", 1.27)
	elif ratio > 1.3 and ratio <= 1.365:
		return ("4:3", 1.33)
	elif ratio > 1.365 and ratio <= 1.4:
		return ("11:8", 1.375)
	elif ratio > 1.4 and ratio <= 1.42:
		return ("1.41:1", 1.41)
	elif ratio > 1.42 and ratio <= 1.45:
		return ("1.43:1", 1.43)
	elif ratio > 1.45 and ratio <= 1.47:
		return ("A3", 1.46154)
	elif ratio > 1.47 and ratio <= 1.55:
		return ("3:2", 1.5)
	elif ratio > 1.55 and ratio <= 1.59:
		return ("F6", 1.57)
	elif ratio > 1.59 and ratio <= 1.61:
		return ("8:5", 1.6)
	elif ratio > 1.61 and ratio <= 1.63:
		return ("golden", 1.612)
	elif ratio > 1.63 and ratio <= 1.7:
		return ("5:3", 1.66)
	elif ratio > 1.7 and ratio <= 1.75:
		return ("7:4", 1.75)
	elif ratio > 1.75 and ratio <= 1.8:
		return ("16:9", 1.77)
	elif ratio > 1.8 and ratio <= 1.9:
		return ("1.85:1", 1.85)
	elif ratio > 1.9 and ratio <= 2.2:
		return ("2:1", 2)
	elif ratio > 2.2 and ratio <= 2.3:
		return ("21:9", 2.33)
	elif ratio > 2.3 and ratio <= 2.5:
		return ("silver", 2.41)		
	else:
		return ("outlier", ratio)

def calculate_price(square_inches):
	# price chart
	if square_inches < 200:
		price = 19.99
	elif square_inches >= 200 and square_inches <= 349:
		price = 29.99
	elif square_inches >= 350 and square_inches <= 499:
		price = 39.99
	elif square_inches >= 500 and square_inches <= 599:
		price = 49.99
	elif square_inches >= 600 and square_inches <= 899:
		price = 59.99	
	elif square_inches >= 900 and square_inches <= 999:
		price = 69.99
	elif square_inches >= 1000 and square_inches <= 1199:
		price = 79.99
	elif square_inches >= 1200 and square_inches <= 1399:
		price = 89.99	
	elif square_inches >= 1400 and square_inches <= 1599:
		price = 99.99
	elif square_inches >= 1600 and square_inches <= 1799:
		price = 109.99
	else:
		price = 119.99

	return price