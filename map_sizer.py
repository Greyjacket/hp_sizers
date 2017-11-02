#!/usr/bin/python
import csv, sys, math
from utils import get_aspect_ratio, calculate_price

try:
	filename = sys.argv[1]
except:
	print "\nPlease input a valid CSV filename.\n"
	print "Format: python scriptname filename.\n"
	exit()

# change the base number to scale by, depending on map or photo
sizes = [24.0, 36.0, 44.0]

newCsv = []
newFile = open('NewSizes.csv', 'wb') #wb for windows, else you'll see newlines added to csv
# open the file from console arguments
with open(filename, 'rb') as csvfile:
	reader = csv.DictReader(csvfile)
	for row in reader:
		newCsv.append(row)

base_tuple = ('Sku', 'ImageHeight', 'ImageWidth','Ratio', 'Aspect Ratio')

for i in range(len(sizes) * 2):
	i += 1
 	base_tuple = base_tuple + ('Height' + str(i), 'Width' + str(i), 'SqIn' + str(i), 'SizeName' + str(i), 'UniqueSku' + str(i), 'Price' + str(i))

# initialize csv writer
writer = csv.writer(newFile)
writer.writerow(base_tuple)

# write the dictionary, do some calculations on the way
for item in newCsv:
	image_width = float(item['ImageWidth'])
	image_height = float(item['ImageHeight'])
	sku = item['Sku']

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

	# only do one round for square ratios
	if ratio_description == "1:1":
		polarity = 1
	else:
		polarity = 0

	while (polarity < 2):

		for size in sizes:		
		
			if(polarity == 0):
				size2 = size * (ratio)
			else:
				size2 = size * (1.0/ratio)

			# this function returns of tuple containing the fractional and integral part of the real number
			size2_split = math.modf(size2)
			decimal_part = size2_split[0]
				
			# round up from .3
			if decimal_part >= .3:
				size2 = math.ceil(size2)
			else:
				size2 = math.floor(size2)

			height = size
			width = size2

			# set the square inches
			square_inches = height * width

			if square_inches > 240 and square_inches <= 2400:

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
				unique_sku = sku + "_" + unique

				# create the size name
				size_name = width_int_str + "in" + " x " + height_int_str + "in"
				
				properties_list.append(height_str)
				properties_list.append(width_str)
				properties_list.append(str(square_inches))
				properties_list.append(size_name)
				properties_list.append(unique_sku)
				properties_list.append(str(price))
			
		polarity+=1

	write_tuple = (sku, image_height, image_width)

	for item in properties_list:
		write_tuple = write_tuple + (item,)

	writer.writerow(write_tuple)
