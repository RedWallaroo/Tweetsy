import twitter
import util
import urllib2
import pdb
import webbrowser
import os, sys 
import oauth2
from etsy import Etsy, EtsyEnvSandbox, EtsyEnvProduction
from etsy.oauth import EtsyOAuthClient
import json
from pprint import pprint

API_ID = 2367105
Etsy_API_ID = '66dg8mzhdt2e31nfmtpn2rna'
oauth_consumer_secret = 'kfteru58n3'
etsy_env= EtsyEnvProduction()


def Get_Listing(listing_id):

    etsy_api = Etsy(api_key=Etsy_API_ID, etsy_env=etsy_env)
    return etsy_api.getListing(listing_id=listing_id)

'''
for x in range (len(data)):
    listing = data[x]
    print "This item: " + data[x]['title'] + "has the following tags: \n" + str(data[x]['tags'])
    replace_tag = raw_input("Which tag would you like to modify? ---> ")
    tags = data[x]['tags']
    if replace_tag in tags:
         replacement_value = raw_input("What are you going to replace it with? ---> ")
         if replacement_value != '':
            loc = tags.index(replace_tag)
            tags[loc] = replacement_value
            list_id = data[x]['listing_id']
            pdb.set_trace()
            response = etsy_api.updateListing(listing_id=list_id, tags=tags)
'''
def Search_Etsy_Tweets():
    """
    Print recent tweets containing `searchTerm`.

    To test this function, at the command line run:
        python twitter_api.py --search=<search term>
    For example,
        python twitter_api.py --search=python
    
    we'll search for tweets containing 'etsy' and filter by links in tweets, we will
    only care about the ones containing listing links.

    """
    api = twitter.Api()
    searchTerm = "etsy"
    tweets = api.GetSearch(searchTerm, include_entities = 1, result_type = "recent", per_page = 5)
    for tweet in tweets:
        tweet_urls = Get_Urls(tweet)
        for item in tweet_urls:
            #util.safe_print(tweet.GetText())
            expanded_url = get_expanded_url(item)
            if expanded_url.find("http://www.etsy.com/listing/") != -1:
                orig_pos = expanded_url.find("http://www.etsy.com/listing/") + 28
                listing_id = expanded_url[orig_pos:orig_pos + 9]
                listing_data = Get_Listing(listing_id)
                #util.safe_print(listing_data)
                print listing_data


def Get_Urls(tweet):
    tweet_urls = []
    for url in tweet.urls:
        tweet_urls.append(url.url)
    return tweet_urls


class HeadRequest(urllib2.Request):
    def get_method(self): return "HEAD"
     
def get_expanded_url(url):
    try:
       expanded_url = urllib2.urlopen(HeadRequest(url))
       return expanded_url.geturl()
    except:
        return "empty"

Search_Etsy_Tweets()