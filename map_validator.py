#!/usr/bin/python
import csv, sys, math, operator, re, os
from utils import get_aspect_ratio, calculate_price, calculate_dimensions

try:
	filename = sys.argv[1]
except:
	print "\nPlease input a valid CSV filename.\n"
	print "Format: python scriptname filename operation.\n"
	exit()

write_filename = 'size_validated_maps.csv'

newCsv = []
newFile = open(write_filename, 'wb') #wb for windows, else you'll see newlines added to csv
# open the file from console arguments
with open(filename, 'rb') as csvfile:
	reader = csv.DictReader(csvfile)
	for row in reader:
		newCsv.append(row)

# write amazon's headers
header_row1 = ('TemplateType=home', 'Version=2014.1119')

header_row2 = ('SKU','Size', 'Size Corrected', 'Update Delete', 'Standard Price')

header_row3 = ('item_sku','size_name', 'size_name2', 'update_delete', 'standard_price')

# initialize csv writer
writer = csv.writer(newFile)

# write the amazon headers
writer.writerow(header_row1)
writer.writerow(header_row2)
writer.writerow(header_row3)

# write the dictionary, do some calculations on the way

for item in newCsv:

	if item['Type'] != "Maps":
		continue

	try:
		sku = item['item_sku']
	except:
		try:
			sku = item['SKU']
		except:
			print "Please format the CSV file with a Sku field. Try \"Sku\" or \"item sku\""
			continue

	try:
		image_width = float(item['ImageWidth'])
	except:
		try:
			image_width = float(item['Width'])
		except:			
			print "ERROR: Image Width not formatted: use ImageWidth or Width. Check Sku " + sku
			continue
	try:
		image_height = float(item['ImageHeight'])
	except:
		try:
			image_height = float(item['Height'])
		except:
			print "ERROR: Image Height not formatted: use ImageHeight or Height. Check Sku " + sku
			exit()

	try:
		item_sizename = item['Size Name']
	except:
		try:
			item_sizename = item['SizeName']
		except:
			try:
				item_sizename = item['Size_Name']
			except:
				print "Please format the SizeName field of your input: SizeName, Size Name, or Size_Name"
	
	item_sizes = []

	if image_height > image_width:
		ratio_raw = round((image_height/image_width), 2) 
		orientation = 'portrait'
	else:
		ratio_raw = round((image_width/image_height), 2) 
		orientation = 'landscape'

	ratio_info  = get_aspect_ratio(ratio_raw)
	ratio_description = ratio_info[0]
	ratio_rounded = ratio_info[1]
	aspect_ratio = ratio_description

	if orientation == 'landscape':
		ratio_normalized = 1.0/ratio_rounded
	else:
		ratio_normalized = ratio_rounded

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
		item_size = calculate_dimensions(24, 'down',ratio_normalized, sku)
		if item_size:		
				item_sizes.append(item_size)
		
		item_size = calculate_dimensions(24, 'up',ratio_normalized, sku)

		if item_size:		
			item_sizes.append(item_size)

		item_size = calculate_dimensions(44, 'down', ratio_normalized, sku)

		# if it's a standard size, check if the 44 sized item is not too close in square inches
		if item_size and ratio_raw <= 2.0 :	
			newItem = {}
			for other_item in item_sizes:
				square_inches_44 = item_size['SqIn']
				square_inches_24 = other_item['SqIn']

				if square_inches_44 >= square_inches_24:
					square_ratio = square_inches_44/square_inches_24
				else:
					square_ratio = square_inches_24/square_inches_44
				if square_ratio < ratio_raw:
					newItem = calculate_dimensions(36, 'up', ratio_normalized, sku)
					break
				else:
					newItem = item_size
			if newItem:
				item_sizes.append(newItem)
		else:
			if item_size:		
				item_sizes.append(item_size)

		item_size = calculate_dimensions(44, 'up', ratio_normalized, sku)

		if item_size:
			item_sizes.append(item_size)
	
	item_sizes.sort(key=operator.itemgetter('SqIn'))

# ------------------------------------------------------------------------------------ filter here
	smallest = 10000
	number = ""
	index = 0
	try:
		comparison_sqin = float(item['SqIn'])
	except:
		try:
			comparison_sqin = float(item['Sq in'])
		except:
			extracted_sizes = re.findall(r'\d+', item_sizename)
			comparison_sqin = float(extracted_sizes[0]) * float(extracted_sizes[1])


	for testsize in item_sizes:
		temp_sqin = float(testsize['SqIn'])
		difference = abs(temp_sqin - comparison_sqin)
		if difference < smallest:
			smallest = difference
			suggested_sizename = testsize['SizeName']
			found_index = index
		index += 1

# ------------------------------------------------------------------------------------ end filter
	try:
		image_name = item['ImageName']
	except:
		try:
			image_name = item['Image Name']
		except:
			try:
				image_name = item['Image_Name']
			except:
				print "Please format the ImageName field: ImageName. Image Name, or Image_Name."
				exit()
	
	item_name = item['Title']
	bullet_point1 = "Professionally Printed Vintage Map Reproduction"
	bullet_point2 = "Giclee Art Print - Printed on High Quality Matte Paper"
	bullet_point3 = "Perfect for the Home or Office. Makes a great gift!"
	bullet_point4 = "100% Satisfaction Guaranteed"
	bullet_point5 = item_name
	keywords = item['Keywords']
	brand_name = 'Historic Pictoric'
	manufacturer = 'Historic Pictoric'
	main_image_url = "www.historicpictoric.com/media/AMZWebImg/SoldProductsUpdate/" + image_name
	item_type = "prints"

	for size in item_sizes:
		item_type = "prints"
		product_description = "<p>" + item['Title'] + "</p>"
		feed_product_type = "art"		

		number1 = str(re.findall(r'\d+', size['SizeName'])[0])
		number2 = str(re.findall(r'\d+', size['SizeName'])[1])

		# format the size names so that they're all alike
		formatted_sizename = re.sub('[ xin]', '', size['SizeName2'])
		formatted_comparison = re.sub('[ xin]', '', item_sizename)
		part_number_str = re.sub('[ xin]', '', size['SizeName'])

		# this is the origin sku 
		if size['SizeName'] == suggested_sizename:
			item_sku =  sku
			update_delete = "PartialUpdate"
			size_name = item_sizename
			size_name_correct = size['SizeName']
			standard_price = size['Price']			
			
			write_tuple = (item_sku, size_name,size_name_correct,update_delete,standard_price)

			writer.writerow(write_tuple)

newFile.close()
