#!/usr/bin/python
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

newCsv = []

input_name = os.path.splitext(filename)[0]
output = 'Ebay_' + input_name + '_' + time.strftime("%m_%d_%Y") + '.csv'

newFile = open(output, 'w') #wb for windows, else you'll see newlines added to csv
totallines = 0

# open the file from console arguments
with open(filename) as csvfile:
	reader = csv.DictReader(csvfile)
	for row in reader:
		newCsv.append(row)
		totallines += 1

header_row1 = ('*Action', 'Custom',	'CustomLabel', '*Category', 'StoreCategory', '*Title', 'Subtitle',	'Relationship', 'RelationshipDetails',	'C:Date of Creation', 'C:Originality',	'C:Listed By',	'C:Subject', 'C:Style',	'C:Size',
'C:Height (Inches)',	'C:Width (Inches)',	'C:Photo Type',	'C:Artist',	'C:Color',	'C:Color Type',	'C:Region of Origin',	'C:Features',	'C:Quantity Type',	'C:Year',	'PicURL',	'GalleryType',	'*Description',	'*Format',	'*Duration', '*StartPrice',	'BuyItNowPrice',	'*Quantity',	'PayPalAccepted',	'PayPalEmailAddress',	'ImmediatePayRequired',	'PaymentInstructions',	'*Location',	
'ShippingType',	'ShippingService-1:Option',	'ShippingService-1:Cost',	'ShippingService-2:Option',	'ShippingService-2:Cost',	'*DispatchTimeMax',	'PromotionalShippingDiscount',	'ShippingDiscountProfileID',	'DomesticRateTable',	'*ReturnsAcceptedOption',	'ReturnsWithinOption',	'RefundOption',	'ShippingCostPaidByOption',	'AdditionalDetails','UseTaxTable')

# initialize csv writer
writer = csv.writer(newFile)

# write the amazon headers
writer.writerow(header_row1)

#this deque  keeps track of duplicate item names, which causes problems on Amazon (and most likely elsewhere)
deque = deque( maxlen= 200)

standard_size_names = ['08in x 10in', '08in x 12in', '11in x 14in', '16in x 20in',
						'18in x 24in', '16in x 24in', '24in x 30in', '24in x 36in', '10in x 08in', '12in x 08in',
						'14in x 11in', '20in x 16in', '24in x 18in', '24in x 16in', '30in x 24in', '36in x 24in']
count = 0;
mod = math.ceil(totallines/20.0)
percent = 0

for item in newCsv:
	
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
				sku = item['Title']

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
		image_name = item['image_name']
	except:
		try:
			image_name = item['name']
		except:
			try:
				image_name = item['Image_Name']
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

	if item_name in deque:
		print ("\nError: duplicate item name in SKU: " + sku)
		exit()
	#
	deque.append(item_name)

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
			keywords = item['original_keywords']
		except:
			print ("Error: Format the input to include a Keywords/keywords field.")
			exit()

	if len(keywords) > 2000:
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
	
	if len(product_description) > 2000:
		print ("Error: Description character count in SKU: " + sku + " exceeds 2000 characters.")
		exit()

	# size the image accordingly: map, photo, or print. Prints and photos share the same algorithm.
	if kind == "Map" or kind == "Maps":
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

	# 
	if options != "":
		options = int(options)	
		long_side_squared = options * options

		for i in range(len(item_sizes) -1, -1, -1):
			size = item_sizes[i]					
			sqin = int(size['SqIn'])
			if long_side_squared < sqin:
				del item_sizes[i]

	pic_url = "www.historicpictoric.com/media" + image_folder +  image_name

	#-------------------------- Generate Parent
	relationship_details = "size="
	for size in item_sizes:
		relationship_details = relationship_details + size['SizeName'] + ';'
	relationship_details = relationship_details[:-1]
	relationship_details = relationship_details.replace(" ", "")
	parent_sku = sku 	
	parent_child = "parent" 
	item_sku = parent_sku
	relationship = ''
	size_name = ""
	standard_price = ""
	quantity = '100'
	paypal_accepted = '1'
	paypal_email = 'brian@historicpictoric.com'
	location = 'NY, USA'
	shipping_option = 'USPSFirstClass'
	shipping_cost = '0'
	dispatch_time_max = '2'
	returns_accepted = 'ReturnsAccepted'

	write_tuple = ('Add', parent_sku, item_sku, '98466', '', item_name, '',	relationship, relationship_details,	'', '',	'',	'', '',	'',
	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	pic_url, '', product_description,	'FixedPrice', 'GTC', standard_price, '', quantity,	paypal_accepted, paypal_email,	'',	'',	location,	
	'',	shipping_option, shipping_cost,	'',	'',	dispatch_time_max,	'',	'',	'',	returns_accepted,	'',	'',	'',	'','')

	writer.writerow(write_tuple)

	#-------------------------- Generate Variations

	for size in item_sizes:
		part_number_str = re.sub('[ xin]', '', size['SizeName'])
		part_number =  sku + "_" + part_number_str 
		size_name = size['SizeName']
		relationship_details = "size=" + size_name
		relationship_details = relationship_details.replace(" ", "")
		relationship = "Variation"
		parent_child = "" # leave blank for children
		item_sku = part_number
		standard_price = size['Price']
		item_name_with_size = item_name + " " + size_name
		
		write_tuple = ('Add', parent_sku, item_sku, '98466', '', item_name_with_size, '',	relationship, relationship_details,	'', '',	'',	'', '',	'',
		'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	pic_url, '', product_description,	'FixedPrice', 'GTC', standard_price, '', quantity,	paypal_accepted, paypal_email,	'',	'',	location,	
		'',	shipping_option, shipping_cost,	'',	'',	dispatch_time_max,	'',	'',	'',	returns_accepted,	'',	'',	'',	'','')
	
		writer.writerow(write_tuple)

print ("\nFile written to " + output)
newFile.close()