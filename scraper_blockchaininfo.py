
from __future__ import print_function
import urllib2
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
	return urllib2.urlopen(url)

filters_size = {2:2500, 4:4650, 8:3550, 16:26450, 32:100}
offset = 0;
for filtr in tqdm(filters_size):
    for offset in xrange(0,filters_size[filtr],50):
        time.sleep(2)
        url = "https://blockchain.info/tags?filter=" + str(filtr) + "&offset=" + str(offset)
        user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
        headers = {'User-Agent': user_agent}
        try:
            req = urllib2.Request(url, headers=headers)
            response = send(req)
            data = response.read()      
            text = data.decode('utf-8')
            text = unicode(text).encode('utf8')
            soup = BeautifulSoup(text, 'html.parser')
        except UnicodeDecodeError:
            print("UNICODE ERROR")


        for index,td in enumerate(soup.find_all('td')):
            if index <4:
                continue
            mod = index % 4
            if mod == 0:
                try:
                    address = re.findall(r'[13][a-km-zA-HJ-NP-Z1-9]{25,34}', str(td))[0]
                except Exception as e:
                    ipaddress = ""
            if mod == 1:
                try:
                    tag = re.findall(r'">.{1,}</span', str(td))[0][2:-6]
                except Exception as e:
                    tag = ""
            if mod == 2:
                try:
                    link = re.findall(r'url=[^\"]{1,}"', str(td))[0][4:-1]
                    link = urllib.unquote(link)
                except Exception as e:
                    link = ""
            if mod == 3:
                verified = "true"
                if "red" in td:
                    verified = "false"
                print(address + "," + tag + "," + link + "," + verified )