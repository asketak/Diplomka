#!/bin/bash
for (( i=79; i<=65535; i++))
	do
echo $i
 netcat -v -w 10 -xlocalhost:9050 -X5 valhallaxmn3fydu.onion $i
done
