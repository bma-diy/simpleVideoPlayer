#!/usr/bin/env python
import random
from random import randint
import time
import subprocess
import os
import logging
import glob
import RPi.GPIO as GPIO

"""
This script works really well and integrates the use of GPIO buttons. 
"""

# initialize GPIO buttons
GPIO.setmode(GPIO.BOARD)

key1 = 12
key2 = 16
key3 = 18

button1_pin = key1
button2_pin = key2
button3_pin = key3

def playmovie(video, loop = False):

	"""plays a video."""

	global myprocess
	global directory

	logging.debug('playmovie: linux: omxplayer %s' % video)

	proccount = isplaying()

	print(proccount)

	if proccount == 1 or proccount == 0:

		logging.debug('playmovie: No videos playing, so play video')

	else:

		logging.debug('playmovie: Video already playing, so quit current video, then play')
		myprocess.communicate(b"q")
		
	if not loop:
		# play with out looping		
		myprocess = subprocess.Popen(['omxplayer',directory + video],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE, close_fds=True)
	
	else:
		# play with loop
		myprocess = subprocess.Popen(['omxplayer','--loop',directory + video],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE, close_fds=True)
	
	time.sleep(1)

def isplaying():

		"""check if omxplayer is running
		if the value returned is a 1 or 0, omxplayer is NOT playing a video
		if the value returned is a 2, omxplayer is playing a video"""

		processname = 'omxplayer'
		tmp = os.popen("ps -Af").read()
		proccount = tmp.count(processname)

		logging.debug("isplaying: proccount: {}".format(proccount))

		return proccount

def getRandom(movie_directory):

		global directory
		movie_name = random.choice(glob.glob(os.path.join(directory + movie_directory, '*')))
		movie_name = movie_name.replace(directory,"")

		return movie_name


logging.basicConfig(level=logging.INFO)

directory = '/home/pi/Videos/'

#program start
logging.info("Begin Player")

GPIO.setup(button1_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button2_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button3_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

current_movie_id = 'nothing'
movie_directory = "supermanf/"	#always starts with superman

try:
	while True: 

		proccount = isplaying()
		logging.debug(str(proccount) + " ****************************")
		if proccount == 1 or proccount == 0:
			logging.debug("Main: Play something since nothing is playing*******")
			time.sleep(5)
			movie_name = getRandom(movie_directory)
			time.sleep(1)

		else:
			print("IN THE ELSE")
			## Button 1
			if GPIO.input(button1_pin) == 0:
				logging.debug("Button 1 Pressed")
				movie_directory = "pawpatrol/" 
				movie_name = getRandom(movie_directory)
				time.sleep(1)

			## Button 2
			elif GPIO.input(button2_pin) == 0:
				logging.debug("Button 2 Pressed")
				movie_directory = "TomandJerry/" 
				movie_name = getRandom(movie_directory)
				time.sleep(1)

			## Button 3
			elif GPIO.input(button3_pin) == 0:
				logging.debug("Button 3 Pressed")
				movie_directory = "supermanf/"
				movie_name = getRandom(movie_directory)
				time.sleep(1)

		movie_name = movie_name.rstrip()

		logging.debug("current_movie_id2: %s" % current_movie_id)

		logging.debug("Movie Name2: %s" % movie_name)

		if current_movie_id != movie_name:

			logging.debug('New Movie')
			
			if movie_name.endswith(('.mp4', '.avi', '.m4v','.mkv')):
				current_movie_id = movie_name 	#we set this here instead of above bc it may mess up on first read
				logging.info("playing: omxplayer %s" % movie_name)
				playmovie(movie_name)
				print("PLAYING MOVIE*****************")


except KeyboardInterrupt:
	GPIO.cleanup()
	print("\nAll Done")