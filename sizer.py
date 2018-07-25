#!/usr/bin/python
import csv, sys, math, operator, re, os, time
from utils import photo_sizer, map_sizer, remove_bom_inplace
from collections import deque
from product_addition import description_text1, description_text2, description_text3

try:
	filename = sys.argv[1]
except:
	print ("\nPlease input a valid CSV filename.\n")
	print ("Format: python scriptname filename.\n")
	exit()

try:
	options = float(sys.argv[2])
except:
	options = 1000.0

newCsv = []

# remove any BOMs
remove_bom_inplace(filename)

input_name = os.path.splitext(filename)[0]
output = 'AMZ_' + input_name + '_' + time.strftime("%m_%d_%Y") + '.csv'

if os.name is 'nt':
	newFile = open(output, 'wb') #wb for windows, else you'll see newlines added to csv
else:
	newFile = open(output, 'w') 

totallines = 0

# open the file from console arguments
with open(filename, 'rt') as csvfile:
	reader = csv.DictReader(csvfile)
	for row in reader:
		newCsv.append(row)
		totallines += 1

header_row1 = ('TemplateType=home', 'Version=2014.1119')

header_row2 = ('Item Type Keyword', 'Product Name', 'Product Description', 'Product Type', 
	'Brand Name', 'Manufacturer', 'Manufacturer Part Number', 'SKU', 'Parent SKU', 'Parentage', 'Relationship Type', 
	'Variation Theme', 'Size', 'Update Delete', 'Standard Price', 'Quantity', 'Product Tax Code', 'Package Quantity', 'Shipping Weight', 'Website Shipping Weight Unit Of Measure', 
	'Key Product Features1', 'Key Product Features2', 'Key Product Features3', 'Key Product Features4', 'Key Product Features5','Main Image URL', 'Shipping-Template', 'Search Terms', 'Subject Matter', 'Other Attributes')

header_row3 = ('item_type', 'item_name', 'product_description', 'feed_product_type', 
	'brand_name', 'manufacturer','part_number', 'item_sku', 'parent_sku','parent_child', 'relationship_type', 
	'variation_theme', 'size_name', 'update_delete', 'standard_price', 'Quantity', 'product_tax_code', 'item_package_quantity', 'website_shipping_weight', 'website_shipping_weight_unit_of_measure',
	'bullet_point1', 'bullet_point2', 'bullet_point3', 'bullet_point4', 'bullet_point5','main_image_url', 'merchant_shipping_group_name', 'generic_keywords1', 'thesaurus_subject_keywords1', 'thesaurus_attribute_keywords1')

# initialize csv writer
# writer = csv.writer(newFile, delimiter='\t')
writer = csv.writer(newFile)

# write the amazon headers
writer.writerow(header_row1)
writer.writerow(header_row2)
writer.writerow(header_row3)

#this deque  keeps track of duplicate item names, which causes problems on Amazon (and most likely elsewhere)
deque = deque( maxlen= 2000)

standard_size_names = ['08in x 10in', '08in x 12in', '11in x 14in', '16in x 20in',
						'18in x 24in', '16in x 24in', '24in x 30in', '24in x 36in', '10in x 08in', '12in x 08in',
						'14in x 11in', '20in x 16in', '24in x 18in', '24in x 16in', '30in x 24in', '36in x 24in']
count = 0;
mod = math.ceil(totallines/20.0)
percent = 0

for item in newCsv:
	
	bullet_point3 = 'Ready to Frame - Fits Standard Size Frames'
	bullet_point4 = "Perfect for the Home or Office. Makes a great gift!"
	bullet_point5 = "100% Satisfaction Guaranteed."

	#-------------------------- Progress Bar

	count += 1

	if count % mod == 0:
		percent += 5    
		sys.stdout.write("\r" + str(percent) + "% completed.")
		sys.stdout.flush()    	
	
	#-------------------------- General Fields Here

	try:			
		sku = item['item_sku']
	except:
		try:
			sku = item['sku']
		except:
			try:
				sku = item['SKU']
			except:
				print ("No item sku found in input. There may be a BOM in the input, or the header row may not be formatted correctly.")
				exit()

	try:
		image_width = float(item['image_width'])
	except:
		try:
			image_width = float(item['width'])
		except:
			print ("Warning: image_width not formatted in SKU: " + sku)
			continue

	try:
		image_height = float(item['image_height'])
	except:
		try:
			image_height = float(item['height'])
		except:
			print ("Warning: Image Height not formatted in SKU: " + sku)
			continue

	try:
		image_filename = item['image_name']
	except:
		try:
			image_filename = item['name']
		except:
			try:
				image_filename = item['Image_Name']
			except:
				print ("Warning: Image Name not formatted in SKU: " + sku)
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
				print ("Please format the input with a Title/ItemName Field")

	if len(item_name) > 188:
		print ("Warning: Title/Item Name character count in SKU: " + sku + " exceeds 188 characters.")
	
	try:
		kind = item['kind']
	except:
		try:
			kind = item['Kind']
		except:
			try:
				kind = item['category']				
			except:
				print ("Error: Format the input to include an item kind or category: Photos, Maps or Prints.")
				exit()

	try:
		collection = item['collection']
	except:
		try:
			collection = item['Collection']
		except:
			collection = ""
			print ("Warning: No collection specified in Sku: " + sku)

	try:
		root_sku = item['root_sku']
	except:
		root_sku = ""	
		print ("Warning: No root_sku specified in Sku: " + sku)

	try:
		keywords = item['keywords']
	except:
		try:
			keywords = item['Keywords']
		except:
			print ("Error: Format the input to include a Keywords/keywords field.")
			exit()

	if len(keywords) > 250:
		print ("Warning: Keyword character count in SKU: " + sku + " exceeds 250 characters.")

	try:
		image_folder = item['image_folder']
	except:
		try:
			kind = item['ImageFolder']
		except:
			print ("Error: Format the input to include an an image folder.")
			exit()

	try:
		product_description = item['product_description'] 
	except:
		try:
			product_description = item['product description']
		except:
			print ("Warning: No product description found for SKU: " + sku)
	
	product_description_tagged = '<p>' + product_description + '</p>'

	# add product disclaimer, shorten if necessary
	if len(product_description_tagged  + '<p>' + description_text1 + '</p>') <= 2000:
		correct_product_description = product_description_tagged  + '<p>' + description_text1 + '</p>'
	elif len(product_description_tagged  + '<p>' + description_text2 + '</p>') <= 2000:
		correct_product_description = product_description_tagged + '<p>' + description_text2 + '</p>'
	elif len(product_description_tagged  + '<p>' + description_text3 + '</p>') <= 2000:
		correct_product_description = product_description_tagged + '<p>' + description_text3 + '</p>'
	else:
		correct_product_description = product_description_tagged

	product_description = correct_product_description

	# size the image accordingly: map, photo, or print. Prints and photos share the same algorithm.
	if kind == "Map" or kind == "Maps" or kind == "maps" or kind == "maps":
		bullet_point1 = "Giclee Art Print on High Quality Matte Paper"
		bullet_point2 = "Professionally Printed Vintage Map Reproduction"
		item_sizes = map_sizer(image_height, image_width, sku)
	else:
		bullet_point1 = "Giclee Art Print on High Quality Archival Matte Paper"
		bullet_point2 = "Professionally Printed Vintage Fine Art Poster Reproduction"

		if kind == "Photograph" or kind == "Photo" or kind == "photo" or kind == "photos":
			bullet_point1 = "Giclee Photo Print on High Quality Archival Luster Photo Paper"
			bullet_point2 = "Professionally Printed Vintage Fine Art Photographic Reproduction"

		item_sizes = photo_sizer(image_height, image_width, sku)
 
	if options != "":
		options = int(options)	
		long_side_squared = options * options

		for i in range(len(item_sizes) -1, -1, -1):
			size = item_sizes[i]					
			sqin = int(size['SqIn'])
			if long_side_squared < sqin:
				del item_sizes[i]

	main_image_url = image_folder + '/' + image_filename
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
		bullet_point5, main_image_url, merchant_shipping_group_name, keywords, collection, root_sku)

	writer.writerow(write_tuple)

	#-------------------------- Generate Variations

	for size in item_sizes:
		part_number_str = re.sub('[ xin]', '', size['SizeName'])
		part_number =  sku + "_" + part_number_str
		parent_child = "" # leave blank for children
		item_sku = part_number
		relationship_type = "variation"
		size_name = size['SizeName']

		# check if size is standard, if not, change the bullets.
		if size_name not in standard_size_names:

			bullet_point3 = "Perfect for the Home or Office. Makes a great gift!"
			bullet_point4 = "100% Satisfaction Guaranteed."
			bullet_point5 = item_name

		standard_price = size['Price']
		quantity = "10"
		item_package_quantity = "1"
		website_shipping_weight = "1"
		website_shipping_weight_unit_of_measure = "lbs"
		merchant_shipping_group_name = "Free_Economy_Shipping_16x20"
		item_name_with_size = item_name + " " + size_name

		# check for duplication
		deque_tuple = (sku,item_name_with_size)
		for item in deque:
			if item[1] == item_name_with_size: 
				print('Warning: Duplicate found in skus: ' + sku +' and ' + item[0])
		deque.append(deque_tuple)


		write_tuple = (item_type, item_name_with_size, product_description, feed_product_type, brand_name, manufacturer,
			part_number, item_sku, parent_sku, parent_child, relationship_type, variation_theme, size_name,
			update_delete, standard_price, quantity, product_tax_code, item_package_quantity, website_shipping_weight, 
			website_shipping_weight_unit_of_measure, bullet_point1, bullet_point2, bullet_point3, bullet_point4,
			bullet_point5, main_image_url, merchant_shipping_group_name, keywords, collection, root_sku)

		writer.writerow(write_tuple)

		item_name_with_size = ""

print ("\nFile written to " + output)
newFile.close()