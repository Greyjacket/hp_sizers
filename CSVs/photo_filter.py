#!/usr/bin/python
import csv, sys, math, operator, re, os
from utils import get_aspect_ratio, calculate_price, calculate_photo_dimensions

try:
	filename = sys.argv[1]
except:
	print "\nPlease input a valid CSV filename.\n"
	print "Format: python scriptname filename.\n"
	exit()

newCsv = []
newFile = open('filtered_photos.csv', 'wb') #wb for windows, else you'll see newlines added to csv

# open the file from console arguments
with open(filename, 'rb') as csvfile:
	reader = csv.DictReader(csvfile)
	for row in reader:
		newCsv.append(row)

# write amazon's headers
header_row1 = ('TemplateType=home', 'Version=2014.1119')

header_row2 = ('Item Type Keyword', 'Product Name', 'Product Description', 'Product Type', 
	'Brand Name', 'Manufacturer', 'Manufacturer Part Number', 'SKU', 'Parent SKU', 'Parentage', 'Relationship Type', 
	'Variation Theme', 'Size', 'Update Delete', 'Standard Price', 'Quantity', 'Product Tax Code', 'Package Quantity', 'Shipping Weight', 'Website Shipping Weight Unit Of Measure', 
	'Key Product Features1', 'Key Product Features2', 'Key Product Features3', 'Key Product Features4', 'Key Product Features5','Main Image URL', 'Shipping-Template', 'Search Terms')

header_row3 = ('item_type', 'item_name', 'product_description', 'feed_product_type', 
	'brand_name', 'manufacturer', 'part_number', 'item_sku', 'parent_sku','parent_child', 'relationship_type', 
	'variation_theme', 'size_name', 'update_delete', 'standard_price', 'Quantity', 'product_tax_code', 'item_package_quantity', 'website_shipping_weight', 'website_shipping_weight_unit_of_measure',
	'bullet_point1', 'bullet_point2', 'bullet_point3', 'bullet_point4', 'bullet_point5','main_image_url', 'merchant_shipping_group_name', 'generic_keywords')

# initialize csv writer
writer = csv.writer(newFile)

# write the amazon headers
writer.writerow(header_row1)
writer.writerow(header_row2)
writer.writerow(header_row3)

# write the dictionary, do some calculations on the way
for item in newCsv:	
	if item['Type'] != "Photograph":
		continue
	
	try:
		sku = item['Sku']
	except:
		try:
			sku = item['item_sku']
		except:
			try:
				sku = item['SKU']
			except:
				print "Please format the CSV file with a Sku field. Try \"Sku\" or \"item sku\""
				exit()

	try:
		image_width = float(item['ImageWidth'])
	except:
		try:
			image_width = float(item['Width'])
		except:			
			print "ERROR: Image Width not formatted: use ImageWidth or Width"
			exit()
	try:
		image_height = float(item['ImageHeight'])
	except:
		try:
			image_height = float(item['Height'])
		except:
			print "ERROR: Image Height not formatted: use ImageHeight or Height."
			exit()

	# keep the aspect ratio >= 1
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

	aspect_ratio = ratio_description
	
	if ratio_rounded < 1.2:
		sizes = [16.0, 24.0, 36.0]
	elif ratio_rounded >= 1.2 and ratio_rounded <= 1.3:
		sizes = [11.0, 16.0, 24.0, 36.0]
	elif ratio_rounded > 1.3 and ratio_rounded <= 1.45:
		sizes = [11.0, 18.0, 24.0]
	elif ratio_rounded > 1.45 and ratio_rounded <= 1.9:
		sizes = [8.0, 16.0, 24.0, 30]
	else:
		sizes = [16.0, 24.0, 36.0]

	for size in sizes:
		if orientation == 'portrait':		
			item_size = calculate_photo_dimensions(size, 'portrait', ratio_rounded, sku)
		else:
			item_size = calculate_photo_dimensions(size, 'landscape',ratio_rounded, sku)

		if item_size:		
				item_sizes.append(item_size)
	
	item_sizes.sort(key=operator.itemgetter('SqIn'))

# ------------------------------------------------------------------------------------ filter here
	smallest = 10000
	number = ""

	try:
		comparison_sqin = float(item['SqIn'])
	except:
		try:
			comparison_sqin = float(item['Sq in'])
		except:
			print "Please format the square inch field: \"SqIn\""

	for testsize in item_sizes:
		temp_sqin = float(testsize['SqIn'])
		difference = abs(temp_sqin - comparison_sqin)
		if difference < smallest:
			smallest = difference
			suggested_sizename = testsize['SizeName']

# ------------------------------------------------------------------------------------ end filter

	bullet_point1 = "Frame Ready - Professionally Restored Photograph"
	bullet_point2 = "High Quality Giclee Art Print - Printed on Museum Quality Luster PhotoPaper"
	bullet_point3 = "Ships Flat - Ready to Frame - Fits Standard Size Frames"
	bullet_point4 = "100% Satisfaction Guaranteed"
	bullet_point5 = ""
	keywords = item_name = item['Keywords']
	#part_number = item['Manufacturer#']

# if single, create a parent sku
	if item['Relationship'] == 'Single':
		parent_sku = sku + "P"
		item_type = "Photograph"
		item_name = item['Title']
		product_description = "<p>" + item['Title'] + "</p>"
		feed_product_type = "art"
		brand_name = 'Historic Pictoric'
		manufacturer = 'Historic Pictoric'
		part_number =  parent_sku 
		parent_child = "parent" # leave blank for children
		item_sku = parent_sku
		relationship_type = ""
		variation_theme = "size"
		size_name = ""
		update_delete = ""
		standard_price = ""
		quantity = ""
		product_tax_code = ""
		item_package_quantity = ""
		website_shipping_weight = ""
		website_shipping_weight_unit_of_measure = ""
		merchant_shipping_group_name = ""
		validated = 'N/A'

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

		main_image_url = "www.historicpictoric.com/media/AMZWebImg/SoldProductsUpdate/" + image_name
		
		write_tuple = (item_type, item_name, product_description, feed_product_type, brand_name, manufacturer,
			part_number, item_sku, "", parent_child, relationship_type, variation_theme, size_name,
			update_delete, standard_price, quantity, product_tax_code, item_package_quantity, website_shipping_weight, 
			website_shipping_weight_unit_of_measure, bullet_point1, bullet_point2, bullet_point3, bullet_point4,
			bullet_point5, main_image_url, merchant_shipping_group_name, keywords, validated)

		writer.writerow(write_tuple)

	for size in item_sizes:
		item_type = "Photograph"
		item_name = item['Title']
		product_description = "<p>" + item['Title'] + "</p>"
		feed_product_type = "art"
		item_sku = sku
		#part_number = sku
		# item_sku = sku + "_" + part_number_str

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

		number1 = str(re.findall(r'\d+', size['SizeName'])[0])
		number2 = str(re.findall(r'\d+', size['SizeName'])[1])

		# format the size names so that they're all alike
		formatted_sizename = re.sub('[ xin]', '', size['SizeName2'])
		formatted_comparison = re.sub('[ xin]', '', item_sizename)
		part_number_str = re.sub('[ xin]', '', size['SizeName'])

		if size['SizeName'] == suggested_sizename:
			parent_child = "" # leave blank for children
			part_number = item['Manufacturer#']
			item_sku =  sku
			validated = True
			update_delete = "PartialUpdate"
			size_name = item_sizename
		else:
			parent_child = "" # leve blank for children
			part_number =  sku + "_" + part_number_str
			item_sku = sku + "_" + part_number_str
			size_name = size['SizeName']
			validated = False
			update_delete = ""

		
		relationship_type = "variation"
		variation_theme = "size"
		# size_name = size['SizeName']
		#size_name = item_sizename
		standard_price = size['Price']
		quantity = "10"
		product_tax_code = 'a_gen_tax'
		item_package_quantity = "1"
		website_shipping_weight = "1"
		website_shipping_weight_unit_of_measure = "lbs"
		bullet_point5 = item_name
		merchant_shipping_group_name = "Free_Economy_Shipping_16x20"

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
		
		if item['Option'] == 'Validate Only' and validated == False:
			continue

		# ignore sizes going up from 44 if the option is set
		if item['Option'] == '<=44':
			if int(number1) > 44 or int(number2) > 44:
				continue

		write_tuple = (item_type, item_name, product_description, feed_product_type, brand_name, manufacturer,
			part_number, item_sku, parent_sku, parent_child, relationship_type, variation_theme, size_name,
			update_delete, standard_price, quantity, product_tax_code, item_package_quantity, website_shipping_weight, 
			website_shipping_weight_unit_of_measure, bullet_point1, bullet_point2, bullet_point3, bullet_point4,
			bullet_point5, main_image_url, merchant_shipping_group_name, keywords, validated)

		writer.writerow(write_tuple)

newFile.close()

