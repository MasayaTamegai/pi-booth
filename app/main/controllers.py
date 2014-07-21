import config, models
import os, subprocess
from flask import session

model = models.UserDataModel(config.user_file_url,config.local_cache_file,config.cache_refresh_rate)

class UserController(object):

	def get_user(self, user_input):

		user = model.get_user(user_input)

		if not user:
			response = { 'code': 0, 'guid': 0, 'name': user_input }
			
		else:
			response = { 'code': 1, 'guid': user.guid, 'name': user.first_name }
			session['user'] = user
		
		return response

			
		''' Below was my initial way to hold a user in session '''
			#users.insert(0,user)
			#check_user_timeout(user)



class PhotoController(object):

	def send_picture(self, uid, image_file):

		if os.path.isfile(image_file):
			
			print("Sending photo...\n------------------------------------------")

			subprocess.call("curl -s -L -u tmwcolin:waitalittle -F \"photo=@/home/pi/pi-booth/" + \
			image_file + ";type=application/octet-stream;\" -F \"guid=" + \
			str(uid) + "\" http://gps.tmw.co.uk/ajax/photobooth.php", shell=True)
			
			print("\n------------------------------------------")
			
		else:
			print("Error: File not found: " + image_file)
