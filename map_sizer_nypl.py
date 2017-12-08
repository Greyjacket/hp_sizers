#!/usr/bin/python
import csv, sys, math, operator, re, os
from utils import get_aspect_ratio, calculate_price, calculate_dimensions


try:
	filename = sys.argv[1]
except:
	print "\nPlease input a valid CSV filename.\n"
	print "Format: python scriptname filename operation.\n"
	exit()

#filename = './CSVs/nypl_sample.csv'
write_filename = 'NYPL.csv'

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
	'Brand Name', 'Manufacturer', 'Manufacturer Part Number', 'SKU', 'Parent SKU', 'Parentage', 'Relationship Type', 
	'Variation Theme', 'Size', 'Update Delete', 'Standard Price', 'Quantity', 'Product Tax Code', 'Package Quantity', 'Shipping Weight', 'Website Shipping Weight Unit Of Measure', 
	'Key Product Features1', 'Key Product Features2', 'Key Product Features3', 'Key Product Features4', 'Key Product Features5','Main Image URL', 'Shipping-Template', 'Search Terms')

header_row3 = ('item_type', 'item_name', 'product_description', 'feed_product_type', 
	'brand_name', 'manufacturer', 'part_number', 'item_sku', 'parent_sku','parent_child', 'relationship_type', 
	'variation_theme', 'size_name', 'update_delete', 'standard_price', 'Quantity', 'product_tax_code', 'item_package_quantity', 'website_shipping_weight', 'website_shipping_weight_unit_of_measure',
	'bullet_point1', 'bullet_point2', 'bullet_point3', 'bullet_point4', 'bullet_point5','main_image_url', 'merchant_shipping_group_name', 'generic_keywords1')

# initialize csv writer
writer = csv.writer(newFile)

# write the amazon headers
writer.writerow(header_row1)
writer.writerow(header_row2)
writer.writerow(header_row3)

# write the dictionary, do some calculations on the way

for item in newCsv:

	try:
		sku = item['Sku']
	except:
		try:
			sku = item['item_sku']
		except:
			print "Please format the CSV file with a Sku field. Try \"Sku\" or \"item sku\""
			exit()

	try:
		image_width = float(item['ImageWidth'])
	except:
		image_width = 1.0
	try:
		image_height = float(item['ImageHeight'])
	except:
		image_height = 1.0

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

	parent_sku = sku + "P"

	item_type = "prints"
	item_name = item['Item Name']
	product_description = "<p>" + item['product_description'] + "</p>"
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
	bullet_point1 = "Professionally Printed Vintage Map Reproduction"
	bullet_point2 = "Giclee Art Print - Printed on High Quality Matte Paper"
	bullet_point3 = "Perfect for the Home or Office. Makes a great gift!"
	bullet_point4 = "100% Satisfaction Guaranteed"
	bullet_point5 = item_name
	merchant_shipping_group_name = ""
	keywords = item['Generic Keywords']
	
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

	main_image_url = "www.historicpictoric.com/media/AMZWebImg/NYPL/NYPL_New/" + image_name
	
	write_tuple = (item_type, item_name, product_description, feed_product_type, brand_name, manufacturer,
		part_number, item_sku, "", parent_child, relationship_type, variation_theme, size_name,
		update_delete, standard_price, quantity, product_tax_code, item_package_quantity, website_shipping_weight, 
		website_shipping_weight_unit_of_measure, bullet_point1, bullet_point2, bullet_point3, bullet_point4,
		bullet_point5, main_image_url, merchant_shipping_group_name, keywords)

	writer.writerow(write_tuple)

	for size in item_sizes:
		item_type = "prints"
		item_name = item['Item Name']
		product_description = "<p>" + item['product_description'] + "</p>"
		feed_product_type = "art"
		part_number_str = re.sub('[ xin]', '', size['SizeName'])
		part_number =  sku + "_" + part_number_str
		parent_child = "" # leave blank for children
		item_sku = sku + "_" + part_number_str
		relationship_type = "variation"
		variation_theme = "size"
		size_name = size['SizeName']
		update_delete = ""
		standard_price = size['Price']
		quantity = "10"
		product_tax_code = 'a_gen_tax'
		item_package_quantity = "1"
		website_shipping_weight = "1"
		website_shipping_weight_unit_of_measure = "lbs"
		bullet_point1 = "Professionally Printed Vintage Map Reproduction"
		bullet_point2 = "Giclee Art Print - Printed on High Quality Matte Paper"
		bullet_point3 = "Perfect for the Home or Office. Makes a great gift!"
		bullet_point4 = "100% Satisfaction Guaranteed"
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
		
		write_tuple = (item_type, item_name, product_description, feed_product_type, brand_name, manufacturer,
			part_number, item_sku, parent_sku, parent_child, relationship_type, variation_theme, size_name,
			update_delete, standard_price, quantity, product_tax_code, item_package_quantity, website_shipping_weight, 
			website_shipping_weight_unit_of_measure, bullet_point1, bullet_point2, bullet_point3, bullet_point4,
			bullet_point5, main_image_url, merchant_shipping_group_name, keywords)

		writer.writerow(write_tuple)

newFile.close()
