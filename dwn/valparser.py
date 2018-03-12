import os
import subprocess

path = '/home/asket/dddiplomka/dwn/iter/'

for filename in os.listdir(path):
	vendor = subprocess.getoutput("""cat """ + filename + """ | grep "Visit vendor" | head -1 | cut -d'"' -f4""")
	price = subprocess.getoutput("""cat """ + filename + """ | grep "</em></li>" | cut -d'(' -f2 | cut -d' ' -f1 """)
	categories = subprocess.getoutput("""cat """ + filename + """ | grep "/categories/" | cut -d'>' -f2 | cut -d'<' -f1 | tail -3 """).split('\n')
	lcategories = len(categories)
	title = subprocess.getoutput("""cat """ + filename + """ | grep -A 2 "product-header" | grep "h1" | cut -d'>' -f2 | cut -d'<' -f1 """)
		
	if lcategories == 3:
		print(vendor + "," + price + "," + categories[0] + "," + categories[1] + "," + categories[2] + "," + "'" + title + "'")
	elif lcategories == 2:
		print(vendor + "," + price + "," + categories[0] + "," + categories[1] + "," + "," + "'" + title + "'")
	else:
		print("ERROR")
	

# 	with open(path + filename) as f:
# 	    for line in f:
# 	        print(line)
