from flask import Flask, render_template, session
from flask.ext.socketio import SocketIO, emit
from .. import socketio
import config
import models, controllers, camera 
import signal, sys, subprocess
import twitter

subprocess.Popen('/usr/bin/midori -a http://localhost/local', shell=True)
'''subprocess.Popen('/usr/bin/midori -e Fullscreen -a http://localhost/local', shell=True)'''
camera = camera.CameraController()
t = twitter.TwitterController()
photo_controller = controllers.PhotoController()



@socketio.on('user', namespace='/photo')
def select_user(message):

	user_input = message['data'].replace(' ','').replace('@','')
	
	# twitter get fullname from username
	# if username doesn't exist then send bad code
	# else emit the user's first name
	response = t.lookup(user_input)
	if response['code'] is not 0:
		print 'Twitter:: got user\'s name %s:' % response['name']
		session['user'] = user_input
		emit('event', response)
	else:
		print 'Twitter:: user does not exist'
		emit('event', response)
	
@socketio.on('restart', namespace='/photo')
def restart(msg):
	''' End user session '''
	session.clear()

@socketio.on('take_pic', namespace='/photo')
def take_pic(msg):
	
	user = session['user']
	filename = user + ".jpg"
	photo = camera.take_picture(filename,user=user)
	# start countdown display
	session['photo'] = photo
	
	emit('image', {'data': photo.web_path })


@socketio.on('send_pic', namespace='/photo')
def send_pic(message):

	user = session['user']
	photo = session['photo']
	try:
		t.post_photo(user,photo.full_path)
		''' End user session '''
		session.clear()
	except Exception as e:
		print e

@socketio.on('connect', namespace='/local')
def local_client_connect():
    print ('Local client connected.')

@socketio.on('connect', namespace='/photo')
def client_connect():
    print ('Client connected.')
    #emit('event', { 'type': 'client_connect' }, namespace='/local')

@socketio.on('disconnect', namespace='/photo')
def client_disconnect():
    print('Client disconnected.')



''' handle command line ctrl+c exit '''    
def signal_handler(signal, frame):
	camera.pin_cleanup();
	print '-----> Quit'
	sys.exit(0)
	

signal.signal(signal.SIGINT, signal_handler)
