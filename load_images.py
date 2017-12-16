import sys, csv
import sqlite3

sqlite_file = 'HPDB.db'    # name of the sqlite database file
table_name1 = 'Images'  # name of the table to be created
table_name2 = 'Collections'  # name of the table to be created
new_field = 'my_1st_column' # name of the column
field_type = 'INTEGER'  # column data type

try:
	filename = sys.argv[1]
except:
	print "\nPlease input a valid CSV filename.\n"
	print "Format: python scriptname filename.\n"
	exit()

newCsv = []	
filename = "./CSVs/" + filename

# open the file from console arguments
with open(filename, 'rb') as csvfile:
	reader = csv.DictReader(csvfile)
	for row in reader:
		newCsv.append(row)

# Connecting to the database file
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

for item in newCsv:
	image_width = item["ImageWidth"]
	image_height = item["ImageHeight"]
	image_name = item['ImageName']
	image_sku = item['Sku']
	collection = "blah"
	url = "todo"

	try:
		format_str = """INSERT INTO Images (Sku, ImageName, ImageURL, ImageHeight, ImageWidth, Collection) VALUES ("{Sku}", "{ImageName}", "{ImageURL}", "{ImageHeight}", "{ImageWidth}", "{Collection}");"""
		sql_command = format_str.format(Sku=image_sku, ImageName=image_name, ImageURL=url, ImageHeight=image_height, ImageWidth=image_width, Collection=collection)
		c.execute(sql_command)

	except sqlite3.IntegrityError:
	    print('ERROR: ID already exists in PRIMARY KEY column {}'.format(id_column))

conn.commit()
conn.close()