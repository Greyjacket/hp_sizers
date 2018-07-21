import csv, sys, math, operator, re, os, time
from utils import photo_sizer, map_sizer
from row_reader import extract_items
from product_addition import description_text
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

#------------------------------------------------------- Create write directory and filenames
input_name = os.path.splitext(filename)[0]

target_directory = 'AMZ_' + input_name
if not os.path.exists(target_directory):
    os.makedirs(target_directory)

update_output = target_directory + '/AMZ_' + input_name + '_' + time.strftime("%m_%d_%Y") + '_update_description.csv'

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

update_file = open(update_output, 'w', newline='', encoding="utf-8")

#------------------------------------------------------- write the amazon headers
header_row1 = ('TemplateType=home', 'Version=2014.1119')
header_row2 = ('SKU', 'Update Delete', 'Product Description')
header_row3 = ('item_sku', 'update_delete','product_description')
update_writer = csv.writer(update_file)
update_writer.writerow(header_row1)
update_writer.writerow(header_row2)
update_writer.writerow(header_row3)


price_list = []
upload_list = []
item_sizes = []
parent_name = ""
field_value = ""

for i in range(len(newCsv)):
	item = newCsv[i]

	try:			
		sku = item['item_sku']
	except:
		try:
			sku = item['sku']
		except:
			try:
				sku = item['SKU']
			except:
				print( "Error: Couldn't find a sku field.")
				exit()
	try:
		product_description = item['product_description'] 
	except:
		errormessage = "Error: No product description found for SKU: " + item['sku']
		print (errormessage)
		exit()

	if len(product_description) < 1000:
		product_description = product_description + '<p>' + description_text + '</p>'
		update_tuple = (sku, 'PartialUpdate', product_description)
		update_writer.writerow(update_tuple)

update_file.close()
