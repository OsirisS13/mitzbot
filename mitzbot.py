#need to disable requests warnings coz it throws some error about https that we dont care about
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()
#!/usr/bin/python
# coding: utf-8

import facebook
import urllib
import urlparse
import subprocess
import warnings
import time
import json
import requests
from bs4 import BeautifulSoup
#########################
#variables to replace to change which pages to check
Mitzbot_FB_APP_ID     = 'xxxxxxxx'
Mitzbot_FB_APP_SECRET = 'xxxxxxxxxxxx'
FBPageName = "xxxxxxxx"
twitterusername = 'xxxxxxxx'
IGusername = "xxxxxxxx"
###########################
date = time.strftime("%c")
def getFBLikes(PageName, FACEBOOK_APP_ID, FACEBOOK_APP_SECRET ):
	# Trying to get an access token. Very awkward.  see http://stackoverflow.com/questions/3058723/programmatically-getting-an-access-token-for-using-the-facebook-graph-api
	oauth_args = dict(client_id     = FACEBOOK_APP_ID,
					  client_secret = FACEBOOK_APP_SECRET,
					  grant_type    = 'client_credentials')
	oauth_curl_cmd = ['curl',
					  'https://graph.facebook.com/oauth/access_token?' + urllib.urlencode(oauth_args)]
	oauth_response = subprocess.Popen(oauth_curl_cmd,
									  stdout = subprocess.PIPE,
									  stderr = subprocess.PIPE).communicate()[0]

	try:
		oauth_access_token = urlparse.parse_qs(str(oauth_response))['access_token'][0]
	except KeyError:
		print('Unable to grab an access token!')
		exit()
		
	#required token generated from here, note this expired https://developers.facebook.com/tools/explorer/?method=GET&path=TopdeckTravel%3Ffields%3Dfan_count&version=v2.8
	#fb_auth_token = "xxxxxxxxxxxx"
	#actual request we sent to facebook 
	fb_request = "https://graph.facebook.com/v2.8/" + PageName + "?fields=fan_count&access_token=" + oauth_access_token
	#send request and store in r
	r = requests.get(fb_request)
	#store parsed json response in variable
	fb_data = json.loads(r.text)
	#print fb_data
	#extract likes and store in variable
	likes = fb_data['fan_count']
	return likes

def getIGfollowers(pagename):
	#luckily no api needed, so can seend straight https request
	IG_request = "https://www.instagram.com/" + pagename + "/?__a=1"
	#load request to variable
	r = requests.get(IG_request)
	#parse returned text via json
	IG_data = json.loads(r.text)
	#extract followers and store in variable
	followers = IG_data['user']['followed_by']['count']
	return followers
	
def getTwitterfollowers(username):
	#parsing this with beautfiul soup, using the following page
	url = "https://twitter.com/" + username
	#add to soup
	soup=BeautifulSoup(requests.get(url).text, 'html.parser')
	#find required element
	twitterfollowers=soup.find('li', {'class':'ProfileNav-item--followers'}).find('a', {'class':'ProfileNav-stat--link'})['title']
	#delete the word followers
	twitterfollowers = twitterfollowers.replace('Followers', '')
	#delete comma
	twitterfollowers = twitterfollowers.replace(',', '')
	return twitterfollowers

FBlikes = getFBLikes(FBPageName, Mitzbot_FB_APP_ID, Mitzbot_FB_APP_SECRET)
IGfollowers = getIGfollowers(IGusername)
twitterfollowers = getTwitterfollowers(twitterusername)
print "Social Stats as at %s: " %(date)
print "FB Likes: %s"  %FBlikes
print "IG Followers: %s" % IGfollowers
print "Twitter Followers: %s" %twitterfollowers
 
