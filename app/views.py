from flask import *
from httplib import *
from app import app
import os
import twitter
import util
import urllib2
import pdb
import webbrowser
import os, sys 
import oauth2
from etsy import Etsy, EtsyEnvSandbox, EtsyEnvProduction


API_ID = 2367105
Etsy_API_ID = '66dg8mzhdt2e31nfmtpn2rna'
oauth_consumer_secret = 'kfteru58n3'
etsy_env= EtsyEnvProduction()


def get_listing(listing_id):

    etsy_api = Etsy(api_key=Etsy_API_ID, etsy_env=etsy_env)
    return etsy_api.getListing(listing_id=listing_id)


def search_etsy_tweets():
    """
    Print recent tweets containing `searchTerm`.
    
    we'll search for tweets containing 'etsy' and filter by links in tweets, we will
    only care about the ones containing listing links.

    """
    api = twitter.Api()
    searchTerm = "etsy"
    tweets = api.GetSearch(searchTerm, include_entities = 1, result_type = "recent", per_page = 5)
    results = []
    for tweet in tweets:
        tweet_urls = get_urls(tweet)
        for item in tweet_urls:
            expanded_url = get_expanded_url(item)
            if expanded_url.find("http://www.etsy.com/listing/") != -1:
                orig_pos = expanded_url.find("http://www.etsy.com/listing/") + 28
                end_pos = expanded_url.find("/",orig_pos)
                listing_id = expanded_url[orig_pos:end_pos]
                listing_data = get_listing(listing_id)
                formatted_listing = format_listing_data(listing_data[0])
                results.append(formatted_listing)
    
    #return jsonify(results)
    return results

def get_listing(listing_id):
    etsy_api = Etsy(api_key=Etsy_API_ID, etsy_env=etsy_env)
    return etsy_api.getListing(listing_id=listing_id)

def get_urls(tweet):
    tweet_urls = []
    for url in tweet.urls:
        tweet_urls.append(url.url)
    return tweet_urls

def format_listing_data(listing_data):
    listing_title = listing_data['title']
    listing_views = listing_data['views']
    listing_favorers = listing_data['num_favorers']
    tweet_location = ''
    tweet_retweets = ''
    listing_score = 10

    '''
     also need to use

     getImage_Listing api call
     need to pass listing_id and listing_image_id to get main image.
     
     '''
    item_data = {'listing_title': listing_title,
            'views': listing_views,
            'favorers': listing_favorers,
            'tweet_location' : tweet_location,
            'retweets' : tweet_retweets,
            'score': listing_score
            }

    formatted_listing = {'listing_id': listing_data['listing_id'],
                          'listing_data': item_data }
    
    
    return formatted_listing
    
class HeadRequest(urllib2.Request):
    def get_method(self): return "HEAD"
     
def get_expanded_url(url):
    try:
       expanded_url = urllib2.urlopen(HeadRequest(url))
       return expanded_url.geturl()
    except:
        return "empty"


@app.route('/')
def display_data():
    data = search_etsy_tweets()
    return render_template('index.html', data = data)