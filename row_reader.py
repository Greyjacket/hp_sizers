def extract_items(item):
	
	error_string = "" 
	return_dict = {}

	try:			
		return_dict['sku'] = item['item_sku']
	except:
		try:
			return_dict['sku'] = item['sku']
		except:
			try:
				return_dict['sku'] = item['SKU']
			except:
				print( "Error: Couldn't find a sku field. There may be a BOM in the input, or the header row may not be formatted correctly.")
				exit()

	try:
		return_dict['image_width'] = float(item['image_width'])
	except:
		try:
			return_dict['image_width'] = float(item['width'])
		except:
			errormessage = "Error: image_width not formatted in SKU: " + item['sku']
			print (errormessage)
			exit()

	try:
		return_dict['image_height'] = float(item['image_height'])
	except:
		try:
			return_dict['image_height'] = float(item['height'])
		except:
			errormessage = "Error: Image Height not formatted in SKU: " + item['sku']
			print (errormessage)
			exit()

	try:
		return_dict['image_filename'] = item['image_filename']
	except:
		try:
			return_dict['image_filename'] = item['name']
		except:
			try:
				image_filename = item['Image_Name']
			except:
				errormessage = "Error: Image Name not formatted in SKU: " + item['sku']
				print (errormessage)
				exit()
	try:
		return_dict['item_name'] = item['item_name']
	except:
		try: 
			return_dict['item_name'] = item['Title']
		except:
			try:
				return_dict['item_name'] = item['title']
			except:
				errormessage = "Error: Please format the input with an item_name Field in SKU: " + item['sku']
				print (errormessage)
				exit()
	
	try:
		return_dict['image_title'] = item['image_title']
	except:
			errormessage = "Error: Please format the input with an image_title Field in SKU: " + item['sku']
			print (errormessage)
			exit()

	try:
		return_dict['category'] = item['kind']
	except:
		try:
			return_dict['category'] = item['Kind']
		except:
			try:
				return_dict['category'] = item['category']				
			except:
				errormessage = "Error: Format the input to include an item kind or category: Photos, Maps or Prints in SKU: " + item['sku'] 
				print (errormessage)
				exit()

	try:
		return_dict['collection'] = item['collection']
	except:
		try:
			return_dict['collection'] = item['Collection']
		except:
			return_dict['collection'] = ""
			print ("Error: No collection specified in Sku: " + item['sku'])
			exit()

	try:
		return_dict['root_sku'] = item['image_sku_id']
	except:
		return_dict['root_sku'] = ""	
		print ("Error: No image_sku_id specified in Sku: " + item['sku'])
		exit()

	try:
		return_dict['keywords'] = item['keywords']
	except:
		try:
			return_dict['keywords'] = item['original_keywords']
		except:
			print ("Error: Format the input to include a keywords field.")
			exit()	

	try:
		return_dict['image_folder'] = item['image_folder']
	except:
		try:
			return_dict['image_folder'] = item['ImageFolder']
		except:
			return_dict['image_folder'] = ""

	try:
		return_dict['image_description'] = item['image_description'] 
	except:
		errormessage = "Error: No image_description found for SKU: " + item['sku']
		print (errormessage)
		exit()

	try:
		return_dict['product_description'] = item['product_description'] 
	except:
		errormessage = "Error: No product description found for SKU: " + item['sku']
		print (errormessage)
		exit()

	return return_dict