from subprocess import call

for filename in os.listdir("./listings"):
	# call(["ls", "-l"])
	printf "http://valhallaxmn3fydu.onion/$filename \\n" | wget --load-cookies cookies.txt -P ./sellers/ -i- "$@"
	printf "http://valhallaxmn3fydu.onion/$filename/palautteet \\n" | wget --load-cookies cookies.txt -P ./feedbacks/ -i- "$@"
done