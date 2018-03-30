# hp_sizers
Sizers for Historic Pictoric

To run:

From within the sizer directory, run this command from the terminal:

python sizer.py FILENAME.csv

FILENAME being the name of the csv file you wish to process.

The file created is named "amazon_sizes.csv"

The CSV's fields must be formatted according to the schema below:

Sku OR item_sku OR SKU

ImageName OR Image Name OR Image_Name

ImageHeight OR Image Height

ImageWidth OR Image Width

kind OR Kind

ItemName OR Item Name OR Title

product_description OR product description

Generic Keywords OR GenericKeywords


Photo/print sizing:

if ratio < 1.2:
	sizes = 12x12, 16x16, 24x24, 36x36
ratio between 1.2 and 1.3
	sizes = 8x10, 11x14, 16x20, 24x30, 32x44 (check this last size )
ratio between 1.3 and 1.45
	sizes = 11x14,18x24,24x32, 32x43
ratio between 1.45 and 1.9
	sizes = 8x12, 16x24,24x36,30x44
anything else:
	sizes = 16x32, 20x40, 24x48


map rounding:

15 to 16
17-19 to 18
23-25 to 24
28-29 to 30
31-34 to 32
35-38 to 36

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