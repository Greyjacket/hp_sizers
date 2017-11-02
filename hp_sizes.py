#!/usr/bin/python
import csv, sys, math

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

try:
	filename = sys.argv[1]
except:
	print "\nPlease input a valid CSV filename.\n"
	print "Format: python scriptname filename type.\n"
	exit()

try:
	filetype = sys.argv[2]
	if sys.argv[2] != 'map' and sys.argv[2] != 'photo':
		print "\nPlease select map or photo.\n"
	exit()

except:
	print "\nPlease input a collection type."
	print "Format: python scriptname filename type."
	print "Valid types are \"map\" or \"photo\".\n"
	exit()

# change the base number to scale by, depending on map or photo
if filetype == "map":
	sizes = [24.0, 36.0, 44.0]
	multiple = 2
else:
	multiple = 1
	sizes = [8.0, 11.0, 16.0, 24.0, 32.0]

newCsv = []
newFile = open('NewSizes.csv', 'wb') #wb for windows, else you'll see newlines added to csv
# open the file from console arguments
with open(filename, 'rb') as csvfile:
	reader = csv.DictReader(csvfile)
	for row in reader:
		newCsv.append(row)


base_tuple = ('Sku', 'ImageHeight', 'ImageWidth','Ratio', 'Aspect Ratio')

for i in range(len(sizes) * multiple):
	i += 1
 	base_tuple = base_tuple + ('Height' + str(i), 'Width' + str(i), 'SqIn' + str(i), 'SizeName' + str(i), 'UniqueSku' + str(i), 'Price' + str(i))

# initialize csv writer
writer = csv.writer(newFile)
writer.writerow(base_tuple)

# write the dictionary, do some calculations on the way
for item in newCsv:
	ImageWidth = float(item['ImageWidth'])
	ImageHeight = float(item['ImageHeight'])

	# keep the aspect ratio >= 1
	if ImageWidth >= ImageHeight:
		ratio = round((ImageWidth/ImageHeight), 2) 
	else: 
		ratio = round((ImageHeight/ImageWidth), 2) 

	ratio_info  = get_aspect_ratio(ratio)
	ratio_description = ratio_info[0]
	ratio = ratio_info[1]

	properties_list = []
	ratio_tuple = ('Ratio', ratio)
	aspect_ratio_tuple = ('Aspect Ratio', ratio_description)	

	properties_list.append(ratio_tuple)
	properties_list.append(aspect_ratio_tuple)
	
	if filetype == 'photo':
		if ratio <= 1.3:
			sizes = [8.0, 11.0, 16.0, 24.0, 32.0]
		elif ratio > 1.3 and ratio < 1.45:
			sizes = [11.0, 18.0, 24.0, 32.0]
		else:
			sizes = [8.0, 16.0, 20.0, 24.0, 32.0]
	count = 1;
	
	# only do one round for square ratios
	if ratio_description == "1:1" and filetype == 'map':
		polarity = 1
	else:
		polarity = 0

	while (polarity < 2):

		for size in sizes:		
		
			if(polarity == 0 and filetype == 'map'):
				size2 = size * (ratio)
				height = size2
				width = size

				# this function returns of tuple containing the fractional and integral part of the real number
				size2_split = math.modf(size2)
				decimal_part = size2_split[0]
				
				# round up from .3
				if decimal_part >= .3:
					size2 = math.ceil(size2)
				else:
					size2 = math.floor(size2)
			elif(polarity != 0 and filetype == 'map'):
				size2 = size * (1.0/ratio)
				# this function returns of tuple containing the fractional and integral part of the real number
				size2_split = math.modf(size2)
				decimal_part = size2_split[0]

				# round up from .3
				if decimal_part >= .3:
					size2 = math.ceil(size2)
				else:
					size2 = math.floor(size2)
			else:
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

			height = size
			width = size2

			# set the square inches
			square_inches = height * width

			if square_inches < 240 and filetype == 'map':
				item['SqIn' + str(count)] = str(square_inches)
				item['Price'+ str(count)] = ""
				item['Height'+ str(count)] = ""
				item['Width'+ str(count)] = ""
				item['UniqueSku'+ str(count)] = ""
				item['Size Name'+ str(count)] = ""

			elif square_inches >= 2400:
				item['SqIn' + str(count)] = str(square_inches)
				item['Price'+ str(count)] = ""
				item['Height'+ str(count)] = ""
				item['Width'+ str(count)] = ""
				item['UniqueSku'+ str(count)] = ""
				item['Size Name'+ str(count)] = ""

			else:
				sqin_tuple = ('SqIn' + str(count), square_inches)

				price = calculate_price(square_inches)
				price_tuple = ('Price'+ str(count), price)

				# get the string value
				height_str = str(height)
				width_str = str(width)

				height_tuple = ('Height'+ str(count), height_str)
				width_tuple = ('Width'+ str(count), width_str)

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
				new_sku = item['Sku'] + "_" + unique
				unique_sku_tuple = ('UniqueSku'+ str(count), item['Sku'] + "_" + unique)

				# create the size name
				size_name = width_int_str + "in" + " x " + height_int_str + "in"
				size_name_tuple = ('Size Name'+ str(count), size_name)
				
				properties_list.append(height_tuple)
				properties_list.append(width_tuple)
				properties_list.append(sqin_tuple)
				properties_list.append(size_name_tuple)
				properties_list.append(unique_sku_tuple)
				properties_list.append(price_tuple)
			count+=1

		# do not get inverted sizes for photos
		if filetype == 'photo':
			polarity+=2
		else:
			polarity+=1



	if filetype == 'map':
		write_tuple = (item['Sku'], item['ImageHeight'], item['ImageWidth'])

		for size in properties_list:
			write_tuple = write_tuple + (size[1],)

		writer.writerow(write_tuple)

	else:	

		write_tuple = (item['Sku'], item['ImageHeight'], item['ImageWidth'])

		for size in properties_list:
			write_tuple = write_tuple + (size[1],)

		writer.writerow(write_tuple)


	# this algorithm is ugly, improve when you can. Compares the square sizes within a specified range
	'''
	size_range = 1.33
	for i in range(len(sizes)):
		i+=1
		currentString = 'SqIn' + str(i)
		currentItem = item[currentString]

		for k in range(len(sizes)):
			k += 1
			nextString = 'SqIn' + str(k)
			nextItem = item[nextString]

			if currentItem is not nextItem:
				closeness = float(currentItem) / float (nextItem)
				if (closeness > (1.00/size_range)) and (closeness < (size_range/1.00)):
					print closeness
					item['Sku'] = "xxxxx"
	'''

			'''
		writer.writerow((item['Sku'], item['ImageHeight'], item['ImageWidth'],
			item['Ratio'], item['Aspect Ratio'], item['Height1'], item['Width1'], item['SqIn1'],
			item['Size Name1'], item['UniqueSku1'], item['Price1'],item['Height2'], item['Width2'], item['SqIn2'],
			item['Size Name2'], item['UniqueSku2'], item['Price2'], item['Height3'], item['Width3'], item['SqIn3'],
			item['Size Name3'], item['UniqueSku3'], item['Price3'], item['Height4'], item['Width4'], item['SqIn4'],
			item['Size Name4'], item['UniqueSku4'], item['Price4'], item['Height5'], item['Width5'], item['SqIn5'],
			item['Size Name5'], item['UniqueSku5'], item['Price5'], item['Height6'], item['Width6'], item['SqIn6'],
			item['Size Name6'], item['UniqueSku6'], item['Price6']))
		'''