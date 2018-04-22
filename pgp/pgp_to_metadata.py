import os
import subprocess
for filename in os.listdir('./dreampgp/'):
    command = ['pgpdump', './dreampgp/' + filename]
    try:
	    x = subprocess.check_output(command)
    except Exception as e:
    	continue
    print x
    # subprocess.call(comman)