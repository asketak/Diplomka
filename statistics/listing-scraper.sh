#!/bin/sh

url_format="http://valhallaxmn3fydu.onion/products/%05d"
seq_start=1
seq_end=103711

for i in `seq $seq_start $seq_end`;
do
   sleep 3
   printf "$url_format\\n" $i | wget --load-cookies cookies.txt  -P ./listings/ -i- "$@"
done


