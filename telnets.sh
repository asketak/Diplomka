#!/bin/bash
for (( i=1; i<=65535; i++))
	do
 netcat -v -w 10 -xlocalhost:9050 -X5 t3e6ly3uoif4zcw2.onion $i
done
