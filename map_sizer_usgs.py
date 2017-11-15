#!/usr/bin/python
import csv, sys, math, operator, re, os
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

write_filename = 'USGS.csv'

newCsv = []
newFile = open(write_filename, 'wb') #wb for windows, else you'll see newlines added to csv
# open the file from console arguments
with open(filename, 'rb') as csvfile:
	reader = csv.DictReader(csvfile)
	for row in reader:
		newCsv.append(row)

# write amazon's headers
header_row1 = ('TemplateType=home', 'Version=2014.1119')

header_row2 = ('Item Type Keyword', 'Product Name', 'Product Description', 'Product Type', 
	'Brand Name', 'Manufacturer', 'Manufacturer Part Number', 'Parentage', 'SKU', 'Parent SKU', 'Relationship Type', 
	'Variation Theme', 'Size', 'Standard Price', 'Quantity', 'Product Tax Code', 'Package Quantity', 'Shipping Weight', 'Website Shipping Weight Unit Of Measure', 
	'Key Product Features1', 'Key Product Features2', 'Key Product Features3', 'Key Product Features4', 'Key Product Features5','Main Image URL')

header_row3 = ('item_type', 'item_name', 'product_description', 'feed_product_type', 
	'brand_name', 'manufacturer', 'part_number', 'parent_child', 'item_sku', 'parent_sku', 'relationship_type', 
	'variation_theme', 'size_name', 'standard_price', 'Quantity', 'product_tax_code', 'item_package_quantity', 'website_shipping_weight', 'website_shipping_weight_unit_of_measure',
	'bullet_point1', 'bullet_point2', 'bullet_point3', 'bullet_point4', 'bullet_point5','main_image_url')

# initialize csv writer
writer = csv.writer(newFile)

# write the amazon headers
writer.writerow(header_row1)
writer.writerow(header_row2)
writer.writerow(header_row3)

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

	aspect_ratio = ratio_description

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
				square_inches1 = item_size['SqIn']
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

	write_tuple = (sku, image_height, image_width)

	for item in properties_list:
		write_tuple = write_tuple + (item,)

	writer.writerow(write_tuple)

newFile.close()
