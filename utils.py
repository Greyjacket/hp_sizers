import math

def process_size(size2):
	# this function returns of tuple containing the fractional and integral part of the real number
	size2_split = math.modf(size2)
	decimal_part = size2_split[0]
		
	# round up from .3
	if decimal_part >= .3:
		size2 = math.ceil(size2)
	else:
		size2 = math.floor(size2)

	if size2 >= 15.0 and size2 < 16.0:
		size2 = 16.0
	if size2 >= 17.0 and size2 < 18.0:
		size2 = 16.0
	if size2 >= 19.0 and size2 < 20.0:
		size2 = 18.0

	if size2 >= 37.0 and size2 <= 38.0:
		size2 = 36.0
	if size2 <= 35.0 and size2 <= 37.0:
		size2 = 36.0

	return size2

def process_photo_size(size, ratio):

	if ratio <= 1.3:
		if size == 8.0:
			size2 = 10.0
		elif size == 11.0:
			size2 = 14.0
		elif size == 16.0:
			size2 = 20.0
		elif size == 24.0:
			size2 = 30.0
		else:
			size2 = 40.0
	elif ratio > 1.3 and ratio < 1.45:
		if size == 11.0:
			size2 = 14.0
		elif size == 18.0:
			size2 = 24.0
		elif size == 24.0:
			size2 = 32.0
		else:
			size2 = 43.0
	else:
		if size == 8.0:
			size2 = 12.0
		elif size == 16.0:
			size2 = 24.0
		elif size == 20.0:
			size2 = 30.0
		elif size == 24.0:
			size2 = 36.0
		else:
			size2 = 44.0

	return size2

def calculate_photo_dimensions(size, orientation, ratio, sku):
	item_size = {}

	if orientation == 'portrait':
			size2 = process_photo_size(size, ratio)
			height = size2
			width = size
	else:
			size2 = process_photo_size(size, ratio)
			height = size
			width = size2

	# set the square inches
	square_inches = height * width
	if square_inches >= 80 and square_inches <= 3200:

		price = calculate_price(square_inches)

		# get the string value
		height_str = str(height)
		width_str = str(width)

		int_str1 = str(int(width))
		int_str2 = str(int(height))

		unique1 = int_str1
		unique2 = int_str2

		width_int_str = str(int(width))
		height_int_str = str(int(height))

		# pad a single digit with a zero if need be
		if len(width_int_str) < 2:
			unique1 = "0" + int_str1
		if len(height_int_str) < 2:
			unique2 = "0" + int_str2

		# create the unique sku
		unique = unique1 + unique2
		unique_sku = sku + "_" + unique

		# create the size name
		size_name = width_int_str + "in" + " x " + height_int_str + "in"
		size_name2 = height_int_str + "in" + " x " + width_int_str + "in"

		item_size['Height'] = height_str
		item_size['Width'] = width_str
		item_size['SqIn'] = square_inches
		item_size['SizeName'] = size_name
		item_size['SizeName2'] = size_name2
		item_size['UniqueSku'] = unique_sku
		item_size['Price'] = price
		item_size['Ratio'] = ratio

		return item_size	

def calculate_dimensions(size, orientation, ratio, sku):
	item_size = {}

	if orientation == 'down':
		if ratio >= 1.0:
			size2 = size * (1.0/ratio)
			size2 = process_size(size2)
			height = size
			width = size2
		else:
			size2 = size * ratio
			size2 = process_size(size2)
			height = size2
			width = size
	elif orientation == 'up':
		if ratio >= 1.0:
			size2 = size * ratio
			size2 = process_size(size2)
			height = size2
			width = size
		else:
			size2 = size * (1.0/ratio)
			size2 = process_size(size2)
			height = size
			width = size2
	else:
		print "Faulty orientation."
		exit()

	# set the square inches
	square_inches = height * width
	if square_inches > 240 and square_inches <= 3200:

		price = calculate_price(square_inches)

		# get the string value
		height_str = str(height)
		width_str = str(width)

		int_str1 = str(int(width))
		int_str2 = str(int(height))

		unique1 = int_str1
		unique2 = int_str2

		width_int_str = str(int(width))
		height_int_str = str(int(height))

		# pad a single digit with a zero if need be
		if len(width_int_str) < 2:
			unique1 = "0" + int_str1
		if len(height_int_str) < 2:
			unique2 = "0" + int_str2

		# create the unique sku
		unique = unique1 + unique2
		unique_sku = sku + "_" + unique

		# create the size name
		size_name = width_int_str + "in" + " x " + height_int_str + "in"
		size_name2 = height_int_str + "in" + " x " + width_int_str + "in"

		item_size['Height'] = height_str
		item_size['Width'] = width_str
		item_size['SqIn'] = square_inches
		item_size['SizeName'] = size_name
		item_size['SizeName2'] = size_name2
		item_size['UniqueSku'] = unique_sku
		item_size['Price'] = price
		item_size['Ratio'] = ratio

		return item_size

def get_aspect_ratio(ratio):
	
	if ratio < 1:
		ratio = 1/ratio

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
	if square_inches < 299:
		price = 29.99
	elif square_inches >= 300 and square_inches <= 399:
		price = 39.99
	elif square_inches >= 400 and square_inches <= 499:
		price = 49.99
	elif square_inches >= 500 and square_inches <= 599:
		price = 54.99
	elif square_inches >= 600 and square_inches <= 699:
		price = 59.99
	elif square_inches >= 700 and square_inches <= 799:
		price = 64.99
	elif square_inches >= 800 and square_inches <= 899:
		price = 69.99	
	elif square_inches >= 900 and square_inches <= 999:
		price = 74.99
	elif square_inches >= 1000 and square_inches <= 1099:
		price = 79.99
	elif square_inches >= 1100 and square_inches <= 1199:
		price = 84.99
	elif square_inches >= 1200 and square_inches <= 1299:
		price = 89.99
	elif square_inches >= 1300 and square_inches <= 1399:
		price = 94.99	
	elif square_inches >= 1400 and square_inches <= 1499:
		price = 99.99	
	elif square_inches >= 1500 and square_inches <= 1599:
		price = 149.99
	elif square_inches >= 1600 and square_inches <= 1699:
		price = 159.99
	elif square_inches >= 1700 and square_inches <= 1799:
		price = 169.99
	elif square_inches >= 1800 and square_inches <= 1899:
		price = 179.99
	elif square_inches >= 1900 and square_inches <= 1999:
		price = 189.99
	elif square_inches >= 2000 and square_inches <= 2099:
		price = 199.99
	elif square_inches >= 2100 and square_inches <= 2199:
		price = 209.99
	elif square_inches >= 2200 and square_inches <= 2299:
		price = 219.99
	elif square_inches >= 2300 and square_inches <= 2399:
		price = 229.99
	elif square_inches >= 2400 and square_inches <= 2499:
		price = 239.99
	elif square_inches >= 2500 and square_inches <= 2599:
		price = 249.99
	elif square_inches >= 2600 and square_inches <= 2699:
		price = 259.99
	elif square_inches >= 2700 and square_inches <= 2799:
		price = 269.99
	elif square_inches >= 2800 and square_inches <= 2899:
		price = 279.99
	elif square_inches >= 2900 and square_inches <= 2999:
		price = 289.99
	elif square_inches >= 3000 and square_inches <= 3099:
		price = 299.99
	elif square_inches >= 3100 and square_inches <= 3199:
		price = 309.99
	else:
		price = 319.99

	return price