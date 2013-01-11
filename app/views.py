import os, sys

from flask import *
from httplib import *

import twitter, urllib
from etsy import Etsy, EtsyEnvSandbox, EtsyEnvProduction
from geopy import geocoders

from app import app

### API IDs ####
Etsy_API_ID = '66dg8mzhdt2e31nfmtpn2rna'

### Default Vars ###
etsy_env= EtsyEnvProduction()
gn = geocoders.GeoNames()

### Main ###
def search_etsy_tweets(tweet_count=5):
    api = twitter.Api()
    searchTerm = "etsy.com/listing/"
    tweets = api.GetSearch(searchTerm, include_entities=1, result_type="recent", per_page=tweet_count, geocode=("39.232253","-2.460937","24000mi"))
    return [json_obj for json_obj 
           in (json_listing(tweet,item) for tweet in tweets for item in [url.expanded_url for url in tweet.urls]) 
           if json_obj != None]
    
def json_listing(tweet, item):
    item_url = item.encode('utf-8') 
    if "etsy.me" in item_url:
        item_url = get_expanded_url(item_url)
    orig_pos = item_url.find("etsy.com/listing/") 
    if orig_pos != -1:
        end_pos = item_url.find("/",orig_pos + 17)
        listing_data, listing_img_url = get_listing(item_url[orig_pos + 17:end_pos]) #Passing Listing_id
        tweet_location = get_location(tweet)
        return format_json_data(listing_data[0], tweet_location, listing_img_url)
      
def get_listing(listing_id):
    etsy_api = Etsy(api_key=Etsy_API_ID, etsy_env=etsy_env)
    listing_images = etsy_api.findAllListingImages(listing_id=int(listing_id)) 
    listing_img_url = listing_images[0]['url_75x75']
    return etsy_api.getListing(listing_id=listing_id), listing_img_url

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

def format_json_data(listing_data, tweet_location, listing_img_url):
    json_listing = {'id' : listing_data['listing_id'],
            'title': listing_data['title'],
            'views': listing_data['views'],
            'favorers': listing_data['num_favorers'],
            'latitude' : tweet_location[0],
            'longitude': tweet_location[1],
            'image_url': listing_img_url
            }
    return json_listing

### Flask ###
@app.route('/', methods = ['GET','POST'])
def index():
    if len(request.form.keys()) == 0:
        return render_template('index.html', data = '')
    else:
        tweet_count = int(request.form.keys()[0])
        data = search_etsy_tweets(tweet_count) 
        return render_template('index.html', data = data)