import time
import json
import warnings
import re
from tqdm import *
import time

import requests
import pprint
from bs4 import BeautifulSoup, NavigableString, Tag

# warnings.filterwarnings('ignore')

class AdvancedSearchScraper(object):


    def __init__(self, query, limit = 1000000, verbose = True):

        self.query = query
        self.verbose = verbose
        if limit:
            self.limit = limit
        else:
            self.limit = float("inf")


    def ajax_call_params(self, oldest_tweet_id, newest_tweet_id):
        query_dict = {"src" : "typd",
                      "f" : "tweets",
                      "include_available_features" : 1,
                      "include_entities" : 1,
                      "reset_error_state" : "false",
                      "max_position" : "TWEET-%s-%s" %(oldest_tweet_id, newest_tweet_id),
                      }
        return query_dict

    def scrape(self):
        self.tweets = []

        #first-page

        # if q is supplied in the params dictionary, requests replaces
        # spaces by + . this results in an unexpected final url.
        # this is the only way to form the correct url.
        headers = {
            "User-Agent" : (
                "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:54.0)"
                " Gecko/20100101 Firefox/54.0"
                )
            }

        response = requests.get("https://twitter.com/search?q=%s" % self.query,
                                params = {"src" : "typd", "f" : "tweets"},
                                verify = False, headers = headers)
        self.tweets+=self.get_tweets_from_html(response.text)

        #ajax
        if len(self.tweets)>0:

            newest_tweet_id = self.tweets[0]["scroll_id"]
            oldest_tweet_id = self.tweets[-1]["scroll_id"]
            pbar = tqdm(total=self.limit)
            pbar_diff = 0;

            while len(self.tweets) <= self.limit:

                # rate limiting! 1 AJAX call in 5 seconds.

                time.sleep(10)

                # if q is supplied in the params dictionary, requests replaces
                # spaces by + . this results in an unexpected final url.
                # this is the only way to form the correct url

                try:
                    response = requests.get(
                        "https://twitter.com/i/search/timeline?q=%s" % self.query,
                        params = self.ajax_call_params(oldest_tweet_id, newest_tweet_id),
                        verify = False, headers = headers)
                    json_data = json.loads(response.text)
                    self.tweets += self.get_tweets_from_html(json_data["items_html"])

                    if self.verbose:
                        print("Scraped {0} tweets so far...".format(len(self.tweets)))

                    if oldest_tweet_id == self.tweets[-1]["scroll_id"]:
                        break

                    oldest_tweet_id = self.tweets[-1]["scroll_id"]
                    pbar.update(len(self.tweets) - pbar_diff)
                    pbar_diff = len(self.tweets)
                except Exception as e:
                    continue

        if isinstance(self.limit, int):
            return self.tweets[:self.limit]

        pbar.close()
        print("VRACIM SE VRACIM SE")
        return self.tweets





    def get_tweets_from_html(self, html_doc):
        tweetlist = []
        html_soup = BeautifulSoup(html_doc, "html.parser")
        tweet_soup_list = html_soup.find_all("div", {"class" : "original-tweet"})
        for tweet_soup in tweet_soup_list:
            try:
                tweet_dict = { "scroll_id" : int(tweet_soup["data-retweet-id"]) }
            except:
                tweet_dict = { "scroll_id" : int(tweet_soup["data-tweet-id"]) }
            try:
                tweet_dict["tweet_id"] = int(tweet_soup["data-tweet-id"])
                tweet_dict["author_name"] = tweet_soup["data-name"]
                tweet_dict["author_handle"] = tweet_soup["data-screen-name"]
                tweet_dict["author_id"] = int(tweet_soup["data-user-id"])
                tweet_dict["author_href"] = tweet_soup.find(
                    "a",{"class" : "account-group"})["href"]
                tweet_dict["tweet_permalink"] = tweet_soup["data-permalink-path"]
                tweet_dict["tweet_text"] = self.prettify_tweet_text_bs_element(
                    tweet_soup.find("p", {"class" : "tweet-text"}))
                tweet_dict["tweet_language"] = tweet_soup.find(
                    "p", {"class" : "tweet-text"})['lang']
                tweet_dict["tweet_time"] = tweet_soup.find(
                    "a",{"class" : "tweet-timestamp"})["title"]
                tweet_dict["tweet_timestamp"] = tweet_soup.find(
                    "span",{"class" : "_timestamp"})["data-time-ms"]
                tweet_dict["retweets"] = int(tweet_soup.find(
                    "span",{"class" : "ProfileTweet-action--retweet"}).find(
                    "span", {"class" : "ProfileTweet-actionCount"})['data-tweet-stat-count'])
                tweet_dict["favorites"] = int(tweet_soup.find(
                    "span",{"class" : "ProfileTweet-action--favorite"}).find(
                    "span", {"class" : "ProfileTweet-actionCount"})['data-tweet-stat-count'])
            except Exception as e:
                print("Error while extracting information from tweet.")
                print(e)
            try:
                tweet_dict["retweet_id"] = int(tweet_soup["data-retweet-id"])
                tweet_dict["retweeter_handle"] = tweet_soup["data-retweeter"]
            except:
                pass
            tweetlist.append(tweet_dict)
        return tweetlist

    def prettify_tweet_text_bs_element(self, tweet_text_bs_element):
        tweet_text = ''
        for child in tweet_text_bs_element.children:
            if isinstance(child, NavigableString):
                tweet_text += child + " "
            elif isinstance(child, Tag):
                try:
                    tag_class = child['class'][0]
                    if tag_class == "twitter-atreply":
                        mention = ''.join([i.string for i in child.contents])
                        tweet_text += mention + " "
                    elif tag_class == "twitter-hashtag":
                        hashtag = ''.join([i.string for i in child.contents])
                        tweet_text += hashtag + " "
                    elif tag_class == "twitter-timeline-link":
                        if isinstance(child["href"], str):
                            tweet_text += child["href"] + " "
                except:
                    if isinstance(child.string, str):
                        tweet_text += child.string + " "
        return " ".join(tweet_text.split())



ass = AdvancedSearchScraper("donate%20bitcoin", limit = 10000)
tweets = ass.scrape();
for tweet in tweets:
    text = str(tweet['tweet_text'].encode('ascii', 'ignore'))
    url = "https://twitter.com" + str(tweet['tweet_permalink'].encode('ascii', 'ignore'))
    address = re.findall(r'[13][a-km-zA-HJ-NP-Z1-9]{25,34}',text)
    if len(address) != 1:
        continue
    print(url + "," + str(address)[2:-2]   )