import os
import subprocess

path = '/home/asket/dddiplomka/dwn/seller/'

for filename in os.listdir(path):
	vendor = filename
	revenue = subprocess.getoutput("""cat """ + filename + """ | grep "Total revenue" | cut -d':' -f2 | cut -d'<' -f1 """)
	positive = subprocess.getoutput("""cat """ + filename + """ | grep -A 2 "Positive feedback:" | head -2 | tail -1 | cut -d'>' -f2 | cut -d'<' -f1 """)
	negative = subprocess.getoutput("""cat """ + filename + """ | grep -A 2 "Negative feedback:" | head -2 | tail -1 | cut -d'>' -f2 | cut -d'<' -f1 """)
	ships_from = subprocess.getoutput("""cat """ + filename + """ | grep "Ships from:" | head -1 | cut -d':' -f2 | cut -d'<' -f1 """)
	print("'" + vendor + "'" + "," + revenue + "," + positive + "," + negative + "," + "'"+ ships_from + "'" )
	

