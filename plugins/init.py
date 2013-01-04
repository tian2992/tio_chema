""" 
This script should be used once to initialize your desktop/command line
application with a oauth access key and access secret. 

Your first step is to login, via the web, to your identi.ca account
and authorize your application. Click Edit next to your username
to edit your profile settings. Then click Connections on the left
side bar. Then, in the right sidebar, click 
"Register an OAuth client application".

When you are done, you will see a page listing your token and secret.
Fill in the consumer_token and consumer_secret variables below with those
values.
"""
""" Fill in these values with values provided in the identi.ca web app when you register your app! """
import tweepy


consumer_token = "d59d15c57b61cc37be4e4b6f112bac65"
consumer_secret = "bf6e387fb19397d8b842c02a9234e422"
host = 'identi.ca'
api_root = '/api/'
oauth_root = api_root + 'oauth/'

auth = tweepy.OAuthHandler(consumer_token, consumer_secret, 'oob')

auth.OAUTH_HOST = host
auth.OAUTH_ROOT = oauth_root
auth.secure = True

try:
  redirect_url = auth.get_authorization_url()
except tweepy.TweepError:
  print 'Error! Failed to get request token.'
  quit()

req_key = auth.request_token.key
req_secret = auth.request_token.secret

print "you don't need these values... just fyi..."
print "auth request key is: " + req_key
print "auth request secret is: " + req_secret

print "Go to this URL for verify code: " + redirect_url

print "enter the verify code from the URL above"
verifier = raw_input('Verify code: ')

auth = tweepy.OAuthHandler(consumer_token, consumer_secret, 'oob')
auth.set_request_token(req_key, req_secret)

auth.OAUTH_HOST = host
auth.OAUTH_ROOT = oauth_root
auth.secure = True

try:
  auth.get_access_token(verifier)
except tweepy.TweepError:
  print 'Error! Failed to get access token.'

print "Store these values in your application. You will re-use them"
print "auth access key is: " + auth.access_token.key 
print "auth access secret is: " + auth.access_token.secret 
print "done with initialization"
