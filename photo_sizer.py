#!/usr/bin/python
import csv, sys, math
from utils import get_aspect_ratio, calculate_price

try:
	filename = sys.argv[1]
except:
	print "\nPlease input a valid CSV filename.\n"
	print "Format: python scriptname filename.\n"
	exit()

sizes = [8.0, 11.0, 16.0, 24.0, 32.0]

newCsv = []
newFile = open('NewSizes.csv', 'wb') #wb for windows, else you'll see newlines added to csv

# open the file from console arguments
with open(filename, 'rb') as csvfile:
	reader = csv.DictReader(csvfile)
	for row in reader:
		newCsv.append(row)

base_tuple = ('Sku', 'ImageHeight', 'ImageWidth','Ratio', 'AspectRatio')

# set the field names
for i in range(len(sizes)):
	i += 1
 	base_tuple = base_tuple + ('Height' + str(i), 'Width' + str(i), 'SqIn' + str(i), 'SizeName' + str(i), 'UniqueSku' + str(i), 'Price' + str(i))

# initialize csv writer
writer = csv.writer(newFile)
writer.writerow(base_tuple)

# write the dictionary, do some calculations on the way
for item in newCsv:
	try:
		image_width = float(item['ImageWidth'])
	except:
		image_width = 1.0
	try:
		image_height = float(item['ImageHeight'])
	except:
		image_height = 1.0

	# keep the aspect ratio >= 1
	if image_width >= image_height:
		ratio = round((image_width/image_height), 2) 
	else: 
		ratio = round((image_height/image_width), 2) 

	ratio_info  = get_aspect_ratio(ratio)
	ratio_description = ratio_info[0]
	ratio = ratio_info[1]

	properties_list = []
	aspect_ratio = ratio_description
	
	properties_list.append(str(ratio))
	properties_list.append(aspect_ratio)
	
	if ratio <= 1.3:
		sizes = [8.0, 11.0, 16.0, 24.0, 32.0]
	elif ratio > 1.3 and ratio < 1.45:
		sizes = [11.0, 18.0, 24.0, 32.0]
	else:
		sizes = [8.0, 16.0, 20.0, 24.0, 32.0]

	for size in sizes:		
		if ratio <= 1.3:
			if size == 8.0:
				size2 = 10.0
			elif size == 11.0:
				size2 = 14.0
			elif size == 16.0:
				size2 = 20.0
			elif size == 24.0:
				size2 = 30.0
			else:
				size2 = 40.0
		elif ratio > 1.3 and ratio < 1.45:
			if size == 11.0:
				size2 = 14.0
			elif size == 18.0:
				size2 = 24.0
			elif size == 24.0:
				size2 = 32.0
			else:
				size2 = 43.0
		else:
			if size == 8.0:
				size2 = 12.0
			elif size == 16.0:
				size2 = 24.0
			elif size == 20.0:
				size2 = 30.0
			elif size == 24.0:
				size2 = 36.0
			else:
				size2 = 44.0

		height = size
		width = size2

		# set the square inches
		square_inches = height * width

		price = calculate_price(square_inches)

		# get the string value
		height_str = str(height)
		width_str = str(width)

		int_str1 = str(int(width))
		int_str2 = str(int(height))

		unique1 = int_str1
		unique2 = int_str2

		width_int_str = str(int(width))
		height_int_str = str(int(height))

		# pad a single digit with a zero if need be
		if len(width_int_str) < 2:
			unique1 = "0" + int_str1
		if len(height_int_str) < 2:
			unique2 = "0" + int_str2

		# create the unique sku
		unique = unique1 + unique2
		unique_sku = item['Sku'] + "_" + unique

		# create the size name
		size_name = width_int_str + "in" + " x " + height_int_str + "in"	

		properties_list.append(height_str)
		properties_list.append(width_str)
		properties_list.append(str(square_inches))
		properties_list.append(size_name)
		properties_list.append(unique_sku)
		properties_list.append(str(price))

	write_tuple = (item['Sku'], item['ImageHeight'], item['ImageWidth'])

	for item in properties_list:
		write_tuple = write_tuple + (item,)

	writer.writerow(write_tuple)
