
from __future__ import print_function
import urllib2
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
	return urllib2.urlopen(url)

url = "https://www.reddit.com/r/Bitcoin/search?q=bitcoin+address&include_over_18=on"
firstflag = 1
while True:
    time.sleep(20)
    sys.stdout.flush()
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
    headers = {'User-Agent': user_agent}
    try:
        req = urllib2.Request(url, headers=headers)
        response = send(req)
        data = response.read()      
        text = data.decode('utf-8')
        text = unicode(text).encode('utf8')
    except UnicodeDecodeError:
        print("UNICODE ERROR")
        sys.exit() 
    soup = BeautifulSoup(text, 'html.parser')
    spans = soup.findAll("span", { "class" : "nextprev" })
    span = str(spans[firstflag])
    line = re.split('"',span)
    futurl = (line[3])
    if firstflag == 0:
        futurl = (line[9])
    firstflag = 0
    addresses = re.findall(r'[13][a-km-zA-HJ-NP-Z1-9]{25,34}', text)
    for address in addresses:
        print(url +"," + address)
    url = futurl

# if len(address) == 0:
	# continue
# if len(address) == 0:  # todo OPRAVIT a kouknout do dat, jestli to neni nekde spatne
	# print("Warning multiple addresses")
# print(url + "," + str(address)[3:-3]   )
	# print(text)

# https://www.reddit.com/r/Bitcoin/search?q=bitcoin+address&amp;include_over_18=on%27%27&amp;count=22&amp;after=t3_28153c