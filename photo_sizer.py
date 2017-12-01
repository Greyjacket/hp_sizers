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
newFile = open('NewSizes_Photos.csv', 'wb') #wb for windows, else you'll see newlines added to csv

# open the file from console arguments
with open(filename, 'rb') as csvfile:
	reader = csv.DictReader(csvfile)
	for row in reader:
		newCsv.append(row)

# initialize csv writer
writer = csv.writer(newFile)

base_tuple = ('Sku', 'ImageHeight', 'ImageWidth','Ratio', 'AspectRatio')

# set the field names
for i in range(5):
	i += 1
 	base_tuple = base_tuple + ('Height' + str(i), 'Width' + str(i), 'SqIn' + str(i), 'SizeName' + str(i), 'UniqueSku' + str(i), 'Price' + str(i))

writer.writerow(base_tuple)

# write the dictionary, do some calculations on the way
for item in newCsv:

	try:
		sku = item['Sku']
	except:
		try:
			sku = item['item_sku']
		except:
			try:
				sku = item['SKU']
			except:
				#print "Please format the CSV file with a Sku field. Try \"Sku\" or \"item sku\""
				sku = item['Title']
	try:
		image_width = float(item['ImageWidth'])
	except:
		print "ERROR: Image Width not formatted"
		exit()
	try:
		image_height = float(item['ImageHeight'])
	except:
		print "ERROR: Image Height not formatted"
		exit()

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

	properties_list = []	
	properties_list.append(str(ratio_rounded))
	properties_list.append(aspect_ratio)

	for size in sizes:
		if orientation == 'portrait':		
			item_size = calculate_photo_dimensions(size, 'portrait', ratio_rounded, sku)
		else:
			item_size = calculate_photo_dimensions(size, 'landscape',ratio_rounded, sku)

		if item_size:		
				item_sizes.append(item_size)
	
	item_sizes.sort(key=operator.itemgetter('SqIn'))

	write_tuple = (sku, item['ImageHeight'], item['ImageWidth'])

	for item in item_sizes:
		properties_list.append(item['Height'])
		properties_list.append(item['Width'])
		properties_list.append(str(item['SqIn']))
		properties_list.append(item['SizeName'])
		properties_list.append(item['UniqueSku'])
		properties_list.append(str(item['Price']))

	write_tuple = (sku, image_height, image_width)

	for item in properties_list:
		write_tuple = write_tuple + (item,)

	writer.writerow(write_tuple)

