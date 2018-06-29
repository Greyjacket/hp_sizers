import csv, sys, math, operator, re, os, time
from utils import photo_sizer, map_sizer
from collections import deque

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

try:
	check_titles = (sys.argv[3])
except:
	check_titles = ""

newCsv = []

input_name = os.path.splitext(filename)[0]
upload_output = 'AMZ_' + input_name + '_' + time.strftime("%m_%d_%Y") + '.csv'
delete_output = 'AMZ_' + input_name + '_' + time.strftime("%m_%d_%Y") + '_delete.csv'
update_output = 'AMZ_' + input_name + '_' + time.strftime("%m_%d_%Y") + '_update.csv'
error_output = 'AMZ_' + input_name + '_' + time.strftime("%m_%d_%Y") + '_error.csv'

totallines = 0
# open the file from console arguments
if os.name is 'nt':
	with open(filename, 'r', encoding="utf-8") as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			newCsv.append(row)
			totallines += 1
else:
	with open(filename, 'r', encoding="utf-8") as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			newCsv.append(row)
			totallines += 1	

delete_file = open(delete_output, 'w', newline='', encoding="utf-8") 
upload_file = open(upload_output, 'w', newline='', encoding="utf-8") 
update_file = open(update_output, 'w', newline='', encoding="utf-8")
error_file = open(error_output, 'w', newline='', encoding="utf-8")

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
upload_writer = csv.writer(upload_file)

# write the amazon headers
upload_writer.writerow(header_row1)
upload_writer.writerow(header_row2)
upload_writer.writerow(header_row3)

# write the amazon headers
header_row2 = ('SKU', 'Update Delete')
header_row3 = ('item_sku', 'update_delete')
delete_writer = csv.writer(delete_file)
delete_writer.writerow(header_row1)
delete_writer.writerow(header_row2)
delete_writer.writerow(header_row3)

#header_row2 = ('SKU', 'Update Delete', 'Product Name', 'Product Description', 'Standard Price', 'Key Product Features1', 'Key Product Features2', 'Key Product Features3', 'Key Product Features4', 'Key Product Features5')
#header_row3 = ('item_sku', 'update_delete', 'item_name','product_description', 'standard_price' 'bullet_point1', 'bullet_point2', 'bullet_point3', 'bullet_point4', 'bullet_point5')
header_row2 = ('SKU', 'Update Delete', 'Product Name', 'Product Description', 'Standard Price')
header_row3 = ('item_sku', 'update_delete', 'item_name','product_description', 'standard_price')
update_writer = csv.writer(update_file)
update_writer.writerow(header_row1)
update_writer.writerow(header_row2)
update_writer.writerow(header_row3)

header_row2 = ('SKU', 'Error')
error_writer = csv.writer(error_file)
error_writer.writerow(header_row2)

count = 0;
mod = math.ceil(totallines/20.0)
percent = 0

price_list = []
upload_list = []
item_sizes = []
parent_name = ""

#this deque  keeps track of duplicate item names, which causes problems on Amazon (and most likely elsewhere)
deque = deque(maxlen= 200)

standard_size_names = ['08in x 10in', '08in x 12in', '11in x 14in', '16in x 20in',
						'18in x 24in', '16in x 24in', '24in x 30in', '24in x 36in', '10in x 08in', '12in x 08in',
						'14in x 11in', '20in x 16in', '24in x 18in', '24in x 16in', '30in x 24in', '36in x 24in']

#for item in newCsv:

for i in range(len(newCsv)):

	error_string = "" 

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
	item = newCsv[i]
	try:
		next_item = newCsv[i+1]
	except:
		next_item = None
	
	try:			
		sku = item['item_sku']
	except:
		try:
			sku = item['sku']
		except:
			try:
				sku = item['SKU']
			except:
				print( "Warning: Couldn't find a sku field.")
				exit()

	try:
		image_width = float(item['image_width'])
	except:
		try:
			image_width = float(item['width'])
		except:
			errormessage = "Warning: image_width not formatted in SKU: " + sku
			print (errormessage)
			error_string = error_string + errormessage

	try:
		image_height = float(item['image_height'])
	except:
		try:
			image_height = float(item['height'])
		except:
			errormessage = "Warning: Image Height not formatted in SKU: " + sku
			print (errormessage)
			error_string = error_string + errormessage + '. '

	try:
		image_filename = item['image_filename']
	except:
		try:
			image_filename = item['name']
		except:
			try:
				image_filename = item['Image_Name']
			except:
				errormessage = "Warning: Image Name not formatted in SKU: " + sku
				print (errormessage)
				error_string = error_string + errormessage + '. '
	try:
		item_name = item['item_name']
	except:
		try: 
			item_name = item['Title']
		except:
			try:
				item_name = item['title']
			except:
				errormessage = "Error: Please format the input with an item_name Field in SKU: " + sku
				print (errormessage)
				error_string = error_string + errormessage + '. '
	
	if len(item_name) > 200:
		errormessage = "Error: Title/Item Name character count in SKU: " + sku + " exceeds 200 characters."
		print (errormessage)

	try:
		image_title = item['image_title']
	except:
			errormessage = "Error: Please format the input with an image_title Field in SKU: " + sku
			print (errormessage)
			error_string = error_string + errormessage + '. '
	
	if len(image_title) > 188:
		errormessage = "Error: image_title character count in SKU: " + sku + " exceeds 188 characters."
		print (errormessage)
		error_string = error_string + errormessage + '. '


	if check_titles != "":
		if item_name in deque:
			print ("\nError: duplicate item name in SKU: " + sku)
			exit()
		deque.append(item_name)
	
	try:
		kind = item['kind']
	except:
		try:
			kind = item['Kind']
		except:
			try:
				kind = item['category']				
			except:
				errormessage = "Error: Format the input to include an item kind or category: Photos, Maps or Prints in SKU: " + sku 
				print (errormessage)
				error_string = error_string + errormessage + '. '

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
		if len(keywords) > 250:
			errormessage = "Warning: Keywords character count in Amazon item: " + sku + " exceeds 250 characters. Falling back to image original."
			error_string = error_string + errormessage + '. '
			try:
				keywords = item['original_keywords']
				if len(keywords) > 250:
					errormessage = "Warning: Keywords character count in Image item: " + item['sku'] + " exceeds 250 characters. Falling back to image original."
					error_string = error_string + errormessage + '. '					
			except:
				print ("Error: Format the input to include an original_keywords field.")
				exit()
	except:
		print ("Error: Format the input to include a keywords field.")
		exit()	

	try:
		image_folder = item['image_folder']
	except:
		try:
			kind = item['ImageFolder']
		except:
			image_folder = ""

	try:
		product_description = item['product_description'] 
	except:
		try:
			product_description = item['product description']
		except:
			errormessage = "Warning: No product description found for SKU: " + sku
			print (errormessage)
			error_string = error_string + errormessage + '. '

	if len(product_description) > 2000:
		errormessage = "Error: Description character count in SKU: " + sku + " exceeds 2000 characters."
		print (errormessage)
		error_string = error_string + errormessage + '. '

	# stop here if there have not been any errors for this record.
	if error_string != "":
		error_tuple = (sku, error_string)
		error_writer.writerow(error_tuple)
		continue

	main_image_url = "www.historicpictoric.com/media" + '/' + image_folder + '/' + image_filename
	brand_name = 'Historic Pictoric'
	manufacturer = 'Historic Pictoric'
	feed_product_type = "art"
	variation_theme = "size"
	item_type = "prints"
	update_delete = ""
	unique = False

	if item['is_parent'] == 't' or item['is_parent'] == 'TRUE':
		parent_name = sku
		parent_sku = sku 
		# size the image accordingly: map, photo, or print. Prints and photos share the same algorithm.
		if kind == "Map" or kind == "Maps":
			bullet_point1 = "Giclee Art Print on High Quality Matte Paper"
			bullet_point2 = "Professionally Printed Vintage Map Reproduction"
			item_sizes = map_sizer(image_height, image_width, root_sku)
		else:
			bullet_point1 = "Giclee Art Print on High Quality Archival Matte Paper"
			bullet_point2 = "Professionally Printed Vintage Fine Art Poster Reproduction"

			if kind == "Photograph" or kind == "Photo" or kind == "photo" or kind == "photos":
				bullet_point1 = "Giclee Photo Print on High Quality Archival Luster Photo Paper"
				bullet_point2 = "Professionally Printed Vintage Fine Art Photographic Reproduction"

			item_sizes = photo_sizer(image_height, image_width, root_sku)

		if options != "":
			options = int(options)	
			long_side_squared = options * options

			for i in range(len(item_sizes) -1, -1, -1):
				size = item_sizes[i]					
				sqin = int(size['SqIn'])
				if long_side_squared < sqin:
					del item_sizes[i]

		if item_name != image_title or product_description != item['image_description']:
			update_tuple = (item['item_sku'], 'PartialUpdate', image_title, item['image_description'])
			update_writer.writerow(update_tuple)


	# ---------------------------------------- Validate parent

		# check next item
		if next_item != None:

			if (next_item['is_parent'] == 't' or next_item['is_parent'] == 'TRUE'):
				unique = True

			'''
			parent_sku = parent_name 
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
			update_delete = "PartialUpdate"

			
			write_tuple = (item_type, image_title, product_description, feed_product_type, brand_name, manufacturer,
				part_number, item_sku, "", parent_child, relationship_type, variation_theme, size_name,
				update_delete, standard_price, quantity, product_tax_code, item_package_quantity, website_shipping_weight, 
				website_shipping_weight_unit_of_measure, bullet_point1, bullet_point2, bullet_point3, bullet_point4,
				bullet_point5, main_image_url, merchant_shipping_group_name, keywords, collection, root_sku)

			upload_list.append(write_tuple)
			'''

	# ---------------------------------------- Validate children

	if (item['is_parent'] != 't' and item['is_parent'] != 'TRUE') or unique == True:

		if item['image_sku_id'] == parent_name:
			#validate the sizenames
			item_size_name = item['size_name']	
			item_price = item['price']
			valid = False

			# validate size, titles, descriptions, prices against what it should be
			for i in range(len(item_sizes) -1, -1, -1):
				record = item_sizes[i]

				if record['SizeName'] == item_size_name:
					valid = True	
					del item_sizes[i]
					item_name_with_size = image_title + " " + record['SizeName']			
					if record['Price'] != item_price or item_name != item_name_with_size or product_description != item['image_description']:
						update_tuple = (item['item_sku'], 'PartialUpdate', item_name_with_size, item['image_description'], record['Price'])
						update_writer.writerow(update_tuple)

			if valid == False and unique == False:
				delete_tuple = (item['item_sku'], 'Delete')
				delete_writer.writerow(delete_tuple)	

			if next_item != None:
				if next_item['is_parent'] == 't' or next_item['is_parent'] == 'TRUE':
					for size in item_sizes:
						part_number_str = re.sub('[ xin]', '', size['SizeName'])
						part_number =  root_sku + "_" + part_number_str
						parent_child = "" # leave blank for children
						item_sku = part_number
						relationship_type = "variation"
						size_name = size['SizeName']
						standard_price = size['Price']
						quantity = "10"
						item_package_quantity = "1"
						website_shipping_weight = "1"
						product_tax_code = 'a_gen_tax'
						website_shipping_weight_unit_of_measure = "lbs"
						merchant_shipping_group_name = "Free_Economy_Shipping_16x20"
						item_name_with_size = image_title + " " + size_name
						
						# check if size is standard, if not, change the bullets.
						if size_name not in standard_size_names:

							bullet_point3 = "Perfect for the Home or Office. Makes a great gift!"
							bullet_point4 = "100% Satisfaction Guaranteed."
							bullet_point5 = image_title

						write_tuple = (item_type, item_name_with_size, item['image_description'], feed_product_type, brand_name, manufacturer,
							part_number, item_sku, parent_sku, parent_child, relationship_type, variation_theme, size_name,
							update_delete, standard_price, quantity, product_tax_code, item_package_quantity, website_shipping_weight, 
							website_shipping_weight_unit_of_measure, bullet_point1, bullet_point2, bullet_point3, bullet_point4,
							bullet_point5, main_image_url, merchant_shipping_group_name, keywords, collection, root_sku)
						upload_list.append(write_tuple)
			else:
				for size in item_sizes:
					part_number_str = re.sub('[ xin]', '', size['SizeName'])
					part_number =  root_sku + "_" + part_number_str
					parent_child = "" # leave blank for children
					item_sku = part_number
					relationship_type = "variation"
					size_name = size['SizeName']
					standard_price = size['Price']
					quantity = "10"
					item_package_quantity = "1"
					website_shipping_weight = "1"
					product_tax_code = 'a_gen_tax'
					website_shipping_weight_unit_of_measure = "lbs"
					merchant_shipping_group_name = "Free_Economy_Shipping_16x20"
					item_name_with_size = image_title + " " + size_name
					update_delete = ""

					# check if size is standard, if not, change the bullets.
					if size_name not in standard_size_names:

						bullet_point3 = "Perfect for the Home or Office. Makes a great gift!"
						bullet_point4 = "100% Satisfaction Guaranteed."
						bullet_point5 = image_title	

					write_tuple = (item_type, item_name_with_size, item['image_description'], feed_product_type, brand_name, manufacturer,
						part_number, item_sku, parent_sku, parent_child, relationship_type, variation_theme, size_name,
						update_delete, standard_price, quantity, product_tax_code, item_package_quantity, website_shipping_weight, 
						website_shipping_weight_unit_of_measure, bullet_point1, bullet_point2, bullet_point3, bullet_point4,
						bullet_point5, main_image_url, merchant_shipping_group_name, keywords, collection, root_sku)

					upload_list.append(write_tuple)					

for record in upload_list:
	upload_writer.writerow(record)

print ("\nFile written to " + upload_output)
print ("\nFile written to " + delete_output)
print ("\nFile written to " + update_output)
print ("\nFile written to " + error_output)

upload_file.close()
delete_file.close()
update_file.close()
error_file.close()