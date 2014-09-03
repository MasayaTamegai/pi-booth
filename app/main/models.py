import threading
import Queue
import time, os
import urllib2
from collections import defaultdict


''' Photo object; created when the camera captures a photo '''
class Photo(object):

	def __init__(self, imgdir, filename, author, preview_dims, width, height, preview_countdown):

		self.imgdir = imgdir
		self.filename = filename
		self.full_path = imgdir + filename
		self.web_path = imgdir.replace('app/','') + filename
		self.author = author
		self.imgw = width
		self.imgh = height
		self.preview_dimensions = preview_dims
		self.countdown = preview_countdown
		self.creation_date = time.strftime('%d-%m-%Y')

		# generate the photo using properties above
		os.system("raspistill -t " + preview_countdown + " -o " + imgdir + filename + " -w " + \
		width + " -h " + height + " -p " + preview_dims)
