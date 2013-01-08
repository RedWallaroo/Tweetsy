import os, sys

from flask import *
from httplib import *

import twitter, urllib2, oauth2
from etsy import Etsy, EtsyEnvSandbox, EtsyEnvProduction
from geopy import geocoders


from app import app
import pdb

### API IDs ####
Etsy_API_ID = '66dg8mzhdt2e31nfmtpn2rna'

### Default Vars ###
etsy_env= EtsyEnvProduction()
gn = geocoders.GeoNames()

### Main ###
def search_etsy_tweets():
    api = twitter.Api()
    searchTerm = "etsy"
    tweets = api.GetSearch(searchTerm, include_entities = 1, result_type = "recent", per_page = 5)
    results = []
    for tweet in tweets:
        pdb.set_trace()
        twitter_user = tweet.GetUser()
        twitter_user_data = api.GetUser(twitter_user.screen_name)
        twitter_user_loc = gn.geocode(twitter_user_data.loc.encode('utf-8'), exactly_one=False)[0]
        tweet_urls = get_urls(tweet)
        #tweet_retweets = get_retweets(tweet)
        tweet_retweets = 1
        tweet_location = 3
        for item in tweet_urls:
            expanded_url = get_expanded_url(item)
            if expanded_url.find("http://www.etsy.com/listing/") != -1:
                orig_pos = expanded_url.find("http://www.etsy.com/listing/") + 28
                end_pos = expanded_url.find("/",orig_pos)
                listing_id = expanded_url[orig_pos:end_pos]
                listing_data = get_listing(listing_id)
                json_listing = format_json_data(listing_data[0], tweet_location, tweet_retweets)
                results.append(json_listing)
    return results

def get_listing(listing_id):
    etsy_api = Etsy(api_key=Etsy_API_ID, etsy_env=etsy_env)
    return etsy_api.getListing(listing_id=listing_id)

def get_urls(tweet):
    tweet_urls = []
    for url in tweet.urls:
        tweet_urls.append(url.url)
    return tweet_urls

def get_retweets(tweet):
    tweet_urls = []
    for url in tweet.retweets:
        tweet_urls.append(url.url)
    return tweet_urls

def get_Score(listing_favorers, tweet_retweets, listing_views):
    return 10

def format_json_data(listing_data, tweet_location, tweet_retweets):
    listing_title = listing_data['title']
    listing_views = listing_data['views']
    listing_favorers = listing_data['num_favorers']
    listing_id = listing_data['listing_id']
    #listing_score = get_score(listing_favorers, tweet_retweets, listing_views)
    listing_score = 100
    '''
     also need to use

     getImage_Listing api call
     need to pass listing_id and listing_image_id to get main image.
     
     '''
    json_listing = {'listing_id' : listing_id,
            'listing_title': listing_title,
            'views': listing_views,
            'favorers': listing_favorers,
            'tweet_location' : tweet_location,
            'retweets' : tweet_retweets,
            'score': listing_score
            }

    #json_listing = {'listing_id': listing_data['listing_id'],
                          #'listing_data': item_data }
    
    
    return json_listing

### Helpers ###
class HeadRequest(urllib2.Request):
    def get_method(self): return "HEAD"
     
def get_expanded_url(url):
    try:
       expanded_url = urllib2.urlopen(HeadRequest(url))
       return expanded_url.geturl()
    except:
        return "empty"

### Flask ###
@app.route('/')
def display_data():
    data = search_etsy_tweets()
    resp = make_response(render_template('index.html', data = data))
    resp.cache_control.no_cache = True
    return resp
    #return render_template('index.html', data = data)