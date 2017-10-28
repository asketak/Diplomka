from __future__ import print_function
import requests
import json
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
from bs4 import BeautifulSoup
from datetime import datetime, timedelta



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


proxies = {
    'http': 'socks5h://127.0.0.1:9050',
    'https': 'socks5h://127.0.0.1:9050'
}

domain = "http://t3e6ly3uoif4zcw2.onion"

cookie = {'MARKET_SESSION': 'g3v5f6b1m92aetq6oljs1jf8q6'}

# data = requests.get(url,proxies=proxies, cookies=cookie).text

# http://lchudifyeqm4ldjj.onion/contactMember?member=stealthmeds&tab=ratings#tabChooser,2d 0h,h . . . 2,0.02
# http://lchudifyeqm4ldjj.onion/contactMember?member=stealthmeds&tab=ratings#tabChooser,2d,h . . . 2,0.02
# http://lchudifyeqm4ldjj.onion/contactMember?member=stealthmeds&tab=ratings#tabChooser,08:13,m . . . t,0.009
linkflag = False

for category in tqdm(range(104,200)):
    for page in tqdm(range(1,10)):
        time.sleep(5)
        sys.stdout.flush()
        text = ""
        if linkflag:
            time.sleep(5)
        linkflag = False
        try:
            url = domain + "/?page=" + str(page) + "&category=" + str(category)
            response = requests.get(url,proxies=proxies, cookies=cookie).text
            text = response.encode('ascii', 'ignore').decode('ascii') # a `str`; this step can't be used if data is binaryo
            soup = BeautifulSoup(text, 'html.parser')
            # print(text)
        except Exception as e:
            # print("exception") 
            time.sleep(5)
            continue

        for link in soup.find_all('a', { "class" : "viewRatings" }, href=True):
            linkflag = True
            try:
                # print("inlinks") 
                rating_url = domain + link['href']
                # print(rating_url)
                response = requests.get(rating_url,proxies=proxies, cookies=cookie).text
                text = response.encode('ascii', 'ignore').decode('ascii','ignore') # a `str`; this step can't be used if data is binaryo
                soup = BeautifulSoup(text, 'html.parser')
                user = rating_url.split("=")[1].split("&")[0]
                outputline = user + ','
                # print(user)
                for index,td in enumerate(soup.find_all('td', { "class" : "dontwrap" })):
                    sys.stdout.flush()
                    mod = index % 4
                    if mod == 0:
                        tim = re.findall(r'>.{1,}<', str(td))
                        tim =  tim[0][1:-1]
                        print(tim)
                        if re.match(r'^([0-9])+d$',tim):  # 10d
                            print("dny")
                            days = tim.strip("d")
                            print(days)
                            date = datetime.today() - timedelta(days=days)
                        if re.match(r'^[0-9]+d [0-9]+h$',tim):  # 10d 5h
                            print("dny hodiny")
                            days = tim.strip("d")
                            print(days)
                            date = datetime.today() - timedelta(days=days)
                        if re.match(r'^[0-9]+:[0-9]+$',tim):  # 08:13
                            print("hodiny")
                        outputline += tim+ ','
                    if mod == 2:
                        user = re.findall(r'>.{1,}<', str(td))
                        outputline += user[0][1:-1] + ','
                    if mod == 3:
                        value = re.findall(r'>.{1,}<', str(td))
                        outputline += value[0][6:-1] 
                        # print(outputline)
                        outputline = user + ','
            except Exception as e:
                continue








    

