# mitzbot
Python 2.7 Script to collect Social Media Stats (Follwers/Likes) from Facebook, Instagram and Twitter for a specified page and store in a Google Sheet document

Requires the following non-stock libraries:

facebook

urllib

urlparse

subprocess

warnings


json

requests

bs4

Note the Facebook portion requires use of the Facebook Graph API, which requires an App ID and App secret to utilize.  Everything else is available with no authentication


Setup:
Edit config.py with the Social Media page\s you want to check,  your Facebook App ID and Secret, your Google Sheets Name and Worksheet, the and the columns to put data in.  Place your Google Client Secret .json file in the working directory.  See https://support.google.com/googleapi/answer/6158857?hl=en

Usage:
Run mitzbot.py [name of config file]
