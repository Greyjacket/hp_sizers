#!/usr/bin/python
import csv, sys, math, operator, re, os
from utils import get_aspect_ratio, calculate_price, calculate_dimensions

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

	ratio = round((image_height/image_width), 2) 
	ratio_info  = get_aspect_ratio(ratio)
	ratio_description = ratio_info[0]
	ratio = ratio_info[1]

	properties_list = []
	aspect_ratio = ratio_description
	
	properties_list.append(str(ratio))
	properties_list.append(aspect_ratio)

	# only do one round for square ratios
	if ratio_description == "1:1":
		ratio = 1.0
		item_size = calculate_dimensions(16, 'up', ratio, sku)
		item_sizes.append(item_size)
		item_size = calculate_dimensions(24,'up', ratio, sku)
		item_sizes.append(item_size)
		item_size = calculate_dimensions(36,'up', ratio, sku)
		item_sizes.append(item_size)
		item_size = calculate_dimensions(44, 'up', ratio, sku)
		item_sizes.append(item_size)
	else:

		# calculate both orientations for 24s, 0 for portrait 1 for landscape
		item_size = calculate_dimensions(24, 'down',ratio, sku)
		if item_size:		
				item_sizes.append(item_size)
		
		item_size = calculate_dimensions(24, 'up',ratio, sku)

		if item_size:		
			item_sizes.append(item_size)

		item_size = calculate_dimensions(44, 'down', ratio, sku)

		# if it's a standard size, check if the 44 sized item is not too close in square inches
		if item_size and ratio <= 2.0 :	
			newItem = {}
			for other_item in item_sizes:
				square_inches_44 = item_size['SqIn']
				square_inches_24 = other_item['SqIn']

				if square_inches_44 >= square_inches_24:
					square_ratio = square_inches_44/square_inches_24
				else:
					square_ratio = square_inches_24/square_inches_44
				if square_ratio < ratio:
					newItem = calculate_dimensions(36, 'up', ratio, sku)
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
				try:
					comparison_sqin = float(comparison['Sqin'])
				except:
					print "Error reading SqIn value in Sku " + comparison['item_sku']
					comparison_sqin = 0

				comparison_price = comparison['standard_price']
				suggested_price = ""
				suggested_size = ""
				comparison_sizename = comparison['size_name Current']
				suggested_sqin = comparison_sqin

				size_match = False

				for key, value in suggestion.iteritems():
					if "SizeName" in key:
						if comparison_sizename == value:
							size_match = True

				if not size_match:
					smallest = 10000
					number = ""
					for key, value in suggestion.iteritems():
						if "SqIn" in key:
							if value is not None:
								temp_sqin = float(value)
								difference = abs(temp_sqin - comparison_sqin)
								if difference < smallest:
									smallest = difference
									number = str(re.findall(r'\d+', key)[0])
									suggested_sqin = temp_sqin

					size_name_key = 'SizeName' + number
					suggested_size = suggestion[size_name_key]
					write = True
				
				actual_price = str(calculate_price(suggested_sqin))

				if comparison_price != actual_price:
					suggested_price = actual_price
					write = True

				if(write):
					new_list.append(comparison['ParentSku'])
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

	os.remove('NewSizes_temp.csv')