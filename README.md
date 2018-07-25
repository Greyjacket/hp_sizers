# BMW Utilities
Amazon Sizer and Validator for Historic Pictoric

### Log:
- 7/25 Added BOM check
- 7/20 Added sales history check
- 7/18 Updated map ratio
- 7/6 Added test case and abstracted return dictionary
- 7/3 pythonized validator.
- 6/30 Fixed plenty of bugs.
- 6/15 Ebay sizer first draft added.
- 6/15 Validator outputs parent as an updated field.
- 6/8 Validator includes singles (check this)
- 5/19 Added collection and root sku to validator and sizer.
- 5/17 Added deque to validator.
- 5/07 Changed 3:2 grouping to 1.39 and above, as opposed to 1.415.
- 4/26 Changed map sizing to scale with the natural ratio for 44 sizes.
- 4/25 Changed bullets according to standard sizes
- 4/17 Removed 16x20 item sizes for maps
- 4/15 Created Validator

---------------------------------------------------------------------------------
To run sizer:

From within the sizer directory, run this command from the terminal:

python sizer.py FILENAME.csv options

FILENAME being the name of the csv file you wish to process.

The file created will be outputted as "AMZ_' + input_filename + '_' + ("%m_%d_%Y") + '.csv"

The CSV's fields must be formatted according to the schema below:

item_sku **OR** Sku **OR** SKU 

image_name **OR** name **OR** Image_Name **OR** name

image_height **OR** height

image_width **OR** width

kind **OR** Kind **OR** category:
	
item_name **OR** Title **OR** title

product_description **OR** product description

keywords **OR** Keywords

image_folder **OR** ImageFolder: Be sure to include the full path to the image folder. The image filename will be concatenated to the end of the pathname.


---------------------------------------------------------------------------------

**options** is an integer representing the longest side of the sizes you wish to generate.

If no value is specified for options, then all sizes will be generated.

---------------------------------------------------------------------------------

To run validator:

python validator.py FILENAME.csv options

FILENAME being the name of the csv file you wish to process.

The validator outputs four files into a target directory called AMZ_ + input name:

- 'AMZ_' + input_name + '_' + ("%m_%d_%Y") + '.csv'
- 'AMZ_' + input_name + '_' + ("%m_%d_%Y") + '_delete.csv'
- 'AMZ_' + input_name + '_' + ("%m_%d_%Y") + '_price.csv'
- 'AMZ_' + input_name + '_' + ("%m_%d_%Y") + '_error.csv'

The file needs to be a table join using the amazon variation table and the image table.

Also, the resultant CSV needs to be sorted in ascending order by Id, else the validator won't function correctly.

Constraints:

The validator requires a CSV of the table join between Images and Amazon.

The CSV input must contain the following fields:

id, item_sku, item_name, product_description, asin, size_name, is_parent, keywords, price, sales, image_sku_id, image_height, image_width, image_title, image_description, image_filename, category, collection, original_keywords

---------------------------------------------------------------------------------

For photos:
Use 'photos', 'photo', 'Photograph', or 'photograph' for the field value.

For Maps:
Use 'maps', 'map', 'Map', or 'Maps' for the field value.
---------------------------------------------------------------------------------

#### Photo/print sizing:

	if ratio less 1.1:
		12 x 12
		16 x 16
		24 x 24
		36 x 36
		44 x 44

	ratio between 1.1 and 1.3:
		8 x 10
		11 x 14
		16 x 20
		18 x 24
		24 x 30
		32 x 44
		44 x 55

	ratio between 1.3 and 1.39:
		8 x 10
		11 x 14
		16 x 20
		18 x 24
		24 x 30
		32 x 44
		44 x 60

	ratio between 1.39 and 1.9:
		8 x 12
		16 x 24
		24 x 36
		30 x 44
		44 x 66

	 ratio between 1.9 and 3.0:
		16 x 32
		20 x 40
		24 x 48
		44 x 88

A ratio larger than 3.0 will be scaled accordingly.

---------------------------------------------------------------------------------
#### Map sizing:

For maps, the ratio is rounded to one of the ratios below.

	if ratio < 1.09:
		16 x 16
		24 x 24
		36 x 36
		44 x 44

	if ratio between 1.09 and 1.15:
		16 x 18
		22 x 24
		32 x 36
		44 scaled down
		44 scaled up

	if ratio between 1.15 and 1.25:
		20 x 24
		24 x 30
		44 scaled down
		44 scaled up

	if ratio between 1.25 and 1.39:
		18 x 24
		24 x 30
		44 scaled down
		44 scaled up

	if ratio between 1.39 and 1.6:
		16 x 24
		24 x 36
		44 scaled down
		44 scaled up

	A ratio larger than 1.6 will be scale accordingly.

---------------------------------------------------------------------------------

#### Pricing Table:

	square_inches < 299:
		price = 29.99
	 square_inches >= 300 and square_inches <= 399:
		price = 39.99
	 square_inches >= 400 and square_inches <= 499:
		price = 49.99
	 square_inches >= 500 and square_inches <= 599:
		price = 54.99
	 square_inches >= 600 and square_inches <= 699:
		price = 59.99
	 square_inches >= 700 and square_inches <= 799:
		price = 64.99
	 square_inches >= 800 and square_inches <= 899:
		price = 69.99	
	 square_inches >= 900 and square_inches <= 999:
		price = 74.99
	 square_inches >= 1000 and square_inches <= 1099:
		price = 79.99
	 square_inches >= 1100 and square_inches <= 1199:
		price = 84.99
	 square_inches >= 1200 and square_inches <= 1299:
		price = 89.99
	 square_inches >= 1300 and square_inches <= 1399:
		price = 94.99	
	 square_inches >= 1400 and square_inches <= 1499:
		price = 99.99	
	 square_inches >= 1500 and square_inches <= 1599:
		price = 149.99
	 square_inches >= 1600 and square_inches <= 1699:
		price = 159.99
	 square_inches >= 1700 and square_inches <= 1799:
		price = 169.99
	 square_inches >= 1800 and square_inches <= 1899:
		price = 179.99
	 square_inches >= 1900 and square_inches <= 1999:
		price = 189.99
	 square_inches >= 2000 and square_inches <= 2099:
		price = 199.99
	 square_inches >= 2100 and square_inches <= 2199:
		price = 209.99
	 square_inches >= 2200 and square_inches <= 2299:
		price = 219.99
	 square_inches >= 2300 and square_inches <= 2399:
		price = 229.99
	 square_inches >= 2400 and square_inches <= 2499:
		price = 239.99
	 square_inches >= 2500 and square_inches <= 2599:
		price = 249.99
	 square_inches >= 2600 and square_inches <= 2699:
		price = 259.99
	 square_inches >= 2700 and square_inches <= 2799:
		price = 269.99
	 square_inches >= 2800 and square_inches <= 2899:
		price = 279.99
	 square_inches >= 2900 and square_inches <= 2999:
		price = 289.99
	 square_inches >= 3000 and square_inches <= 3099:
		price = 299.99
	 square_inches >= 3100 and square_inches <= 3199:
		price = 309.99
	 square_inches >= 3200 and square_inches <= 3299:
		price = 319.99
	 square_inches >= 3300 and square_inches <= 3399:
		price = 329.99
	 square_inches >= 3400 and square_inches <= 3499:
		price = 339.99
	 square_inches >= 3500 and square_inches <= 3599:
		price = 349.99
	 square_inches >= 3600 and square_inches <= 3699:
		price = 359.99
	 square_inches >= 3700 and square_inches <= 3799:
		price = 369.99
	 square_inches >= 3800 and square_inches <= 3899:
		price = 379.99
	 square_inches >= 3900 and square_inches <= 3999:
		price = 389.99
	 square_inches >= 4000 and square_inches <= 4099:
		price = 399.99
	 square_inches >= 4100 and square_inches <= 4199:
		price = 409.99
	else:
		price = 419.99
