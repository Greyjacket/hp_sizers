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
	print "Format: python scriptname filename operation.\n"
	exit()

try:
	operation = sys.argv[2]
except:
	operation = ""

if operation == "filter":
	write_filename = 'NewSizes_temp.csv'
else:
	write_filename = 'NewSizes.csv'

# change the base number to scale by, depending on map or photo
sizes = [24.0, 36.0, 44.0]

newCsv = []
newFile = open(write_filename, 'wb') #wb for windows, else you'll see newlines added to csv
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

	try:
		sku = item['Sku']
	except:
		try:
			sku = item['item_sku']
		except:
			print "Please format the CSV file with a Sku field. Try \"Sku\" or \"item sku\""
			break

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
		item_size = calculate_dimensions(16, orientation)
		item_sizes.append(item_size)
		item_size = calculate_dimensions(24, orientation)
		item_sizes.append(item_size)
		item_size = calculate_dimensions(36, orientation)
		item_sizes.append(item_size)
		item_size = calculate_dimensions(44, orientation)
		item_sizes.append(item_size)
	else:
		orientation = 0

		# calculate both orientations for 24s, 0 for portrait 1 for landscape
		while (orientation < 2):
			item_size = calculate_dimensions(24, orientation)
			if item_size:		
				item_sizes.append(item_size)
			orientation+=1
		
		item_size = calculate_dimensions(44, 1)

		# if it's a standard size, check if the 44 sized item is not too close in square inches
		if item_size and ratio <= 2.0 :	
			newItem = {}
			for other_item in item_sizes:
				square_inches1 = other_item['SqIn']
				square_inches2 = other_item['SqIn']

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
		else:
			if item_size:		
				item_sizes.append(item_size)

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

newFile.close()

if operation == "filter":
	
	suggestions = []
	with open(write_filename, 'rb') as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			suggestions.append(row)
	
	comparisons = []
	with open(filename, 'rb') as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			comparisons.append(row)

	newFile = open("Filtered.csv", 'wb') #wb for windows, else you'll see newlines added to csv
	base_tuple = ('parent Sku', 'item_sku', 'relationship_type', 'Image Name','Image Height', 
		'Image Width', 'Ratio', 'size_name_current', 'size_name_suggested', 'current_price', 'suggested_price')

	# initialize csv writer
	writer = csv.writer(newFile)
	writer.writerow(base_tuple)

	for suggestion in suggestions:
		new_item = {}
		new_list =[]
		write = False;

		for comparison in comparisons:
			if suggestion['Sku'] == comparison['item_sku']:

				comparison_price = comparison['standard_price']
				comparison_sqin = float(comparison['Sq in'])
				actual_price = str(calculate_price(comparison_sqin))
				suggested_price = ""
				suggested_size = ""

				price_match = False

				if comparison_price != actual_price:
					suggested_price = actual_price
					write = True

				comparison_sizename = comparison['size_name Current']
				
				size_match = False

				size_list = []
				for key, value in suggestion.iteritems():
					if "SizeName" in key:
						if value is not None:
							size_list.append(value)
						if comparison_sizename == value:
							size_match = True

				if not size_match:
					suggested_size = "To be Done"
					write = True

				if(write):
					new_list.append(comparison['Parent Sku'])
					new_list.append(comparison['item_sku'])
					new_list.append(comparison['relationship_type'])
					new_list.append(comparison['ImageName'])
					new_list.append(comparison['ImageHeight'])
					new_list.append(comparison['ImageWidth'])
					new_list.append(comparison['ratio'])
					new_list.append(comparison_sizename)
					new_list.append(suggested_size)
					new_list.append(comparison_price)	
					new_list.append(suggested_price)	
		
		if(write):
			write_tuple = ()
			for item in new_list:
				write_tuple = write_tuple + (item,)
			writer.writerow(write_tuple)

	# print item['Size chk 1']
	#for key, value in item.iteritems():
	#	print key
