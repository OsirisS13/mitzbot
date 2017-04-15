#!/usr/bin/python
# coding: utf-8
#need to disable requests warnings coz it throws some error about https that we dont care about
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()
import facebook
import urllib
import urlparse
import subprocess
import warnings
import time
import json
import requests
from bs4 import BeautifulSoup
#for taking command line arguments
import sys
#google sheets imports
from mitzbot_update_googlesheets import updategooglesheets
#program takes details from the file specified in the launching arguments
detailsfile = str(sys.argv[1])
SocialPageDetails = __import__(detailsfile)
#########################
#now assign all variables from the details file locally into this one
Mitzbot_FB_APP_ID  = SocialPageDetails.Mitzbot_FB_APP_ID
Mitzbot_FB_APP_SECRET = SocialPageDetails.Mitzbot_FB_APP_SECRET
FBPageName = SocialPageDetails.FBPageName
twitterusername = SocialPageDetails.twitterusername
IGusername = SocialPageDetails.IGusername
spreadsheet = SocialPageDetails.spreadsheet
worksheet = SocialPageDetails.worksheet
fbcolumn = SocialPageDetails.fbcolumn
igcolumn = SocialPageDetails.igcolumn
twittercolumn = SocialPageDetails.twittercolumn
storagefile = SocialPageDetails.storagefile
###########################
timeanddate = time.strftime("%c")
date = (time.strftime("%d/%m/%Y"))

def get_fb_token(app_id, app_secret):           
    payload = {'grant_type': 'client_credentials', 'client_id': app_id, 'client_secret': app_secret}
    file = requests.post('https://graph.facebook.com/oauth/access_token?', params = payload)
    #print file.text #to test what the FB api responded with    
    result = file.text.split("=")[1]
    #print file.text #to test the TOKEN
    return result

def getFBLikes(PageName, FACEBOOK_APP_ID, FACEBOOK_APP_SECRET ):
	#sending app ID and app Secret direct
	oauth_access_token = FACEBOOK_APP_ID +'|' + FACEBOOK_APP_SECRET	
	#actual request we sent to facebook 
	fb_request = "https://graph.facebook.com/v2.8/" + PageName + "?fields=fan_count&access_token=" + oauth_access_token
	#send request and store in r
	r = requests.get(fb_request)
	#store parsed json response in variable
	fb_data = json.loads(r.text)
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

try:
	FBlikes = getFBLikes(FBPageName, Mitzbot_FB_APP_ID, Mitzbot_FB_APP_SECRET)
except:
	FBlikes = ""
try:
	IGfollowers = getIGfollowers(IGusername)
except:
	IGfollowers = ""
try:
	twitterfollowers = getTwitterfollowers(twitterusername)
except:
	twitterfollowers = ""
print "%s Social Stats as at %s: "  %(FBPageName, timeanddate)
print "FB Likes: %s"  %FBlikes
print "IG Followers: %s" % IGfollowers
print "Twitter Followers: %s" %twitterfollowers

#run the update sheets function
updategooglesheets(storagefile,spreadsheet,worksheet,timeanddate,FBlikes,fbcolumn,IGfollowers,igcolumn,twitterfollowers,twittercolumn)
