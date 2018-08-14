import csv, sys, math, operator, re, os, time
from utils import photo_sizer, map_sizer, remove_bom_inplace
from row_reader import extract_items
from product_addition import description_text1, description_text2, description_text3
from collections import deque
from functools import reduce

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

# remove any BOMs
remove_bom_inplace(filename)
#------------------------------------------------------- Create write directory and filenames
input_name = os.path.splitext(filename)[0]

target_directory = 'AMZ_' + input_name
if not os.path.exists(target_directory):
    os.makedirs(target_directory)

upload_output = target_directory + '/AMZ_' + input_name + '_' + time.strftime("%m_%d_%Y") + '.csv'
delete_output = target_directory + '/AMZ_' + input_name + '_' + time.strftime("%m_%d_%Y") + '_delete.csv'
update_output = target_directory + '/AMZ_' + input_name + '_' + time.strftime("%m_%d_%Y") + '_update.csv'
error_output = target_directory + '/AMZ_' + input_name + '_' + time.strftime("%m_%d_%Y") + '_error.csv'

#------------------------------------------------------- Create target files
totallines = 0
newCsv = []

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

#------------------------------------------------------- write the amazon headers
upload_writer.writerow(header_row1)
upload_writer.writerow(header_row2)
upload_writer.writerow(header_row3)

header_row2 = ('Sku', 'Update Delete')
header_row3 = ('item_sku', 'update_delete')
delete_writer = csv.writer(delete_file)
delete_writer.writerow(header_row1)
delete_writer.writerow(header_row2)
delete_writer.writerow(header_row3)

header_row2 = ('SKU', 'Update Delete', 'Product Name', 'Product Description', 'Standard Price', 'Size', 'Key Product Features1', 'Key Product Features2', 'Key Product Features3', 'Key Product Features4', 'Key Product Features5', 'Subject Matter', 'Other Attributes')
header_row3 = ('item_sku', 'update_delete', 'item_name','product_description', 'standard_price', 'size_name', 'bullet_point1', 'bullet_point2', 'bullet_point3', 'bullet_point4', 'bullet_point5','thesaurus_subject_keywords1', 'thesaurus_attribute_keywords1')

update_writer = csv.writer(update_file)
update_writer.writerow(header_row1)
update_writer.writerow(header_row2)
update_writer.writerow(header_row3)

header_row2 = ('sku', 'Error', 'Field Value')
error_writer = csv.writer(error_file)
error_writer.writerow(header_row2)

price_list = []
upload_list = []
item_sizes = []
parent_name = ""
field_value = ""

#------------------------------------------------------- this deque  keeps track of duplicate item names
deque = deque(maxlen= 2000)

standard_size_names = ['08in x 10in', '08in x 12in', '11in x 14in', '16in x 20in',
						'18in x 24in', '16in x 24in', '24in x 30in', '24in x 36in', '10in x 08in', '12in x 08in',
						'14in x 11in', '20in x 16in', '24in x 18in', '24in x 16in', '30in x 24in', '36in x 24in']

count = 0;
mod = math.ceil(totallines/20.0)
percent = 0

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
		last_child = next_item['is_parent'] in ['True', 'true', 'TRUE', 't', 'T']
	except:
		next_item = None	
		last_child = True

	return_dict = extract_items(item)

	sku = return_dict['sku']
	item_name = return_dict['item_name']
	image_title = return_dict['image_title']
	keywords = return_dict['keywords']
	amz_description = return_dict['product_description']
	product_description_tagged = '<p>' + return_dict['image_description'] + '</p>'

	if len(product_description_tagged  + '<p>' + description_text1 + '</p>') <= 2000:
		correct_product_description = product_description_tagged  + '<p>' + description_text1 + '</p>'
	elif len(product_description_tagged  + '<p>' + description_text2 + '</p>') <= 2000:
		correct_product_description = product_description_tagged + '<p>' + description_text2 + '</p>'
	elif len(product_description_tagged  + '<p>' + description_text3 + '</p>') <= 2000:
		correct_product_description = product_description_tagged + '<p>' + description_text3 + '</p>'
	else:
		correct_product_description = product_description_tagged

	collection = return_dict['collection']
	category = return_dict['category']
	image_folder = return_dict['image_folder']
	image_filename = return_dict['image_filename']
	image_height = return_dict['image_height']
	image_width = return_dict['image_width']
	root_sku = return_dict['root_sku']

	if len(item_name) > 200:
		field_value = 'item_name'
		errormessage = "Error: AMZ item name character count in SKU: " + sku + " exceeds 200 characters."
		error_string = error_string + errormessage 
		print (errormessage)
	
	if len(image_title) > 188:
		field_value = 'image_title'
		errormessage = "Error: image_title character count in SKU: " + sku + " exceeds 188 characters."
		print (errormessage)
		error_string = error_string + errormessage 

	if len(keywords) > 250:
		errormessage = "Warning: Keywords character count in Amazon item: " + sku + " exceeds 250 characters."
		error_string = error_string + errormessage 

	if len(correct_product_description) > 2000:
		field_value = 'product_description'
		errormessage = "Warning: Product Description character count in SKU: " + sku + " exceeds 2000 characters."
		print (errormessage)
		error_string = error_string + errormessage 

	# stop here if there have not been any errors for this record.
	if error_string != "":
		error_tuple = (sku, error_string, field_value)
		error_writer.writerow(error_tuple)
		continue

	main_image_url = "###PATH###" + '/' + image_folder + '/' + image_filename
	brand_name = 'Historic Pictoric'
	manufacturer = 'Historic Pictoric'
	feed_product_type = "art"
	variation_theme = "size"
	item_type = "prints"
	update_delete = ""
	is_parent = True if item['is_parent'] in ['True', 'true', 'TRUE', 't', 'T'] else False
	unique = False
	
	if is_parent:

		is_map = True if category in ['Maps', 'maps', 'Map', 'map'] else False

		parent_name = sku
		parent_sku = sku 

		# size the image accordingly: map, photo, or print. Prints and photos share the same algorithm.
		if is_map:
			bullet_point1 = "Giclee Art Print on High Quality Matte Paper"
			bullet_point2 = "Professionally Printed Vintage Map Reproduction"
			item_sizes = map_sizer(image_height, image_width, root_sku)
		else:
			bullet_point1 = "Giclee Art Print on High Quality Archival Matte Paper"
			bullet_point2 = "Professionally Printed Vintage Fine Art Poster Reproduction"
			
			is_photograph = True if category in ['Photograph', 'Photos', 'Photo', 'photo', 'photos'] else False

			if is_photograph:
				bullet_point1 = "Giclee Photo Print on High Quality Archival Luster Photo Paper"
				bullet_point2 = "Professionally Printed Vintage Fine Art Photographic Reproduction"	
			
			item_sizes = photo_sizer(image_height, image_width, root_sku)

		if options:
			options = int(options)	
			long_side_squared = options * options

			for i in range(len(item_sizes) -1, -1, -1):
				size = item_sizes[i]					
				sqin = int(size['SqIn'])
				if long_side_squared < sqin:
					del item_sizes[i]

		if collection == "Biodiversity Library":
			bullet_point1 = "This is a high quality single print - NOT the entire catalog/magazine"
			bullet_point2 = "Professionally Printed Fine Art Reproduction - Giclee Art Print on High Quality Matte Paper"

		if item_name != image_title:
			update_tuple = (item['item_sku'], 'PartialUpdate', image_title, '', '', '', '', '', '', '', '', '', '')
			update_writer.writerow(update_tuple)

		# check if item is its own parent
		if next_item:
			unique = True if next_item['is_parent'] in ['True', 'true', 'TRUE', 't', 'T'] else False
		else:
			unique = True


	# ---------------------------------------- Validate children

	if not is_parent or unique:

		if item['image_sku_id'] == parent_name or (item['image_sku_id']+'P') == parent_name:

			item_size_name = item['size_name']	
			item_price = item['price']
			valid = False
			sales = float(item['sales'])
			closest_record = ''
			smallest_sqin = 100000			

			# validate size, titles, descriptions, prices against what it should be
			for i in range(len(item_sizes) -1, -1, -1):
				record = item_sizes[i]
				correct_size_name = record['SizeName']
				correct_item_name = image_title + " " + correct_size_name
				correct_price = record['Price']

				# this is to preserve sales history
				if correct_size_name != item_size_name:

					if sales > 0:
						size_values1 = [int(s) for s in item_size_name.replace('in', '').split() if s.isdigit()]
						size_values2 = [int(s) for s in correct_size_name.replace('in', '').split() if s.isdigit()]
						
						if not size_values1:
							item_size_name_adjusted = item_size_name.replace('x', ' x ')
							size_values1 = [int(s) for s in item_size_name_adjusted.replace('in', '').split() if s.isdigit()]

							if not size_values1:
								print('Error: Check size name of record: ' + item_sku + '. Value is: ' + item_size_name)
								exit()

						sqin1 = reduce(lambda x, y: x*y, size_values1)
						sqin2 = reduce(lambda x, y: x*y, size_values2)

						if abs(sqin2 - sqin1) <= smallest_sqin:
							smallest_sqin = abs(sqin2 - sqin1)
							closest_record = record

						# item is valid if orientation is wrong
						if set(size_values1).issubset(size_values2):
							valid = True
							del item_sizes[i]

							if correct_price != item_price or correct_item_name != item_name or correct_product_description != amz_description:
								update_tuple = (item['item_sku'], 'PartialUpdate', correct_item_name, correct_product_description, correct_price, correct_size_name, bullet_point1, bullet_point2, bullet_point3, bullet_point4, bullet_point5, collection, parent_sku)
								update_writer.writerow(update_tuple)
							
							else:
								update_tuple = (item['item_sku'], 'PartialUpdate', '', '', '', size_name, bullet_point1, bullet_point2, bullet_point3, bullet_point4, bullet_point5, collection, parent_sku)
								update_writer.writerow(update_tuple)	

				else:					
					valid = True	
					del item_sizes[i]

					if correct_size_name not in standard_size_names:
						bullet_point3 = "Perfect for the Home or Office. Makes a great gift!"
						bullet_point4 = "100% Satisfaction Guaranteed."
						bullet_point5 = image_title

					if correct_price != item_price or item_name != correct_item_name or product_description != amz_description:
						update_tuple = (item['item_sku'], 'PartialUpdate', correct_item_name, correct_product_description, correct_price, correct_size_name, bullet_point1, bullet_point2, bullet_point3, bullet_point4, bullet_point5, collection, parent_sku)
						update_writer.writerow(update_tuple)
			
			# clear the closest size if necessary (else we'll have duplicates)
			if not valid and sales > 0:
				valid = True
				for i in range(len(item_sizes) -1, -1, -1):
					record = item_sizes[i]
					if closest_record['SizeName'] == record['SizeName']:
						del item_sizes[i]

				correct_size_name = closest_record['SizeName']
				correct_item_name = image_title + " " + correct_size_name
				correct_price = closest_record['Price']

				if correct_size_name not in standard_size_names:
					bullet_point3 = "Perfect for the Home or Office. Makes a great gift!"
					bullet_point4 = "100% Satisfaction Guaranteed."
					bullet_point5 = image_title

				update_tuple = (item['item_sku'], 'PartialUpdate', correct_item_name, correct_product_description, correct_price, correct_size_name, bullet_point1, bullet_point2, bullet_point3, bullet_point4, bullet_point5, collection, parent_sku)
				update_writer.writerow(update_tuple)

			# delete if not valid and child is not its own parent
			if not valid and not unique:
				delete_tuple = (item['item_sku'], 'Delete')
				delete_writer.writerow(delete_tuple)	

			# check if we've reached the last child in the list
			if last_child:
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

					# check for duplication
					deque_tuple = (parent_sku,item_name_with_size)
					for item in deque:
						if item[1] == item_name_with_size: 
							error_tuple = (parent_sku, "Error: duplicate item name in child sku: " + part_number + '\n' + item_name_with_size + '.' +
								' Conflicting sku is: ' + item[0] + ' with item name: ' + item[1], 'item_name')
							error_writer.writerow(error_tuple)
					deque.append(deque_tuple)

					write_tuple = (item_type, item_name_with_size, correct_product_description, feed_product_type, brand_name, manufacturer,
						part_number, item_sku, parent_name, parent_child, relationship_type, variation_theme, size_name,
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