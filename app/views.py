import os, sys

from flask import *
from httplib import *

import twitter, urllib
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
    tweets = api.GetSearch(searchTerm, include_entities=1, result_type="popular", per_page=100, geocode=("39.232253","-2.460937","24000mi"))
    results = []
    for tweet in tweets:
        tweet_urls = get_urls(tweet)
        for item in tweet_urls:
            expanded_url = get_expanded_url(item.encode('utf-8'))
            if expanded_url.find("http://www.etsy.com/listing/") != -1:
                orig_pos = expanded_url.find("http://www.etsy.com/listing/") + 28
                end_pos = expanded_url.find("/",orig_pos)
                listing_id = expanded_url[orig_pos:end_pos]
                listing_data = get_listing(listing_id)
                tweet_location = get_location(tweet)
                json_listing = format_json_data(listing_data[0], tweet_location)
                results.append(json_listing)
    return results

def get_listing(listing_id):
    etsy_api = Etsy(api_key=Etsy_API_ID, etsy_env=etsy_env)
    return etsy_api.getListing(listing_id=listing_id)

def get_urls(tweet):
    tweet_urls = [url.expanded_url for url in tweet.urls]
    return tweet_urls

def get_location(tweet):
    if tweet.geo != None:
        tweet_coordinates = tweet.get.coordinates
    elif tweet.location != None:
        if tweet.location.find("iPhone") != -1:
            tweet_geocode = tweet.location.replace("iPhone: ", "")  
        else:
            try:
                tweet_geocode = gn.geocode(tweet.location, exactly_one=False)
            except:
                tweet_geocode = None

            if tweet_geocode == None: 
                tweet_coordinates = ("34.0522342","-118.4911912")
            else:
                tweet_coordinates = tweet_geocode[0][1]
    else:
        tweet_coordinates = ("34.0522342","-118.4911912")

    return tweet_coordinates

def get_expanded_url(url):
    try:
        resp = urllib.urlopen(url)
        return resp.url
    except:
        return 'empty'

def format_json_data(listing_data, tweet_location):
    listing_title = listing_data['title'][:50] + "..."
    listing_views = listing_data['views']
    listing_favorers = listing_data['num_favorers']
    listing_id = listing_data['listing_id']
    #listing_image = listing_data['listing']
    '''
     also need to use

     getImage_Listing api call
     need to pass listing_id and listing_image_id to get main image.
     
     '''
    json_listing = {'id' : listing_id,
            'title': listing_title,
            'views': listing_views,
            'favorers': listing_favorers,
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