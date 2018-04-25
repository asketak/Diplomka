import os
import subprocess
import sys
from pprint import pprint

orig_stdout = sys.stdout
f = open('listings.csv', 'w')
sys.stdout = f

path = './listings/'

for filename in os.listdir(path):
	vendor = subprocess.getoutput("""cat """ + path + filename + """ | grep "Visit vendor" | head -1 | cut -d'"' -f4""")
	price = subprocess.getoutput("""cat """ + path + filename + """ | grep "</em></li>" | cut -d'(' -f2 | cut -d' ' -f1 """)
	categories = subprocess.getoutput("""cat """ + path + filename + """ | grep "/categories/" | cut -d'>' -f2 | cut -d'<' -f1 | tail -3 """).split('\n')
	lcategories = len(categories)
	title = subprocess.getoutput("""cat """ +  path +filename + """ | grep -A 2 "product-header" | grep "h1" | cut -d'>' -f2 | cut -d'<' -f1 """)
		
	if lcategories == 3:
		print("'" + vendor + "'," + price + ",'" + categories[0] + "','" + categories[1] + "','" + categories[2] + "'," + "'" + title + "'")
	elif lcategories == 2:
		print("'" + vendor + "'," + price + ",'" + categories[0] + "','" + categories[1] + "','" + "'," + "'" + title + "'")
	elif lcategories == 1:
		print("'" + vendor + "'," + price + ",'" + categories[0] + "','"  + "','"  + "'," + "'" + title + "'")
	elif lcategories == 0:
		print("'" + vendor + "'," + price + ",'"  + "','"  + "','"  + "'," + "'" + title + "'")
	else:
		pprint("ERROR")
	
