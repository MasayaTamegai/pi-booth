#!/usr/bin/env python
import config
from twython import Twython, TwythonError

API_KEY = config.API_KEY
API_SECRET = config.API_SECRET
ACCESS_TOKEN = config.ACCESS_TOKEN
ACCESS_TOKEN_SECRET = config.ACCESS_TOKEN_SECRET

twitter = Twython(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)


class TwitterController(object):
	
	def lookup(self, screenname):
		try:
			user = twitter.lookup_user(screen_name=screenname)[0]['name']
			response = {'code': 1, 'name': user}
			return response
			
		except TwythonError:
			response = {'code': 0, 'name': screenname}
			return response
		
	def post_photo(self, user, photo_path):
		msg = '@%s took a photo using the TMW Pi-Booth' % user
		photo = open(photo_path, 'rb')
		twitter.update_status_with_media(media=photo, status=msg)
