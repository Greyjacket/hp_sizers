import math, operator
import os, sys, codecs

 # https://www.stefangordon.com/remove-bom-mark-from-text-files-in-python/
def remove_bom_inplace(path):
    """Removes BOM mark, if it exists, from a file and rewrites it in-place"""
    buffer_size = 4096
    bom_length = len(codecs.BOM_UTF8)
 
    with open(path, "r+b") as fp:
        chunk = fp.read(buffer_size)
        if chunk.startswith(codecs.BOM_UTF8):
            i = 0
            chunk = chunk[bom_length:]
            while chunk:
                fp.seek(i)
                fp.write(chunk)
                i += len(chunk)
                fp.seek(bom_length, os.SEEK_CUR)
                chunk = fp.read(buffer_size)
            fp.seek(-bom_length, os.SEEK_CUR)
            fp.truncate()

def process_photo_size(size, ratio):
	
	if ratio < 1.1:
		if size == 12.0:
			size2 = 12.0
		elif size == 16.0:
			size2 = 16.0
		elif size == 24.0:
			size2 = 24.0
		elif size == 36.0:
			size2 = 36.0
		else: 
			size2 = 44.0
	elif ratio >= 1.1 and ratio < 1.3:
		if size == 8.0:
			size2 = 10.0
		elif size == 11.0:
			size2 = 14.0
		elif size == 16.0:
			size2 = 20.0
		elif size == 18.0:
			size2 = 24.0
		elif size == 24.0:
			size2 = 30.0
		elif size == 32.0:
			size2 = 44.0		
		else:
			size2 = 55.0
	elif ratio >= 1.3 and ratio < 1.39:
		if size == 8.0:
			size2 = 10.0
		elif size == 11.0:
			size2 = 14.0
		elif size == 16.0:
			size2 = 20.0
		elif size == 18.0:
			size2 = 24.0
		elif size == 24.0:
			size2 = 30.0
		elif size == 32.0:
			size2 = 44.0		
		else:
			size2 = 60.0
	elif ratio >= 1.39 and ratio < 1.9:
		if size == 8.0:
			size2 = 12.0
		elif size == 16.0:
			size2 = 24.0
		elif size == 24.0:
			size2 = 36.0
		elif size == 30.0:
			size2 = 44.0
		else:
			size2 = 66.0
	elif ratio >= 1.9 and ratio < 3.0:
		if size == 16.0:
			size2 = 32.0
		elif size == 20.0:
			size2 = 40.0
		elif size == 24.0:
			size2 = 48.0
		else: 
			size2 = 88.0		
	else:
		size2 = size * 1/ratio
		size_split = math.modf(size2)
		decimal_part = size_split[0]
		
		# round up from .5
		if decimal_part >= .5:
			size2 = math.ceil(size2)
		else:
			size2 = math.floor(size2)	
	return size2

def photo_sizer(image_height, image_width, sku):

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

	sizes = get_photo_sizes(ratio_rounded)

	options_list = {}

	for size in sizes:
		if orientation == 'portrait':		
			item_size = calculate_photo_dimensions(size, 'portrait', ratio_rounded, sku)
		else:
			item_size = calculate_photo_dimensions(size, 'landscape',ratio_rounded, sku)

		if item_size:		
			item_sizes.append(item_size)
	
	item_sizes.sort(key=operator.itemgetter('SqIn'))

	return item_sizes

def get_photo_sizes(ratio):

	if ratio < 1.1:
		sizes = [16.0, 24.0, 36.0, 44.0]
	elif ratio >= 1.1 and ratio < 1.39:
		sizes = [11.0, 16.0, 18.0, 24.0, 32.0, 44.0]
	elif ratio >= 1.39 and ratio < 1.9:
		sizes = [8.0, 16.0, 24.0, 30.0, 44.0]
	elif ratio >= 1.9 and ratio < 3.0:
		sizes = [16.0, 20.0, 24.0, 44.0]
	else:
		sizes = [44.0]
	return sizes

def calculate_photo_dimensions(size, orientation, ratio, sku):
	item_size = {}

	if orientation == 'portrait':
		size2 = process_photo_size(size, ratio)
		height = size2
		width = size
	else:
		size2 = process_photo_size(size, ratio)
		height = size
		width = size2

	# set the square inches
	square_inches = height * width

	if square_inches >= 80 and square_inches <= 4800:

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
			unique1 = "0" + width_int_str
		if len(height_int_str) < 2:
			unique2 = "0" + height_int_str

		# create the unique sku
		unique = unique1 + unique2
		unique_sku = sku + "_" + unique

		# create the size name
		size_name = unique1 + "in" + " x " + unique2 + "in"
		size_name2 = unique2 + "in" + " x " + unique1 + "in"

		item_size['Height'] = height_str
		item_size['Width'] = width_str
		item_size['SqIn'] = square_inches
		item_size['SizeName'] = size_name
		item_size['SizeName2'] = size_name2
		item_size['UniqueSku'] = unique_sku
		item_size['Price'] = price
		item_size['Ratio'] = ratio

		return item_size	

#------------------------------------------------------------- Map Sizer below

def process_map_size(size, ratio, ratio_raw, direction):

	if ratio == 1.0:
		if size == 16.0:
			size2 = 16.0
		elif size == 24.0:
			size2 = 24.0		
		elif size == 36.0:
			size2 = 36.0
		else: 
			size2 = 44.0

	elif ratio == 1.1:
		if size == 16.0:
			size2 = 18.0
		elif size == 24.0:
			size2 = 22.0
		elif size == 36.0:
			size2 = 32.0
		elif size == 44.0 and direction == 'down':
			size2 = process_second_map_size(44.0 * 1/ratio_raw)
		else:
			size2 = process_second_map_size(44.0 * ratio_raw)

	elif ratio == 1.25:

		if size == 24.0 and direction == 'down':
			size2 = 20.0
		elif size == 24.0 and direction == 'up':
			size2 = 30.0
		elif size == 44.0 and direction == 'down':
			size2 = process_second_map_size(44.0 * 1/ratio_raw)
		else:
			size2 = process_second_map_size(44.0 * ratio_raw)

	elif ratio == 1.33:

		if size == 24.0 and direction == 'down':
			size2 = 18.0
		elif size == 24.0 and direction == 'up':
			size2 = 30.0
		elif size == 44.0 and direction == 'down':
			size2 = process_second_map_size(44.0 * 1/ratio_raw)
		else:
			size2 = process_second_map_size(44.0 * ratio_raw)
			
	elif ratio == 1.5:
		if size == 24.0 and direction == 'down':
			size2 = 16.0
		elif size == 24.0 and direction == 'up':
			size2 = 36.0
		elif size == 44.0 and direction == 'down':
			size2 = process_second_map_size(44.0 * 1/ratio_raw)
		else:
			size2 = process_second_map_size(44.0 * ratio_raw)
	else:
		if size == 24.0 and direction == 'down':
			size2 = process_second_map_size(24.0 * 1/ratio_raw)
		elif size == 24.0 and direction == 'up':
			size2 = process_second_map_size(24.0 * ratio_raw)
		elif size == 36.0 and direction == 'up':
			size2 = process_second_map_size(36.0 * ratio_raw)
		else:
			size2 = process_second_map_size(44.0 * 1/ratio_raw)			
	
	return size2

def process_second_map_size(size2):
	# this function returns of tuple containing the fractional and integral part of the real number
	size2_split = math.modf(size2)
	decimal_part = size2_split[0]
		
	# round up from .3
	if decimal_part >= .3:
		size2 = math.ceil(size2)
	else:
		size2 = math.floor(size2)

	if size2 == 15.0:
		size2 = 16.0
		
	return size2

def map_sizer(image_height, image_width, sku):
	# only do one round for square ratios
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
		ratio_raw = 1.0/ratio_raw
	else:
		ratio_normalized = ratio_rounded
	
	aspect_ratio = ratio_description

	if ratio_rounded == 1.0:
		
		item_size = generate_item_info(16, 'up',ratio_normalized, ratio_raw, sku)
		if item_size:		
			item_sizes.append(item_size)

		item_size = generate_item_info(24, 'up',ratio_normalized, ratio_raw, sku)
		if item_size:		
			item_sizes.append(item_size)

		item_size = generate_item_info(36, 'up',ratio_normalized, ratio_raw, sku)
		if item_size:
			item_sizes.append(item_size)

		item_size = generate_item_info(44, 'up',ratio_normalized, ratio_raw, sku)
		if item_size:
			item_sizes.append(item_size)

	elif ratio_rounded == 1.1:
		item_size = generate_item_info(16, 'up',ratio_normalized, ratio_raw, sku)
		if item_size:		
			item_sizes.append(item_size)
		
		item_size = generate_item_info(24, 'down',ratio_normalized, ratio_raw, sku)
		if item_size:		
			item_sizes.append(item_size)

		item_size = generate_item_info(36, 'down',ratio_normalized, ratio_raw, sku)
		if item_size:		
			item_sizes.append(item_size)

		item_size = generate_item_info(44, 'down',ratio_normalized, ratio_raw, sku)
		if item_size:
			item_sizes.append(item_size)

		item_size = generate_item_info(44, 'up',ratio_normalized, ratio_raw, sku)
		if item_size:
			item_sizes.append(item_size)

	elif ratio_rounded == 1.25:
		item_size = generate_item_info(24, 'down',ratio_normalized, ratio_raw, sku)
		if item_size:		
			item_sizes.append(item_size)

		item_size = generate_item_info(24, 'up',ratio_normalized, ratio_raw, sku)
		if item_size:		
			item_sizes.append(item_size)

		item_size = generate_item_info(44, 'down',ratio_normalized, ratio_raw, sku)
		if item_size:
			item_sizes.append(item_size)

		item_size = generate_item_info(44, 'up',ratio_normalized, ratio_raw, sku)
		if item_size:
			item_sizes.append(item_size)


	elif ratio_rounded == 1.33:
		item_size = generate_item_info(24, 'down',ratio_normalized, ratio_raw, sku)
		if item_size:		
			item_sizes.append(item_size)

		item_size = generate_item_info(24, 'up',ratio_normalized, ratio_raw, sku)
		if item_size:		
			item_sizes.append(item_size)

		item_size = generate_item_info(44, 'down',ratio_normalized, ratio_raw, sku)
		if item_size:
			item_sizes.append(item_size)

		item_size = generate_item_info(44, 'up',ratio_normalized, ratio_raw, sku)
		if item_size:
			item_sizes.append(item_size)


	elif ratio_rounded == 1.5:
		item_size = generate_item_info(24.0, 'down',ratio_normalized, ratio_raw, sku)
		if item_size:		
			item_sizes.append(item_size)

		item_size = generate_item_info(24.0, 'up',ratio_normalized, ratio_raw, sku)
		if item_size:		
			item_sizes.append(item_size)

		item_size = generate_item_info(44.0, 'down',ratio_normalized, ratio_raw, sku)
		if item_size:
			item_sizes.append(item_size)

		item_size = generate_item_info(44.0, 'up',ratio_normalized, ratio_raw, sku)
		if item_size:
			item_sizes.append(item_size)

	else:
		item_size = generate_item_info(24.0, 'down',ratio_normalized, ratio_raw, sku)
		if item_size:		
			item_sizes.append(item_size)

		item_size = generate_item_info(24.0, 'up',ratio_normalized, ratio_raw, sku)
		if item_size:		
			item_sizes.append(item_size)

		item_size = generate_item_info(44.0, 'down',ratio_normalized, ratio_raw, sku)
		if item_size:
			item_sizes.append(item_size)

		item_size = generate_item_info(36.0, 'up',ratio_normalized, ratio_raw, sku)
		if item_size:
			item_sizes.append(item_size)

	item_sizes.sort(key=operator.itemgetter('SqIn'))

	return item_sizes

def generate_item_info(size, orientation, ratio, ratio_raw, sku):
	item_size = {}

	if orientation == 'down':
		if ratio >= 1.0:
			size2 = process_map_size(size, ratio, ratio_raw,'down')
			height = size
			width = size2
		else:
			size2 = process_map_size(size, 1.0/ratio, 1.0/ratio_raw, 'down')
			height = size2
			width = size
	elif orientation == 'up':
		if ratio >= 1.0:
			size2 = process_map_size(size, ratio, ratio_raw, 'up')
			height = size2
			width = size
		else:
			size2 = process_map_size(size, 1.0/ratio, 1.0/ratio_raw, 'up')
			height = size
			width = size2
	else:
		print ("Faulty orientation.")
		exit()

	# set the square inches
	square_inches = height * width
	if square_inches >= 144 and square_inches <= 4800:

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
		size_name = unique1 + "in" + " x " + unique2 + "in"
		size_name2 = unique2 + "in" + " x " + unique1 + "in"

		item_size['Height'] = height_str
		item_size['Width'] = width_str
		item_size['SqIn'] = square_inches
		item_size['SizeName'] = size_name
		item_size['SizeName2'] = size_name2
		item_size['UniqueSku'] = unique_sku
		item_size['Price'] = price
		item_size['Ratio'] = ratio

		return item_size

def get_aspect_ratio(ratio):
	
	if ratio < 1:
		ratio = 1/ratio

	if ratio < 1.09:
		return ("1:1", 1.0)
	elif ratio >= 1.09 and ratio < 1.15:
		return ('', 1.1)
	elif ratio >= 1.15 and ratio < 1.25:
		return ("6:5", 1.25)
	elif ratio >= 1.25 and ratio < 1.39:
		return ("4:3", 1.33)
	elif ratio >= 1.39 and ratio < 1.66:
		return ("3:2", 1.5)
	elif ratio >= 1.66 and ratio < 2.1:
		return ("scaled", 1.6)
	else:
		return ("oversize", 2.5)

def calculate_price(square_inches):
	# price chart
	if square_inches < 299:
		price = 29.99
	elif square_inches >= 300 and square_inches <= 399:
		price = 39.99
	elif square_inches >= 400 and square_inches <= 499:
		price = 49.99
	elif square_inches >= 500 and square_inches <= 599:
		price = 54.99
	elif square_inches >= 600 and square_inches <= 699:
		price = 59.99
	elif square_inches >= 700 and square_inches <= 799:
		price = 64.99
	elif square_inches >= 800 and square_inches <= 899:
		price = 69.99	
	elif square_inches >= 900 and square_inches <= 999:
		price = 74.99
	elif square_inches >= 1000 and square_inches <= 1099:
		price = 79.99
	elif square_inches >= 1100 and square_inches <= 1199:
		price = 84.99
	elif square_inches >= 1200 and square_inches <= 1299:
		price = 89.99
	elif square_inches >= 1300 and square_inches <= 1399:
		price = 94.99	
	elif square_inches >= 1400 and square_inches <= 1499:
		price = 99.99	
	elif square_inches >= 1500 and square_inches <= 1599:
		price = 149.99
	elif square_inches >= 1600 and square_inches <= 1699:
		price = 159.99
	elif square_inches >= 1700 and square_inches <= 1799:
		price = 169.99
	elif square_inches >= 1800 and square_inches <= 1899:
		price = 179.99
	elif square_inches >= 1900 and square_inches <= 1999:
		price = 189.99
	elif square_inches >= 2000 and square_inches <= 2099:
		price = 199.99
	elif square_inches >= 2100 and square_inches <= 2199:
		price = 209.99
	elif square_inches >= 2200 and square_inches <= 2299:
		price = 219.99
	elif square_inches >= 2300 and square_inches <= 2399:
		price = 229.99
	elif square_inches >= 2400 and square_inches <= 2499:
		price = 239.99
	elif square_inches >= 2500 and square_inches <= 2599:
		price = 249.99
	elif square_inches >= 2600 and square_inches <= 2699:
		price = 259.99
	elif square_inches >= 2700 and square_inches <= 2799:
		price = 269.99
	elif square_inches >= 2800 and square_inches <= 2899:
		price = 279.99
	elif square_inches >= 2900 and square_inches <= 2999:
		price = 289.99
	elif square_inches >= 3000 and square_inches <= 3099:
		price = 299.99
	elif square_inches >= 3100 and square_inches <= 3199:
		price = 309.99
	elif square_inches >= 3200 and square_inches <= 3299:
		price = 319.99
	elif square_inches >= 3300 and square_inches <= 3399:
		price = 329.99
	elif square_inches >= 3400 and square_inches <= 3499:
		price = 339.99
	elif square_inches >= 3500 and square_inches <= 3599:
		price = 349.99
	elif square_inches >= 3600 and square_inches <= 3699:
		price = 359.99
	elif square_inches >= 3700 and square_inches <= 3799:
		price = 369.99
	elif square_inches >= 3800 and square_inches <= 3899:
		price = 379.99
	elif square_inches >= 3900 and square_inches <= 3999:
		price = 389.99
	elif square_inches >= 4000 and square_inches <= 4099:
		price = 399.99
	elif square_inches >= 4100 and square_inches <= 4199:
		price = 409.99
	else:
		price = 419.99

	return price