import os, sys

from flask import *
from httplib import *

import twitter, urllib
from etsy import Etsy, EtsyEnvSandbox, EtsyEnvProduction
from geopy import geocoders


from app import app
import pdb
import time

### API IDs ####
Etsy_API_ID = '66dg8mzhdt2e31nfmtpn2rna'

### Default Vars ###
etsy_env= EtsyEnvProduction()
gn = geocoders.GeoNames()

### Main ###
def search_etsy_tweets():
    starttime = time.clock()
    api = twitter.Api()
    searchTerm = "etsy"
    tweets = api.GetSearch(searchTerm, include_entities=1, result_type="recent", per_page=50, geocode=("39.232253","-2.460937","24000mi"))
    return [json_obj for json_obj 
           in (json_listing(tweet,item) for tweet in tweets for item in [url.expanded_url for url in tweet.urls]) 
           if json_obj != None]
    
def json_listing(tweet, item):
    expanded_url = get_expanded_url(item.encode('utf-8'))
    orig_pos = expanded_url.find("http://www.etsy.com/listing/") 
    if orig_pos != -1:
        end_pos = expanded_url.find("/",orig_pos + 28)
        listing_data = get_listing(expanded_url[orig_pos + 28:end_pos]) #Passing Listing_id
        tweet_location = get_location(tweet)
        return format_json_data(listing_data[0], tweet_location)

      
def get_listing(listing_id):
    etsy_api = Etsy(api_key=Etsy_API_ID, etsy_env=etsy_env)
    return etsy_api.getListing(listing_id=listing_id)

def get_location(tweet): 
    tweet_coordinates = ("34.0522342","-118.4911912") #default when no location available
    if tweet.location != None and tweet.location != '':
        if tweet.location.find("iPhone") != -1:
            tweet_coordinates = tweet.location.replace("iPhone: ", "")  
        else:
            try:
                tweet_geocode = gn.geocode(tweet.location, exactly_one=False)
            except:
                tweet_geocode = None
            if tweet_geocode != None: 
                tweet_coordinates = tweet_geocode[0][1]
    if tweet.geo != None and tweet.geo != '':
        tweet_coordinates = tweet.geo.coordinates
    return tweet_coordinates

def get_expanded_url(url):
    try:
        resp = urllib.urlopen(url)
        return resp.url
    except:
        return None

def format_json_data(listing_data, tweet_location):
    #listing_image = listing_data['listing']
    '''
     also need to use

     getImage_Listing api call
     need to pass listing_id and listing_image_id to get main image.
     
     '''
    json_listing = {'id' : listing_data['listing_id'],
            'title': listing_data['title'][:50] + "...",
            'views': listing_data['views'],
            'favorers': listing_data['num_favorers'],
            'latitude' : tweet_location[0],
            'longitude': tweet_location[1],
            }
    
    return json_listing

### Flask ###
@app.route('/')
def display_data():
    data = search_etsy_tweets()
    resp = make_response(render_template('index.html', data = data))
    resp.cache_control.no_cache = True
    return resp