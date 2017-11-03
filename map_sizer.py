#!/usr/bin/python
import csv, sys, math, operator
from utils import get_aspect_ratio, calculate_price

def calculate_dimensions(size, orientation):
	item_size = {}

	if(orientation == 0):
		size2 = size * (ratio)
	else:
		size2 = size * (1.0/ratio)

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

	if(orientation == 0):
		height = size
		width = size2
	else:
		height = size2
		width = size

	# set the square inches
	square_inches = height * width
	if square_inches > 240 and square_inches <= 2400:

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
		
		item_size['Height'] = height_str
		item_size['Width'] = width_str
		item_size['SqIn'] = square_inches
		item_size['SizeName'] = size_name
		item_size['UniqueSku'] = unique_sku
		item_size['Price'] = price

		return item_size

try:
	filename = sys.argv[1]
except:
	print "\nPlease input a valid CSV filename.\n"
	print "Format: python scriptname filename.\n"
	exit()

# change the base number to scale by, depending on map or photo
sizes = [24.0, 36.0, 44.0]

newCsv = []
newFile = open('NewSizes.csv', 'wb') #wb for windows, else you'll see newlines added to csv
# open the file from console arguments
with open(filename, 'rb') as csvfile:
	reader = csv.DictReader(csvfile)
	for row in reader:
		newCsv.append(row)

base_tuple = ('Sku', 'ImageHeight', 'ImageWidth','Ratio', 'Aspect Ratio')

for i in range(len(sizes) * 2):
	i += 1
 	base_tuple = base_tuple + ('Height' + str(i), 'Width' + str(i), 'SqIn' + str(i), 'SizeName' + str(i), 'UniqueSku' + str(i), 'Price' + str(i))

# initialize csv writer
writer = csv.writer(newFile)
writer.writerow(base_tuple)

# write the dictionary, do some calculations on the way
for item in newCsv:
	try:
		image_width = float(item['ImageWidth'])
	except:
		image_width = 1.0
	try:
		image_height = float(item['ImageHeight'])
	except:
		image_height = 1.0

	sku = item['Sku']
	item_sizes = []

	# keep the aspect ratio >= 1

	if image_width >= image_height:
		ratio = round((image_width/image_height), 2) 
	else: 
		ratio = round((image_height/image_width), 2) 

	ratio_info  = get_aspect_ratio(ratio)

	# if we encountered an exception note it in the record
	if image_width == 1.0:
		ratio_description = "error"
	else:
		ratio_description = ratio_info[0]
		ratio = ratio_info[1]

	properties_list = []
	aspect_ratio = ratio_description
	
	properties_list.append(str(ratio))
	properties_list.append(aspect_ratio)

	# only do one round for square ratios
	if ratio_description == "1:1":
		orientation = 1
		item_size = calculate_dimensions(24, orientation)
		item_sizes.append(item_size)
		item_size = calculate_dimensions(36, orientation)
		item_sizes.append(item_size)
		item_size = calculate_dimensions(44, orientation)
		item_sizes.append(item_size)
	else:
		orientation = 0

		while (orientation < 2):
			item_size = calculate_dimensions(24, orientation)
			if item_size:		
				item_sizes.append(item_size)
			orientation+=1
		
		item_size = calculate_dimensions(44, 1)

		if item_size:	
			newItem = {}
			for item in item_sizes:
				square_inches1 = item['SqIn']
				square_inches2 = item_size['SqIn']

				if square_inches1 >= square_inches2:
					square_ratio = square_inches1/square_inches2
				else:
					square_ratio = square_inches2/square_inches1
				if square_ratio < ratio:
					newItem = calculate_dimensions(36, 0)
					break
				else:
					newItem = item_size

			if newItem:
				item_sizes.append(newItem)

	item_sizes.sort(key=operator.itemgetter('SqIn'))
	
	for item in item_sizes:
		properties_list.append(item['Height'])
		properties_list.append(item['Width'])
		properties_list.append(str(item['SqIn']))
		properties_list.append(item['SizeName'])
		properties_list.append(item['UniqueSku'])
		properties_list.append(str(item['Price']))

	write_tuple = (sku, image_height, image_width)

	for item in properties_list:
		write_tuple = write_tuple + (item,)

	writer.writerow(write_tuple)
