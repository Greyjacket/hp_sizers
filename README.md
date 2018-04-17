# hp_sizers
Amazon Sizer and Validator for Historic Pictoric

Log:

4/17 Removed 16x20 item sizes for maps
4/15 Created Validator

---------------------------------------------------------------------------------
To run sizer:

From within the sizer directory, run this command from the terminal:

python sizer.py FILENAME.csv options

FILENAME being the name of the csv file you wish to process.

options is an integer representing the longest side of the sizes you wish to generate.

The file created is named "AMZ_' + input_filename + '_' + ("%m_%d_%Y") + '.csv"

---------------------------------------------------------------------------------

To run validator:

python validator.py FILENAME.csv options

FILENAME being the name of the csv file you wish to process.

options is an integer representing the longest side of the sizes you wish to generate.

The validator outputs three files:

'AMZ_' + input_name + '_' + ("%m_%d_%Y") + '.csv'
'AMZ_' + input_name + '_' + ("%m_%d_%Y") + '_delete.csv'
'AMZ_' + input_name + '_' + ("%m_%d_%Y") + '_price.csv'

---------------------------------------------------------------------------------


The CSV's fields must be formatted according to the schema below:

item_sku OR Sku OR SKU 

image_name OR name OR Image_Name or name

image_height OR height

image_width OR width

kind OR Kind or category

item_name OR Title OR title

product_description OR product description

keywords OR Keywords

image_folder OR ImageFolder

---------------------------------------------------------------------------------

Photo/print sizing:

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
	elif ratio >= 1.3 and ratio < 1.415:
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
	elif ratio >= 1.415 and ratio < 1.9:
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

---------------------------------------------------------------------------------
map sizing:

For maps, the ratio is rounded to one of the ratios below.

	if ratio == 1.0:
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

	if ratio == 1.1:
		if size == 16.0:
			size2 = 18.0
		elif size == 24.0:
			size2 = 22.0
		elif size == 36.0:
			size2 = 32.0
		elif size == 44.0 and direction == 'down':
			size2 = 40.0
		else:
			size2 = 49.0

	if ratio == 1.25:

		if size == 24.0 and direction == 'down':
			size2 = 18.0
		elif size == 24.0 and direction == 'up':
			size2 = 30.0
		elif size == 44.0 and direction == 'down':
			size2 = 32.0
		else:
			size2 = 55.0

	if ratio == 1.33:

		if size == 24.0 and direction == 'down':
			size2 = 18.0
		elif size == 24.0 and direction == 'up':
			size2 = 32.0
		elif size == 44.0 and direction == 'down':
			size2 = 32.0
		else:
			size2 = 60.0
			
	if ratio == 1.5:
		if size == 24.0 and direction == 'down':
			size2 = 16.0
		elif size == 24.0 and direction == 'up':
			size2 = 32.0
		elif size == 44.0 and direction == 'down':
			size2 = 30.0
		else:
			size2 = 66.0
	if ratio == 2.0:
		if size == 16.0:
			size2 = 32.0
		elif size == 20.0:
			size2 = 40.0
		elif size == 24.0:
			size2 = 48.0
		else: 
			size2 = 88.0

---------------------------------------------------------------------------------

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
	else:
		price = 319.99