from subprocess import call
import subprocess

bash1 = """ printf "http://valhallaxmn3fydu.onion/$filename \\n" | wget --load-cookies cookies.txt -P ./sellers/ -i- "$@" """
bash2 = """ printf "http://valhallaxmn3fydu.onion/$filename/palautteet \\n" | wget --load-cookies cookies.txt -O ./feedbacks/$filename -i- "$@" && cat ./feedbacks/$filename """


x = []
with open("listings.csv") as file:
	for l in file:
		seller_nick  = l.split("\"")[1::2][0].replace('/', '')
		x.append(seller_nick)

x = list(set(x))

for seller_nick in x:
	b1 = bash1.replace('$filename',seller_nick)
	b2 = bash2.replace('$filename',seller_nick)
	process = subprocess.getoutput(b1)
	process = subprocess.getoutput(b2)

	num=2
	while """<span class="next">""" in process:
		bash3 = """ printf "http://valhallaxmn3fydu.onion/$filename/palautteet/$num \\n" | wget --load-cookies cookies.txt -O ./feedbacks/$filename.$num -i- "$@" && cat ./feedbacks/$filename.$num"""
		b3 = bash3.replace('$filename',seller_nick).replace('$num',str(num))
		num += 1
		process = subprocess.getoutput(b3)

