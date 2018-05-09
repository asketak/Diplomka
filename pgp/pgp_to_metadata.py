import os
import subprocess
for filename in os.listdir('./keys/'):
    command = ['pgpdump', './keys/' + filename]
    try:
	    x = subprocess.check_output(command)
    except Exception as e:
    	continue
    print x
    # subprocess.call(comman)
