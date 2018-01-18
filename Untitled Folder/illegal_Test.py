#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv, sys, math, operator, re, os
from utils import photo_sizer

try:
	filename = sys.argv[1]
except:
	print "\nPlease input a valid CSV filename.\n"
	print "Format: python scriptname filename.\n"
	exit()

newCsv = []
output = 'photo_print_amazon_sizes.csv'
newFile = open(output, 'wb') #wb for windows, else you'll see newlines added to csv

# open the file from console arguments
with open(filename, 'rb') as csvfile:
	reader = csv.DictReader(csvfile)
	for row in reader:
		newCsv.append(row)

for item in newCsv:

	try:
		test = item['Title']
	except:
		print "Bad Format"
		exit()

	string1 = test.decode('utf8')
	#string2 = test.encode('utf8')
	string3 = "Flügel"
	#string4 = unicode(u"Ã«", 'utf8')
	#print u"Ã«"
	print string1
	#print string4.encode('utf8')
	#print unicode(string4, errors='replace')
	#print string4.encode("utf8", "replace")
	#print string4