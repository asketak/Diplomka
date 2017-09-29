
from __future__ import print_function
import urllib
from bs4 import BeautifulSoup
import re
import sys
import time
from tqdm import *
import time
from functools import wraps
import re
import sys

def retry(ExceptionToCheck, tries=4, delay=3, backoff=2, logger=None):
    """Retry calling the decorated function using an exponential backoff.

    http://www.saltycrane.com/blog/2009/11/trying-out-retry-decorator-python/
    original from: http://wiki.python.org/moin/PythonDecoratorLibrary#Retry

    :param ExceptionToCheck: the exception to check. may be a tuple of
        exceptions to check
    :type ExceptionToCheck: Exception or tuple
    :param tries: number of times to try (not retry) before giving up
    :type tries: int
    :param delay: initial delay between retries in seconds
    :type delay: int
    :param backoff: backoff multiplier e.g. value of 2 will double the delay
        each retry
    :type backoff: int
    :param logger: logger to use. If None, print
    :type logger: logging.Logger instance
    """
    def deco_retry(f):

        @wraps(f)
        def f_retry(*args, **kwargs):
            mtries, mdelay = tries, delay
            while mtries > 1:
                try:
                    return f(*args, **kwargs)
                except ExceptionToCheck, e:
                    msg = "%s, Retrying in %d seconds..." % (str(e), mdelay)
                    if logger:
                        logger.warning(msg)
                    else:
                        print(msg)
                    time.sleep(mdelay)
                    mtries -= 1
                    mdelay *= backoff
            return f(*args, **kwargs)

        return f_retry  # true decorator

    return deco_retry

def warning(*objs):
    print("ITERACE: ", *objs, file=sys.stderr)

@retry(Exception, tries=8, delay=3, backoff=2)
def send(url):
	return urllib.urlopen(url)

for x in tqdm(range(1060000,10,-1)):
	sys.stdout.flush()
	try:
		url = "https://bitcointalk.org/index.php?action=profile;u=" + `x`
		response = send(url)
		data = response.read()      # a `bytes` object
		text = data.decode('utf-8') # a `str`; this step can't be used if data is binaryo
		text = unicode(text).encode('utf8')
	except UnicodeDecodeError:
		continue
	address = re.findall(r'>[13][a-km-zA-HJ-NP-Z1-9]{25,34}<', text)
	if len(address) != 1:
		continue
	print("Warning multiple addresses")
	print(url + "," + str(address)[3:-3]   )
	# print(text)

