#!/usr/bin/python
import csv, sys, math, operator, re, os, time
from utils import photo_sizer, map_sizer
from collections import deque

try:
	filename = sys.argv[1]
except:
	print "\nPlease input a valid CSV filename.\n"
	print "Format: python scriptname filename.\n"
	exit()

try:
	options = float(sys.argv[2])
except:
	options = 1000.0

newCsv = []

input_name = os.path.splitext(filename)[0]
output = 'AMZ_' + input_name + '_' + time.strftime("%m_%d_%Y") + '.csv'

newFile = open(output, 'wb') #wb for windows, else you'll see newlines added to csv
totallines = 0
# open the file from console arguments
with open(filename, 'rb') as csvfile:
	reader = csv.DictReader(csvfile)
	for row in reader:
		newCsv.append(row)
		totallines += 1

header_row1 = ('TemplateType=home', 'Version=2014.1119')

header_row2 = ('Item Type Keyword', 'Product Name', 'Product Description', 'Product Type', 
	'Brand Name', 'Manufacturer', 'Manufacturer Part Number', 'SKU', 'Parent SKU', 'Parentage', 'Relationship Type', 
	'Variation Theme', 'Size', 'Update Delete', 'Standard Price', 'Quantity', 'Product Tax Code', 'Package Quantity', 'Shipping Weight', 'Website Shipping Weight Unit Of Measure', 
	'Key Product Features1', 'Key Product Features2', 'Key Product Features3', 'Key Product Features4', 'Key Product Features5','Main Image URL', 'Shipping-Template', 'Search Terms')

header_row3 = ('item_type', 'item_name', 'product_description', 'feed_product_type', 
	'brand_name', 'manufacturer','part_number', 'item_sku', 'parent_sku','parent_child', 'relationship_type', 
	'variation_theme', 'size_name', 'update_delete', 'standard_price', 'Quantity', 'product_tax_code', 'item_package_quantity', 'website_shipping_weight', 'website_shipping_weight_unit_of_measure',
	'bullet_point1', 'bullet_point2', 'bullet_point3', 'bullet_point4', 'bullet_point5','main_image_url', 'merchant_shipping_group_name', 'generic_keywords1')

# initialize csv writer
writer = csv.writer(newFile)

# write the amazon headers
writer.writerow(header_row1)
writer.writerow(header_row2)
writer.writerow(header_row3)

bullet_point3 = "Perfect for the Home or Office. Makes a great gift!"
bullet_point4 = "100% Satisfaction Guaranteed."

count = 0;
mod = math.ceil(totallines/20.0)
percent = 0

#this deque  keeps track of duplicate item names, which causes problems on Amazon (and most likely elsewhere)
deque = deque( maxlen= 200)

for item in newCsv:
	
	#-------------------------- Progress Bar

	count += 1

	if count % mod == 0:
		percent += 5    
		sys.stdout.write("\r" + str(percent) + "% completed.")
		sys.stdout.flush()    	
	
	#-------------------------- General Fields Here

	try:
		sku = item['sku']
	except:
		try:
			sku = item['item_sku']
		except:
			try:
				sku = item['SKU']
			except:
				sku = item['Title']
	try:
		image_width = float(item['image_width'])
	except:
		try:
			image_width = float(item['ImageWidth'])
		except:
			print "Warning: image_width not formatted in SKU: " + sku
			continue

	try:
		image_height = float(item['image_height'])
	except:
		try:
			image_height = float(item['ImageHeight'])
		except:
			print "Warning: Image Height not formatted in SKU: " + sku
		continue

	try:
		image_name = item['image_name']
	except:
		try:
			image_name = item['ImageName']
		except:
			try:
				image_name = item['Image_Name']
			except:
				print "Warning: Image Name not formatted in SKU: " + sku
				continue
	try:
		item_name = item['item_name']
	except:
		try: 
			item_name = item['Title']
		except:
			try:
				item_name = item['title']
			except:
				print "Please format the input with a Title/ItemName Field"

	if len(item_name) > 188:
		print "Warning: Title/Item Name character count in SKU: " + sku + " exceeds 188 characters."
	
	# check if item_name already exists previously
	if item_name in deque:
		print ("\nError: duplicate item name in SKU: " + sku)
		exit()
	#
	deque.append(item_name)

	try:
		kind = item['kind']
	except:
		try:
			kind = item['Kind']
		except:
			print "Error: Format the input to include an item kind: Photos or Prints."
			exit()

	try:
		keywords = item['keywords']
	except:
		try:
			keywords = item['Keywords']
		except:
			print "Error: Format the input to include a Keywords/keywords field."
			exit()

	if len(keywords) > 250:
		print "Warning: Description character count in SKU: " + sku + " exceeds 250 characters."

	try:
		image_folder = item['image_folder']
	except:
		try:
			kind = item['ImageFolder']
		except:
			print "Error: Format the input to include an an image folder."
			exit()

	try:
		product_description = item['product_description'] 
	except:
		try:
			product_description = item['product description']
		except:
			print "Warning: No product description found for SKU: " + sku
	
	if len(product_description) > 2000:
		print "Error: Description character count in SKU: " + sku + " exceeds 2000 characters."
		exit()

	# size the image accordingly: map, photo, or print. Prints and photos share the same algorithm.
	if kind == "Map" or kind == "Maps":
		bullet_point1 = "Giclee Art Print on High Quality Matte Paper"
		bullet_point2 = "Professionally Printed Vintage Map Reproduction"
		item_sizes = map_sizer(image_height, image_width, sku)
	else:
		bullet_point1 = "Giclee Art Print on High Quality Archival Matte Paper"
		bullet_point2 = "Professionally Printed Vintage Fine Art Poster Reproduction"

		if kind == "Photograph" or kind == "Photo" or kind == "photo":
			bullet_point1 = "Giclee Photo Print on High Quality Archival Luster Photo Paper"
			bullet_point2 = "Professionally Printed Vintage Fine Art Photographic Reproduction"

		item_sizes = photo_sizer(image_height, image_width, sku)

	# 
	if options != "":
		options = int(options)	
		long_side_squared = options * options

		for i in xrange(len(item_sizes) -1, -1, -1):
			size = item_sizes[i]					
			sqin = int(size['SqIn'])
			if long_side_squared < sqin:
				del item_sizes[i]

	bullet_point5 = item_name	
	main_image_url = "www.historicpictoric.com/media" + image_folder +  image_name
	brand_name = 'Historic Pictoric'
	manufacturer = 'Historic Pictoric'
	feed_product_type = "art"
	variation_theme = "size"
	item_type = "prints"
	update_delete = ""

	#-------------------------- Generate Parent

	parent_sku = sku + "P"	
	part_number =  parent_sku 
	parent_child = "parent" 
	item_sku = parent_sku
	relationship_type = ""
	size_name = ""
	standard_price = ""
	quantity = ""
	product_tax_code = 'a_gen_tax'
	item_package_quantity = ""
	website_shipping_weight = ""
	website_shipping_weight_unit_of_measure = ""
	merchant_shipping_group_name = ""
	
	write_tuple = (item_type, item_name, product_description, feed_product_type, brand_name, manufacturer,
		part_number, item_sku, "", parent_child, relationship_type, variation_theme, size_name,
		update_delete, standard_price, quantity, product_tax_code, item_package_quantity, website_shipping_weight, 
		website_shipping_weight_unit_of_measure, bullet_point1, bullet_point2, bullet_point3, bullet_point4,
		bullet_point5, main_image_url, merchant_shipping_group_name, keywords)

	writer.writerow(write_tuple)

	#-------------------------- Generate Variations

	for size in item_sizes:
		part_number_str = re.sub('[ xin]', '', size['SizeName'])
		part_number =  sku + "_" + part_number_str
		parent_child = "" # leave blank for children
		item_sku = part_number
		relationship_type = "variation"
		size_name = size['SizeName']
		standard_price = size['Price']
		quantity = "10"
		item_package_quantity = "1"
		website_shipping_weight = "1"
		website_shipping_weight_unit_of_measure = "lbs"
		merchant_shipping_group_name = "Free_Economy_Shipping_16x20"
		item_name_with_size = item_name + " " + size_name
		
		write_tuple = (item_type, item_name_with_size, product_description, feed_product_type, brand_name, manufacturer,
			part_number, item_sku, parent_sku, parent_child, relationship_type, variation_theme, size_name,
			update_delete, standard_price, quantity, product_tax_code, item_package_quantity, website_shipping_weight, 
			website_shipping_weight_unit_of_measure, bullet_point1, bullet_point2, bullet_point3, bullet_point4,
			bullet_point5, main_image_url, merchant_shipping_group_name, keywords)

		writer.writerow(write_tuple)

		item_name_with_size = ""

print "\nFile written to " + output
newFile.close()