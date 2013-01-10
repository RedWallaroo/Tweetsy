Tweetsy
=======

Description: Tweetsy is a data visualization app that uses the Etsy and the Twitter API to gather information about tweets 
mentioning Etsy listings in them. It then locates the tweets on a map using D3.js (Datamaps library).

        Usage: Load /index page and hover over bubbles to display listing information.

Live version: 

        tweetsy.herokuapp.com

### NOTES: 

This application is a work in progress. For details on the "TO DO" list refer to the end of this file.

TECHNICAL DETAILS
-------

Tweetsy uses the following components:

### Flask :
Tweetsy was written as a Flask application and includes a couple ofl ines of code using the Jinja2 syntax.

### Twitter API:   
python-twitte (https://code.google.com/p/python-twitter/) is a Python wrapper around the Twitter API and it is used
here along with the GET Search method to pull tweets matching our search criteria.
		
		tweets = api.GetSearch(searchTerm, include_entities=1, result_type="recent", per_page=10, geocode=("39.232253","-2.460937","24000mi"))

- The 'include-entities' parameter returns items such as the URLS included in the tweets.
- The 'geocode' parameters returns items containing geolocation data that are within '24000mi' of "39.232253","-2.460937" (arbitraty location)					  		   
### Etsy API:
etsy-python (https://github.com/mcfunley/etsy-python) is a Python wrapper around the Etsy API and it is used here
to obtain listing data and listing image information.

	    def get_listing(listing_id):
            etsy_api = Etsy(api_key=Etsy_API_ID, etsy_env=etsy_env)
            listing_images = etsy_api.findAllListingImages(listing_id=int(listing_id)) 
            listing_img_url = listing_images[0]['url_75x75']
            return etsy_api.getListing(listing_id=listing_id), listing_img_url

### Datamaps:
Datamaps (http://datamaps.github.com/) is a JS package for Interactive maps and data visualizations. It uses Backbone, Underscore, Zepto and
D3.js

Tweetsy visualizations are a modification of this Datamaps example: http://bl.ocks.org/4255924
		

TO DO
-------

Tweetsy relies on the GET Search Twitter API and as such, it is affected by Twitter's rate limit of 150 requests/hour.
As well, gathering and processing the Twitter Data in real-time (on page_load) is a very time-consuming process and currently restricts
the number of data nodes we can display on the Tweetsy map. (This number has been set to 10 to reduce page loading time)

In order to get past these deficiencies, Tweetsy needs to be modified to use the Twitter Streaming API instead. 
With this, tweet data can be gathered, processed, and stored as an independent process. Then, once Tweetsy's landing page has loaded,
tweet data can be displayed on the map by firing off Ajax calls to pull data off its storage location.
