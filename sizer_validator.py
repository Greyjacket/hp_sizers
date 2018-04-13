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

fieldnames = ['item_sku']
writer = csv.DictWriter(newFile, fieldnames=fieldnames)
writer.writeheader()

count = 0;
mod = math.ceil(totallines/20.0)
percent = 0

#this deque  keeps track of duplicate item names, which causes problems on Amazon (and most likely elsewhere)
price_list = []

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

	try:
		kind = item['kind']
	except:
		try:
			kind = item['Kind']
		except:
			print "Error: Format the input to include an item kind: Photos or Prints."
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

	# ---------------------------------------- Validation here
	item_size_name = item['size_name']	
	item_price = item['price']
	valid = False
	
	for sku in item_sizes:
		if sku['SizeName'] == "":
			continue
		if sku['SizeName'] == item_size_name:
			valid = True			
			if sku['Price'] != item_price:
				price_list.append(sku)

	if valid == False:
		writer.writerow({'item_sku': item['item_sku']})

print "\nFile written to " + output
newFile.close()