import os
import subprocess
import re

spath = './sellers/'
fpath = './feedbacks/'

# orig_stdout = sys.stdout
# f = open('sellers.csv', 'w')
# sys.stdout = f

# for filename in os.listdir(spath):
# 	vendor = filename
# 	filename = spath + filename
# 	revenue = subprocess.getoutput("""cat """ + filename + """ | grep "Total revenue" | cut -d':' -f2 | cut -d'<' -f1 """)
# 	positive = subprocess.getoutput("""cat """ + filename + """ | grep -A 2 "Positive feedback:" | head -2 | tail -1 | cut -d'>' -f2 | cut -d'<' -f1 """)
# 	negative = subprocess.getoutput("""cat """ + filename + """ | grep -A 2 "Negative feedback:" | head -2 | tail -1 | cut -d'>' -f2 | cut -d'<' -f1 """)
# 	ships_from = subprocess.getoutput("""cat """ + filename + """ | grep "Ships from:" | head -1 | cut -d':' -f2 | cut -d'<' -f1 """)
# 	print("'" + vendor + "'" + "," + revenue + "," + positive + "," + negative + "," + "'"+ ships_from + "'" )
	
# sys.stdout.flush()
# f2 = open('feedbacks.csv', 'w')
# sys.stdout = f2

# for filename in os.listdir(fpath):

filename = "arnold"
vendor = filename
filename = spath + filename
buyer = subprocess.getoutput("""cat """ + filename + """ | grep "***" | tr -d * """)
buyer_eur_num = subprocess.getoutput("""cat """ + filename + """ | grep "bull" """)
buyer_eur_num = buyer_eur_num.replace("&nbsp;","").replace("&bull;",",").replace("+","").replace("€","")
buyer_eur_num = re.split('\n', buyer_eur_num)
buyer_eur_num = [w[1:-1] for w in buyer_eur_num]


positive = subprocess.getoutput("""cat """ + filename + """ | grep -A 2 "Positive feedback:" | head -2 | tail -1 | cut -d'>' -f2 | cut -d'<' -f1 """)
negative = subprocess.getoutput("""cat """ + filename + """ | grep -A 2 "Negative feedback:" | head -2 | tail -1 | cut -d'>' -f2 | cut -d'<' -f1 """)
ships_from = subprocess.getoutput("""cat """ + filename + """ | grep "Ships from:" | head -1 | cut -d':' -f2 | cut -d'<' -f1 """)

print("'" + vendor + "'" + "," + revenue + "," + positive + "," + negative + "," + "'"+ ships_from + "'" )

sys.stdout.flush()