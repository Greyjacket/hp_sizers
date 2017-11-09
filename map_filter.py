#!/usr/bin/python
import csv, sys, math, operator, re, os
from utils import get_aspect_ratio, calculate_price

def calculate_dimensions(size, orientation):
	item_size = {}

	if(orientation == 0):
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

	if size2 >= 15.0 and size2 < 16.0:
		size2 = 16.0
	if size2 >= 17.0 and size2 < 18.0:
		size2 = 16.0
	if size2 >= 19.0 and size2 < 20.0:
		size2 = 18.0			

	if(orientation == 0):
		height = size
		width = size2
	else:
		height = size2
		width = size

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
		
		item_size['Height'] = height_str
		item_size['Width'] = width_str
		item_size['SqIn'] = square_inches
		item_size['SizeName'] = size_name
		item_size['UniqueSku'] = unique_sku
		item_size['Price'] = price

		return item_size

try:
	filename = sys.argv[1]
except:
	print "\nPlease input a valid CSV filename.\n"
	print "Format: python scriptname filename operation.\n"
	exit()

write_filename = 'Filtered.csv'

newCsv = []
newFile = open(write_filename, 'wb') #wb for windows, else you'll see newlines added to csv
# open the file from console arguments
with open(filename, 'rb') as csvfile:
	reader = csv.DictReader(csvfile)
	for row in reader:
		newCsv.append(row)

base_tuple = ('ParentSku', 'ItemSku', 'relationship_type', 'ImageName','ImageHeight', 
		'ImageWidth', 'Ratio', 'SizeNameCurrent', 'SizeNameSuggested', 'CurrentPrice', 'SuggestedPrice')

# initialize csv writer
writer = csv.writer(newFile)
writer.writerow(base_tuple)

for item in newCsv:

	try:
		sku = item['Sku']
	except:
		try:
			sku = item['item_sku']
		except:
			print "Please format the CSV file with a Sku field. Try \"Sku\" or \"item sku\""
			exit()

	try:
		image_width = float(item['ImageWidth'])
	except:
		try:
			image_width = float(item['Image Width'])
		except:
			print "Warning: Blank value found for image width in Sku: " + sku + ". Ignoring this Sku."
			continue;
	try:
		image_height = float(item['ImageHeight'])
	except:
		try:
			image_height = float(item['Image Height'])
		except:
			print "Warning: Blank value found for image height in Sku: " + sku + ". Ignoring this Sku."
			continue;

	comparison_price = item['standard_price']
	
	try:
		comparison_sizename = item['SizeNameCurrent']
	except:		
		try:
			comparison_sizename = item['size_name Current']
		except:
			print "Please check your SizeNameCurrent field."
			exit()

	try:
		comparison_sqin = float(item['SqIn'])
	except:		
		try:
			comparison_sqin = float(item['Sqin'])
		except:		
			try:
				comparison_sqin = float(item['Sq in'])
			except:		
				try:
					comparison_sqin = float(item['Sq In'])
				except:
					print "Please check your SqIn field. It's possible there's a duplicate column name."
					exit()

	item_sizes = []

	# keep the aspect ratio >= 1
	if image_width >= image_height:
		ratio = round((image_width/image_height), 2) 
	else: 
		ratio = round((image_height/image_width), 2) 

	ratio_info  = get_aspect_ratio(ratio)

	# if we encountered an exception note it in the record
	if image_width == 1.0:
		ratio_description = "error"
	else:
		ratio_description = ratio_info[0]
		ratio = ratio_info[1]

	properties_list = []
	aspect_ratio = ratio_description
	
	properties_list.append(str(ratio))
	properties_list.append(aspect_ratio)

	# only do one round for square ratios
	if ratio_description == "1:1":
		orientation = 1
		item_size = calculate_dimensions(16, orientation)
		item_sizes.append(item_size)
		item_size = calculate_dimensions(24, orientation)
		item_sizes.append(item_size)
		item_size = calculate_dimensions(36, orientation)
		item_sizes.append(item_size)
		item_size = calculate_dimensions(44, orientation)
		item_sizes.append(item_size)
	else:
		orientation = 0

		# calculate both orientations for 24s, 0 for portrait 1 for landscape
		while (orientation < 2):
			item_size = calculate_dimensions(24, orientation)
			if item_size:		
				item_sizes.append(item_size)
			orientation+=1
		
		item_size = calculate_dimensions(44, 1)

		# if it's a standard size, check if the 44 sized item is not too close in square inches
		if item_size and ratio <= 2.0 :	
			newItem = {}
			for other_item in item_sizes:
				square_inches1 = item_size['SqIn']
				square_inches2 = other_item['SqIn']

				if square_inches1 >= square_inches2:
					square_ratio = square_inches1/square_inches2
				else:
					square_ratio = square_inches2/square_inches1
				if square_ratio < ratio:
					newItem = calculate_dimensions(36, 0)
					break
				else:
					newItem = item_size

			if newItem:
				item_sizes.append(newItem)
		else:
			if item_size:		
				item_sizes.append(item_size)

	item_sizes.sort(key=operator.itemgetter('SqIn'))

	newdict ={}

	count = 1
	for record in item_sizes:
		newdict['Height' + str(count)] = record['Height']
		newdict['Width' + str(count)] = record['Width']
		newdict['SqIn' + str(count)] = record['SqIn']
		newdict['SizeName' + str(count)] = record['SizeName']
		newdict['UniqueSku' + str(count)] = record['UniqueSku']
		newdict['Price' + str(count)] = record['Price']
		count+=1

	####################### FILTER HERE ###############################
	new_item = {}
	new_list =[]
	suggested_price = ""
	suggested_size = ""
	suggested_sqin = comparison_sqin
	size_match = False

	for key,value in newdict.iteritems():
		if "SizeName" in key:
			if comparison_sizename == value:
				size_match = True

	if not size_match:
		smallest = 10000
		number = ""
		for key, value in newdict.iteritems():
			if "SqIn" in key:
				if value is not None:
					temp_sqin = float(value)
					difference = abs(temp_sqin - comparison_sqin)
					if difference < smallest:
						smallest = difference
						number = str(re.findall(r'\d+', key)[0])
						suggested_sqin = temp_sqin

		size_name_key = 'SizeName' + number
		suggested_size = newdict[size_name_key]
		write = True

	actual_price = str(calculate_price(suggested_sqin))

	if comparison_price != actual_price:
		suggested_price = actual_price
		write = True

	if(write):
		try:
			new_list.append(item['ParentSku'])
		except:
			try:
				new_list.append(item['Parent Sku'])
			except:
				print "Check your ParentSku field. Should be Parent Sku or ParentSku."

		new_list.append(item['item_sku'])
		new_list.append(item['relationship_type'])

		try:
			new_list.append(item['ImageName'])
		except:
			try:
				new_list.append(item['Image Name'])
			except:
				print "Check your ImageName field. Should be Image Name or ImageName."		

		new_list.append(image_height)
		new_list.append(image_width)
		new_list.append(item['ratio'])
		new_list.append(comparison_sizename)
		new_list.append(suggested_size)
		new_list.append(comparison_price)	
		new_list.append(suggested_price)	

		write_tuple = ()
		for item in new_list:
			write_tuple = write_tuple + (item,)
			
		writer.writerow(write_tuple)

newFile.close()

